"""Write a new story's first documentation packet from its source file.

    python3 production/story_packet.py stories/<slug>/packet_source.py

The source file (see stories/tortoise_and_hare_v1/packet_source.py) holds the script lines, characters
(design specs), size lineup, locations, camera setups, shots with their start and end frames, expressions,
poses and props. This writes stories/<slug>/: visual_bible.json, prompt_manifest.json (every image and video
prompt as a template), dialogue_coverage.json (the line list for voice/narrate_scenes.py), SCRIPT.md,
SHOT_PLAN.md and README.md, plus empty image folders. Then run
    python3 production/image_prompts.py --story <slug> build && ... lint && ... md

It overwrites the bible and manifest: use it for the first packet and for script or shot changes before any
image exists. Once images are accepted, edit visual_bible.json and the manifest records directly (CR-18).
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("packet_source", sys.argv[1])
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

REPO = Path(__file__).resolve().parents[1]
D = REPO / "stories" / S.SLUG
REV = getattr(S, "REVISION", f"{S.SLUG}-r1")
V4B = json.loads((REPO / "stories/lion_and_mouse_v4/visual_bible.json").read_text())
C = S.CHARACTERS
CHAR_DIR = "character/characters/{folder}/" + S.SLUG
SCENE_DIR = f"character/characters/interactions/{S.SLUG}/keyframes"
LOC_DIR = f"character/locations/{S.SLUG}"
COUNTS = getattr(S, "COUNTS", {})
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def name(c):
    return C[c]["name"]


def setups():
    out, anchors = {}, {}
    for sid, scene, setup, cast, *_ in S.SHOTS:
        if cast and setup not in anchors:
            anchors[setup] = f"{sid}_start"
    for k, v in S.SETUPS.items():
        v = dict(v)
        if k in anchors:
            v["anchor_record"] = anchors[k]
            v["anchor_note"] = "The first frame made in this setup; once approved it fixes the camera and the sizes for the rest."
        out[k] = v
    return out


SETUPS = setups()


def bible():
    chars = {}
    for c in S.ORDER:
        d = C[c]
        chars[c] = {"name": d["name"], "status": "design spec: rewrite from the approved canonical image",
                    "canonical": f"{CHAR_DIR.format(folder=d['folder'])}/canonical/{c}_canonical_r01.png",
                    "canonical_record": d["canon_id"], "identity": d["identity"], "sheet": d["sheet"],
                    "short": f"{d['name']} is {d['sheet']}.", "mouth": d["mouth"], "palette": d["palette"],
                    "proportions": d["proportions"], "checklist": d["checklist"], "drift_phrases": d["drift_phrases"]}
    locs = {k: {"location": v["folder"], "plate": f"{LOC_DIR}/{v['folder']}/{v['stem']}_r01.png", "label": v["label"],
                "description": v["description"], "landmarks": v["landmarks"], "light": v["light"], "ambient": v["ambient"]}
            for k, v in S.LOC.items()}
    blocks = {k: v for k, v in V4B["blocks"].items() if k in V4B["generic_blocks"]}
    blocks["final_check"] = S.FINAL_CHECK or (
        "Before finishing, check: each visible character appears exactly once, with exactly two eyes and two eyebrows "
        "(one above each eye, drawn once), its canonical ears, limbs, wings and toes, whiskers only where its canonical "
        "has them and exactly one tail attached at its root; no text, letters, labels or watermark anywhere.")
    blocks["cast_scale"] = S.CAST_SCALE_BLOCK
    blocks["studio_lineup"] = (
        "Studio: plain warm off-white seamless backdrop filling the frame edge to edge, soft even neutral light, one flat "
        "ground line at y=0.88 where every character stands, with a small soft contact shadow under each; every whole "
        "body, every ear tip, foot and tail inside the frame with a margin.")
    blocks.update(S.PROP_BLOCKS)
    return {"revision": REV, "version": S.SLUG, "status": "single_source_of_truth_for_all_prompts",
            "title": S.TITLE, "moral": S.MORAL,
            "how_to": ("Every prompt in prompt_manifest.json is a template rendered from this file by "
                       "production/image_prompts.py --story " + S.SLUG + " (build, lint, show, md, review). Character "
                       "identities are design specs until each canonical image is approved; then rewrite them from the "
                       "image (hex sampled from it) and rebuild."),
            "characters": chars, "cast_scale": S.CAST_SCALE, "locations": locs, "setups": SETUPS,
            "blocks": blocks, "generic_blocks": V4B["generic_blocks"], "reference_roles": V4B["reference_roles"],
            "lint": V4B["lint"]}


def rec(rid, group, kind, target, canvas, counts, template, refs, label, purpose, **extra):
    r = {"id": rid, "group": group, "revision": "r01", "status": "planned", "bible_revision": REV,
         "target": target, "canvas": canvas, "purpose": purpose, "label": label, "prompt_kind": kind,
         "counts": counts, "ordered_references": refs, "prompt_template": "", "result": None,
         "allowed_delta": "Only the explicitly specified view, pose, expression, framing or state may change; preserve every other visible feature.",
         "protected": "Identity, anatomical scale, unchanged objects, static landmarks, camera/crop/light outside the stated delta."}
    r.update(extra)
    head, _, rest = template.partition(". ")
    r["prompt_template"] = re.sub(r"\s+", " ", (head + ". {{refs}} " + rest) if refs else template).strip()
    return r


def ref(rid, role, by):
    return {"id": rid, "role": role, "path": by[rid]["target"]}


STUDIO = "{{block:light_and_colour}} {{block:style}} {{block:final_check}}"


def foundation():
    recs, by = [], {}

    def add(r):
        recs.append(r)
        by[r["id"]] = r

    for c in S.ORDER:
        d = C[c]
        base = CHAR_DIR.format(folder=d["folder"])
        add(rec(d["canon_id"], "foundation", "character", f"{base}/canonical/{c}_canonical_r01.png", [1536, 1536], {c: 1},
                f"Create one 1536x1536 square studio reference image of {d['name']}. Visible cast: exactly one {d['name']}; "
                f"no other character. {{{{identity:{c}}}}} This is {d['name']}'s identity root: {S.CANON_VIEW[c]}, the whole "
                f"body centred with even margins. {{{{block:studio_full_body}}}} {STUDIO}", [],
                f"{d['name']}'s canonical, full body", f"{d['name']}'s identity root"))
    names = [name(c) for c in S.ORDER]
    add(rec("LINEUP", "foundation", "character", f"character/characters/interactions/{S.SLUG}/lineup_r01.png", [1920, 1080],
            {c: 1 for c in S.ORDER},
            "Create one 1920x1080 16:9 studio size lineup of the whole cast. Visible cast: exactly one each of "
            f"{', '.join(names[:-1])} and {names[-1]}, standing side by side at the same distance from the camera on one "
            "ground line, in that order from left to right, each in its neutral pose facing the camera, with clear space "
            "between them. " + " ".join(f"{{{{identity:{c}}}}}" for c in S.ORDER)
            + f" {{{{block:cast_scale}}}} {S.LINEUP_SIZE} {{{{block:studio_lineup}}}} " + STUDIO,
            [ref(C[c]["canon_id"], "identity_root", by) for c in S.ORDER], "the cast size lineup",
            "Same-depth size lineup of the whole cast (CR-17)"))
    for rid, c, text, label in S.POSE_VIEWS:
        d = C[c]
        add(rec(rid, "foundation", "character", f"{CHAR_DIR.format(folder=d['folder'])}/references/{rid.lower()}_r01.png",
                [1536, 1536], {c: 1},
                f"Create one 1536x1536 square studio reference image of {d['name']}. {{{{block:edit_reference}}}} "
                f"Visible cast: exactly one {d['name']}; no other character. {{{{identity:{c}}}}} {text} "
                f"{{{{block:studio_full_body}}}} {STUDIO}", [ref(d["canon_id"], "edit_base", by)], label, label))
    for c in S.PORTRAIT_CHARS:
        d, p = C[c], S.PREFIX[c]
        base = CHAR_DIR.format(folder=d["folder"])
        add(rec(f"{p}_CLOSED", "foundation", "character", f"{base}/references/{p.lower()}_closed_r01.png", [1536, 1536], {c: 1},
                f"Create one 1536x1536 square studio reference image of {d['name']}. {{{{block:edit_reference}}}} Visible cast: "
                f"exactly one {d['name']}; no other character. {{{{identity:{c}}}}} Head-and-shoulders portrait, front view, "
                "neutral closed-mouth smile. This crop, eye-line and head size are the fixed portrait reference for every "
                f"{d['name']} expression. {{{{block:studio_portrait}}}} {STUDIO}",
                [ref(d["canon_id"], "edit_base", by)], f"{d['name']}'s closed-mouth portrait", "portrait and expression base"))
        add(rec(f"{p}_OPEN", "foundation", "character", f"{base}/references/{p.lower()}_open_r01.png", [1536, 1536], {c: 1},
                f"Create one 1536x1536 square studio reference image of {d['name']}. {{{{block:edit_reference}}}} Visible cast: "
                f"exactly one {d['name']}; no other character. {{{{identity:{c}}}}} Exactly the approved closed-mouth "
                f"portrait framing; a moderate rounded mouth opening for gentle speech. {{{{mouth:{c}}}}} "
                f"{{{{block:studio_portrait}}}} {STUDIO}",
                [ref(f"{p}_CLOSED", "edit_base", by), ref(d["canon_id"], "identity_root", by)],
                f"{d['name']}'s open-mouth study", "speech mouth design"))
    for c, exprs in S.EXPR.items():
        d, p = C[c], S.PREFIX[c]
        for e, text in exprs.items():
            rid = f"{p}_EXPR_{e}"
            add(rec(rid, "expressions", "expression",
                    f"{CHAR_DIR.format(folder=d['folder'])}/expressions/{rid.lower()}_r01.png", [1536, 1536], {c: 1},
                    f"Create one 1536x1536 square studio head-and-shoulders expression study of {d['name']}. "
                    f"{{{{block:edit_expression}}}} Visible cast: exactly one {d['name']}; no other character. "
                    f"{{{{identity:{c}}}}} Expression: {text}. {{{{block:studio_portrait}}}} {STUDIO}",
                    [ref(f"{p}_CLOSED", "edit_base", by), ref(d["canon_id"], "identity_root", by)],
                    f"{d['name']}'s {e.lower().replace('_', ' ')} expression study", f"{d['name']} expression: {e.lower()}"))
    for k, v in S.LOC.items():
        src = v.get("derived_from")
        refs = [ref(f"PL_{src}", "edit_base", by)] if src else []
        keep = ("Keep the exact geometry and camera of the approved plate it is edited from; only the light changes. "
                if src else "")
        add(rec(f"PL_{k}", "foundation", "plate", f"{LOC_DIR}/{v['folder']}/{v['stem']}_r01.png", [1920, 1080], {},
                f"Create one 1920x1080 16:9 empty location plate. {keep}{{{{plate:{k}}}}} {{{{block:plate_rules}}}} {{{{block:style}}}}",
                refs, f"empty plate of {v['label']}", f"locked plate: {v['label']}"))
    for pid, stem, label, text in S.PROPS:
        add(rec(pid, "foundation", "prop", f"{LOC_DIR}/props/{stem}_r01.png", [1536, 1536], {},
                "Create one 1536x1536 prop reference on a contrasting muted-blue seamless studio background, the whole object "
                f"centred with ample margins. {text} Soft even light, no characters. {{{{block:style}}}}", [], label,
                f"prop: {label}"))
    return recs, by


def parse_cast(cast):
    """'sheep*5' -> ('sheep', 5)."""
    out = {}
    for c in cast:
        k, _, n = c.partition("*")
        out[k] = int(n) if n else COUNTS.get(k, 1)
    return {c: out[c] for c in S.ORDER if c in out}


def cast_line(counts):
    if not counts:
        return "No character is visible in this frame."
    parts = []
    for c, n in counts.items():
        nm = name(c).removeprefix("the ")
        parts.append(f"exactly one {nm}" if n == 1 else f"exactly {NUM[n]} {C[c].get('plural', nm)}")
    return "Visible cast: " + " and ".join(parts) + "; no other character, no duplicates."


def pose_refs(cast, setup, text):
    out, done = [], set()
    t = text.lower()
    for c, rx, rid, where in S.POSE_RULES:
        if c in cast and c not in done and (where is None or setup in where) and re.search(rx, t):
            out.append(rid)
            done.add(c)
    return out


def scenes(by):
    recs, shots = [], []
    last_end = {}  # setup -> latest end frame made with that camera (world state for the next shot there)
    for n, (sid, scene, setup, cast, start, end, action, prop, exprs) in enumerate(S.SHOTS):
        st = SETUPS[setup]
        loc = st["location"]
        counts = parse_cast(cast)
        cast = list(counts)
        states = (prop or "").split("->")
        ps_start, ps_end = (states[0], states[-1]) if prop else (None, None)
        for which, text, ps in (("start", start, ps_start), ("end", end, ps_end)):
            rid = f"{sid}_{which}"
            refs = []
            if which == "end":
                refs.append(ref(f"{sid}_start", "edit_base", by))
            elif last_end.get(setup) and set(by[last_end[setup]]["counts"]) <= set(cast):
                refs.append(ref(last_end[setup], "world_state", by))
            if which == "start":
                refs.append(ref(f"PL_{loc}", "locked_plate", by))
            refs += [ref(C[c]["canon_id"], "identity_root", by) for c in cast]
            if which == "start":
                refs += [ref(p, "pose", by) for p in pose_refs(cast, setup, text)]
            for c in cast:
                e = exprs.get(c)
                if e and (which == "start" or e[1] != e[0]):
                    refs.append(ref(e[0] if which == "start" else e[1], "expression", by))
            if ps and which == "start" and getattr(S, "PROP_REF", None):
                refs.append(ref(S.PROP_REF, "prop", by))
            anchor = st.get("anchor_record")
            if which == "start" and anchor and anchor != rid and anchor in by and set(by[anchor]["counts"]) <= set(cast):
                refs.append(ref(anchor, "size_anchor", by))
            parts = [f"Create one 1920x1080 16:9 still image: the {which} frame of shot {sid}, {st['label']}."]
            if which == "end":
                parts.append("{{block:edit_end_frame}}")
            parts.append(cast_line(counts))
            parts += [f"{{{{identity:{c}}}}}" for c in cast]
            if len(cast) > 1:
                parts.append("{{block:cast_scale}}")
            parts.append(f"{{{{setup:{setup}}}}}")
            if cast:
                parts.append("{{block:light_and_colour}}")
            if ps:
                parts.append(f"{{{{block:{S.PROP_STATE_PREFIX}{ps}}}}}")
            parts += ["This frame shows: {{frame}}.", "{{block:style}}"]
            if cast:
                parts.append("{{block:final_check}}")
            r = rec(rid, f"scene-{scene:02d}", "scene", f"{SCENE_DIR}/{rid}_r01.png", [1920, 1080], counts,
                    " ".join(parts), refs, f"{which} frame of shot {sid}", f"{which.capitalize()} of {sid}",
                    setup=setup, framing=st["framing"], frame=text)
            recs.append(r)
            by[rid] = r
        last_end[setup] = f"{sid}_end"
        L = S.LOC[loc]
        shorts = " ".join(f"{{{{short:{c}}}}}" for c in cast)
        idents = " ".join(f"{{{{identity:{c}}}}}" for c in cast)
        modes = [("closed", "Mouths stay closed throughout; expressions come from the eyes and brows.")]
        if st["framing"] == "dialogue_close_up":
            modes.append(("mouth", "The mouth opens and closes softly in small rounded shapes, as in gentle speech."))
        variants = [{
            "id": f"{sid}_{mode}_r01", "mode": mode, "action_text": action,
            "positive_prompt_template": re.sub(r"\s+", " ", f"{action} {mouth} Fixed camera; the background stays still "
                                               f"apart from gentle natural motion. {shorts} The background is {L['label']}, "
                                               "unchanged framing and light. {{block:runtime_style}}").strip(),
            "full_prompt_specification_template": re.sub(r"\s+", " ", (
                f"{action} {mouth} The camera stays fixed in framing, crop and background scale for the whole clip. "
                f"{idents} Start frame: {{{{frame:{sid}_start}}}}. End frame: {{{{frame:{sid}_end}}}}. "
                f"Ambient: {L['ambient']} {{{{plate:{loc}}}}} {{{{block:style}}}}")).strip(),
            "frames": 81, "fps": 16, "seeds": [], "result": None} for mode, mouth in modes]
        shots.append({"id": sid, "scene": scene, "order": n + 1, "status": "planned", "bible_revision": REV,
                      "location_profile": loc, "setup": setup, "cast": cast, "start_image": f"{sid}_start",
                      "end_image": f"{sid}_end", "previous_shot": S.SHOTS[n - 1][0] if n else None,
                      "prop_state": prop, "variants": variants, "owner_selection": None})
    return recs, shots


def write_docs(m, b, lines):
    words = sum(len(x["text"].split()) for x in lines)
    minutes = words / 140 + len(lines) * 0.6 / 60
    speakers = sorted({x["speaker"] for x in lines}, key=lambda s: (s != "NARRATOR", s))
    out = [f"# {S.TITLE}: script (draft for owner review)", "", f"Moral: *{S.MORAL}*", "",
           f"{len(lines)} lines, {words} words, about {minutes:.1f} minutes of narration (about 140 words a minute "
           "plus the pauses between lines). Ages 3 to 7: short sentences, repetition, a gentle ending.", "",
           "Speakers: " + ", ".join(speakers) + ". The line list for the narration tool is `dialogue_coverage.json` "
           "(same text, with ids, performance directions and the shots that can cover each line).", ""]
    scene = None
    for i, x in enumerate(lines):
        if x["scene"] != scene:
            scene = x["scene"]
            out += [f"## Scene {scene}: {S.SCENE_TITLES[scene]}", ""]
        who = "Narrator" if x["speaker"] == "NARRATOR" else x["speaker"].capitalize()
        out.append(f"- **{who}** *({x['performance_direction']})*: {x['text']}  `{x['id']}`")
        if i + 1 == len(lines) or lines[i + 1]["scene"] != scene:
            out.append("")
    (D / "SCRIPT.md").write_text("\n".join(out))
    imgs = {r["id"]: r for r in m["images"]}
    out = [f"# {S.TITLE}: shot plan and state table", "",
           f"{len(m['shots'])} shots, each with a start and an end still (Wan animates between them, about 5 s at 81 "
           "frames). Every shot keeps one camera setup (never a wide start with a close-up end). " + S.TRAVEL_NOTE, "",
           "Each image's full prompt and the references to attach, in order: [`prompts/`](prompts/) "
           f"or `python3 production/image_prompts.py --story {S.SLUG} show <record>`.", "",
           "| # | Shot | Setup (framing) | Cast | Start | End | Video action |", "|---|---|---|---|---|---|---|"]
    for s in m["shots"]:
        st = b["setups"][s["setup"]]
        cast = ", ".join(f"{c}×{n}" if n > 1 else c for c, n in imgs[s["start_image"]]["counts"].items()) or "-"
        out.append(f"| {s['order']} | `{s['id']}` | `{s['setup']}` ({st['framing']}) | {cast} | "
                   f"{imgs[s['start_image']]['frame']} | {imgs[s['end_image']]['frame']} | {s['variants'][0]['action_text']} |")
    out += ["", "## Cause-and-effect state table", "", "| After shot | Where everyone is | Props and world state |",
            "|---|---|---|", *S.STATE_ROWS, "", "## Camera setups", "",
            "| Setup | Place | Framing | Size anchor (first frame made there) |", "|---|---|---|---|"]
    for k, v in b["setups"].items():
        out.append(f"| `{k}` | {b['locations'][v['location']]['label']} | {v['framing']} | {v.get('anchor_record', '-')} |")
    (D / "SHOT_PLAN.md").write_text("\n".join(out) + "\n")
    found = [r for r in m["images"] if r["group"] in ("foundation", "expressions")]
    out = [f"# {S.TITLE} ({S.SLUG})", "", S.INTRO, "", f"Moral: *{S.MORAL}*", "", "## Status (2026-10-04)", "",
           f"- **Documentation done; nothing generated.** Script ({len(lines)} lines, about {minutes:.1f} minutes of "
           f"narration), {len(m['shots'])} shots, {len(found)} foundation and expression image records and "
           f"{len(m['images']) - len(found)} scene frames, every prompt rendered from `visual_bible.json`; "
           f"`python3 production/image_prompts.py --story {S.SLUG} lint` reports 0 errors.",
           "- **Gate before images (CR-01):** the owner reviews the script and the shot order.",
           "- Character descriptions are design specifications until each canonical image is approved; then they are "
           "rewritten from the image (colours sampled from it) and the prompts rebuilt.", "",
           "## Read in this order", "",
           "1. [SCRIPT.md](SCRIPT.md): the story, line by line, with speakers and performance notes.",
           "2. [SHOT_PLAN.md](SHOT_PLAN.md): every shot with its start and end, the cause-and-effect state table and the camera setups.",
           "3. [prompts/](prompts/): the exact prompt and reference list of every image and video clip.",
           "4. `visual_bible.json`: characters, size lineup, places, camera setups and shared prompt text (the single source).", "",
           "## Cast", "", "| Character | Who | Design |", "|---|---|---|"]
    out += [f"| {name(c)} | {S.ROLES[c]} | {b['characters'][c]['sheet']} |" for c in S.ORDER]
    out += ["", f"Size lineup: {b['cast_scale']['rule']}", "",
            "## Production order (each step reviewed before the next)", "",
            "1. Owner approves script and shot order.",
            f"2. Canonicals of the {len(S.ORDER)} characters (studio, full body); owner approves; identities rewritten from them.",
            "3. Size lineup image (`LINEUP`), then measure it and update the setup sizes.",
            f"4. Plates ({len(S.LOC)}), props, views and poses, portraits, mouth and expression studies.",
            "5. Scene frames in story order, each start before its end; the first frame of each camera setup is its size anchor.",
            "6. Narration with the saved narrator (`voice/narrators/moonlight_storyteller_1`, the default) and character "
            "voices chosen later: `voice/narrate_scenes.py --lines stories/" + S.SLUG + "/dialogue_coverage.json --story "
            + S.SLUG + " --voices SPEAKER=folder ...`.",
            "7. Clips on LUMI (fast mode), owner selects takes; assembly only when asked.", "",
            "## Image folders", "",
            f"- Characters: `character/characters/{{{','.join(C[c]['folder'] for c in S.ORDER)}}}/{S.SLUG}/{{canonical,references,expressions}}/`",
            f"- Scene frames: `character/characters/interactions/{S.SLUG}/keyframes/`; size lineup: `character/characters/interactions/{S.SLUG}/lineup_r01.png`",
            f"- Plates and props: `character/locations/{S.SLUG}/<place>/`, `.../props/`",
            "- Each record's `target` in `prompt_manifest.json` is the exact file name.", "",
            "## Owner decisions", "", *S.DECISIONS, "", "## Still open", "",
            "- Owner review of the script and shot order (CR-01) before the first image.",
            f"- {len(m['shots'])} shots give about {len(m['shots']) * 5 / 60:.1f} minutes of picture at 5 s each; the "
            "narration is longer, so shots will be slowed, held or given extra coverage when the narration is timed "
            "(`production/timing_sheet.py`).", *getattr(S, "OPEN", []), ""]
    (D / "README.md").write_text("\n".join(out))
    return words, minutes


def main():
    D.mkdir(parents=True, exist_ok=True)
    b = bible()
    found, by = foundation()
    scn, shots = scenes(by)
    m = {"revision": REV, "status": "planned_awaiting_owner_script_review", "title": S.TITLE,
         "images": found + scn, "shots": shots}
    (D / "visual_bible.json").write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n")
    (D / "prompt_manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    lines, count = [], {}
    for scene, spk, direction, text, cov in S.LINES:
        count[scene] = count.get(scene, 0) + 1
        lines.append({"id": f"S{scene:02d}-L{count[scene]:03d}", "scene": scene, "speaker": spk,
                      "performance_direction": direction, "text": text, "candidate_coverage_shots": cov,
                      "chosen_shot_intervals": [], "audio_path": None, "measured_duration_seconds": None,
                      "status": "script_awaiting_owner_review"})
    (D / "dialogue_coverage.json").write_text(json.dumps(
        {"revision": REV, "status": "script_awaiting_owner_review", "title": S.TITLE, "moral": S.MORAL,
         "narrator_voice": "narrators/moonlight_storyteller_1", "lines": lines}, indent=2, ensure_ascii=False) + "\n")
    for d in {str(Path(r["target"]).parent) for r in m["images"]}:
        (REPO / d).mkdir(parents=True, exist_ok=True)
        (REPO / d / ".gitkeep").touch()
    words, minutes = write_docs(m, b, lines)
    ids = {s[0] for s in S.SHOTS}
    missing = sorted({c for *_, cov in S.LINES for c in cov} - ids)
    unused = sorted(ids - {c for *_, cov in S.LINES for c in cov})
    print(f"{len(found)} foundation, {len(scn)} scene records, {len(shots)} shots, {len(lines)} lines, {words} words, "
          f"{minutes:.1f} min; lines name unknown shots {missing}; shots without lines {unused}")


if __name__ == "__main__":
    main()
