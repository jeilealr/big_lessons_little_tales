#!/usr/bin/env python3
"""Export a production handoff package (production -> publishing). PROPOSED, not yet adopted.

The handoff is the only thing production gives the publishing repository: one uncompressed tar with
`handoff.json` (record kind `production-handoff`, schema_version 1) and `files/<asset_id>/<name>` for
every selected asset. Publishing imports it with its own tools; it never reads this repository.

    python3 production/export_handoff.py export \\
        --selection stories/<slug>/handoff_selection.yaml \\
        --allocation production/handoff/allocations/<story_id>.json \\
        --operator "<your name>" --out /path/outside/the/repo
    python3 production/export_handoff.py verify-contract

Rules this tool enforces (details: docs/publishing-handoff.md):
  * Explicit selection only. Every file is named in the selection file; nothing is globbed and there is
    no "latest revision" logic (contrast production/export_runtime.py, which feeds renders).
  * Pinned contract. production/contracts/CONTRACT.lock (record kind contract-lock, v1) names the
    contract package; every pinned file under production/contracts/feltwillow-contracts/<version>/ must match
    its locked sha256, and no unlisted file may be there.
  * Dirty worktree. Unrelated uncommitted paths are recorded in the handoff; a selected file that is
    modified, untracked or differs from the commit is refused. Git-tracked files are shipped as the
    committed blob bytes.
  * Read-only on the repository. Git runs with optional locks disabled (no index refresh); the only
    writes go to --out, which must lie outside the repository.
  * Deterministic: canonical-json-v1 record within the H1 safe domain; tar members sorted, mtime 0,
    uid/gid 0, mode 0644, no compression. The archive sha256 is printed and written next to the tar so
    the operator can give it to the importer out of band.
  * Components: images, audio, video (no reading text: it is authored in publishing, L-28). Audio is
    handed off lossless only (WAV/FLAC; MP3/M4A -> HANDOFF_AUDIO_NOT_LOSSLESS, L-29). Every image/audio/video
    asset records `measurement: {tool, version}`: images and audio are measured with the standard library
    (`feltwillow-stdlib`), video with `ffprobe` (PATH or --ffprobe); without ffprobe video is refused
    (MEASUREMENT_TOOL_UNAVAILABLE), never estimated.

Dependencies: Python >= 3.10 standard library + PyYAML (+ ffprobe only when video is selected). If `jsonschema` happens to be installed, the
record is also validated against the pinned schemas (`--schema-check auto`, the default); this never
changes the bytes produced.

Exit codes: 0 exported; 2 refused (nothing written); 3 dry run finished with blocking findings;
1 internal error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import stat
import struct
import subprocess
import sys
import tarfile
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

TOOL_VERSION = "0.3.0"
TOOL_NAME = "production/export_handoff.py"
REPOSITORY = "jeilealr/feltwillow-production"
EMITS = 1                      # production-handoff schema_version this exporter writes
ALGORITHM_ID = "feltwillow-canonical-json-v1"
LOCK_REL = "production/contracts/CONTRACT.lock"
PIN_DIR_REL = "production/contracts/feltwillow-contracts"
DEFAULT_ALLOCATION_DIR = "production/handoff/allocations"
TEXT_LIMIT = 8 * 2**20         # text assets and the selection file are read whole; cap them
HEAD_LIMIT = 8 * 2**20         # bytes read for measuring binary media
CHUNK = 1 << 20

# Same conventions as feltwillow/paths.py (REPO from this file's location, WORK from FELTWILLOW_WORK or REPO/work),
# computed here instead of imported so the tool also runs against a fixture tree given with --repo.
DEFAULT_REPO = Path(__file__).resolve().parents[1]

# ------------------------------------------------------------------------------------------ contract
# Copied from the H1 contract (common.v2 / production-handoff.v1 / h1_contracts.py). The pinned schemas
# remain the authority; these tables let the exporter refuse early with a clear message.
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SLUG_RE = re.compile(r"^[a-z0-9_]+$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")
SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?$")
TS_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
RELPATH_RE = re.compile(r"^(?!/)(?!.*//)(?!(?:.*/)?\.{1,2}(?:/|$))[A-Za-z0-9_@+-][A-Za-z0-9_.@+/-]*$")
# H2 common.v2 dirty_path (L-21): like relpath, but leading-dot segments (.gitignore, .claude/...) allowed.
DIRTY_PATH_RE = re.compile(r"^(?!/)(?!.*//)(?!(?:.*/)?\.{1,2}(?:/|$))[A-Za-z0-9_.@+-][A-Za-z0-9_.@+/-]*$")
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
HANDOFF_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.(?:en|de|es|fr|ru|uk)\.h[0-9]{4}$")
URL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://|^//|^[A-Za-z]:\\")
GLOB_CHARS = set("*?[]{}")
LANGUAGES = ("en", "de", "es", "fr", "ru", "uk")
SOURCE_PURPOSES = ("script", "dialogue", "reading-adaptation", "transcript-source", "runtime",
                   "prompt-manifest", "voices", "timing", "rights-index", "selection", "other")
RIGHTS_COMPONENTS = ("underlying-story", "adaptation", "translation", "voices", "images", "music",
                     "sound-effects", "video", "compute-resources")
RELATIONS = ("export", "mixdown", "transcode", "resize", "crop", "loudness-normalize", "caption-timing",
             "text-adaptation", "other")
STORES = ("production-git", "production-work", "owner-master-store")
# L-28: reading text is authored in publishing (reading-edition.v1), so there is no reading-text role here.
# L-29: audio is handed off lossless (WAV/FLAC) only; publishing derives delivery MP3s.
LOSSY_AUDIO = {"audio/mpeg", "audio/mp4"}
ROLE_MEDIA = {
    "spoken-transcript": {"text/plain"},
    "audio-master": {"audio/wav", "audio/flac"},
    "illustration": {"image/png", "image/jpeg", "image/webp"},
    "cover-art": {"image/png", "image/jpeg"},
    "video-master": {"video/mp4", "video/quicktime"},
    "video-delivery": {"video/mp4"},
    "thumbnail": {"image/png", "image/jpeg"},
    "captions": {"text/vtt"},
    "chapters": {"application/json"},
}
REQUIRED_MEASURES = {
    "illustration": ("width_px", "height_px"), "cover-art": ("width_px", "height_px"),
    "thumbnail": ("width_px", "height_px"),
    "audio-master": ("duration_ms", "sample_rate_hz", "channels"),
    "video-master": ("duration_ms", "width_px", "height_px", "frame_rate"),
    "video-delivery": ("duration_ms", "width_px", "height_px", "frame_rate"),
}
COMPONENT_SLOTS = {
    "images": {"illustration_assets": "illustration", "cover_asset": "cover-art"},
    "audio": {"master_asset": "audio-master", "transcript_asset": "spoken-transcript"},
    "video": {"master_asset": "video-master", "captions_asset": "captions", "thumbnail_asset": "thumbnail"},
}
REQUIRED_SLOTS = {"images": None, "audio": "master_asset", "video": "master_asset"}   # images: >= 1 image
MAX_DIRTY_PATHS = 10000


class Refusal(Exception):
    """A condition that stops the export immediately (nothing can be checked after it)."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


class Findings:
    def __init__(self):
        self.items: list[str] = []

    def add(self, code: str, detail: str = ""):
        self.items.append(f"{code}: {detail}" if detail else code)

    def __bool__(self):
        return bool(self.items)


# ------------------------------------------------------------------- canonical-json-v1 (H1 domain)
MAX_SAFE_INT = 2**53 - 1
_KEY_RE = re.compile(r"^[\x20-\x7e]*$")


def check_domain(value, depth: int = 0) -> None:
    """Raise Refusal(CJ_*) if a value is outside the H1 safe domain (same rules as publishing's cj1)."""
    if depth > 64:
        raise Refusal("CJ_DEPTH")
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        if not -MAX_SAFE_INT <= value <= MAX_SAFE_INT:
            raise Refusal("CJ_INT_RANGE", str(value))
        return
    if isinstance(value, float):
        raise Refusal("CJ_FLOAT", repr(value))
    if isinstance(value, str):
        if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
            raise Refusal("CJ_LONE_SURROGATE")
        if any(unicodedata.category(c) == "Cn" for c in value):
            raise Refusal("CJ_UNASSIGNED_CODEPOINT", "Unicode " + unicodedata.unidata_version)
        if not unicodedata.is_normalized("NFC", value):
            raise Refusal("CJ_NOT_NFC", repr(value[:40]))
        return
    if isinstance(value, list):
        for item in value:
            check_domain(item, depth + 1)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str) or not _KEY_RE.match(key):
                raise Refusal("CJ_KEY_NOT_ASCII", repr(key))
            check_domain(item, depth + 1)
        return
    raise Refusal("CJ_SYNTAX", "unsupported type " + type(value).__name__)


def canonical_bytes(value) -> bytes:
    check_domain(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Refusal("CJ_DUPLICATE_KEY", repr(key))
        out[key] = value
    return out


def _no_float(text):
    raise Refusal("CJ_FLOAT", text)


def _no_const(text):
    raise Refusal("CJ_SYNTAX", "non-JSON constant " + text)


def loads_strict(data: bytes):
    if data.startswith(b"\xef\xbb\xbf"):
        raise Refusal("CJ_BOM")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise Refusal("CJ_INVALID_UTF8", str(exc)) from None
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_float=_no_float,
                           parse_int=lambda t: int(t), parse_constant=_no_const)
    except Refusal:
        raise
    except (ValueError, RecursionError) as exc:
        raise Refusal("CJ_SYNTAX", str(exc)[:200]) from None
    check_domain(value)
    return value


# ------------------------------------------------------------------------------------------- git
class Git:
    """Read-only Git access. Optional locks off, so `status` never rewrites the index."""

    def __init__(self, repo: Path):
        self.repo = repo
        self.env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0", "LC_ALL": "C"}
        self.base = ["git", "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false",
                     "-c", "core.quotePath=false", "-C", str(repo)]

    def run(self, *args: str, check=True) -> bytes:
        proc = subprocess.run(self.base + list(args), env=self.env, capture_output=True)
        if check and proc.returncode != 0:
            raise Refusal("GIT_FAILED", " ".join(args[:2]) + ": " + proc.stderr.decode(errors="replace")[:300])
        return proc.stdout

    def text(self, *args: str) -> str:
        return self.run(*args).decode("utf-8").strip()

    def ls_entry(self, commit: str, path: str):
        """(mode, type, object_id) of a committed path, or None if absent."""
        out = self.run("ls-tree", "-z", "--full-tree", commit, "--", path)
        for rec in out.split(b"\0"):
            if not rec:
                continue
            meta, _, name = rec.partition(b"\t")
            if name.decode("utf-8", errors="surrogateescape") == path:
                mode, typ, oid = meta.decode().split()
                return mode, typ, oid
        return None

    def blob_stream(self, oid: str):
        return subprocess.Popen(self.base + ["cat-file", "blob", oid], env=self.env, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL)

    def dirty_paths(self) -> list[str]:
        out = self.run("status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=none")
        paths, parts, i = set(), out.split(b"\0"), 0
        while i < len(parts):
            rec = parts[i]
            i += 1
            if not rec:
                continue
            xy, path = rec[:2].decode(), rec[3:].decode("utf-8", errors="surrogateescape")
            paths.add(path)
            if "R" in xy or "C" in xy:     # rename/copy: the next field is the original path
                if i < len(parts) and parts[i]:
                    paths.add(parts[i].decode("utf-8", errors="surrogateescape"))
                i += 1
        return sorted(paths)


# -------------------------------------------------------------------------------- media measurement
def _measure_png(head: bytes):
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return {"width_px": w, "height_px": h}


def _measure_jpeg(head: bytes):
    if head[:3] != b"\xff\xd8\xff":
        return None
    i = 2
    while i + 9 < len(head):
        if head[i] != 0xFF:
            i += 1
            continue
        marker = head[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7 or marker == 0xFF:
            i += 1 if marker == 0xFF else 2
            continue
        seg = struct.unpack(">H", head[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", head[i + 5:i + 9])
            return {"width_px": w, "height_px": h} if w and h else None
        i += 2 + seg
    return None


def _measure_webp(head: bytes):
    if head[:4] != b"RIFF" or head[8:12] != b"WEBP":
        return None
    chunk = head[12:16]
    if chunk == b"VP8X" and len(head) >= 30:
        return {"width_px": 1 + int.from_bytes(head[24:27], "little"),
                "height_px": 1 + int.from_bytes(head[27:30], "little")}
    if chunk == b"VP8 " and len(head) >= 30 and head[23:26] == b"\x9d\x01\x2a":
        w, h = struct.unpack("<HH", head[26:30])
        return {"width_px": w & 0x3FFF, "height_px": h & 0x3FFF}
    if chunk == b"VP8L" and len(head) >= 25 and head[20] == 0x2F:
        b = int.from_bytes(head[21:25], "little")
        return {"width_px": (b & 0x3FFF) + 1, "height_px": ((b >> 14) & 0x3FFF) + 1}
    return None


def _ms(numerator: int, rate: int) -> int:
    """Integer milliseconds, rounded half up (H1: integers only)."""
    return (numerator * 1000 + rate // 2) // rate


def _measure_wav(head: bytes, size: int):
    if head[:4] != b"RIFF" or head[8:12] != b"WAVE":
        return None
    i, fmt = 12, None
    while i + 8 <= len(head):
        cid, clen = head[i:i + 4], struct.unpack("<I", head[i + 4:i + 8])[0]
        if cid == b"fmt " and i + 24 <= len(head):
            _tag, channels, rate, byte_rate, _align = struct.unpack("<HHIIH", head[i + 8:i + 22])
            fmt = (channels, rate, byte_rate)
        elif cid == b"data" and fmt:
            channels, rate, byte_rate = fmt
            data_len = min(clen, size - (i + 8))
            if not (channels and rate and byte_rate and data_len > 0):
                return None
            return {"duration_ms": max(1, _ms(data_len, byte_rate)), "sample_rate_hz": rate, "channels": channels}
        i += 8 + clen + (clen & 1)
    return None


def _measure_flac(head: bytes):
    if head[:4] != b"fLaC" or len(head) < 42 or (head[4] & 0x7F) != 0:
        return None
    info = int.from_bytes(head[18:26], "big")
    rate = info >> 44
    channels = ((info >> 41) & 0x7) + 1
    total = info & ((1 << 36) - 1)
    if not rate or not total:
        return None
    return {"duration_ms": max(1, _ms(total, rate)), "sample_rate_hz": rate, "channels": channels}


def sniff_and_measure(media_type: str, head: bytes, size: int, whole: bytes | None):
    """Return (sniff_ok, measured dict of the fields this tool can measure)."""
    if media_type == "image/png":
        m = _measure_png(head)
        return m is not None, m or {}
    if media_type == "image/jpeg":
        return head[:3] == b"\xff\xd8\xff", _measure_jpeg(head) or {}
    if media_type == "image/webp":
        return head[:4] == b"RIFF" and head[8:12] == b"WEBP", _measure_webp(head) or {}
    if media_type == "audio/wav":
        return head[:4] == b"RIFF" and head[8:12] == b"WAVE", _measure_wav(head, size) or {}
    if media_type == "audio/flac":
        return head[:4] == b"fLaC", _measure_flac(head) or {}
    if media_type == "audio/mpeg":
        return head[:3] == b"ID3" or (len(head) > 1 and head[0] == 0xFF and (head[1] & 0xE0) == 0xE0), {}
    if media_type in ("audio/mp4", "video/mp4", "video/quicktime"):
        return head[4:8] in (b"ftyp", b"moov", b"wide", b"mdat"), {}
    if whole is None:
        return False, {}
    try:
        text = whole.decode("utf-8")
    except UnicodeDecodeError:
        return False, {}
    if "\x00" in text or not unicodedata.is_normalized("NFC", text):
        return False, {}
    if media_type == "text/vtt":
        return text.startswith("WEBVTT"), {}
    if media_type.endswith("json"):
        try:
            return isinstance(loads_strict(whole), dict), {}
        except Refusal:
            return False, {}
    return media_type == "text/plain", {}


TEXT_TYPES = {"text/plain", "text/vtt", "application/json"}
VIDEO_TYPES = {"video/mp4", "video/quicktime"}


def stdlib_measurement() -> dict:
    import platform
    return {"tool": "feltwillow-stdlib", "version": f"export_handoff-{TOOL_VERSION}+py{platform.python_version()}"}


class Ffprobe:
    """ffprobe for video measurement (L-29). Located once; absent -> video refused, never guessed."""

    def __init__(self, explicit: str | None):
        import shutil
        self.path = explicit or shutil.which("ffprobe")
        self.version, self.error = None, None
        if not self.path:
            self.error = "ffprobe not found on PATH (use --ffprobe PATH)"
            return
        try:
            out = subprocess.run([self.path, "-version"], capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
            line = out.stdout.decode("utf-8", "replace").splitlines()[0] if out.returncode == 0 and out.stdout else ""
        except (OSError, subprocess.TimeoutExpired) as exc:
            line, self.error = "", f"{self.path}: {exc}"
        parts = line.split()
        if len(parts) >= 3 and parts[0] == "ffprobe" and parts[1] == "version":
            self.version = parts[2][:64]
        elif not self.error:
            self.error = f"{self.path} -version did not start with 'ffprobe version' ({line[:80]!r})"

    def measure(self, path: Path):
        """Return measured dict or raise Refusal. Integer ms (half up) and a rational frame rate."""
        from decimal import Decimal, ROUND_HALF_UP
        cmd = [self.path, "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height,avg_frame_rate,r_frame_rate,duration:format=duration", "-of", "json",
               "file:" + str(path)]
        try:
            out = subprocess.run(cmd, capture_output=True, timeout=600, stdin=subprocess.DEVNULL)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise Refusal("MEASUREMENT_FAILED", str(exc)) from None
        if out.returncode != 0:
            raise Refusal("MEASUREMENT_FAILED", out.stderr.decode("utf-8", "replace")[:200])
        try:
            info = json.loads(out.stdout, parse_float=Decimal)
            st = info["streams"][0]
            rate = st.get("avg_frame_rate") or "0/0"
            if rate in ("0/0", "0/1"):
                rate = st.get("r_frame_rate") or "0/0"
            num, den = (int(x) for x in rate.split("/"))
            dur = Decimal(str(st.get("duration") or info.get("format", {}).get("duration")))
            ms = int((dur * 1000).quantize(Decimal(1), rounding=ROUND_HALF_UP))
            m = {"width_px": int(st["width"]), "height_px": int(st["height"]), "duration_ms": max(ms, 1),
                 "frame_rate": {"numerator": num, "denominator": den} if num > 0 and den > 0 else None}
        except (KeyError, IndexError, ValueError, TypeError, ArithmeticError) as exc:
            raise Refusal("MEASUREMENT_FAILED", f"unexpected ffprobe output: {exc}") from None
        if m["frame_rate"] is None or m["width_px"] < 1 or m["height_px"] < 1:
            raise Refusal("MEASUREMENT_FAILED", "no video stream / frame rate")
        return m


# --------------------------------------------------------------------------------- selection file
def load_yaml_strict(data: bytes):
    import yaml

    class Loader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in seen:
                raise Refusal("SELECTION_INVALID", f"duplicate key {key!r} (line {key_node.start_mark.line + 1})")
            seen.add(key)
        return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)

    Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    try:
        text = data.decode("utf-8", errors="strict")
        return yaml.load(text, Loader=Loader)  # noqa: S506 - SafeLoader subclass
    except Refusal:
        raise
    except Exception as exc:  # YAML syntax, bad UTF-8
        raise Refusal("SELECTION_INVALID", str(exc)[:300]) from None


SELECTION_KEYS = {"kind", "schema_version", "example", "story_id", "language", "handoff_revision", "purpose",
                  "supersedes", "reason", "production_slugs", "editorial_selection", "source_files", "assets",
                  "components", "missing_masters", "rights_evidence", "generation_provenance"}
ASSET_KEYS = {"asset_id", "role", "media_type", "store", "path", "package_name", "derived_from", "selection_note"}
SOURCE_KEYS = {"source_id", "purpose", "path"}


def _keys(obj, allowed, where, f: Findings, required=None):
    if not isinstance(obj, dict):
        f.add("SELECTION_INVALID", f"{where} must be a mapping")
        return False
    extra = set(obj) - allowed
    if extra:
        f.add("SELECTION_INVALID", f"{where}: unknown keys {sorted(map(str, extra))}")
    missing = (required if required is not None else allowed) - set(obj)
    if missing:
        f.add("SELECTION_INVALID", f"{where}: missing keys {sorted(missing)}")
    return not extra and not missing


def check_relpath(p, where, f: Findings) -> bool:
    if not isinstance(p, str) or not p:
        f.add("SELECTION_INVALID", f"{where}: path must be a non-empty string")
        return False
    if GLOB_CHARS & set(p):
        f.add("SELECTION_GLOB_FORBIDDEN", f"{where}: {p!r} (name every file explicitly; no patterns, no 'latest')")
        return False
    if (p.startswith("/") or "\\" in p or "\x00" in p or URL_RE.match(p)
            or any(seg in ("", ".", "..") for seg in p.split("/"))):
        f.add("UNSAFE_PATH", f"{where}: {p!r}")
        return False
    if not RELPATH_RE.match(p) or len(p) > 512:
        f.add("UNSAFE_PATH", f"{where}: {p!r} is outside the contract's relpath pattern")
        return False
    return True


def private_ref(ev, where, ctx, f: Findings):
    """Selection evidence -> contract private_ref. `repo_path` refs are hashed from the commit."""
    if isinstance(ev, dict) and set(ev) == {"repo_path"}:
        p = ev["repo_path"]
        if not check_relpath(p, where, f):
            return None
        if p in ctx["dirty"]:
            f.add("EVIDENCE_REF_DIRTY", f"{where}: {p} has uncommitted changes; commit it or cite a committed file")
            return None
        entry = ctx["git"].ls_entry(ctx["commit"], p)
        if entry is None or entry[1] != "blob" or entry[0] == "120000":
            f.add("EVIDENCE_REF_UNTRACKED", f"{where}: {p}")
            return None
        h = hashlib.sha256(ctx["git"].run("cat-file", "blob", entry[2])).hexdigest()
        return {"ref": p, "sha256": h}
    if isinstance(ev, dict) and set(ev) == {"ref", "sha256"}:
        ref, sha = ev["ref"], ev["sha256"]
        if not isinstance(ref, str) or not ref or len(ref) > 512 or URL_RE.match(ref) or ref.startswith("/"):
            f.add("REMOTE_REFERENCE_FORBIDDEN", f"{where}: ref must be a private relative label, never a URL or absolute path")
            return None
        if sha is not None and not (isinstance(sha, str) and SHA_RE.match(sha)):
            f.add("SELECTION_INVALID", f"{where}: sha256 must be 64 lowercase hex or null")
            return None
        return {"ref": ref, "sha256": sha}
    f.add("SELECTION_INVALID", f"{where}: evidence must be {{repo_path: ...}} or {{ref: ..., sha256: ...}}")
    return None


# ------------------------------------------------------------------------------------- file access
def _inside(child: Path, root: Path) -> bool:
    try:
        child.relative_to(root)
        return True
    except ValueError:
        return False


def open_plain_file(root: Path, rel: str, where: str, f: Findings):
    """Resolve root/rel without following any symlink; return (Path, size) or None."""
    path = root / rel
    if not path.exists() and not path.is_symlink():
        f.add("SELECTED_FILE_MISSING", f"{where}: {rel}")
        return None
    cur = root
    for seg in rel.split("/"):
        cur = cur / seg
        if cur.is_symlink():
            f.add("SYMLINK_FORBIDDEN", f"{where}: {rel} (symlink at {cur.relative_to(root)})")
            return None
    real = path.resolve()
    if not _inside(real, root.resolve()):
        f.add("PATH_OUTSIDE_REPO", f"{where}: {rel}")
        return None
    st = os.lstat(path)
    if not stat.S_ISREG(st.st_mode):
        f.add("NOT_A_REGULAR_FILE", f"{where}: {rel}")
        return None
    return path, st.st_size


def _hash_stream(read, keep_head: int, keep_all_limit: int | None):
    h, n, head, whole = hashlib.sha256(), 0, bytearray(), bytearray()
    while True:
        chunk = read(CHUNK)
        if not chunk:
            break
        h.update(chunk)
        n += len(chunk)
        if len(head) < keep_head:
            head += chunk[:keep_head - len(head)]
        if keep_all_limit is not None and n <= keep_all_limit:
            whole += chunk
    return h.hexdigest(), n, bytes(head), (bytes(whole) if keep_all_limit is not None and n <= keep_all_limit else None)


class Source:
    """Where one selected file's bytes come from. `open()` yields the exact bytes that get shipped."""

    def __init__(self, kind, git=None, oid=None, path=None):
        self.kind, self.git, self.oid, self.path = kind, git, oid, path

    def open(self):
        if self.kind == "blob":
            proc = self.git.blob_stream(self.oid)
            return proc.stdout, proc
        fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        return os.fdopen(fd, "rb"), None


def resolve_git_file(rel, where, ctx, f: Findings, allow_untracked=False):
    """A tracked, clean file: returns Source(blob) after comparing the worktree bytes with the commit."""
    if not check_relpath(rel, where, f):
        return None
    git, commit = ctx["git"], ctx["commit"]
    entry = git.ls_entry(commit, rel)
    if entry is None:
        if rel in ctx["dirty"]:
            f.add("SELECTED_SOURCE_DIRTY", f"{where}: {rel} is untracked (commit it before exporting)")
        else:
            opened = open_plain_file(ctx["repo"], rel, where, Findings())
            f.add("SELECTED_FILE_MISSING" if opened is None else "SELECTED_SOURCE_UNTRACKED", f"{where}: {rel}")
        return None
    mode, typ, oid = entry
    if mode == "120000":
        f.add("SYMLINK_FORBIDDEN", f"{where}: {rel} is a committed symlink")
        return None
    if typ != "blob":
        f.add("NOT_A_REGULAR_FILE", f"{where}: {rel} ({typ})")
        return None
    if rel in ctx["dirty"]:
        f.add("SELECTED_SOURCE_DIRTY", f"{where}: {rel} has uncommitted changes")
        return None
    opened = open_plain_file(ctx["repo"], rel, where, f)
    if opened is None:
        return None
    src = Source("blob", git=git, oid=oid)
    stream, proc = src.open()
    blob_sha, blob_n, _, _ = _hash_stream(stream.read, 0, None)
    proc.wait()
    with open(opened[0], "rb") as fh:
        wt_sha, _, _, _ = _hash_stream(fh.read, 0, None)
    if wt_sha != blob_sha:
        f.add("SELECTED_SOURCE_DIRTY", f"{where}: {rel} differs from commit {commit[:12]} (filters or unstaged edit)")
        return None
    return src


def resolve_plain(root: Path, rel: str, where: str, f: Findings):
    if not check_relpath(rel, where, f):
        return None
    opened = open_plain_file(root, rel, where, f)
    if opened is None:
        return None
    return Source("file", path=opened[0])


# ------------------------------------------------------------------------------------ contract lock
def verify_contract(repo: Path, f: Findings, contracts_dir: Path | None = None):
    """Check CONTRACT.lock and the pinned files. Returns (lock, pin_dir) or raises Refusal.

    `contracts_dir` (default <repo>/production/contracts) is overridable only for --dry-run."""
    cdir = contracts_dir or (repo / "production" / "contracts")
    lock_path = cdir / "CONTRACT.lock"
    if not lock_path.is_file() or lock_path.is_symlink():
        raise Refusal("CONTRACT_LOCK_MISSING", str(lock_path))
    lock = loads_strict(lock_path.read_bytes())
    pkg = lock.get("package") if isinstance(lock, dict) else None
    ok = (isinstance(lock, dict) and lock.get("kind") == "contract-lock" and isinstance(pkg, dict)
          and set(lock) == {"kind", "schema_version", "example", "canonicalization", "package", "files", "producer_emits"}
          and isinstance(lock.get("example"), bool) and isinstance(lock.get("files"), list) and lock["files"])
    if not ok:
        raise Refusal("CONTRACT_LOCK_INVALID", "not a contract-lock record (H2 field set incl. canonicalization)")
    if lock.get("canonicalization") != ALGORITHM_ID:
        raise Refusal("CONTRACT_LOCK_INVALID", f"canonicalization must be {ALGORITHM_ID}")
    if lock.get("schema_version") != 1:
        raise Refusal("CONTRACT_VERSION_UNSUPPORTED", f"contract-lock schema_version={lock.get('schema_version')!r}")
    if (pkg.get("name") != "feltwillow-contracts" or not SEMVER_RE.match(str(pkg.get("version", "")))
            or not SHA_RE.match(str(pkg.get("archive_sha256", "")))):
        raise Refusal("CONTRACT_LOCK_INVALID", "package name/version/archive_sha256")
    emits = lock.get("producer_emits", {}).get("production-handoff") if isinstance(lock.get("producer_emits"), dict) else None
    if emits != EMITS:
        raise Refusal("CONTRACT_VERSION_UNSUPPORTED",
                      f"lock says producer emits production-handoff v{emits}; this exporter writes v{EMITS}")
    pin_dir = cdir / "feltwillow-contracts" / pkg["version"]
    if not pin_dir.is_dir() or pin_dir.is_symlink():
        raise Refusal("CONTRACT_PIN_MISSING", f"{pin_dir}/")
    locked = {}
    for entry in lock["files"]:
        if not (isinstance(entry, dict) and set(entry) == {"path", "sha256"} and isinstance(entry["path"], str)
                and RELPATH_RE.match(entry["path"]) and SHA_RE.match(str(entry["sha256"]))):
            raise Refusal("CONTRACT_LOCK_INVALID", f"file entry {entry!r}")
        if entry["path"] in locked:
            raise Refusal("CONTRACT_LOCK_INVALID", "duplicate path " + entry["path"])
        locked[entry["path"]] = entry["sha256"]
    if f"schemas/production-handoff.v{EMITS}.schema.json" not in locked:
        raise Refusal("LOCK_MISSING_EMITTED_SCHEMA", f"schemas/production-handoff.v{EMITS}.schema.json")
    present = set()
    for p in pin_dir.rglob("*"):
        rel = p.relative_to(pin_dir).as_posix()
        if p.is_symlink():
            f.add("CONTRACT_LOCK_MISMATCH", f"symlink in pinned contract: {rel}")
        elif p.is_file():
            present.add(rel)
    for rel in sorted(present - set(locked)):
        f.add("CONTRACT_LOCK_MISMATCH", f"unlisted file in pinned contract: {rel}")
    for rel, want in sorted(locked.items()):
        p = pin_dir / rel
        if rel not in present:
            f.add("CONTRACT_LOCK_MISMATCH", f"missing pinned file: {rel}")
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() != want:
            f.add("CONTRACT_LOCK_MISMATCH", f"sha256 differs from lock: {rel}")
    archive = cdir / f"feltwillow-contracts-{pkg['version']}.tar"
    if archive.is_file():
        with open(archive, "rb") as fh:
            if _hash_stream(fh.read, 0, None)[0] != pkg["archive_sha256"]:
                f.add("CONTRACT_LOCK_MISMATCH", f"{archive.name} does not match package.archive_sha256")
    return lock, pin_dir


def schema_check(record, pin_dir: Path, mode: str, f: Findings, selection=None) -> str:
    if mode == "off":
        return "off"
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry, Resource
    except ImportError:
        if mode == "required":
            f.add("SCHEMA_CHECK_UNAVAILABLE", "jsonschema/referencing not installed")
            return "unavailable"
        return "skipped (jsonschema not installed)"
    resources, target = [], None
    for p in sorted((pin_dir / "schemas").glob("*.schema.json")):
        data = loads_strict(p.read_bytes())
        resources.append((data["$id"], Resource.from_contents(data)))
        if p.name == f"production-handoff.v{EMITS}.schema.json":
            target = data
    registry = Registry().with_resources(resources)      # no retrieval callback: never fetches a $ref
    validator = Draft202012Validator(target, registry=registry, format_checker=FormatChecker())
    for err in sorted(validator.iter_errors(record), key=lambda e: list(map(str, e.absolute_path))):
        f.add("SCHEMA_VIOLATION", ".".join(map(str, err.absolute_path)) + ": " + err.message[:200])
    sel_schema = pin_dir / "schemas" / "handoff-selection.v1.schema.json"
    if selection is not None and sel_schema.is_file():       # H2 releases the selection format (L-23)
        sv = Draft202012Validator(loads_strict(sel_schema.read_bytes()), registry=registry, format_checker=FormatChecker())
        for err in sorted(sv.iter_errors(selection), key=lambda e: list(map(str, e.absolute_path))):
            f.add("SELECTION_INVALID", "schema: " + ".".join(map(str, err.absolute_path)) + ": " + err.message[:200])
        return "pinned schema (handoff + selection)"
    return "pinned schema"


# ----------------------------------------------------------------------------------------- export
def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ts(s: str):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def build(args) -> int:
    t0 = time.monotonic()
    f = Findings()
    dry = args.dry_run
    repo = Path(args.repo).resolve()
    git = Git(repo)
    try:
        top = Path(git.text("rev-parse", "--show-toplevel")).resolve()
    except Refusal:
        raise Refusal("NOT_A_GIT_REPO", str(repo)) from None
    if top != repo:
        raise Refusal("NOT_REPO_ROOT", f"--repo must be the repository root ({top})")
    out = Path(args.out).resolve()
    if _inside(out, repo):
        raise Refusal("OUT_INSIDE_REPO", "--out must be outside the repository (the exporter never writes into it)")
    work = Path(args.work or os.environ.get("FELTWILLOW_WORK") or (repo / "work"))   # resolved only if a work asset is selected
    master = args.master_root or os.environ.get("FELTWILLOW_MASTER_ROOT")
    master = Path(master).resolve() if master else None

    # 1. pinned contract
    if args.dry_run_contract and not dry:
        raise Refusal("SELECTION_INVALID", "--dry-run-contract is only allowed with --dry-run")
    lock, pin_dir = verify_contract(repo, f, Path(args.dry_run_contract).resolve() if args.dry_run_contract else None)
    if args.dry_run_contract:
        f.add("CONTRACT_NOT_PINNED_IN_REPO", f"dry run used {args.dry_run_contract}")

    # 2. repository state (read-only)
    commit = git.text("rev-parse", "--verify", "HEAD^{commit}")
    branch = git.run("symbolic-ref", "--short", "-q", "HEAD", check=False).decode().strip() or "(detached)"
    dirty = git.dirty_paths()
    bad = [p for p in dirty if not DIRTY_PATH_RE.match(p) or len(p) > 512]
    if bad:
        f.add("DIRTY_PATH_UNREPRESENTABLE",
              f"{len(bad)} uncommitted path(s) cannot be recorded under the contract's dirty_path rule, e.g. "
              + ", ".join(repr(p) for p in bad[:5]) + " (commit, restore or remove them; see docs/publishing-handoff.md)")
    if len(dirty) > MAX_DIRTY_PATHS:
        f.add("DIRTY_PATHS_TOO_MANY", str(len(dirty)))
    dirty_set = set(dirty)
    for p in dirty:
        if p == PIN_DIR_REL or p.startswith(PIN_DIR_REL + "/") or p == LOCK_REL:
            f.add("CONTRACT_PIN_DIRTY", f"{p} (commit the pinned contract before exporting)")
            break
    me = Path(__file__).resolve()
    tool_rel = me.relative_to(repo).as_posix() if _inside(me, repo) else None
    tool_dirty = (tool_rel is None or tool_rel in dirty_set or git.ls_entry(commit, tool_rel) is None)
    if tool_dirty:
        f.add("EXPORTER_DIRTY", "the exporter must run from committed code inside --repo"
              + ("" if tool_rel else f" (running from {me})"))
    ctx = {"repo": repo, "git": git, "commit": commit, "dirty": dirty_set}

    # 3. selection file (explicit; itself recorded as a source file so it is pinned by commit + digest)
    sel_arg = Path(args.selection)
    sel_path = sel_arg if sel_arg.is_absolute() else (repo / sel_arg)
    if not sel_path.is_file():
        raise Refusal("SELECTION_MISSING", f"{args.selection} (an explicit selection file is required; there is no default)")
    if sel_path.stat().st_size > TEXT_LIMIT:
        raise Refusal("SELECTION_INVALID", "selection file too large")
    sel = load_yaml_strict(sel_path.read_bytes())
    if not _keys(sel, SELECTION_KEYS, "selection", f):
        raise Refusal("SELECTION_INVALID", "; ".join(f.items[-2:]))
    if sel["kind"] != "handoff-selection" or sel["schema_version"] != 1:
        raise Refusal("SELECTION_INVALID", "kind must be handoff-selection, schema_version 1")
    sel_rel = sel_path.resolve().relative_to(repo).as_posix() if _inside(sel_path.resolve(), repo) else None
    sel_source = None
    if sel_rel is not None:
        sel_source = resolve_git_file(sel_rel, "selection file", ctx, f)
    else:
        f.add("SELECTION_OUTSIDE_REPO", f"{sel_path} is not in the repository (allowed only for --dry-run)")
    if sel_rel is not None and not re.match(r"^stories/[a-z0-9_]+/handoff_selection(\.[a-z0-9_-]+)?\.yaml$", sel_rel):
        f.add("SELECTION_INVALID", "selection must live at stories/<slug>/handoff_selection.yaml")

    # 4. allocation (issued by publishing; read-only here)
    story_id, lang = sel["story_id"], sel["language"]
    if not (isinstance(story_id, str) and ID_RE.match(story_id) and len(story_id) <= 64):
        raise Refusal("SELECTION_INVALID", "story_id")
    if lang not in LANGUAGES:
        raise Refusal("SELECTION_INVALID", f"language must be one of {LANGUAGES}")
    alloc_path = Path(args.allocation) if args.allocation else repo / DEFAULT_ALLOCATION_DIR / f"{story_id}.json"
    if not alloc_path.is_absolute():
        alloc_path = repo / alloc_path
    if not alloc_path.is_file():
        raise Refusal("STORY_NOT_ALLOCATED", f"allocation record not found: {alloc_path}")
    alloc = loads_strict(alloc_path.read_bytes())
    if not (isinstance(alloc, dict) and alloc.get("kind") == "story-allocation" and alloc.get("schema_version") == 1):
        raise Refusal("ALLOCATION_INVALID", "not a story-allocation v1 record")
    if alloc.get("story_id") != story_id:
        f.add("STORY_NOT_ALLOCATED", f"allocation is for {alloc.get('story_id')!r}, selection names {story_id!r}")
    if alloc.get("status") != "allocated":
        f.add("STORY_NOT_ALLOCATED", f"allocation status {alloc.get('status')!r}")
    if lang not in (alloc.get("planned_languages") or []):
        f.add("LANGUAGE_NOT_PLANNED", lang)
    slugs = sel["production_slugs"]
    if not (isinstance(slugs, list) and slugs and all(isinstance(s, str) and SLUG_RE.match(s) for s in slugs)
            and len(set(slugs)) == len(slugs)):
        f.add("SELECTION_INVALID", "production_slugs")
        slugs = []
    for s in slugs:
        if s not in (alloc.get("production_slugs") or []):
            f.add("SLUG_NOT_ALLOCATED", s)
    if sel_rel and sel_rel.count("/") >= 2 and sel_rel.split("/")[1] not in slugs:
        f.add("SLUG_NOT_ALLOCATED", f"selection folder {sel_rel.split('/')[1]} not in production_slugs")

    # 5. identity and lineage
    rev, purpose = sel["handoff_revision"], sel["purpose"]
    if not (isinstance(rev, int) and not isinstance(rev, bool) and 1 <= rev <= 9999):
        raise Refusal("SELECTION_INVALID", "handoff_revision must be an integer 1..9999")
    if purpose not in ("initial", "correction", "revocation"):
        raise Refusal("SELECTION_INVALID", "purpose")
    sup = sel["supersedes"]
    if (rev == 1) != (sup is None) or (rev == 1) != (purpose == "initial"):
        f.add("PURPOSE_REVISION_MISMATCH", "revision 1 <=> purpose initial <=> supersedes null")
    if sup is not None and not (isinstance(sup, dict) and set(sup) == {"handoff_id", "payload_sha256"}
                                and HANDOFF_ID_RE.match(str(sup["handoff_id"])) and SHA_RE.match(str(sup["payload_sha256"]))
                                and str(sup["handoff_id"]).startswith(f"{story_id}.{lang}.h")
                                and int(str(sup["handoff_id"])[-4:]) < rev):
        f.add("SELECTION_INVALID", "supersedes must be {handoff_id (same edition, lower revision), payload_sha256}")
    if purpose != "initial" and not (isinstance(sel["reason"], str) and sel["reason"].strip()):
        f.add("REASON_REQUIRED")
    handoff_id = f"{story_id}.{lang}.h{rev:04d}"

    # 6. source files
    source_files = []
    if sel_source is not None:
        source_files.append(("handoff-selection", "selection", sel_rel, sel_source))
    for i, s in enumerate(sel["source_files"] or []):
        where = f"source_files[{i}]"
        if not _keys(s, SOURCE_KEYS, where, f):
            continue
        if not (isinstance(s["source_id"], str) and ID_RE.match(s["source_id"])):
            f.add("SELECTION_INVALID", f"{where}.source_id")
            continue
        if s["purpose"] not in SOURCE_PURPOSES:
            f.add("SELECTION_INVALID", f"{where}.purpose")
            continue
        src = resolve_git_file(s["path"], where, ctx, f)
        if src is not None:
            source_files.append((s["source_id"], s["purpose"], s["path"], src))
    ids = [x[0] for x in source_files]
    if len(ids) != len(set(ids)):
        f.add("DUPLICATE_SOURCE_ID")
    sf_records = []
    for sid, spurpose, path, src in source_files:
        stream, proc = src.open()
        sha, n, _, _ = _hash_stream(stream.read, 0, None)
        proc.wait()
        if n < 1:
            f.add("SELECTION_INVALID", f"source {path} is empty")
        sf_records.append({"source_id": sid, "purpose": spurpose, "repo_role": "production", "path": path,
                           "commit": commit, "sha256": sha, "bytes": max(n, 1)})

    # 7. assets (pass 1: hash and measure, no writes)
    assets, plan, ffprobe = [], [], None
    for i, a in enumerate(sel["assets"] or []):
        where = f"assets[{i}]"
        if not _keys(a, ASSET_KEYS, where, f, required=ASSET_KEYS - {"package_name", "derived_from", "selection_note"}):
            continue
        aid, role, mtype, store = a["asset_id"], a["role"], a["media_type"], a["store"]
        if not (isinstance(aid, str) and ID_RE.match(aid) and len(aid) <= 64):
            f.add("SELECTION_INVALID", f"{where}.asset_id")
            continue
        if mtype in LOSSY_AUDIO:
            f.add("HANDOFF_AUDIO_NOT_LOSSLESS", f"{aid}: {mtype} (hand off the WAV/FLAC master; publishing derives MP3)")
            continue
        if role not in ROLE_MEDIA:
            f.add("SELECTION_INVALID", f"{where}.role {role!r}"
                  + (" (reading text is authored in publishing, L-28)" if role == "reading-text" else ""))
            continue
        if mtype not in ROLE_MEDIA[role]:
            f.add("MEDIA_TYPE_ROLE_MISMATCH", f"{aid}: {mtype} for {role}")
            continue
        if store not in STORES:
            f.add("SELECTION_INVALID", f"{where}.store must be one of {STORES}")
            continue
        if mtype in VIDEO_TYPES:      # tool first: without ffprobe a video can never be measured
            if ffprobe is None:
                ffprobe = Ffprobe(args.ffprobe)
            if ffprobe.error:
                f.add("MEASUREMENT_TOOL_UNAVAILABLE", f"{aid}: {ffprobe.error}")
                continue
        rel = a["path"]
        if store == "production-git":
            src = resolve_git_file(rel, where, ctx, f)
            ref = rel
        elif store == "production-work":
            src = resolve_plain(work.resolve(), rel, where, f)
            ref = "FELTWILLOW_WORK/" + str(rel)
        else:
            if master is None:
                f.add("STATE_ROOT_UNSET", f"{where}: owner-master-store needs --master-root or FELTWILLOW_MASTER_ROOT")
                continue
            if _inside(master, repo):
                f.add("STATE_ROOT_UNSAFE", "the master store must not be inside the production repository")
                continue
            src = resolve_plain(master, rel, where, f)
            ref = "FELTWILLOW_MASTER_ROOT/" + str(rel)
        if src is None:
            continue
        if mtype in VIDEO_TYPES and src.kind != "file":
            f.add("MEASUREMENT_UNSUPPORTED", f"{aid}: video must come from production-work or the master store")
            continue
        name = a.get("package_name") or Path(rel).name
        if not NAME_RE.match(name):
            f.add("PACKAGE_NAME_INVALID", f"{aid}: {name!r} (set package_name: [A-Za-z0-9][A-Za-z0-9_.-]{{0,127}})")
            continue
        stream, proc = src.open()
        keep_all = TEXT_LIMIT if mtype in TEXT_TYPES else None
        sha, n, head, whole = _hash_stream(stream.read, HEAD_LIMIT, keep_all)
        if proc:
            proc.wait()
        if n < 1:
            f.add("SELECTION_INVALID", f"{aid}: empty file")
            continue
        if mtype in TEXT_TYPES and whole is None:
            f.add("TEXT_ASSET_TOO_LARGE", aid)
            continue
        ok, measured = sniff_and_measure(mtype, head, n, whole)
        if not ok:
            f.add("MEDIA_TYPE_MISMATCH", f"{aid}: bytes are not {mtype}")
            continue
        measurement = None
        if mtype in VIDEO_TYPES:
            try:
                measured = ffprobe.measure(src.path)
            except Refusal as exc:
                f.add(exc.code, f"{aid}: {exc}")
                continue
            measurement = {"tool": "ffprobe", "version": ffprobe.version}
        elif mtype.split("/")[0] in ("image", "audio"):
            measurement = stdlib_measurement()
        m = {k: measured.get(k) for k in ("width_px", "height_px", "duration_ms", "sample_rate_hz", "channels")}
        m["frame_rate"] = measured.get("frame_rate")
        missing = [k for k in REQUIRED_MEASURES.get(role, ()) if m[k] is None]
        if missing:
            f.add("MEASUREMENT_UNSUPPORTED",
                  f"{aid}: cannot measure {missing} from {mtype}")
            continue
        derived = []
        for j, d in enumerate(a.get("derived_from") or []):
            if not (isinstance(d, dict) and set(d) == {"sha256", "asset_id", "relation"}
                    and SHA_RE.match(str(d["sha256"])) and d["relation"] in RELATIONS
                    and (d["asset_id"] is None or (isinstance(d["asset_id"], str) and ID_RE.match(d["asset_id"])))):
                f.add("SELECTION_INVALID", f"{where}.derived_from[{j}]")
                continue
            derived.append(dict(d))
        note = a.get("selection_note")
        if note is not None and not (isinstance(note, str) and 1 <= len(note) <= 500):
            f.add("SELECTION_INVALID", f"{where}.selection_note")
            note = None
        assets.append({
            "asset_id": aid, "role": role, "media_type": mtype, "bytes": n, "sha256": sha,
            "transport": "embedded", "package_path": f"files/{aid}/{name}", "measured": m,
            "measurement": measurement,
            "derived_from": derived,
            "origin": {"store": store, "ref": ref, "commit": commit if store == "production-git" else None},
            "selection_note": note,
        })
        plan.append((f"files/{aid}/{name}", src, sha, n))
    by_id = {}
    for a in assets:
        if a["asset_id"] in by_id:
            f.add("DUPLICATE_ASSET_ID", a["asset_id"])
        by_id[a["asset_id"]] = a
    lower = [p[0].lower() for p in plan]
    if len(lower) != len(set(lower)):
        f.add("DUPLICATE_PACKAGE_PATH")
    for a in assets:
        for d in a["derived_from"]:
            if d["asset_id"] is not None and d["asset_id"] in by_id and by_id[d["asset_id"]]["sha256"] != d["sha256"]:
                f.add("PARENT_HASH_MISMATCH", f"{a['asset_id']} -> {d['asset_id']}")
            if d["sha256"] == a["sha256"]:
                f.add("DERIVATION_CYCLE", a["asset_id"])

    # 8. components (explicit; missing masters are declared, never guessed)
    comps_in = sel["components"]
    components = {"images": None, "audio": None, "video": None}
    used = set()
    missing_decl = sel["missing_masters"] or []
    declared_missing = set()
    for j, mm in enumerate(missing_decl):
        if not (isinstance(mm, dict) and set(mm) == {"component", "slot", "status", "note"}
                and mm["component"] in COMPONENT_SLOTS and mm["slot"] in COMPONENT_SLOTS[mm["component"]]):
            f.add("SELECTION_INVALID", f"missing_masters[{j}]")
            continue
        declared_missing.add((mm["component"], mm["slot"]))
    if not _keys(comps_in, {"images", "audio", "video"}, "components", f):
        comps_in = {}
    for comp, slots in COMPONENT_SLOTS.items():
        c = comps_in.get(comp)
        if c is None:
            continue
        if not _keys(c, set(slots), f"components.{comp}", f):
            continue
        out_c = {}
        for slot, role in slots.items():
            val = c[slot]
            vals = val if isinstance(val, list) else [val]
            if (comp, slot) in declared_missing and any(v is not None for v in vals):
                f.add("SELECTION_INVALID", f"components.{comp}.{slot} is filled but also listed in missing_masters")
            for v in vals:
                if v is None:
                    continue
                used.add(v)
                if v not in by_id:
                    f.add("UNKNOWN_ASSET", f"{comp}.{slot}={v}")
                elif by_id[v]["role"] != role:
                    f.add("WRONG_ASSET_ROLE", f"{comp}.{slot}={v}")
            out_c[slot] = val
        if REQUIRED_SLOTS[comp] is None:
            if not out_c.get("illustration_assets") and out_c.get("cover_asset") is None:
                f.add("COMPONENT_INCOMPLETE", "images needs at least one illustration or a cover")
        elif out_c.get(REQUIRED_SLOTS[comp]) is None:
            f.add("COMPONENT_INCOMPLETE",
                  f"{comp}.{REQUIRED_SLOTS[comp]} is required for a {comp} component"
                  + (" (declared missing in missing_masters)" if (comp, REQUIRED_SLOTS[comp]) in declared_missing else ""))
        components[comp] = out_c
    if purpose == "revocation":
        if any(components.values()) or assets:
            f.add("REVOCATION_WITH_ASSETS")
    elif not any(components.values()):
        f.add("NO_COMPONENTS", "select at least one complete component (images, audio or video)")
    unused = sorted(set(by_id) - used)
    if unused:
        f.add("UNREFERENCED_ASSET", ",".join(unused))

    # 9. selection, rights, provenance
    es = sel["editorial_selection"]
    editorial = None
    if _keys(es, {"selected_by", "selected_at", "statement", "evidence"}, "editorial_selection", f):
        if not (isinstance(es["selected_at"], str) and TS_RE.match(es["selected_at"])):
            f.add("SELECTION_INVALID", "editorial_selection.selected_at must be a quoted UTC string YYYY-MM-DDTHH:MM:SSZ")
        else:
            editorial = {"selected_by": es["selected_by"], "selected_at": es["selected_at"], "statement": es["statement"],
                         "evidence": [r for r in (private_ref(e, f"editorial_selection.evidence[{k}]", ctx, f)
                                                  for k, e in enumerate(es["evidence"] or [])) if r]}
    rights = []
    for k, r in enumerate(sel["rights_evidence"] or []):
        if _keys(r, {"component", "evidence", "note"}, f"rights_evidence[{k}]", f):
            if r["component"] not in RIGHTS_COMPONENTS:
                f.add("SELECTION_INVALID", f"rights_evidence[{k}].component")
                continue
            ref = private_ref(r["evidence"], f"rights_evidence[{k}]", ctx, f)
            if ref:
                rights.append({"component": r["component"], "evidence": ref, "note": r["note"]})
    provenance = []
    for k, g in enumerate(sel["generation_provenance"] or []):
        if _keys(g, {"asset_id", "tools", "evidence"}, f"generation_provenance[{k}]", f):
            if g["asset_id"] not in by_id:
                f.add("UNKNOWN_ASSET", f"generation_provenance.{g['asset_id']}")
            ev = None if g["evidence"] is None else private_ref(g["evidence"], f"generation_provenance[{k}]", ctx, f)
            provenance.append({"asset_id": g["asset_id"], "tools": g["tools"], "evidence": ev})

    created_at = args.created_at or utc_now()
    if not TS_RE.match(created_at):
        raise Refusal("SELECTION_INVALID", "--created-at must be YYYY-MM-DDTHH:MM:SSZ")
    if editorial and _ts(created_at) < _ts(editorial["selected_at"]):
        f.add("TIMESTAMP_ORDER", "export time is before the selection time")

    example = bool(sel["example"]) or bool(lock["example"]) or bool(alloc.get("example"))
    record = {
        "kind": "production-handoff", "schema_version": EMITS, "example": example,
        "canonicalization": ALGORITHM_ID,
        "contract_package": {"name": "feltwillow-contracts", "version": lock["package"]["version"],
                             "archive_sha256": lock["package"]["archive_sha256"]},
        "envelope": {
            "created_at": created_at, "operator": args.operator,
            "exporter": {"tool": TOOL_NAME, "tool_version": TOOL_VERSION, "repository": REPOSITORY,
                         "commit": commit, "tool_dirty": tool_dirty},
            "transport": "self-contained-tar"},
        "payload": {
            "handoff_id": handoff_id, "story_id": story_id, "language": lang, "handoff_revision": rev,
            "purpose": purpose, "supersedes": sup, "reason": sel["reason"],
            "story_allocation_sha256": digest(alloc), "production_slugs": slugs,
            "source_repositories": [{"repo_role": "production", "repository": REPOSITORY, "branch": branch,
                                     "commit": commit,
                                     "worktree": {"state": "dirty" if dirty else "clean", "dirty_paths": dirty}}],
            "source_files": sf_records, "assets": assets, "components": components,
            "editorial_selection": editorial, "rights_evidence": rights, "generation_provenance": provenance,
        },
    }
    try:
        body = canonical_bytes(record)
    except Refusal as exc:
        f.add(exc.code, "record: " + str(exc))
        body = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    schema_mode = "not run (earlier findings)"
    if not f or dry:
        schema_mode = schema_check(record, pin_dir, args.schema_check, f, sel) if editorial else schema_mode
    t_checked = time.monotonic()

    summary = {"handoff_id": handoff_id, "example": example, "dry_run": dry, "repository_commit": commit,
               "dirty_paths": len(dirty), "assets": len(assets), "source_files": len(sf_records),
               "contract_package": record["contract_package"], "schema_check": schema_mode,
               "findings": f.items}
    if f and not dry:
        summary["result"] = "refused"
        print(json.dumps(summary, indent=2))
        for item in f.items:
            print("REFUSED " + item, file=sys.stderr)
        return 2

    # 10. write the package (pass 2: stream exact bytes into the tar, verifying each digest again)
    out.mkdir(parents=True, exist_ok=True)
    stem = handoff_id + (".DRYRUN" if dry else "")
    final = out / f"{stem}.tar"
    for p in (final, out / f"{stem}.tar.sha256", out / f"{stem}.export.json"):
        if p.exists():
            raise Refusal("OUT_EXISTS", f"{p} already exists (exports never overwrite)")
    tmp = out / f".{stem}.tar.tmp-{secrets.token_hex(4)}"
    try:
        with open(tmp, "xb") as fh:
            with tarfile.open(fileobj=fh, mode="w", format=tarfile.PAX_FORMAT) as tar:
                tar.addfile(_tarinfo("handoff.json", len(body)), _BytesReader(body))
                for name, src, want_sha, want_n in sorted(plan, key=lambda x: x[0]):
                    stream, proc = src.open()
                    reader = _HashingReader(stream)
                    try:
                        tar.addfile(_tarinfo(name, want_n), reader)
                    except OSError:
                        raise Refusal("SOURCE_CHANGED_DURING_EXPORT", name + " (shorter than when it was hashed)") from None
                    rest = stream.read(1)
                    if proc:
                        proc.stdout.close()
                        proc.wait()
                    else:
                        stream.close()
                    if reader.n != want_n or reader.h.hexdigest() != want_sha or rest:
                        raise Refusal("SOURCE_CHANGED_DURING_EXPORT", name)
            fh.flush()
            os.fsync(fh.fileno())
        with open(tmp, "rb") as fh:
            archive_sha, archive_n, _, _ = _hash_stream(fh.read, 0, None)
        os.link(tmp, final)          # fails instead of overwriting if the name appeared meanwhile
    finally:
        if tmp.exists():
            tmp.unlink()
    payload_sha = digest(record["payload"])
    (out / f"{stem}.tar.sha256").write_text(f"{archive_sha}  {final.name}\n", encoding="utf-8")
    summary.update({"result": "dry-run" if dry else "exported", "archive": str(final), "archive_sha256": archive_sha,
                    "archive_bytes": archive_n, "payload_sha256": payload_sha,
                    "record_sha256": hashlib.sha256(body).hexdigest(), "created_at": created_at,
                    "seconds_checks": round(t_checked - t0, 3), "seconds_total": round(time.monotonic() - t0, 3),
                    "private": "contains production provenance; do not publish this file"})
    (out / f"{stem}.export.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if dry:
        print(f"DRY RUN: not importable (tool_dirty={tool_dirty}); findings: {len(f.items)}", file=sys.stderr)
        return 3 if f else 0
    print(f"\nGive the importer this archive digest out of band:\n  {archive_sha}  {final.name}", file=sys.stderr)
    return 0


class _BytesReader:
    def __init__(self, data: bytes):
        self.data, self.pos = data, 0

    def read(self, n=-1):
        n = len(self.data) - self.pos if n is None or n < 0 else n
        chunk = self.data[self.pos:self.pos + n]
        self.pos += len(chunk)
        return chunk


class _HashingReader:
    def __init__(self, stream):
        self.stream, self.h, self.n = stream, hashlib.sha256(), 0

    def read(self, n=-1):
        chunk = self.stream.read(n)
        self.h.update(chunk)
        self.n += len(chunk)
        return chunk


def _tarinfo(name: str, size: int) -> tarfile.TarInfo:
    ti = tarfile.TarInfo(name)
    ti.size, ti.type, ti.mtime, ti.mode, ti.uid, ti.gid = size, tarfile.REGTYPE, 0, 0o644, 0, 0
    ti.uname = ti.gname = ""
    return ti


def cmd_verify_contract(args) -> int:
    f = Findings()
    lock, pin_dir = verify_contract(Path(args.repo).resolve(), f)
    result = {"contract_package": lock["package"], "example": lock["example"], "pinned_files": len(lock["files"]),
              "producer_emits": lock["producer_emits"], "findings": f.items, "result": "mismatch" if f else "ok"}
    print(json.dumps(result, indent=2))
    return 2 if f else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=str(DEFAULT_REPO), help="production repository root (default: this checkout)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser("export", help="build one handoff package")
    ex.add_argument("--selection", required=True, help="stories/<slug>/handoff_selection.yaml (repo-relative)")
    ex.add_argument("--allocation", help=f"story-allocation JSON from publishing (default {DEFAULT_ALLOCATION_DIR}/<story_id>.json)")
    ex.add_argument("--operator", required=True, help="who runs the export (label, not authentication)")
    ex.add_argument("--out", required=True, help="output directory OUTSIDE the repository")
    ex.add_argument("--work", help="generated-files root (default: FELTWILLOW_WORK or <repo>/work, as feltwillow/paths.py)")
    ex.add_argument("--master-root", help="owner master store (default: FELTWILLOW_MASTER_ROOT)")
    ex.add_argument("--ffprobe", help="ffprobe binary for video measurement (default: ffprobe on PATH)")
    ex.add_argument("--created-at", help="fixed UTC export time (tests/reproduction); default now")
    ex.add_argument("--schema-check", choices=("auto", "required", "off"), default="auto")
    ex.add_argument("--dry-run-contract", help="dry run only: directory holding CONTRACT.lock + feltwillow-contracts/<version>/ "
                    "when the repository has no pinned contract yet")
    ex.add_argument("--dry-run", action="store_true",
                    help="collect every finding, still write a *.DRYRUN.tar for size/timing; never importable")
    sub.add_parser("verify-contract", help="check CONTRACT.lock against the pinned contract files")
    args = ap.parse_args(argv)
    if args.cmd == "export" and not (1 <= len(args.operator) <= 128):
        ap.error("--operator must be 1..128 characters")
    try:
        return cmd_verify_contract(args) if args.cmd == "verify-contract" else build(args)
    except Refusal as exc:
        print(json.dumps({"result": "refused", "findings": [str(exc)]}, indent=2))
        print("REFUSED " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
