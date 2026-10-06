#!/usr/bin/env python3
"""One source of truth for the story's image and video prompts.

Every prompt in stories/<story>/prompt_manifest.json is stored as a template. Shared text
(character identity, setup size and background, studio, light, style) lives once in
stories/<story>/visual_bible.json and is pulled in through placeholders, so a character is
described with the same canonical words in every prompt. `lint` proves that.

    python3 production/image_prompts.py lint              # exit 1 on any error
    python3 production/image_prompts.py build             # re-render after editing the bible or a template
    python3 production/image_prompts.py show s14_opening_start
    python3 production/image_prompts.py md                # rewrite stories/<story>/prompts/*.md

Placeholders (double braces):
    {{identity:milo}}   full canonical description of a character (bible characters.<id>.identity)
    {{short:milo}}      one-sentence description for video prompts (characters.<id>.short)
    {{mouth:milo}}      the character's approved open-mouth design (characters.<id>.mouth)
    {{setup:trap_wide}} camera, background and character sizes of a camera setup (bible setups.<id>)
    {{plate:trap_morning}} location description, landmarks and light (bible locations.<id>)
    {{block:style}}     any shared text block (bible blocks.<name>)
    {{refs}}            the record's ordered references, numbered as attached, each with its role
                        in plain words (bible reference_roles) and its file name
    {{frame}}           what this frame shows (the record's `frame` text); {{frame:<record id>}} is
                        another record's, so a video prompt states exactly its start and end images

Image records:   prompt_template -> positive_prompt
Video variants:  positive_prompt_template -> positive_prompt,
                 full_prompt_specification_template -> full_prompt_specification
The rendered fields are what an image or video tool receives; never edit them by hand.
Workflow and review rules: .claude/skills/consistent-image-prompts/SKILL.md.
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(r"\{\{(identity|short|mouth|setup|plate|block|refs|frame):?([A-Za-z0-9_]*)\}\}")
CHARACTER_KINDS = {"scene", "character", "expression"}  # kinds that must describe every visible character
# An older version's image may leak its identity, so it may only supply composition or an expression.
OLD_VERSION_ROLES = {"staging_only", "expression", "camera_geometry"}
# Blocks that tell the model to edit the first attached image: that image must be the edit base.
EDIT_BLOCKS = {"edit_end_frame", "edit_reference", "edit_expression", "edit_open_mouth"}

# Conflict detector: a sentence written outside the canonical blocks that names a colour together
# with a body feature is a second, competing character description.
COLOUR_WORDS = r"grey|gray|brown|taupe|cream|ivory|white|black|pink|rose|rosy|coral|salmon|peach|red|crimson|" \
               r"scarlet|orange|rust|ginger|amber|ochre|golden|gold|yellow|mustard|tan|beige|blue|green|purple|violet"
FEATURE_WORDS = r"body|fur|belly|chest|muzzle|nose|eyes?|iris(?:es)?|sclera|brows?|eyebrows?|ears?|mane|tail|" \
                r"paws?|whiskers?|cheeks?|crown|face|legs?|arms?|toes?|snout"
COLOUR_RE = re.compile(rf"\b({COLOUR_WORDS})(?:-\w+)?\b", re.I)
FEATURE_RE = re.compile(rf"\b({FEATURE_WORDS})\b", re.I)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
PUNCTUATION_SLIP = re.compile(r"[.;,:]\s*[.;,]")  # e.g. a block ending in "." followed by a template "."


def story_paths(story):
    d = REPO / "stories" / story
    return d, d / "prompt_manifest.json", d / "visual_bible.json"


def load(story):
    d, mp, bp = story_paths(story)
    return json.loads(mp.read_text()), json.loads(bp.read_text())


def save_manifest(story, manifest):
    _, mp, _ = story_paths(story)
    mp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- rendering

def plate_text(bible, loc_id, landmarks=True):
    loc = bible["locations"][loc_id]
    parts = [loc["description"]]
    if landmarks and loc.get("landmarks"):
        parts.append("Fixed landmarks: " + "; ".join(loc["landmarks"]) + ".")
    if loc.get("light"):
        parts.append(loc["light"])
    return " ".join(parts)


def setup_text(bible, setup_id, chars=()):
    """Camera, background and the measured sizes of the characters in this frame only, so a frame
    without a character never reads that character's size. Close-ups name the place without its
    landmark list, because the background is blurred."""
    s = bible["setups"][setup_id]
    treat = s.get("background_treatment")
    background = plate_text(bible, s["location"], landmarks=not treat)
    if treat:
        background = f"{treat} {background}"
    sizes = [s.get("size", {}).get(c, "") for c in chars]
    if len(chars) > 1:
        sizes.append(s.get("relation", ""))
    return " ".join(p for p in [s["camera"], background, *sizes] if p)


def ref_character(bible, ref, target):
    """Name of the single character a reference shows (its record's counts), else a neutral word."""
    chars = [c for c, n in ((target or {}).get("counts") or {}).items() if c in bible["characters"] and n > 0]
    if ref.get("character") in bible["characters"]:
        chars = [ref["character"]]
    return bible["characters"][chars[0]]["name"] if len(chars) == 1 else "the character"


def refs_text(bible, rec, images):
    """Numbered list of the attached reference images, so the prompt states what each one is for."""
    items = []
    for k, ref in enumerate(rec.get("ordered_references", []), 1):
        target = images.get(ref.get("id"))
        path = target["target"] if target else ref.get("path", "")
        what = (target or {}).get("label") or ref.get("note") or ref.get("id", "")
        sentence = bible["reference_roles"][ref["role"]].format(who=ref_character(bible, ref, target),
                                                                 what=what.rstrip("."))
        items.append(f"({k}) {sentence} [{Path(path).name}].")
    return ("Attached reference images, in this order: " + " ".join(items)) if items else ""


def resolve(bible, kind, arg, rec=None, images=None):
    if kind == "identity":
        return bible["characters"][arg]["identity"]
    if kind == "short":
        return bible["characters"][arg]["short"]
    if kind == "mouth":
        return bible["characters"][arg]["mouth"]
    if kind == "frame":
        return ((images or {})[arg] if arg else rec)["frame"].rstrip(".")
    if kind == "setup":
        return setup_text(bible, arg, visible_characters(rec or {}, bible))
    if kind == "plate":
        return plate_text(bible, arg)
    if kind == "refs":
        return refs_text(bible, rec or {}, images or {})
    return bible["blocks"][arg]


def render(bible, template, rec=None, images=None):
    out = PLACEHOLDER.sub(lambda m: resolve(bible, m.group(1), m.group(2), rec, images), template)
    return re.sub(r"\s+", " ", out).strip()


def placeholders(template):
    return [(m.group(1), m.group(2)) for m in PLACEHOLDER.finditer(template)]


def literal_text(template):
    return PLACEHOLDER.sub(" ", template)


def build(manifest, bible):
    """Render every template into its prompt field; returns the number of changed fields."""
    changed = 0
    images = {r["id"]: r for r in manifest["images"]}
    for rec in manifest["images"]:
        if "prompt_template" in rec:
            new = render(bible, rec["prompt_template"], rec, images)
            changed += rec.get("positive_prompt") != new
            rec["positive_prompt"] = new
    for shot in manifest["shots"]:
        for v in shot["variants"]:
            for tkey, key in (("positive_prompt_template", "positive_prompt"),
                              ("full_prompt_specification_template", "full_prompt_specification")):
                if tkey in v:
                    new = render(bible, v[tkey], None, images)
                    changed += v.get(key) != new
                    v[key] = new
            rt = v.get("runtime_export_candidate")
            if rt:
                sheets = {c: bible["characters"][c]["sheet"] for c in shot.get("cast", [])}
                changed += rt.get("character_sheets") != sheets
                rt["character_sheets"] = sheets
    return changed


# ---------------------------------------------------------------- lint

def visible_characters(rec, bible):
    return sorted(c for c in rec.get("counts", {}) if c in bible["characters"] and rec["counts"][c] > 0)


def identity_conflicts(text, where, allow=()):
    """Sentences outside the canonical blocks that pair a colour with a body feature."""
    hits = []
    for sentence in SENTENCE_SPLIT.split(text):
        if any(a in sentence for a in allow):
            continue
        if COLOUR_RE.search(sentence) and FEATURE_RE.search(sentence):
            hits.append(f"{where}: identity words outside the canonical block: \"{sentence.strip()[:160]}\"")
    return hits


def drift_hits(bible, text):
    hits = []
    for cid, c in bible["characters"].items():
        for phrase in c.get("drift_phrases", []):
            if re.search(rf"\b{re.escape(phrase)}\b", text, re.I):
                hits.append(f"{cid}: '{phrase}'")
    for phrase in bible.get("lint", {}).get("forbidden_in_prompts", []):
        if re.search(rf"\b{re.escape(phrase)}\b", text, re.I):
            hits.append(f"'{phrase}'")
    return hits


def lint(manifest, bible):
    errors, warnings = [], []
    E, W = errors.append, warnings.append
    images = {r["id"]: r for r in manifest["images"]}
    allow = bible.get("lint", {}).get("allow_phrases", [])

    # The bible itself must be coherent: the short description may not introduce colour words that
    # the full canonical description does not use, and no block may contain a drift phrase.
    for cid, c in bible["characters"].items():
        full_colours = {w.lower() for w in COLOUR_RE.findall(c["identity"])}
        for w in COLOUR_RE.findall(c["short"]) + COLOUR_RE.findall(c["sheet"]):
            if w.lower() not in full_colours:
                E(f"bible characters.{cid}: short/sheet colour '{w}' is not in the canonical identity")
        if not c["short"].startswith(c["name"] + " is " + c["sheet"]):
            E(f"bible characters.{cid}: short must read '<Name> is <sheet>...'")
    for name, text in [(f"blocks.{k}", v) for k, v in bible["blocks"].items()] + \
                      [(f"characters.{k}.identity", v["identity"]) for k, v in bible["characters"].items()]:
        for h in drift_hits(bible, text):
            E(f"bible {name}: drift phrase {h}")
    for sid, s in bible["setups"].items():
        if s["location"] not in bible["locations"]:
            E(f"bible setups.{sid}: unknown location {s['location']}")
        if s.get("anchor_record") and s["anchor_record"] not in images:
            E(f"bible setups.{sid}: anchor_record {s['anchor_record']} is not a manifest record")
        elif s.get("anchor_record") and images[s["anchor_record"]].get("setup") != sid:
            E(f"bible setups.{sid}: anchor_record {s['anchor_record']} belongs to another setup")
        size_text = " ".join(list(s.get("size", {}).values()) + [s.get("relation", "")])
        for h in identity_conflicts(s["camera"] + " " + size_text, f"bible setups.{sid}", allow):
            E(h)
        for c in s.get("size", {}):
            if c not in bible["characters"]:
                E(f"bible setups.{sid}: size for unknown character {c}")

    shot_of = {}
    for s in manifest["shots"]:
        shot_of[s["start_image"]] = (s, "start")
        shot_of[s["end_image"]] = (s, "end")

    for rec in manifest["images"]:
        rid = rec["id"]
        tpl = rec.get("prompt_template")
        if tpl is None:
            E(f"{rid}: no prompt_template")
            continue
        try:
            rendered = render(bible, tpl, rec, images)
        except KeyError as e:
            E(f"{rid}: placeholder refers to a missing bible entry {e}")
            continue
        if rendered != rec.get("positive_prompt"):
            E(f"{rid}: positive_prompt differs from its rendered template (run build; never edit it by hand)")
        ph = placeholders(tpl)
        kind = rec.get("prompt_kind")
        vis = visible_characters(rec, bible)
        ids = [a for k, a in ph if k == "identity"]
        if kind in CHARACTER_KINDS:
            for c in vis:
                if ids.count(c) != 1:
                    E(f"{rid}: visible character {c} needs exactly one {{{{identity:{c}}}}} (found {ids.count(c)})")
        for c in ids:
            if c not in vis:
                E(f"{rid}: {{{{identity:{c}}}}} but {c} is not in counts")
        own_text = " ".join([literal_text(tpl), rec.get("label", ""), rec.get("frame", "")])
        for h in identity_conflicts(own_text, rid, allow + rec.get("lint_allow", [])):
            E(h)
        if rec.get("ordered_references") and not rec.get("label"):
            W(f"{rid}: no label (used when other prompts name this image as a reference)")
        for h in drift_hits(bible, rendered):
            E(f"{rid}: drift phrase {h}")
        if PUNCTUATION_SLIP.search(rendered):
            E(f"{rid}: doubled punctuation in the rendered prompt: '{PUNCTUATION_SLIP.search(rendered).group(0)}'")

        frames = [a for k, a in ph if k == "frame"]
        if kind == "scene" and (frames != [""] or not rec.get("frame")):
            E(f"{rid}: a scene prompt needs a `frame` text and exactly one {{{{frame}}}}")
        if any(k == "block" and a in EDIT_BLOCKS for k, a in ph):
            first = (rec.get("ordered_references") or [{}])[0]
            if first.get("role") != "edit_base":
                E(f"{rid}: the prompt edits the first attached image, but its role is '{first.get('role')}', not edit_base")

        if kind == "scene":
            setups = [a for k, a in ph if k == "setup"]
            if len(setups) != 1:
                E(f"{rid}: scene prompt needs exactly one {{{{setup:...}}}} (found {len(setups)})")
                continue
            sid = setups[0]
            if sid not in bible["setups"]:
                continue
            s = bible["setups"][sid]
            if rec.get("setup") != sid:
                E(f"{rid}: record setup '{rec.get('setup')}' but template uses {sid}")
            if rec.get("framing") != s["framing"]:
                E(f"{rid}: framing '{rec.get('framing')}' but setup {sid} is '{s['framing']}'")
            if s["framing"] in ("scene_wide", "close_two_shot"):
                for c in vis:
                    if c not in s.get("size", {}):
                        E(f"{rid}: setup {sid} has no measured size for visible character {c}")
            plate = bible["locations"][s["location"]].get("plate")
            refs = [r["path"] for r in rec.get("ordered_references", [])]
            if plate and plate not in refs and not rid.endswith(("_end", "_open")):
                W(f"{rid}: locked plate {plate} is not among the references")
            if rid in shot_of:
                shot, which = shot_of[rid]
                other = images.get(shot["end_image" if which == "start" else "start_image"])
                if other and other.get("setup") != rec.get("setup"):
                    E(f"{rid}: start and end of {shot['id']} use different setups "
                      f"({rec.get('setup')} / {other.get('setup')})")
                if which == "end":
                    first = (rec.get("ordered_references") or [{}])[0]
                    if first.get("id") != shot["start_image"]:
                        E(f"{rid}: first reference must be its start frame {shot['start_image']} (edit base)")

        refs = rec.get("ordered_references", [])
        n_refs = [k for k, _ in ph].count("refs")
        if refs and n_refs != 1:
            E(f"{rid}: {len(refs)} reference images but {n_refs} {{{{refs}}}} placeholders; the prompt must name them")
        canon_of = {c.get("canonical_record"): cid for cid, c in bible["characters"].items()}
        attached = {canon_of[r["id"]] for r in refs if r.get("id") in canon_of}
        for ref in refs:
            attached.update(c for c in ref.get("covers_characters", []) if c in bible["characters"])
        if kind in CHARACTER_KINDS:
            for c in vis:
                if c not in attached and bible["characters"][c].get("canonical_record") != rid:
                    E(f"{rid}: {c} is visible but its canonical {bible['characters'][c].get('canonical_record')} "
                      f"is not attached")
        for ref in refs:
            shown = visible_characters(images[ref["id"]], bible) if ref.get("id") in images else []
            if ref.get("role") != "staging_only" and set(shown) - set(vis):
                E(f"{rid}: reference {ref['id']} shows {sorted(set(shown) - set(vis))}, who is not in this frame")
        for c in sorted(attached - set(vis)):
            E(f"{rid}: canonical of {c} attached although {c} is not visible (it may be drawn into the frame)")
        for ref in refs:
            if ref.get("role") not in bible["reference_roles"]:
                E(f"{rid}: reference {ref.get('id')} has unknown role '{ref.get('role')}' (see bible reference_roles)")
            p = ref.get("path", "")
            if ref.get("id") in images:
                cur = images[ref["id"]]["target"]
                if p != cur:
                    E(f"{rid}: reference {ref['id']} points to {p}, current target is {cur}")
                p = cur
            if p and not (REPO / p).exists() and images.get(ref.get("id"), {}).get("status") != "planned":
                (W if ref.get("id") in images else E)(f"{rid}: reference file missing: {p}")
            if re.search(r"/v[0-9]+/", p) and f"/{bible.get('version', 'v4')}/" not in p \
                    and ref.get("role") not in OLD_VERSION_ROLES:
                E(f"{rid}: older-version reference {p} may only be {sorted(OLD_VERSION_ROLES)}")
        for word in bible.get("lint", {}).get("warn_words", []):
            if re.search(rf"\b{word}\b", rendered, re.I):
                W(f"{rid}: rendered prompt contains '{word}'")

    for shot in manifest["shots"]:
        cast = shot.get("cast", [])
        for v in shot["variants"]:
            vid = v["id"]
            for tkey, key, want in (("positive_prompt_template", "positive_prompt", "short"),
                                    ("full_prompt_specification_template", "full_prompt_specification", "identity")):
                tpl = v.get(tkey)
                if tpl is None:
                    E(f"{vid}: no {tkey}")
                    continue
                try:
                    rendered = render(bible, tpl, None, images)
                except KeyError as e:
                    E(f"{vid}: placeholder refers to a missing bible entry or record {e}")
                    continue
                if rendered != v.get(key):
                    E(f"{vid}: {key} differs from its rendered template (run build)")
                endpoints = (v.get("start_image", shot["start_image"]), v.get("end_image", shot["end_image"]))
                for k, a in placeholders(tpl):
                    if k == "frame" and a not in endpoints:
                        E(f"{vid}: {{{{frame:{a}}}}} is not this variant's start or end image")
                got = [a for k, a in placeholders(tpl) if k == want]
                for c in cast:
                    if got.count(c) != 1:
                        E(f"{vid}: {key} needs exactly one {{{{{want}:{c}}}}}")
                for h in identity_conflicts(literal_text(tpl), f"{vid}.{key}", allow):
                    E(h)
                for h in drift_hits(bible, v.get(key, "")):
                    E(f"{vid}.{key}: drift phrase {h}")
                if PUNCTUATION_SLIP.search(rendered):
                    E(f"{vid}.{key}: doubled punctuation: '{PUNCTUATION_SLIP.search(rendered).group(0)}'")
    return errors, warnings


# ---------------------------------------------------------------- markdown

def md_image(rec, images):
    lines = [f"## Image {rec['id']}", ""]
    tgt = rec["target"]
    exists = (REPO / tgt).exists()
    review = ((rec.get("result") or {}).get("review") or {})
    lines += [f"- Target: `{tgt}`{'' if exists else ' (missing)'}",
              f"- Status: `{rec.get('status')}` · revision `{rec.get('revision')}`"
              + (f" · review `{review.get('status')}`" if isinstance(review, dict) and review.get("status") else ""),
              f"- Kind: `{rec.get('prompt_kind')}`"
              + (f" · setup `{rec['setup']}` · framing `{rec.get('framing')}`" if rec.get("setup") else ""),
              f"- Canvas: {rec['canvas'][0]} × {rec['canvas'][1]}",
              "- Ordered references:"]
    for k, ref in enumerate(rec.get("ordered_references", []), 1):
        p = images[ref["id"]]["target"] if ref.get("id") in images else ref.get("path")
        lines.append(f"  {k}. `{p}` — {ref.get('role', '')}{'' if (REPO / p).exists() else ' (missing)'}")
    lines += ["", "**Prompt (rendered from the template)**", "", rec["positive_prompt"], ""]
    if rec.get("negative_prompt"):
        lines += ["**Review-only exclusions** (not sent: no negative pass)", "", rec["negative_prompt"], ""]
    if rec.get("acceptance"):
        lines += ["**Acceptance**", ""] + [f"- [ ] {a}" for a in rec["acceptance"]] + [""]
    return lines


def md_shot(shot):
    lines = [f"## Video {shot['id']}", "",
             f"- Start `{shot['start_image']}` → end `{shot['end_image']}` · cast: {', '.join(shot.get('cast', [])) or 'none'}", ""]
    for v in shot["variants"]:
        ends = f" · start `{v['start_image']}` → end `{v['end_image']}`" if v.get("start_image") else ""
        lines += [f"### {v['id']} ({v.get('mode')}){ends}", "", v["positive_prompt"], ""]
    return lines


def write_md(story, manifest):
    d, _, _ = story_paths(story)
    out_dir = d / "prompts"
    out_dir.mkdir(exist_ok=True)
    images = {r["id"]: r for r in manifest["images"]}
    groups = {}
    for rec in manifest["images"]:
        groups.setdefault(rec["group"], []).append(rec)
    shots_by_group = {}
    for s in manifest["shots"]:
        shots_by_group.setdefault(f"scene-{s['scene']:02d}", []).append(s)
    written = []
    for group, recs in groups.items():
        lines = [f"# {group}: prompt records", "",
                 "Generated by `python3 production/image_prompts.py md` from `../prompt_manifest.json` and "
                 "`../visual_bible.json`; do not edit by hand. Shared character, setup and style text comes "
                 "from the bible, so every prompt describes the characters identically.", ""]
        for rec in recs:
            lines += md_image(rec, images)
        for shot in shots_by_group.get(group, []):
            lines += md_shot(shot)
        (out_dir / f"{group}.md").write_text("\n".join(lines).rstrip() + "\n")
        written.append(group)
    return written


# ---------------------------------------------------------------- review sheet

def review_sheet(story, manifest, bible, rid, candidate=None, out=None):
    """Side-by-side gate for one record: canonicals, setup anchor, plate and previous shot above,
    the candidate below, scene images with a 0.1 grid so sizes can be compared."""
    from PIL import Image, ImageDraw, ImageFont
    images = {r["id"]: r for r in manifest["images"]}
    rec = images[rid]
    font = ImageFont.load_default(size=18)
    top = []
    for c in visible_characters(rec, bible):
        canon = bible["characters"][c].get("canonical")
        if canon:
            top.append((REPO / canon, f"{c} canonical"))
    for ref in rec.get("ordered_references", []):
        if "expression" in ref.get("role", ""):
            top.append((REPO / ref["path"], ref["id"]))
    s = bible["setups"].get(rec.get("setup") or "", {})
    if s.get("anchor_record") in images and s["anchor_record"] != rid:
        top.append((REPO / images[s["anchor_record"]]["target"], f"size anchor {s['anchor_record']}"))
    plate = bible["locations"].get(s.get("location", ""), {}).get("plate")
    if plate:
        top.append((REPO / plate, "locked plate"))
    shots = {sh["id"]: sh for sh in manifest["shots"]}
    own = next((sh for sh in manifest["shots"] if rid in (sh["start_image"], sh["end_image"])), None)
    prev = shots.get(own.get("previous_shot")) if own else None
    if prev and prev["end_image"] in images:
        top.append((REPO / images[prev["end_image"]]["target"], f"previous shot end ({prev['id']})"))
    cand = Path(candidate) if candidate else REPO / rec["target"]
    bottom = [(cand, f"{rid} {'candidate' if candidate else 'current'}")]

    def tile(path, label, w, h, grid):
        im = Image.new("RGB", (w, h + 26), "white")
        if path.exists():
            src = Image.open(path).convert("RGB")
            src.thumbnail((w, h))
            if grid:
                d = ImageDraw.Draw(src)
                for k in range(1, 10):
                    d.line([(src.width * k / 10, 0), (src.width * k / 10, src.height)], fill=(255, 0, 255))
                    d.line([(0, src.height * k / 10), (src.width, src.height * k / 10)], fill=(0, 255, 255))
            im.paste(src, (0, 0))
        ImageDraw.Draw(im).text((4, h + 4), label if path.exists() else label + " (missing)", fill="black", font=font)
        return im

    tw, th = 420, 300
    row1 = [tile(p, lab, tw, th, "canonical" not in lab and "EXPR" not in lab) for p, lab in top]
    big = tile(bottom[0][0], bottom[0][1], tw * 2, th * 2, True)
    width = max(len(row1) * (tw + 6), big.width)
    sheet = Image.new("RGB", (width, th + 32 + big.height), "white")
    for k, t in enumerate(row1):
        sheet.paste(t, (k * (tw + 6), 0))
    sheet.paste(big, (0, th + 32))
    out = Path(out) if out else REPO / "work" / "review" / f"{rid}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    return out


# ---------------------------------------------------------------- new story

def new_story(slug, template_story):
    """Create stories/<slug>/ with an empty manifest and a bible skeleton that keeps the shared
    blocks and lint settings of an existing story; characters, locations and setups start empty."""
    d, mp, bp = story_paths(slug)
    if bp.exists() or mp.exists():
        sys.exit(f"{d} already has a bible or manifest")
    _, _, tbp = story_paths(template_story)
    tb = json.loads(tbp.read_text())
    bible = {
        "revision": f"{slug}-draft",
        "how_to": "Fill in order: characters (from approved prop-free canonicals), cast_scale, locations "
                  "(one approved plate each), setups (camera + measured size anchor), then manifest records "
                  "with prompt templates. See .claude/skills/consistent-image-prompts/SKILL.md.",
        "characters": {"example_id": {
            "name": "Example", "canonical": "character/characters/<story>/Example/canonical/<file>.png",
            "identity": "Full canonical description written from the approved canonical image: silhouette, "
                        "head, ears, eyes, brows, nose, muzzle, mouth, whiskers, seams, torso, limbs, tail, "
                        "colours with hex codes, proportions, feature counts, surface, brightness.",
            "sheet": "one-line predicate for video prompts", "short": "Example is one-line predicate for video prompts.",
            "palette": {}, "proportions": {}, "checklist": [], "drift_phrases": []}},
        "cast_scale": {"lineup": "Same-depth standing heights and head widths of every character, as ratios."},
        "locations": {}, "setups": {},
        # only story-independent text; the size lineup and props are rewritten per story
        "blocks": {k: v for k, v in tb["blocks"].items() if k in tb.get("generic_blocks", [])},
        "generic_blocks": tb.get("generic_blocks", []),
        "reference_roles": tb.get("reference_roles", {}),
        "lint": tb.get("lint", {}),
    }
    d.mkdir(parents=True, exist_ok=True)
    bp.write_text(json.dumps(bible, indent=2, ensure_ascii=False) + "\n")
    mp.write_text(json.dumps({"revision": f"{slug}-draft", "images": [], "shots": []}, indent=2) + "\n")
    return d


# ---------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", default="lion_and_mouse_v4")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lint", help="check every prompt; exit 1 on errors")
    b = sub.add_parser("build", help="render templates into the prompt fields")
    b.add_argument("--check", action="store_true", help="only report whether a build would change anything")
    s = sub.add_parser("show", help="print one record's template and rendered prompt")
    s.add_argument("record")
    sub.add_parser("md", help="rewrite stories/<story>/prompts/*.md from the manifest")
    r = sub.add_parser("review", help="side-by-side review sheet for one record -> work/review/<id>.jpg")
    r.add_argument("record")
    r.add_argument("--image", help="candidate file to review instead of the record's current target")
    r.add_argument("--out")
    n = sub.add_parser("new-story", help="create stories/<slug>/ with an empty manifest and a bible skeleton")
    n.add_argument("slug")
    args = ap.parse_args()
    if args.cmd == "new-story":
        print("created", new_story(args.slug, args.story).relative_to(REPO))
        return
    manifest, bible = load(args.story)

    if args.cmd == "lint":
        errors, warnings = lint(manifest, bible)
        for w in warnings:
            print("warning:", w)
        for e in errors:
            print("ERROR:", e)
        print(f"{len(errors)} errors, {len(warnings)} warnings")
        sys.exit(1 if errors else 0)
    if args.cmd == "build":
        n = build(manifest, bible)
        if args.check:
            print(f"{n} prompt fields would change")
            sys.exit(1 if n else 0)
        save_manifest(args.story, manifest)
        print(f"{n} prompt fields re-rendered")
    elif args.cmd == "show":
        rec = next((r for r in manifest["images"] if r["id"] == args.record), None)
        if rec is None:
            sys.exit(f"no image record {args.record}")
        images = {r["id"]: r for r in manifest["images"]}
        print("TEMPLATE:\n" + rec.get("prompt_template", "(none)") + "\n\nRENDERED:\n"
              + render(bible, rec["prompt_template"], rec, images))
    elif args.cmd == "md":
        print("wrote", ", ".join(f"prompts/{g}.md" for g in write_md(args.story, manifest)))
    elif args.cmd == "review":
        print(review_sheet(args.story, manifest, bible, args.record, args.image, args.out))


if __name__ == "__main__":
    main()
