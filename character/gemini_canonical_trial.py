#!/usr/bin/env python3
"""Cloud trial: neutral full-body canonical takes of Leo and Milo with a Gemini
Pro image model, conditioned on the v4 canonicals and the v4 visual bible.

Outputs go to character/characters/<Name>/cloud_trial/ with one prompt record
(.json) per image, then a contact sheet against the current v4 canonicals.
These are candidates for owner review, not approved canonicals.

    python3 character/gemini_canonical_trial.py --list-models
    python3 character/gemini_canonical_trial.py --dry-run
    python3 character/gemini_canonical_trial.py --takes 3
    python3 character/gemini_canonical_trial.py --sheet-only

Auth: the API key travels in the x-goog-api-key header. In the cloud container
the egress proxy injects it; elsewhere set GEMINI_API_KEY (never print it).
Stdlib only for the API; Pillow for the contact sheet.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BIBLE = REPO / "stories/lion_and_mouse_v4/visual_bible.json"
API = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-3-pro-image-preview"

CANON = {
    "Milo": "character/characters/Milo/v4/canonical/full-body_milo_neutral_pose_r01.png",
    "Leo": "character/characters/Leo/v4/canonical/full-body_leo_neutral_pose_r01.png",
}

# Per-character deltas on top of the bible identity. Milo's v4 crown is already
# smooth in the reference, so the trial reinforces it rather than "editing out".
EMPHASIS = {
    "Milo": (
        "Milo's head is one smooth rounded felt dome from brow to the back of the "
        "head, with the same short felt texture as the rest of the face and no "
        "separate hair, tuft or crest. Slender build: slim waist, narrow chest, "
        "thin arms and legs, as in the reference. Large round dark-brown irises."
    ),
    "Leo": (
        "Leo keeps his full, voluminous circular rust-orange mane of layered fuzzy "
        "wool locks framing the whole face and upper chest, exactly the colour and "
        "outline of the reference (rust-orange, not crimson). Large round "
        "dark-brown irises."
    ),
}

# Per character: naming the other character's traits invites a second figure.
_COMMON = (
    "duplicate characters, extra limbs, extra paws, extra tails, disconnected tail, "
    "fused anatomy, changed face, changed iris colour, blue eyes, yellow eyes, "
    "plastic skin, glossy CGI, realistic fur, clothing, text, watermark, "
    "smeared face, blurry subject, props, scenery"
)
EXCLUSIONS = {
    "Milo": _COMMON + ", chubby body, separate top-hair tuft, hair crest on the head",
    "Leo": _COMMON + ", crimson mane, shrunken mane",
}

ACCEPTANCE = [
    "Exactly one character; whole body, ears, paws and single tail visible with margins",
    "Identity matches the v4 canonical (face, palette, proportions)",
    "Eyes: large round dark-brown irises, cream sclera",
    "Milo: smooth crown, no top tuft or crest; slender build",
    "Leo: full rust-orange mane, original volume and outline",
    "Neutral relaxed frontal stance, closed mouth, plain warm off-white studio backdrop",
    "Felt material reads as handmade wool felt, not plastic/CGI fur",
]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_prompt(name, bible):
    key = name.lower()
    return " ".join([
        "Using the attached image as the identity reference for this exact "
        f"character, create one new neutral full-body character reference of {name}.",
        bible["identity"][key],
        EMPHASIS[name],
        "Front view, standing in a relaxed neutral pose, closed gentle mouth, "
        "looking at the camera, the whole body centred with comfortable margins "
        "on all sides. Square canvas, warm off-white seamless studio backdrop, "
        "soft even neutral studio light and a small soft contact shadow under the feet.",
        bible["style"],
        "Only this one character; no props, scenery, text or watermark.",
        f"Avoid: {EXCLUSIONS[name]}.",
    ])


def api_key_header():
    key = os.environ.get("GEMINI_API_KEY")
    # Empty header lets the proxy inject the credential; a real key wins locally.
    return {"x-goog-api-key": key} if key else {}


def call(url, body=None, timeout=300):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", **api_key_header()},
        method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def check_connection():
    try:
        models = call(f"{API}/models?pageSize=1000").get("models", [])
    except urllib.error.HTTPError as e:
        sys.exit(f"Gemini API not reachable: HTTP {e.code}: {e.read()[:300].decode(errors='replace')}")
    return models


def generate(model, prompt, ref_path, aspect="1:1", size="2K"):
    body = {
        "contents": [{"role": "user", "parts": [
            {"inline_data": {"mime_type": "image/png",
                             "data": base64.b64encode(Path(ref_path).read_bytes()).decode()}},
            {"text": prompt},
        ]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": aspect, "imageSize": size},
        },
    }
    resp = call(f"{API}/models/{model}:generateContent", body)
    parts = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    images = [p for p in parts if "inlineData" in p or "inline_data" in p]
    text = " ".join(p["text"] for p in parts if "text" in p)
    meta = {k: resp.get(k) for k in ("modelVersion", "responseId", "usageMetadata")}
    meta["finishReason"] = resp.get("candidates", [{}])[0].get("finishReason")
    meta["text"] = text or None
    if not images:
        raise RuntimeError(f"no image returned: {json.dumps(meta)[:500]}")
    img = images[0].get("inlineData") or images[0]["inline_data"]
    return base64.b64decode(img["data"]), img.get("mimeType", "image/png"), meta


def out_dir(name):
    return REPO / "character/characters" / name / "cloud_trial"


def run(args):
    bible = json.loads(BIBLE.read_text())
    for name in args.characters:
        ref = REPO / CANON[name]
        assert ref.exists(), ref
        prompt = build_prompt(name, bible)
        d = out_dir(name)
        d.mkdir(parents=True, exist_ok=True)
        print(f"== {name}: {len(prompt.split())} words\n{prompt}\n")
        for take in range(1, args.takes + 1):
            stem = f"full-body_{name.lower()}_neutral_pose_gemini_t{take:02d}"
            record = {
                "id": stem.upper(),
                "status": "candidate_for_owner_review",
                "purpose": f"Cloud trial: alternative v4 neutral full-body canonical take for {name}",
                "bible": {"path": str(BIBLE.relative_to(REPO)), "revision": bible.get("revision")},
                "references": [{"path": CANON[name], "role": "identity_reference",
                                "sha256": sha256(ref)}],
                "engine": {"api": "Gemini API generateContent", "model": args.model,
                           "imageConfig": {"aspectRatio": "1:1", "imageSize": args.size},
                           "seed": None},
                "positive_prompt": prompt,
                "exclusions": EXCLUSIONS[name] + " (embedded in the prompt as an 'Avoid:' sentence; the API has no negative prompt)",
                "acceptance": ACCEPTANCE,
                "requested_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "result": None,
            }
            if args.dry_run:
                record["status"] = "planned_not_executed"
                record.pop("requested_at")
                (d / f"{stem}.json").write_text(json.dumps(record, indent=2) + "\n")
                continue
            try:
                data, mime, meta = generate(args.model, prompt, ref, size=args.size)
            except (urllib.error.HTTPError, RuntimeError) as e:
                err = e.read()[:500].decode(errors="replace") if isinstance(e, urllib.error.HTTPError) else str(e)
                record["result"] = {"error": err}
                (d / f"{stem}.json").write_text(json.dumps(record, indent=2) + "\n")
                print(f"  take {take}: FAILED {err[:200]}")
                continue
            ext = {"image/jpeg": ".jpg", "image/webp": ".webp"}.get(mime, ".png")
            img = d / f"{stem}{ext}"
            img.write_bytes(data)
            record["result"] = {"path": str(img.relative_to(REPO)), "mime": mime,
                                "sha256": sha256(img), **meta}
            (d / f"{stem}.json").write_text(json.dumps(record, indent=2) + "\n")
            print(f"  take {take}: {img.relative_to(REPO)}")
            time.sleep(args.pause)


def contact_sheet(path, characters):
    from PIL import Image, ImageDraw, ImageFont
    cell, pad, label_h = 512, 16, 40
    rows = []
    for name in characters:
        takes = sorted(p for p in out_dir(name).glob("*_gemini_t*.*") if p.suffix != ".json")
        rows.append([(f"{name} v4 canonical (current)", REPO / CANON[name])] +
                    [(p.stem.split("_")[-1] + " Gemini", p) for p in takes])
    cols = max(len(r) for r in rows)
    W = pad + cols * (cell + pad)
    H = pad + len(rows) * (cell + label_h + pad)
    sheet = Image.new("RGB", (W, H), (245, 242, 236))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    for r, row in enumerate(rows):
        y = pad + r * (cell + label_h + pad)
        for c, (label, p) in enumerate(row):
            x = pad + c * (cell + pad)
            im = Image.open(p).convert("RGB")
            im.thumbnail((cell, cell))
            sheet.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
            if c == 0:
                draw.rectangle([x - 4, y - 4, x + cell + 3, y + cell + 3], outline=(60, 120, 60), width=4)
            draw.text((x, y + cell + 8), label, fill=(30, 30, 30), font=font)
    sheet.save(path)
    print(f"contact sheet: {path.relative_to(REPO)} ({W}x{H})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--characters", nargs="+", default=["Leo", "Milo"], choices=list(CANON))
    ap.add_argument("--takes", type=int, default=3)
    ap.add_argument("--size", default="2K", help="imageSize: 1K, 2K or 4K")
    ap.add_argument("--pause", type=float, default=5.0, help="seconds between calls")
    ap.add_argument("--dry-run", action="store_true", help="print prompts and write planned records (result null), no API call")
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--sheet-only", action="store_true")
    ap.add_argument("--sheet", default="character/characters/cloud_trial_contact_sheet.jpg")
    args = ap.parse_args()

    if args.list_models:
        for m in check_connection():
            if "image" in m["name"] or "pro" in m["name"]:
                print(m["name"], "-", m.get("displayName"))
        return
    if not args.sheet_only:
        if not args.dry_run:
            names = {m["name"].split("/")[-1] for m in check_connection()}
            if args.model not in names:
                sys.exit(f"model {args.model} not offered to this key; try --list-models")
        run(args)
    if not args.dry_run:
        contact_sheet(REPO / args.sheet, args.characters)


if __name__ == "__main__":
    main()
