#!/usr/bin/env python3
"""Write a chained story's packet (CR-21) from its source file and an earlier version.

    python3 production/chain_packet.py stories/lion_and_mouse_v6/chain_source.py
    python3 production/image_prompts.py --story lion_and_mouse_v6 build && ... lint && ... md
    python3 production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v5 apply

The source (see stories/lion_and_mouse_v6/chain_source.py) names the BASE story whose bible and
accepted images are reused, the NEW_IMAGES the chain still needs (boundary frames, open-mouth
frames, entrances, empty views) and the PIECES in film order. This writes stories/<slug>/:
visual_bible.json (the base bible with `chained_coverage` on), prompt_manifest.json (the base
image records it carries over, the new image records, one shot per piece), dialogue_coverage.json
(the base line list, each line mapped to its pieces), SHOT_PLAN.md and README.md.

Carried over: every base image record except the expression studies (group `expressions`), whose
records stay in the base story; scene records reach those files by path. A piece with `reuse`
copies the base variant verbatim, so its renders can be reused (lint checks endpoints, prompt and
frames). Other pieces get new video prompts that describe only what is in frame (the v5 scene 15
lesson: in fast mode a named absent object is drawn in).

It overwrites the packet: use it until the first new image is accepted, then edit the bible and
manifest directly (CR-18), as with production/story_packet.py.
"""
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("chain_source", sys.argv[1])
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

REPO = Path(__file__).resolve().parents[1]
D = REPO / "stories" / S.SLUG
BASE = REPO / "stories" / S.BASE
KEYFRAMES = f"character/characters/{S.SLUG}/interactions/keyframes"

bb = json.loads((BASE / "visual_bible.json").read_text())
bm = json.loads((BASE / "prompt_manifest.json").read_text())
bc = json.loads((BASE / "dialogue_coverage.json").read_text())
base_images = {r["id"]: r for r in bm["images"]}
base_variants = {v["id"]: (s, v) for s in bm["shots"] for v in s["variants"]}
LINES = {ln["id"]: ln for ln in bc["lines"]}
CHARS = bb["characters"]
NUM = {1: "one", 2: "two", 3: "three"}


def resolve_base_files():
    """Record id -> the file the base story's renders actually used. The owner renamed some v5 files after
    the records were written; export_runtime.py --images resolves them through the image-set READMEs, and
    so does this. A target that exists only with a doubled extension (`.png.png`) is taken as it is."""
    sys.path.insert(0, str(REPO / "production"))
    from export_runtime import image_map
    try:
        found = {rid: str(f.resolve().relative_to(REPO.resolve())) for rid, f in image_map(S.BASE).items()}
    except FileNotFoundError:
        found = {}
    for r in bm["images"]:
        t = REPO / r["target"]
        if r["id"] not in found and not t.exists() and Path(str(t) + ".png").exists():
            found[r["id"]] = r["target"] + ".png"
    return found


def bible():
    b = copy.deepcopy(bb)
    b.update(revision=S.REVISION, version=S.SLUG, status="single_source_of_truth_for_all_prompts",
             chained_coverage=True, keyframe_chrono_naming=True)
    b["how_to"] = (f"Chained story (CR-21), built by production/chain_packet.py from {S.BASE}. Every prompt in "
                   f"prompt_manifest.json is a template rendered from this file by production/image_prompts.py --story "
                   f"{S.SLUG}; piece timing comes from production/chain_plan.py.")
    b["blocks"].update(S.BLOCKS)
    b["reference_roles"].update(S.REFERENCE_ROLES)
    return b


def ref(rid, role, images):
    if rid in images:
        return {"id": rid, "role": role, "path": images[rid]["target"]}
    if rid in base_images:            # an expression study kept in the base story: attached by path
        r = base_images[rid]
        chars = [c for c, n in r.get("counts", {}).items() if c in CHARS and n]
        return {"id": rid, "role": role, "path": r["target"], "character": chars[0] if chars else None,
                "note": r.get("label")}
    raise SystemExit(f"unknown reference {rid}")


def cast_line(counts):
    vis = [c for c in CHARS if counts.get(c)]
    if not vis:
        return "No character is visible in this frame."
    parts = [f"exactly {NUM[counts[c]]} {CHARS[c]['name']}" for c in vis]
    return "Visible cast: " + " and ".join(parts) + "; no other character, no duplicates."


def new_image(spec, images, b):
    """A scene record built like the base story's scene records (CR-18 template order)."""
    setup = b["setups"][spec["setup"]]
    world = images.get(spec.get("world_from") or "") or base_images.get(spec.get("world_from") or "")
    counts = dict(spec.get("counts") or (world or {}).get("counts") or {})
    if spec.get("chars") is not None:   # the cast is the spec's; only prop counts come from the world frame
        counts = {k: v for k, v in counts.items() if k not in CHARS} | {c: 1 for c in spec["chars"]}
    vis = [c for c in CHARS if counts.get(c)]
    refs = [ref(rid, role, images) for rid, role in spec["refs"]]
    parts = [f"Create one 1920x1080 16:9 still image: {spec['what']}, {setup['label']}.", "{{refs}}"]
    if refs and refs[0]["role"] == "edit_base":
        parts.append("{{block:edit_open_mouth}}" if spec.get("mouth") else "{{block:edit_chain_frame}}")
    parts.append(cast_line(counts))
    parts += [f"{{{{identity:{c}}}}}" for c in vis]
    if len(vis) > 1:
        parts.append("{{block:cast_scale}}")
    parts.append(f"{{{{setup:{spec['setup']}}}}}")
    if vis:
        parts.append("{{block:light_and_colour}}")
    if world:                         # the world-state blocks (acorn, net) of the frame it continues
        parts += re.findall(r"\{\{block:(?:acorn|net)_[a-z_]+\}\}", world["prompt_template"])
    if spec.get("state"):
        parts.append(spec["state"])
    if spec.get("mouth"):
        parts.append(f"{{{{mouth:{spec['mouth']}}}}}")
    parts += ["This frame shows: {{frame}}.", "{{block:style}}"]
    if vis:
        parts.append("{{block:final_check}}")
    return {"id": spec["id"], "group": None, "revision": "r01", "status": "planned", "bible_revision": S.REVISION,
            "target": None, "canvas": [1920, 1080], "purpose": spec["why"], "label": spec["what"],
            "prompt_kind": "scene", "counts": counts, "ordered_references": refs, "setup": spec["setup"],
            "framing": setup["framing"], "frame": spec["frame"], "prompt_template": " ".join(parts),
            "allowed_delta": spec.get("delta", "Only what `frame` describes changes from the first reference."),
            "protected": "Identity, anatomical scale, plate landmarks, camera, crop and light; prop state unless stated.",
            "acceptance": [], "result": None}


def mouth_sentence(mode, start, end):
    if mode == "ambient":
        return "No character is in the scene; only the ambient motion moves."
    if mode != "mouth":
        return "Mouths stay closed throughout; expressions come from the eyes and brows."
    opens, closes = end.endswith("_open"), start.endswith("_open")
    tail = ("ending on the approved open-mouth shape" if opens else
            "starting from the approved open-mouth shape and ending with the lips closed" if closes else
            "ending with the lips closed")
    return f"The speaking mouth opens and closes softly in small rounded shapes, as in gentle speech, {tail}."


def endpoint_text(rid, images):
    rec = images[rid]
    return "{{frame:" + rid + "}}" if rec.get("frame") else "the empty approved view of this place"


def piece(p, order, prev, images, b):
    setup = b["setups"][p["setup"]]
    loc = b["locations"][setup["location"]]
    cast = [c for c in CHARS if any(images[i].get("counts", {}).get(c) for i in (p["start"], p["end"]))]
    shot = {"id": p["id"], "scene": p["scene"], "order": order, "status": "planned", "bible_revision": S.REVISION,
            "setup": p["setup"], "location_profile": setup["location"], "cast": cast,
            "start_image": p["start"], "end_image": p["end"], "lines": p["lines"],
            "join_in": p.get("join", "chain"), "previous_shot": prev, "owner_selection": None}
    for k in ("cut", "transition", "hold", "reuse"):
        if p.get(k) is not None:
            shot[{"cut": "cut_reason"}.get(k, k)] = p[k]
    if p.get("reuse"):
        _, v = base_variants[p["reuse"]]
        v = copy.deepcopy(v)
        v.update(id=f"{p['id']}_{v['mode']}_reuse", start_image=p["start"], end_image=p["end"],
                 dialogue_line_ids=p["lines"], reused_from={"story": S.BASE, "variant": p["reuse"]})
        shot["reuse"] = {"story": S.BASE, "variant": p["reuse"]}
        shot["variants"] = [v]
        return shot
    mode = p.get("mode", "closed")
    shorts = " ".join(f"{{{{short:{c}}}}}" for c in cast)
    idents = " ".join(f"{{{{identity:{c}}}}}" for c in cast)
    close = setup["framing"] == "dialogue_close_up"
    ambient = "The softly blurred background stays calm." if close else loc["ambient"]
    body = " Head-and-shoulders portrait; the body stays still." if close else ""
    speech = mouth_sentence(mode, p["start"], p["end"])
    speakers = sorted({LINES[i]["speaker"] for i in p["lines"]} - {"NARRATOR"})
    pos = (f"{p['action']}{body} {speech} Fixed camera. {ambient} {shorts} The view is {setup['label']}, "
           "unchanged framing and light. {{block:runtime_style}}")
    full = (f"{p['action']}{body} {speech} The camera stays fixed in framing, crop and background scale for the "
            f"whole clip. {idents} Start frame: {endpoint_text(p['start'], images)}. End frame: "
            f"{endpoint_text(p['end'], images)}. Ambient: {loc['ambient']} {{{{plate:{setup['location']}}}}} "
            "{{block:style}}")
    shot["variants"] = [{
        "id": f"{p['id']}_{mode}_r01", "mode": mode, "action_text": p["action"],
        "start_image": p["start"], "end_image": p["end"],
        "positive_prompt_template": re.sub(r"\s+", " ", pos).strip(),
        "full_prompt_specification_template": re.sub(r"\s+", " ", full).strip(),
        "negative_prompt": S.REVIEW_NEGATIVE, "frames": 81, "fps": 16, "size": [1280, 720],
        "seeds": [1, 2] if (p["start"] == p["end"]) else [1, 2, 3],
        "speaker": (speakers[0] if len(speakers) == 1 else None) if mode == "mouth" else None,
        "dialogue_line_ids": p["lines"], "result": None}]
    return shot


def main():
    b = bible()
    images = {r["id"]: dict(copy.deepcopy(r), carried_from=S.BASE) for r in bm["images"] if r["group"] != "expressions"}
    for rid, f in resolve_base_files().items():
        if rid in images and images[rid]["target"] != f:
            images[rid]["base_target"] = images[rid]["target"]
            images[rid]["target"] = f
    order = list(images)
    for spec in S.NEW_IMAGES:
        if spec["id"] in images:
            raise SystemExit(f"duplicate image id {spec['id']}")
        images[spec["id"]] = new_image(spec, images, b)
        order.append(spec["id"])
    ids = [p["id"] for p in S.PIECES]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate piece ids")
    shots, prev = [], None
    for n, p in enumerate(S.PIECES, 1):
        for k in ("start", "end"):
            if p[k] not in images:
                raise SystemExit(f"{p['id']}: unknown {k} image {p[k]}")
        shots.append(piece(p, n, prev, images, b))
        prev = p["id"]
    # new images: group, chronological file name (first use in the scene) and the pieces they join
    seen, users = {}, {}
    for s in shots:
        for which, rid in (("start", s["start_image"]), ("end", s["end_image"])):
            users.setdefault(rid, []).append(f"{which} of {s['id']}")
            rec = images[rid]
            if rec.get("prompt_kind") != "scene" or rid in seen:
                continue
            scene = f"s{s['scene']:02d}"
            seen[rid] = (scene, sum(1 for v in seen.values() if v[0] == scene) + 1)
    for spec in S.NEW_IMAGES:
        rec = images[spec["id"]]
        if spec["id"] not in seen:
            raise SystemExit(f"new image {spec['id']} is used by no piece")
        scene, k = seen[spec["id"]]
        name = spec["id"].split("_", 1)[1]
        rec["group"] = f"scene-{int(scene[1:]):02d}"
        rec["target"] = f"{KEYFRAMES}/{scene}_{k:02d}_{name}_r01.png"
        rec["acceptance"] = [
            "Identity: every checklist item of each visible character against its canonical (CR-13, CR-17).",
            "Size: the setup's measured sizes and the size anchor; same depth, same size (CR-16).",
            "Plate: landmarks, light and crop as in the locked plate (CR-06).",
            "Boundary image (CR-21): it must work as " + " and as ".join(sorted(set(users[spec["id"]])))
            + "; one simple action reaches it from the neighbouring images."]
        if spec.get("mouth"):
            rec["acceptance"].append("Open mouth (CR-19): only the mouth differs from the first reference; the "
                                     "opening matches the approved *_OPEN study.")
    # references point at current targets (new images got theirs above; carried ones may be resolved)
    for rec in images.values():
        for r in rec.get("ordered_references", []):
            if r.get("id") in images and images[r["id"]].get("target"):
                r["path"] = images[r["id"]]["target"]
    manifest = {"revision": S.REVISION, "status": "planned_awaiting_owner_review", "title": S.TITLE,
                "base_story": S.BASE, "audio_story": S.AUDIO_STORY,
                "schema_note": "Chained coverage (CR-21): one shot per piece, in film order, each with one variant.",
                "images": [images[i] for i in order], "shots": shots}
    D.mkdir(parents=True, exist_ok=True)
    (REPO / KEYFRAMES).mkdir(parents=True, exist_ok=True)
    (REPO / KEYFRAMES / ".gitkeep").touch()
    (D / "visual_bible.json").write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n")
    (D / "prompt_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    cov = copy.deepcopy(bc)
    cov.update(revision=S.REVISION, note=f"Line list of {S.BASE} (narration rendered there); "
               "candidate_coverage_shots = the v6 pieces that cover each line.")
    for ln in cov["lines"]:
        ln["candidate_coverage_shots"] = [s["id"] for s in shots if ln["id"] in s["lines"]]
    (D / "dialogue_coverage.json").write_text(json.dumps(cov, indent=2, ensure_ascii=False) + "\n")
    write_docs(manifest, b, images, users)
    n_reuse = sum(1 for s in shots if s.get("reuse"))
    print(f"{len(shots)} pieces ({n_reuse} reuse {S.BASE} renders), {len(S.NEW_IMAGES)} new images, "
          f"{len(manifest['images'])} image records")


def write_docs(m, b, images, users):
    shots = m["shots"]
    new = [images[s["id"]] for s in S.NEW_IMAGES]
    holds = sum(1 for s in shots if s["start_image"] == s["end_image"])
    out = [f"# {S.TITLE}: chained shot plan", "",
           f"Generated by `production/chain_packet.py` from `chain_source.py`; do not edit by hand. {len(shots)} pieces "
           f"in film order (CR-21): each is one clip of 49 to 81 frames whose length comes from the narration lines it "
           f"covers (`production/chain_plan.py`, see `TIMING_SHEET.md` for times, frames and speeds). `chain` = starts "
           f"on the previous piece's end image; `cut (reason)` = a planned cut. {sum(1 for s in shots if s.get('reuse'))} "
           f"pieces reuse a {S.BASE} render; {holds} are holds or landscapes (start = end).", "",
           "| # | Piece | Setup | Join | Start → end | Lines | Action |", "|---|---|---|---|---|---|---|"]
    for s in shots:
        join = "chain" if s["join_in"] == "chain" else f"cut ({s['cut_reason']}" + (
            f", {s['transition']})" if s.get("transition") else ")")
        mark = lambda rid: f"**`{rid}`**" if rid in {r['id'] for r in new} else f"`{rid}`"
        act = s["variants"][0]["action_text"]
        if s.get("reuse"):
            act = f"(reuses `{s['reuse']['variant']}`) {act}"
        out.append(f"| {s['order']} | `{s['id']}` | `{s['setup']}` | {join} | {mark(s['start_image'])} → "
                   f"{mark(s['end_image'])} | {', '.join(x.split('-')[1] for x in s['lines'])} | {act} |")
    out += ["", "Bold = a new image (list below).", "", "## New images", "",
            f"{len(new)} images, all `planned`. Each prompt and its ordered references: `prompts/scene-NN.md` or "
            f"`python3 production/image_prompts.py --story {S.SLUG} show <id>`.", "",
            "| Image | File | Setup | Shows | Joins |", "|---|---|---|---|---|"]
    for r in new:
        out.append(f"| `{r['id']}` | `{Path(r['target']).name}` | `{r['setup']}` | {r['frame']} | "
                   f"{'; '.join(sorted(set(users[r['id']])))} |")
    (D / "SHOT_PLAN.md").write_text("\n".join(out) + "\n")
    readme = S.README.format(pieces=len(shots), new=len(new), reuse=sum(1 for s in shots if s.get("reuse")),
                             holds=holds, renders=len(shots) - sum(1 for s in shots if s.get("reuse")))
    (D / "README.md").write_text(readme)


if __name__ == "__main__":
    main()
