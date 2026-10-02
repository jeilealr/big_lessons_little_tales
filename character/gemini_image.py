#!/usr/bin/env python3
"""Generate, review and accept v4 manifest images with the Gemini API.

Workflow (docs/gemini-images.md):

    # 1. candidates for one or more records (Lite for studio refs, Nano Banana 2 for scenes; 1K)
    python3 character/gemini_image.py gen --record s02_place_acorn_end --revision r02 --takes 2
    # 2. look at them next to the current target
    python3 character/gemini_image.py sheet --record s02_place_acorn_end --revision r02
    # 3. promote the chosen take: copies it to <stem>_r02.png and updates the manifest
    python3 character/gemini_image.py accept s02_place_acorn_end_r02_nb2lite_t01 --note "leg gap clear ..."

    python3 character/gemini_image.py gen --record L_SIDE_R --dry-run     # print what would be sent
    python3 character/gemini_image.py models                             # image models visible to the key

What is sent: each ordered reference (resolved by id to that record's *current*
manifest target, so an accepted r02 start feeds its end frame), labelled with its
role, then the record's positive prompt, then the revision's fix text from
stories/lion_and_mouse_v4/revisions/<rev>.json. The negative prompt is not sent
(the API has no negative field); it stays a review criterion.

Candidates: <target dir>/gemini/<stem>_<rev>_<model tag>_tNN.png + .json sidecar,
normalised to the record canvas. Only `accept` writes a target or the manifest.

Auth: header x-goog-api-key from GEMINI_API_KEY; with it unset, the cloud
container's egress proxy injects the key. Stdlib for the API, Pillow for images.
"""
import argparse
import base64
import datetime as dt
import hashlib
import io
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "stories/lion_and_mouse_v4/prompt_manifest.json"
REVISIONS = REPO / "stories/lion_and_mouse_v4/revisions"
# One row per generated take (ok or failed), so cost per model can be reported from data.
LEDGER = REVISIONS / "gemini_ledger.csv"
LEDGER_COLS = ["date", "record", "revision", "candidate", "model", "size", "outcome", "retries", "est_usd"]
API = "https://generativelanguage.googleapis.com/v1beta"
# Lite matched GPT on single-character studio references; for 16:9 scene edits it ignored
# scale (Milo grew from 0.3 to 0.55 of the frame), so scenes default to Nano Banana 2.
STUDIO_MODEL = "gemini-3.1-flash-lite-image"
SCENE_MODEL = "gemini-3.1-flash-image"
# Approximate USD per output image, from third-party summaries of Google's 2026
# price list (ai.google.dev is not reachable from the cloud container). Check billing.
PRICE = {
    ("gemini-3.1-flash-lite-image", "1K"): 0.034,
    ("gemini-3.1-flash-image", "1K"): 0.067,  # sources disagree: 0.045-0.067
    ("gemini-3.1-flash-image", "2K"): 0.101,
    ("gemini-3.1-flash-image", "4K"): 0.151,
    ("gemini-3-pro-image", "1K"): 0.134,
    ("gemini-3-pro-image", "2K"): 0.134,
    ("gemini-3-pro-image", "4K"): 0.24,
    ("gemini-3-pro-image-preview", "1K"): 0.134,
    ("gemini-3-pro-image-preview", "2K"): 0.134,
}
TAG = {"gemini-3.1-flash-lite-image": "nb2lite", "gemini-3.1-flash-image": "nb2",
       "gemini-3-pro-image": "nbpro", "gemini-3-pro-image-preview": "nbpro"}


# ---------------------------------------------------------------- API

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def call(url, body=None, timeout=300):
    key = os.environ.get("GEMINI_API_KEY")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method="POST" if data else "GET",
        headers={"Content-Type": "application/json", **({"x-goog-api-key": key} if key else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def generate(model, parts, ratio, size):
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"],
                                 "imageConfig": {"aspectRatio": ratio, "imageSize": size}}}
    resp = call(f"{API}/models/{model}:generateContent", body)
    cand = resp.get("candidates", [{}])[0]
    out = cand.get("content", {}).get("parts", [])
    imgs = [p.get("inlineData") or p.get("inline_data") for p in out if "inlineData" in p or "inline_data" in p]
    meta = {k: resp.get(k) for k in ("modelVersion", "responseId", "usageMetadata")}
    meta["finishReason"] = cand.get("finishReason")
    meta["text"] = " ".join(p["text"] for p in out if "text" in p) or None
    if not imgs:
        raise RuntimeError(f"no image returned: {json.dumps(meta)[:500]}")
    return base64.b64decode(imgs[0]["data"]), meta


# ---------------------------------------------------------------- manifest

def load_manifest():
    return json.loads(MANIFEST.read_text())


def save_manifest(m):
    MANIFEST.write_text(json.dumps(m, indent=2) + "\n")


def load_revision(rev):
    p = REVISIONS / f"{rev}.json"
    return json.loads(p.read_text()).get("records", {}) if rev and p.exists() else {}


def base_stem(target):
    return re.sub(r"_r\d\d$", "", Path(target).stem)


def resolve_refs(rec, by_id, fix):
    """Reference list for this request: manifest refs (minus dropped) plus the revision's extras.
    An id that is itself a manifest record resolves to that record's current target."""
    drop = set(fix.get("drop_references", []))
    refs = [r for r in rec.get("ordered_references", []) if r["id"] not in drop]
    refs += fix.get("extra_references", [])
    out = []
    for r in refs:
        path = by_id[r["id"]]["target"] if r["id"] in by_id else r["path"]
        if not (REPO / path).exists():
            sys.exit(f"{rec['id']}: missing reference {r['id']} -> {path}")
        out.append({"id": r["id"], "role": r["role"], "path": path, "sha256": sha256(REPO / path)})
    return out


def prompt_text(rec, fix):
    text = rec["positive_prompt"]
    if fix.get("fix"):
        text += " Revision fix (owner review): " + fix["fix"]
    return text


def build_parts(refs, text):
    """A role label before each reference tells the model what to take from it."""
    parts = []
    for k, r in enumerate(refs, 1):
        path = REPO / r["path"]
        parts.append({"text": f"Reference image {k} ({r['id']}): role = {r['role'].replace('_', ' ')}."})
        mime = "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
        parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(path.read_bytes()).decode()}})
    parts.append({"text": text})
    return parts


def aspect(canvas):
    w, h = canvas
    return "1:1" if w == h else "16:9" if abs(w / h - 16 / 9) < 0.01 else f"{w}:{h}"


def normalise(data, canvas):
    """Centre-crop to the canvas aspect (Gemini 16:9 is 1376x768 at 1K), then resize to the canvas."""
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGB")
    raw = im.size
    w, h = canvas
    if abs(im.width / im.height - w / h) > 1e-3:
        if im.width / im.height > w / h:
            cw = round(im.height * w / h)
            im = im.crop(((im.width - cw) // 2, 0, (im.width + cw) // 2, im.height))
        else:
            ch = round(im.width * h / w)
            im = im.crop((0, (im.height - ch) // 2, im.width, (im.height + ch) // 2))
    return im.resize((w, h), Image.LANCZOS), raw


def ledger_add(**row):
    import csv
    new = not LEDGER.exists()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in LEDGER_COLS})


def cand_dir(rec):
    return (REPO / rec["target"]).parent / "gemini"


# ---------------------------------------------------------------- commands

def cmd_gen(args):
    m = load_manifest()
    by_id = {r["id"]: r for r in m["images"]}
    fixes = load_revision(args.revision)
    for rid in args.record:
        if rid not in by_id:
            sys.exit(f"not in manifest: {rid}")
        rec, fix = by_id[rid], fixes.get(rid, {})
        model = args.model or fix.get("model") or (STUDIO_MODEL if rec["canvas"][0] == rec["canvas"][1] else SCENE_MODEL)
        tag = TAG.get(model, model.replace("gemini-", ""))
        refs = resolve_refs(rec, by_id, fix)
        text = prompt_text(rec, fix)
        if args.extra:
            text += " " + args.extra
        parts = build_parts(refs, text)
        print(f"== {rid} [{rec.get('status')}] {model}, canvas {rec['canvas']}, {len(refs)} refs, {len(text.split())} words")
        for r in refs:
            print(f"   ref {r['id']}: {r['role']} <- {r['path']}")
        if fix.get("fix"):
            print(f"   fix: {fix['fix'][:300]}")
        if args.dry_run:
            continue
        out = cand_dir(rec)
        out.mkdir(parents=True, exist_ok=True)
        prefix = f"{base_stem(rec['target'])}_{args.revision}_{tag}_t"
        start = len(list(out.glob(prefix + "*.json")))
        for take in range(start + 1, start + args.takes + 1):
            stem = f"{prefix}{take:02d}"
            record = {
                "id": rid, "candidate": stem, "revision": args.revision,
                "status": "candidate_for_review",
                "canvas": rec["canvas"], "ordered_references": refs,
                "tool": "Gemini API generateContent (character/gemini_image.py)",
                "model": model, "seed": None,
                "imageConfig": {"aspectRatio": aspect(rec["canvas"]), "imageSize": args.size},
                "est_cost_usd": PRICE.get((model, args.size)),
                "prompt_sent": text,
                "negative_prompt_review_only": rec.get("negative_prompt"),
                "requested_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            }
            retried, data = [], None
            for attempt in range(args.retries + 1):
                try:
                    data, meta = generate(model, parts, aspect(rec["canvas"]), args.size)
                    break
                except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError, TimeoutError) as e:
                    err = e.read()[:500].decode(errors="replace") if isinstance(e, urllib.error.HTTPError) else str(e)
                    # Leo trips the safety filter at random (same request blocked, then passed) and the
                    # service returns 503 under load; all are worth a retry. A block bills input tokens only.
                    # A RuntimeError is an answer without an image (safety block, or a bare STOP that
                    # also happens at random); anything else is a network or service error.
                    transient = not isinstance(e, RuntimeError) or "upstream request failed" in err
                    if attempt == args.retries:
                        break
                    if "spending cap" in err:
                        sys.exit("Gemini project spending cap reached: raise it at https://ai.studio/spend")
                    retried.append(err[:300])
                    print(f"   take {take}: {'busy' if transient else 'no image'}, retry {attempt + 1}/{args.retries}")
                    time.sleep(args.pause * (6 if transient else 1))
            record["retried"] = retried
            if data is None:
                record["result"] = {"error": err}
                print(f"   take {take}: FAILED {err[:200]}")
            else:
                im, raw = normalise(data, rec["canvas"])
                png = out / f"{stem}.png"
                im.save(png)
                record["result"] = {"output_path": str(png.relative_to(REPO)), "sha256": sha256(png),
                                    "raw_size": list(raw), **meta}
                print(f"   take {take}: {png.relative_to(REPO)}")
            (out / f"{stem}.json").write_text(json.dumps(record, indent=2) + "\n")
            ledger_add(date=dt.date.today().isoformat(), record=rid, revision=args.revision, candidate=stem,
                       model=model, size=args.size, outcome="failed" if data is None else "ok",
                       retries=len(retried), est_usd="" if data is None else PRICE.get((model, args.size), ""))
            time.sleep(args.pause)


def cmd_sheet(args):
    """Current target (left) and every candidate of the revision, one row per record."""
    from PIL import Image, ImageDraw, ImageFont
    m = load_manifest()
    by_id = {r["id"]: r for r in m["images"]}
    font = ImageFont.load_default(size=18)
    w, h = 480, 270
    rows = []
    for rid in args.record:
        rec = by_id[rid]
        cands = sorted(cand_dir(rec).glob(f"{base_stem(rec['target'])}_{args.revision}_*.png"))
        # Identity roots sit beside every candidate: a face that drifts from the canonical
        # (s08 r02: cool grey, small eyes, no seam) is only obvious side by side.
        ident = [(REPO / r["path"], r["id"]) for r in rec.get("ordered_references", []) if r["role"] == "identity_root"]
        rows.append(ident + [(REPO / rec["target"], f"{rid} current")] +
                    [(c, c.stem.split(f"_{args.revision}_")[1]) for c in cands])
    cols = max(len(r) for r in rows)
    sheet = Image.new("RGB", (cols * (w + 6), len(rows) * (h + 26)), "white")
    d = ImageDraw.Draw(sheet)
    for j, row in enumerate(rows):
        for k, (p, label) in enumerate(row):
            x, y = k * (w + 6), j * (h + 26)
            if p.exists():
                im = Image.open(p).convert("RGB")
                im.thumbnail((w, h))
                sheet.paste(im, (x, y))
            d.text((x + 3, y + h + 3), label, fill="black", font=font)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)
    print(out)


def cmd_accept(args):
    """Copy a reviewed candidate to the record's new target and record it in the manifest."""
    hits = list(REPO.glob(f"character/**/gemini/{args.candidate}.json"))
    if len(hits) != 1:
        sys.exit(f"candidate {args.candidate}: {len(hits)} matches")
    cand = json.loads(hits[0].read_text())
    m = load_manifest()
    rec = next(r for r in m["images"] if r["id"] == cand["id"])
    src = REPO / cand["result"]["output_path"]
    assert sha256(src) == cand["result"]["sha256"], "candidate changed since generation"
    new_target = str(Path(rec["target"]).parent / f"{base_stem(rec['target'])}_{cand['revision']}.png")
    shutil.copyfile(src, REPO / new_target)
    if rec.get("revision") != cand["revision"]:
        rec.setdefault("superseded", []).append({"revision": rec.get("revision"), "status": rec.get("status"),
                                                 "result": rec.get("result")})
    rec.update({"revision": cand["revision"], "target": new_target, "status": "accepted"})
    rec["result"] = {
        "output_path": new_target, "sha256": sha256(REPO / new_target),
        "tool": cand["tool"], "model": cand["model"], "model_details": cand["result"].get("modelVersion"),
        "seed": None, "candidate": cand["candidate"], "imageConfig": cand["imageConfig"],
        "normalised": f"{cand['result']['raw_size'][0]}x{cand['result']['raw_size'][1]} -> "
                      f"{rec['canvas'][0]}x{rec['canvas'][1]}",
        "ordered_references": cand["ordered_references"],
        "prompt_sent": cand["prompt_sent"],
        "review": {"status": "accepted_pending_owner_review", "reviewer": args.reviewer,
                   "date": dt.date.today().isoformat(), "review_note": args.note},
    }
    save_manifest(m)
    print(f"{rec['id']}: {new_target}")


def cmd_ledger(_):
    """Markdown table: images, failed takes and estimated cost per model and size."""
    import csv
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0, 0.0])
    for r in csv.DictReader(LEDGER.open()):
        a = agg[(r["model"], r["size"])]
        if r["outcome"] == "ok":
            a[0] += 1
            a[2] += float(r["est_usd"] or 0)
        else:
            a[1] += 1
    print("| Model | Size | Images | Failed takes | ~USD/image | ~USD total |")
    print("|---|---|---|---|---|---|")
    for (mdl, size), (n, nf, usd) in sorted(agg.items()):
        print(f"| {mdl} | {size} | {n} | {nf} | {PRICE.get((mdl, size), 0):.3f} | {usd:.2f} |")
    tot = [sum(v[i] for v in agg.values()) for i in range(3)]
    print(f"| **total** | | **{tot[0]}** | {tot[1]} | | **{tot[2]:.2f}** |")


def cmd_models(_):
    for mdl in call(f"{API}/models?pageSize=1000").get("models", []):
        if "image" in mdl["name"]:
            print(mdl["name"], "-", mdl.get("displayName"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen", help="generate candidates")
    g.add_argument("--record", nargs="+", required=True, help="manifest image id(s)")
    g.add_argument("--revision", default="r02", help="revision tag; fixes from revisions/<rev>.json")
    g.add_argument("--model", help="default: revision file, else Lite for square studio, NB2 for 16:9 scenes")
    g.add_argument("--size", default="1K", help="imageSize: 1K, 2K or 4K")
    g.add_argument("--takes", type=int, default=1)
    g.add_argument("--extra", help="one-off text appended to the prompt (recorded in the sidecar)")
    g.add_argument("--retries", type=int, default=4, help="extra attempts after a no-image answer or a network/5xx error")
    g.add_argument("--pause", type=float, default=5.0, help="seconds between calls")
    g.add_argument("--dry-run", action="store_true", help="print what would be sent, no API call")
    s = sub.add_parser("sheet", help="contact sheet: current target + candidates")
    s.add_argument("--record", nargs="+", required=True)
    s.add_argument("--revision", default="r02")
    s.add_argument("--out", default=str(REPO / "work/review/gemini_sheet.jpg"))
    a = sub.add_parser("accept", help="promote a candidate to the record target")
    a.add_argument("candidate", help="candidate stem, e.g. s02_place_acorn_end_r02_nb2lite_t01")
    a.add_argument("--note", required=True, help="what was checked at full size")
    a.add_argument("--reviewer", default="agent visual review")
    sub.add_parser("models", help="list image models visible to the key")
    sub.add_parser("ledger", help="cost table per model from revisions/gemini_ledger.csv")
    args = ap.parse_args()
    {"gen": cmd_gen, "sheet": cmd_sheet, "accept": cmd_accept, "models": cmd_models, "ledger": cmd_ledger}[args.cmd](args)


if __name__ == "__main__":
    main()
