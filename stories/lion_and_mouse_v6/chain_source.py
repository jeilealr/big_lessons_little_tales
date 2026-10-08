"""The Lion and the Mouse v6: chained coverage of the v5 narration (CR-21).

    python3 production/chain_packet.py stories/lion_and_mouse_v6/chain_source.py
    python3 production/image_prompts.py --story lion_and_mouse_v6 build
    python3 production/image_prompts.py --story lion_and_mouse_v6 lint
    python3 production/image_prompts.py --story lion_and_mouse_v6 md
    python3 production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v5 apply

The film is the v5 English narration (11:23.7, 161 lines), cut into pieces of 2.45 to 6.33 s.
Each piece lists the lines it covers; chain_plan.py gives it its seconds and frame count.
Pieces reuse v5 images and, where the endpoints and prompt match, v5 renders. NEW_IMAGES are the
frames the chain still needs. Owner request 2026-10-08; see docs/changelog.md.
"""
SLUG = "lion_and_mouse_v6"
BASE = "lion_and_mouse_v5"
AUDIO_STORY = "lion_and_mouse_v5"
TITLE = "The Lion and the Mouse (v6, chained)"
REVISION = "v6-chain-2026-10-08"

BLOCKS = {
    "edit_chain_frame": (
        "This is an edit of the first attached reference, an accepted frame of the same camera setup: keep its "
        "camera, crop, background, light and every character's identity, colours, brightness and size exactly; "
        "change only what this frame shows below. It is the hand-off between two clips, so the pose must be one "
        "a single small action reaches from the neighbouring frames."),
    "edit_open_mouth": (
        "This is an edit of the accepted closed-mouth frame (the first attached reference): keep its camera, crop, "
        "background, light and the character's identity, colours, brightness, size, pose, head position, gaze and "
        "expression exactly; open only the mouth into the approved rounded speech shape shown in the attached "
        "mouth-design reference, with the same interior and any teeth as in that reference. This is the single "
        "open-mouth key frame the talking clips animate to and from, so the open shape stays identical to the "
        "character's approved speech mouth."),
}
REFERENCE_ROLES = {
    "empty_copy": ("the frame to reproduce without its characters ({what}): copy its camera, background, light, "
                   "every prop and the exact position of each prop, and leave out every character, so this frame "
                   "shows the place empty"),
}
REVIEW_NEGATIVE = ("Review only (fast mode has no negative pass): duplicate characters, extra or missing limbs, "
                   "extra tails, changed face or colours, a character growing or shrinking, a cut, zoom or camera "
                   "move inside the clip, objects that are in neither the start nor the end frame.")


def L(scene, *nums):
    return [f"S{scene:02d}-L{n:03d}" for n in nums]


# ---------------------------------------------------------------- new images
def open_frame(iid, setup, closed, char, why, extra=""):
    canon, study, name = {"milo": ("MILO_CANON", "M_OPEN", "Milo"), "leo": ("LEO_CANON", "L_OPEN", "Leo")}[char]
    return dict(id=iid, setup=setup, world_from=closed, mouth=char, why=why,
                what=f"the open-mouth key frame after {closed}",
                refs=[(closed, "edit_base"), (canon, "identity_root"), (study, "mouth_design")],
                frame=(f"Exactly the frame {closed} in every detail, with the same expression, pose, head size and "
                       f"position, gaze, backdrop and light, except {name} opens the mouth into the approved rounded "
                       f"speech shape shown in the mouth-design reference{extra}"))


def edit_frame(iid, setup, base, plate, chars, frame, why, world_from=None, state=None, more=()):
    canon = {"milo": "MILO_CANON", "leo": "LEO_CANON"}
    refs = [(base, "edit_base")] + ([(plate, "locked_plate")] if plate != base else []) \
        + [(canon[c], "identity_root") for c in chars] + list(more)
    return dict(id=iid, setup=setup, world_from=world_from or base, what=f"the chain key frame {iid}",
                refs=refs, frame=frame, why=why, state=state, chars=chars)


ACORN_ON_STONE = "The story acorn rests on the flat feeding stone, not yet held."
NEW_IMAGES = [
    edit_frame("s01_milo_at_edge", "stream_afternoon_wide", "PL_stream_afternoon", "PL_stream_afternoon", ["milo"],
               "One Milo at x=0.08,y=0.84, just inside the left edge of the frame, upright right-facing walking stance "
               "at the same size as in the size anchor; paws empty; mouth closed", "Milo walks into the opening landscape",
               world_from="s01_explores_start", state=ACORN_ON_STONE,
               more=[("M_SIDE_R", "pose"), ("s01_explores_start", "size_anchor")]),
    edit_frame("s01_milo_at_stone", "stream_afternoon_wide", "s01_explores_end", "PL_stream_afternoon", ["milo"],
               "Milo stands at about x=0.56 with his feet near y=0.80 just in front of the flat feeding stone, facing it, "
               "reaching up with both empty paws toward the story acorn on top of the stone; mouth closed",
               "Milo finds the acorn (S01-L003)", state=ACORN_ON_STONE),
    edit_frame("s03_milo_at_fork_edge", "fork_wide", "PL_fork_sunset", "PL_fork_sunset", ["milo"],
               "One Milo at x=0.10,y=0.86, just inside the left edge of the frame, upright right-facing walking stance at "
               "the same size as in the size anchor; paws empty; mouth closed", "Milo walks into the fork view",
               world_from="s03_two_paths_start", more=[("M_SIDE_R", "pose"), ("s03_two_paths_start", "size_anchor")]),
    edit_frame("s03_milo_looks_up", "fork_wide", "s03_two_paths_end", "PL_fork_sunset", ["milo"],
               "Same position, body, paws and tail as before; Milo's head tilts up and his eyes look at the darkening "
               "sky above the trees; mouth closed", "Milo looks at the darkening sky (S03-L006)"),
    open_frame("s03_decides_open", "fork_milo_closeup", "s03_decides_start", "milo", "Milo says 'The shortcut' (S03-L009)"),
    dict(id="s05_leo_asleep_cu", setup="tree_dusk_leo_closeup", what="a close-up of the sleeping Leo",
         why="'His mane rested against the grass. His eyes were closed.' (S05-L002/3)",
         refs=[("PL_tree_dusk", "locked_plate"), ("LEO_CANON", "identity_root"), ("L_ASLEEP", "expression"),
               ("s07_leo_annoyed_start", "framing")], counts={"leo": 1},
         frame="Leo asleep in the close-up framing: eyes closed, brows relaxed, mouth closed, head tilted slightly "
               "down, the whole mane inside the frame; a peaceful face"),
    edit_frame("s05_milo_lands_wide", "tree_dusk_wide", "s05_paw_contact_end", "PL_tree_dusk", ["leo", "milo"],
               "Leo still asleep exactly as before, eyes closed; Milo has tumbled forward and now sits on the ground "
               "right against the tip of Leo's nose, legs splayed, dazed, mouth closed",
               "the tumble ends in the wide shot (replaces the v5 wide-to-two-shot bridge, which was a zoom)"),
    edit_frame("s06_leo_head_up", "tree_dusk_contact", "s05_nose_aftermath_end", "PL_tree_dusk", ["leo", "milo"],
               "Leo has lifted his head from his paws, eyes open in surprise; Milo has slid down from his nose and "
               "stands on the path just in front of him, looking up, startled, mouth closed",
               "'The lion lifted his head in surprise. The mouse scrambled down onto the path.' (S06-L001)"),
    open_frame("s07_leo_annoyed_open", "tree_dusk_leo_closeup", "s07_leo_annoyed_end", "leo", "Leo speaks, annoyed (S07-L001/2)"),
    open_frame("s07_milo_sorry_open", "tree_dusk_milo_closeup", "s07_milo_sorry_start", "milo", "Milo: 'I'm sorry!' (S07-L003)"),
    open_frame("s07_milo_apology_open", "tree_dusk_milo_closeup", "s07_milo_sorry_end", "milo", "Milo apologises (S07-L005)"),
    open_frame("s08_leo_softens_open", "tree_dusk_leo_closeup", "s08_leo_softens_end", "leo", "Leo speaks kindly (S08)"),
    open_frame("s08_milo_surprised_open", "tree_dusk_milo_closeup", "s08_milo_surprised_start", "milo",
               "'You're... letting me go?' (S08-L012)"),
    open_frame("s08_milo_grateful_open", "tree_dusk_milo_closeup", "s08_milo_surprised_end", "milo", "Milo thanks Leo (S08-L019/21)"),
    edit_frame("s09_leo_rests", "tree_day_wide", "PL_tree_day", "PL_tree_day", ["leo"],
               "Leo lies relaxed alone beneath the great tree in daylight, in the same place, pose and size as in the "
               "friends frames, head up, eyes soft, mouth closed", "'the lion returned to his favorite shady tree' (S09-L006)",
               world_from="s16_friends_start"),
    dict(id="s10_trap_set", setup="trap_wide", what="the empty trap path with the net set", world_from="s10_curious_step_start",
         why="landscape of the trap before Leo comes (S10-L001); also the 'hunter's net' memory (S16-L008)",
         refs=[("s10_curious_step_start", "empty_copy"), ("PL_trap_morning", "locked_plate"), ("PROP_NET", "prop")],
         counts={"world_net": 1, "world_trigger": 1},
         frame="The straight forest path in morning light with nobody on it; the single net hangs bundled in the "
               "branches above the path exactly where it is before Leo arrives, and the small trigger disc lies "
               "partly hidden under the leaves on the path"),
    open_frame("s11_leo_worried_open", "trap_leo_closeup", "s11_why_wont_it_break_start", "leo", "'No... Come on!' (S11-L003/4)"),
    open_frame("s11_leo_call_open", "trap_leo_closeup", "s11_call_start", "leo", "Leo's call for help (S11-L008)",
               extra=", held open as in one long deep call"),
    open_frame("s13_leo_warns_open", "trap_leo_closeup", "s13_leo_doubtful_start", "leo", "'Little one? You should stay back.' (S13-L003/5)"),
    edit_frame("s13_milo_at_net", "trap_wide", "s13_milo_confident_end", "PL_trap_morning", ["leo", "milo"],
               "Milo has stepped forward to about x=0.33, right beside the left edge of the draped net, looking up at Leo "
               "with a calm closed smile; Leo is unchanged under the net", "'The mouse stepped closer.' (S13-L009)"),
    dict(id="s13_milo_cu", setup="trap_milo_closeup", what="a close-up of Milo at the net",
         why="Milo's lines in S13 were unreadable in the wide shot (v5 review); a close-up like S15's",
         refs=[("PL_trap_morning", "locked_plate"), ("MILO_CANON", "identity_root"), ("M_EXPR_CALM_CONFIDENT", "expression"),
               ("s15_milo_modest_start", "framing")], counts={"milo": 1},
         frame="Milo looks calm and confident: brows level, bright steady eyes looking up and to the right, a small "
               "closed smile"),
    open_frame("s13_milo_cu_open", "trap_milo_closeup", "s13_milo_cu", "milo", "'...not too strong for my teeth.' (S13-L010/14)"),
    open_frame("s13_leo_doubtful_open", "trap_leo_closeup", "s13_leo_doubtful_end", "leo", "'Your teeth?' (S13-L012)"),
    dict(id="s14_milo_holds_rope", setup="trap_bite", what="the frame before the first bite", world_from="s14_gnaw_fray_start",
         why="'With both little paws holding it steady, the mouse began to gnaw.' (S14-L001)",
         refs=[("s14_gnaw_fray_start", "edit_base"), ("PL_trap_morning", "locked_plate"), ("LEO_CANON", "identity_root"),
               ("MILO_CANON", "identity_root")],
         frame="Exactly the gnawing frame except Milo is not yet biting: he holds the same strand steady with both paws "
               "and looks at it closely, mouth closed; the strand is intact"),
    edit_frame("s14_gnaw_wide", "trap_wide", "s13_milo_at_net", "PL_trap_morning", ["leo", "milo"],
               "Milo stands at the left edge of the draped net at about x=0.31, holding one strand in both paws and biting "
               "it with his two small front teeth; Leo lies low under the net and watches him", "the slow work, seen whole (S14-L004/5)",
               more=[("M_GNAW", "mouth_design")]),
    open_frame("s15_leo_amazed_open", "trap_leo_closeup", "s15_leo_amazed_start", "leo", "'You did it.' (S15-L001/2)"),
    open_frame("s15_milo_modest_open", "trap_milo_closeup", "s15_milo_modest_start", "milo", "'I told you my teeth might help.' (S15-L003)"),
    open_frame("s15_leo_grateful_open", "trap_leo_closeup", "s15_leo_amazed_end", "leo", "Leo's grateful lines (S15-L006/8/10)"),
    open_frame("s15_milo_sincere_open", "trap_milo_closeup", "s15_milo_sincere_start", "milo", "Milo's kindness lines (S15-L009/15)"),
    edit_frame("s15_leo_sits", "trap_wide", "s14_free_hold_end", "PL_trap_morning", ["leo", "milo"],
               "Leo has sat down on his haunches on the path in front of the fallen net, looking down at Milo with a soft "
               "closed smile; Milo stands at the far left looking up at him with a small closed smile",
               "'He had always thought of strength as...' (S15-L017/19)"),
    edit_frame("s15_leo_bows", "trap_wide", "s15_leo_sits", "PL_trap_morning", ["leo", "milo"],
               "Leo has lowered his big head gently toward Milo until his nose is just above the ground near him; Milo "
               "looks up; both have soft closed smiles; Leo's front paws stay on the ground",
               "'Strength could also mean choosing gentleness' (S15-L021)", world_from="s14_free_hold_end"),
    dict(id="s15_leo_smiles", setup="trap_leo_closeup", what="Leo's smile", world_from="s15_leo_amazed_end",
         why="'The lion smiled.' (S15-L023)",
         refs=[("s15_leo_amazed_end", "edit_base"), ("PL_trap_morning", "locked_plate"), ("LEO_CANON", "identity_root"),
               ("L_EXPR_SMILE", "expression")],
         frame="The same close-up; Leo smiles warmly: relaxed brows, soft eyes, a broad closed smile"),
    edit_frame("s16_friends_resting", "tree_day_wide", "s16_friends_end", "PL_tree_day", ["leo", "milo"],
               "Leo rests his head down on his front paws with his eyes gently closed and a content smile; Milo curls up "
               "against Leo's front paw, eyes closed, smiling", "'one small act is enough to begin another' (S16-L011)"),
]

# ---------------------------------------------------------------- pieces, in film order
def P(pid, scene, setup, start, end, lines, action="", mode="closed", join="chain", cut=None, transition=None,
      hold=None, reuse=None):
    if start == end and mode != "ambient" and hold is None:
        hold = True
    return dict(id=pid, scene=scene, setup=setup, start=start, end=end, lines=lines, action=action, mode=mode,
                join=join, cut=cut, transition=transition, hold=hold, reuse=reuse)


def CUT(reason, transition=None):
    return dict(join="cut", cut=reason, transition=transition)


SA, SS, FW, FM = "stream_afternoon_wide", "stream_sunset_wide", "fork_wide", "fork_milo_closeup"
SR, TW, TC, TL, TM, TS = "shortcut_run", "tree_dusk_wide", "tree_dusk_contact", "tree_dusk_leo_closeup", \
    "tree_dusk_milo_closeup", "tree_sky_plate"
HW, RW, DW = "home_night_wide", "trap_wide", "tree_day_wide"
RL, RM, RB, FR = "trap_leo_closeup", "trap_milo_closeup", "trap_bite", "forest_run"
TALK = "speaks gently"

PIECES = [
    # Scene 1: the stream bank in the afternoon
    P("s01_stream_landscape", 1, SA, "PL_stream_afternoon", "PL_stream_afternoon", L(1, 1),
      "The empty stream bank in warm afternoon light: the stream ripples and sparkles, leaf and grass tips sway gently "
      "in a light breeze.", mode="ambient", **CUT("film_start")),
    P("s01_enter", 1, SA, "PL_stream_afternoon", "s01_milo_at_edge", L(1, 1),
      "Milo walks in from the left edge of the frame along the grass lane, upright, looking ahead with curiosity."),
    P("s01_walk_on", 1, SA, "s01_milo_at_edge", "s01_explores_start", L(1, 2),
      "Milo walks steadily to the right along the grass lane, looking around at the bushes and the stream."),
    P("s01_explores", 1, SA, "s01_explores_start", "s01_explores_end", L(1, 2), reuse="s01_explores_closed_r01"),
    P("s01_to_stone", 1, SA, "s01_explores_end", "s01_milo_at_stone", L(1, 3),
      "Milo turns toward the flat feeding stone, takes two small steps to it and reaches up toward the acorn on top "
      "with both paws."),
    P("s01_takes_acorn", 1, SA, "s01_milo_at_stone", "s01_acorn_start", L(1, 4),
      "Milo lifts the acorn down from the stone, sits back on the grass and raises it to his mouth with both paws."),
    P("s01_acorn", 1, SA, "s01_acorn_start", "s01_acorn_end", L(1, 4), reuse="s01_acorn_functional_r01"),
    P("s01_content", 1, SA, "s01_acorn_end", "s01_acorn_end", L(1, 4),
      "Milo sits contentedly holding the acorn and chews slowly; his ears twitch and he breathes calmly."),
    # Scene 2: sunset at the stream
    P("s02_sunset_hold", 2, SS, "s02_notice_start", "s02_notice_start", L(2, 1),
      "The evening light slowly deepens over the stream. Milo sits holding the acorn at his chest, content; his ears "
      "twitch and he breathes calmly.", **CUT("time_change", "crossfade")),
    P("s02_notice", 2, SS, "s02_notice_start", "s02_notice_end", L(2, 1, 2), reuse="s02_notice_closed_r01"),
    P("s02_oh_late", 2, SS, "s02_notice_end", "s02_stand_with_acorn_end", L(2, 2, 3),
      "Milo's ears go up, he says a short startled line, and he rises from sitting to standing on the same spot, "
      "holding the acorn steadily in both paws.", mode="mouth"),
    P("s02_turn_to_stone", 2, SS, "s02_stand_with_acorn_end", "s02_place_acorn_start", L(2, 4),
      "Milo turns toward the feeding stone and takes one small step to it, holding the acorn."),
    P("s02_place_acorn", 2, SS, "s02_place_acorn_start", "s02_place_acorn_end", L(2, 4), reuse="s02_place_acorn_closed_r01"),
    # Scene 3: the fork
    P("s03_fork_landscape", 3, FW, "PL_fork_sunset", "PL_fork_sunset", L(3, 1),
      "The empty fork in the path at sunset: distant clouds drift slowly, leaf and grass tips stir softly.",
      mode="ambient", **CUT("location_change")),
    P("s03_enter", 3, FW, "PL_fork_sunset", "s03_milo_at_fork_edge", L(3, 2),
      "Milo walks in from the left edge of the frame onto the path, upright, looking ahead."),
    P("s03_to_fork", 3, FW, "s03_milo_at_fork_edge", "s03_two_paths_start", L(3, 3),
      "Milo walks to the centre of the fork and stops, turning his head to look along the safe left path toward the "
      "sunlit meadow."),
    P("s03_two_paths", 3, FW, "s03_two_paths_start", "s03_two_paths_end", L(3, 4, 5), reuse="s03_two_paths_closed_r01"),
    P("s03_eyes_shortcut", 3, FW, "s03_two_paths_end", "s03_two_paths_end", L(3, 5),
      "Milo keeps looking along the shortcut into the darker trees, ears forward, breathing calmly."),
    P("s03_sky", 3, FW, "s03_two_paths_end", "s03_milo_looks_up", L(3, 6),
      "Milo tilts his head up to look at the darkening sky above the trees; his body stays still."),
    P("s03_long_path", 3, FW, "s03_milo_looks_up", "s03_two_paths_start", L(3, 7),
      "Milo lowers his head and turns to look along the safe left path."),
    P("s03_shortcut_again", 3, FW, "s03_two_paths_start", "s03_two_paths_end", L(3, 8),
      "Milo turns his gaze from the safe left path to the shortcut on the right."),
    P("s03_says_shortcut", 3, FM, "s03_decides_start", "s03_decides_open", L(3, 9),
      f"Milo, deep in thought, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s03_home_before_stars", 3, FM, "s03_decides_open", "s03_decides_end", L(3, 10),
      f"Milo {TALK} with growing determination; his brows level and his eyes turn steady toward the camera, ending in a "
      "small closed smile.", mode="mouth"),
    # Scene 4: the shortcut
    P("s04_run_in", 4, SR, "PL_shortcut_dusk", "s04_shortcut_run_start", L(4, 1, 2),
      "Milo runs in from the left edge along the dirt lane, upright, in one continuous run.", **CUT("location_change")),
    P("s04_shortcut_run", 4, SR, "s04_shortcut_run_start", "s04_shortcut_run_end", L(4, 3, 4), reuse="s04_shortcut_run_closed_r01"),
    P("s04_run_out", 4, SR, "s04_shortcut_run_end", "PL_shortcut_dusk", L(4, 5),
      "Milo runs on to the right and out of the frame at the right edge; the lane stays empty and the leaf tips settle."),
    # Scene 5: the sleeping lion
    P("s05_leo_sleeps", 5, TW, "s05_leo_sleeps_start", "s05_leo_sleeps_end", L(5, 1), reuse="s05_leo_sleeps_closed_r01",
      **CUT("location_change", "crossfade")),
    P("s05_breathes", 5, TW, "s05_leo_sleeps_end", "s05_leo_sleeps_start", L(5, 1),
      "Leo sleeps peacefully with slow, deep breaths; his extended front paw stays flat across the path."),
    P("s05_sleeping_face", 5, TL, "s05_leo_asleep_cu", "s05_leo_asleep_cu", L(5, 2, 3),
      "Leo sleeps peacefully: slow breathing lifts his mane slightly; his eyes stay closed and his face relaxed.",
      **CUT("close_up")),
    P("s05_milo_comes", 5, TW, "s05_leo_sleeps_start", "s05_paw_contact_start", L(5, 4),
      "Leo sleeps on, still. Milo walks in from the left edge along the path toward the sleeping lion, upright, looking "
      "ahead.", **CUT("close_up")),
    P("s05_paw_contact", 5, TW, "s05_paw_contact_start", "s05_paw_contact_end", L(5, 5, 6, 7), reuse="s05_paw_contact_closed_r01"),
    P("s05_tumble", 5, TW, "s05_paw_contact_end", "s05_milo_lands_wide", L(5, 8, 9),
      "Milo trips over the tip of Leo's extended paw, tumbles forward in one small roll along the grass and comes to "
      "rest against Leo's nose. Leo sleeps on with his eyes closed."),
    P("s05_dazed", 5, TC, "s05_nose_aftermath_start", "s05_nose_aftermath_start", L(5, 9),
      "Milo sits dazed against Leo's nose and blinks; Leo sleeps on, breathing slowly.", **CUT("close_up")),
    P("s05_eyes_open", 5, TC, "s05_nose_aftermath_start", "s05_nose_aftermath_end", L(5, 9, 10), reuse="s05_nose_aftermath_closed_r01"),
    P("s05_what_was_that", 5, TC, "s05_nose_aftermath_end", "s05_nose_aftermath_end", L(5, 11),
      "Leo, eyes open in surprise, says one short line; Milo stays still against his nose.", mode="mouth"),
    # Scene 6: blocked
    P("s06_lifts_head", 6, TC, "s05_nose_aftermath_end", "s06_leo_head_up", L(6, 1),
      "Leo lifts his head from his paws in surprise; Milo slides down from his nose onto the path and stands looking up."),
    P("s06_wide_awake", 6, TW, "s06_barrier_start", "s06_barrier_start", L(6, 1),
      "Leo, awake in a low crouch, watches the little mouse; Milo stands frozen on the path; both breathe.",
      **CUT("close_up")),
    P("s06_barrier", 6, TW, "s06_barrier_start", "s06_barrier_end", L(6, 2), reuse="s06_barrier_closed_r01"),
    P("s06_blocked", 6, TW, "s06_barrier_end", "s06_barrier_end", L(6, 2),
      "Leo's paw rests on the path, blocking the way; Milo trembles slightly and looks up at Leo."),
    P("s06_froze", 6, TM, "s07_milo_sorry_start", "s07_milo_sorry_start", L(6, 3),
      "Milo stands frozen with wide eyes, trembling slightly and breathing quickly.", **CUT("close_up")),
    P("s06_dusk_sky", 6, TS, "PL_tree_sky", "PL_tree_sky", L(6, 4),
      "The dusk sky above the great tree: clouds drift slowly, leaf edges flutter, the first stars twinkle faintly.",
      mode="ambient", **CUT("camera_change")),
    P("s06_still_blocked", 6, TW, "s06_barrier_end", "s06_barrier_end", L(6, 4),
      "Leo's paw rests on the path beside the little mouse; both stay still and breathe; leaf tips stir.",
      **CUT("camera_change")),
    P("s06_leo_frowns", 6, TL, "s07_leo_annoyed_start", "s07_leo_annoyed_end", L(6, 5), reuse="s07_leo_annoyed_closed_r01",
      **CUT("close_up")),
    # Scene 7: words at the tree
    P("s07_you_woke_me", 7, TL, "s07_leo_annoyed_end", "s07_leo_annoyed_open", L(7, 1),
      f"Leo {TALK} but firmly, with mild annoyance.", mode="mouth"),
    P("s07_why_racing", 7, TL, "s07_leo_annoyed_open", "s07_leo_annoyed_end", L(7, 2),
      f"Leo {TALK} but firmly, with mild annoyance.", mode="mouth"),
    P("s07_im_sorry", 7, TM, "s07_milo_sorry_start", "s07_milo_sorry_open", L(7, 3),
      f"Milo, startled and worried, {TALK} and quickly.", mode="mouth", **CUT("close_up")),
    P("s07_shortcut_home", 7, TM, "s07_milo_sorry_open", "s07_milo_sorry_end", L(7, 4),
      f"Milo {TALK}; his face becomes earnest and apologetic.", mode="mouth"),
    P("s07_promise", 7, TM, "s07_milo_sorry_end", "s07_milo_apology_open", L(7, 5),
      f"Milo, apologetic, {TALK}.", mode="mouth"),
    # Scene 8: kindness
    P("s08_looks_down", 8, TW, "s06_barrier_end", "s06_barrier_end", L(8, 1, 2),
      "Leo looks down at the little mouse; Milo trembles slightly beside the paw; both stay in place.", **CUT("close_up")),
    P("s08_could_frighten", 8, TL, "s08_leo_softens_start", "s08_leo_softens_start", L(8, 3),
      "Leo looks down thoughtfully with mild annoyance, breathing slowly; only his eyes move a little.", **CUT("close_up")),
    P("s08_milo_trembles", 8, TM, "s07_milo_sorry_start", "s07_milo_sorry_start", L(8, 4, 5),
      "Milo trembles slightly with wide worried eyes, breathing quickly.", **CUT("close_up")),
    P("s08_strongest", 8, TW, "s06_barrier_end", "s06_barrier_end", L(8, 5, 6),
      "Leo towers over the tiny mouse in a calm low crouch; Milo stands small beside the paw; both breathe.",
      **CUT("close_up")),
    P("s08_did_not_mean", 8, TL, "s08_leo_softens_start", "s08_leo_softens_start", L(8, 6),
      "Leo looks down thoughtfully, breathing slowly; his eyes soften a little.", **CUT("close_up")),
    P("s08_softened", 8, TL, "s08_leo_softens_start", "s08_leo_softens_end", L(8, 7),
      "Leo's face slowly softens into a kind small smile."),
    P("s08_well", 8, TL, "s08_leo_softens_end", "s08_leo_softens_open", L(8, 8, 9), f"Leo {TALK} with a kind smile.", mode="mouth"),
    P("s08_go_home", 8, TL, "s08_leo_softens_open", "s08_leo_softens_end", L(8, 10), f"Leo {TALK} with a kind smile.", mode="mouth"),
    P("s08_look_where", 8, TL, "s08_leo_softens_end", "s08_leo_softens_open", L(8, 11), f"Leo {TALK} with a kind smile.", mode="mouth"),
    P("s08_letting_go", 8, TM, "s08_milo_surprised_start", "s08_milo_surprised_open", L(8, 12),
      f"Milo, surprised, {TALK} in wonder.", mode="mouth", **CUT("close_up")),
    P("s08_mistake", 8, TL, "s08_leo_softens_open", "s08_leo_softens_end", L(8, 13, 14), f"Leo {TALK} with a kind smile.",
      mode="mouth", **CUT("close_up")),
    P("s08_no_reason", 8, TL, "s08_leo_softens_end", "s08_leo_softens_open", L(8, 15), f"Leo {TALK} with a kind smile.", mode="mouth"),
    P("s08_stares", 8, TM, "s08_milo_surprised_open", "s08_milo_surprised_start", L(8, 16),
      "Milo closes his mouth and stares up in surprise, eyes wide.", mode="mouth", **CUT("close_up")),
    P("s08_expected_anger", 8, TW, "s08_kindness_start", "s08_kindness_start", L(8, 17),
      "Leo lies calmly beside the little mouse; both look at each other with soft eyes, breathing gently.",
      **CUT("close_up")),
    P("s08_kindness", 8, TW, "s08_kindness_start", "s08_kindness_end", L(8, 18), reuse="s08_kindness_closed_r01"),
    P("s08_thank_you", 8, TM, "s08_milo_surprised_end", "s08_milo_grateful_open", L(8, 19, 20),
      f"Milo, grateful, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s08_same_kindness", 8, TM, "s08_milo_grateful_open", "s08_milo_surprised_end", L(8, 21),
      f"Milo, grateful, {TALK} with a small smile.", mode="mouth"),
    P("s08_perhaps", 8, TL, "s08_leo_softens_end", "s08_leo_softens_open", L(8, 22, 23), f"Leo {TALK} with a kind smile.",
      mode="mouth", **CUT("close_up")),
    P("s08_stars_almost", 8, TL, "s08_leo_softens_open", "s08_leo_softens_end", L(8, 24), f"Leo {TALK} with a kind smile.", mode="mouth"),
    # Scene 9: home, days pass
    P("s09_hurries", 9, SR, "s09_milo_hurries_start", "s09_milo_hurries_end", L(9, 1, 2), reuse="s09_milo_hurries_closed_r01",
      **CUT("location_change")),
    P("s09_stars", 9, TS, "s09_stars_start", "s09_stars_end", L(9, 3, 4), reuse="s09_stars_ambient_r01",
      **CUT("location_change", "crossfade")),
    P("s09_home", 9, HW, "s09_home_start", "s09_home_end", L(9, 5), reuse="s09_home_closed_r01",
      **CUT("location_change", "crossfade")),
    P("s09_leo_returns", 9, DW, "PL_tree_day", "s09_leo_rests", L(9, 6),
      "Leo walks in from the right edge under the great tree in daylight and settles down to lie in the shade.",
      **CUT("location_change", "crossfade")),
    P("s09_leo_dozes", 9, DW, "s09_leo_rests", "s09_leo_rests", L(9, 7),
      "Leo rests calmly in the shade, breathing slowly; his tail tip twitches; leaves sway softly."),
    # Scene 10: the trap
    P("s10_trap_landscape", 10, RW, "s10_trap_set", "s10_trap_set", L(10, 1),
      "The quiet forest path in morning light with the bundled net still in the branches above; leaves and fern tips "
      "sway softly.", mode="ambient", **CUT("location_change", "crossfade")),
    P("s10_leo_walks_in", 10, RW, "s10_trap_set", "s10_curious_step_start", L(10, 1),
      "Leo walks in from the left edge along the path, looking down at the leaves; the bundled net stays still above."),
    P("s10_curious_step", 10, RW, "s10_curious_step_start", "s10_curious_step_end", L(10, 2, 3), reuse="s10_curious_step_closed_r01"),
    P("s10_release", 10, RW, "s10_curious_step_end", "s10_net_falls_start", L(10, 3),
      "The bundled net above Leo comes loose and begins to open and drop; Leo's paw stays on the trigger."),
    P("s10_net_falls", 10, RW, "s10_net_falls_start", "s10_net_falls_end", L(10, 4), reuse="s10_net_falls_closed_r01"),
    # Scene 11: caught
    P("s11_grips", 11, RW, "s10_net_falls_end", "s11_pull_once_start", L(11, 1),
      "Under the draped net, Leo lowers himself and grips one strand with a front paw, looking worried."),
    P("s11_tug", 11, RW, "s11_pull_once_start", "s11_pull_once_end", L(11, 2),
      "Leo gives the strand one small careful tug; it pulls taut and holds."),
    P("s11_no_come_on", 11, RL, "s11_why_wont_it_break_start", "s11_leo_worried_open", L(11, 3, 4),
      f"Leo, worried, {TALK} and urgently.", mode="mouth", **CUT("close_up")),
    P("s11_why_wont", 11, RL, "s11_leo_worried_open", "s11_why_wont_it_break_end", L(11, 5),
      f"Leo, worried, {TALK}; his worry settles a little.", mode="mouth"),
    P("s11_lies_low", 11, RW, "s11_pull_once_end", "s11_waits_start", L(11, 6),
      "Leo lets go of the strand and lies down low under the net, all paws on the ground, looking to the left.",
      **CUT("close_up")),
    P("s11_waits", 11, RW, "s11_waits_start", "s11_waits_end", L(11, 7), reuse="s11_waits_closed_r01"),
    P("s11_calls", 11, RL, "s11_call_start", "s11_leo_call_open", L(11, 8),
      "Leo raises his head a little and calls out with one deep, long call.", mode="mouth", **CUT("close_up")),
    P("s11_echo", 11, RL, "s11_leo_call_open", "s11_call_end", L(11, 9),
      "Leo's call fades; he closes his mouth and listens hopefully, brows eased.", mode="mouth"),
    # Scene 12: the mouse hears
    P("s12_hears", 12, FR, "s12_hears_start", "s12_hears_end", L(12, 1), reuse="s12_hears_closed_r01",
      **CUT("location_change")),
    P("s12_the_lion", 12, FR, "s12_hears_end", "s12_hears_end", L(12, 2, 3),
      "Milo stands poised with his ears raised and says two short words.", mode="mouth"),
    P("s12_runs", 12, FR, "s12_hears_end", "s12_runs_end", L(12, 4, 5),
      "Milo starts running from his listening position across the lane to the left in one continuous run."),
    P("s12_runs_out", 12, FR, "s12_runs_end", "PL_run_morning", L(12, 6, 7),
      "Milo keeps running to the left and out of the frame at the left edge; the lane stays empty and the leaf tips settle."),
    P("s12_empty_lane", 12, FR, "PL_run_morning", "PL_run_morning", L(12, 8),
      "The empty forest lane in morning light; leaves and grass tips sway softly.", mode="ambient"),
    P("s12_leo_waits", 12, RW, "s11_waits_end", "s11_waits_end", L(12, 9),
      "Leo lies low under the net, breathing calmly, looking to the left.", **CUT("location_change")),
    P("s12_milo_arrives", 12, RW, "s11_waits_end", "s13_arrives_start", L(12, 10),
      "Milo runs in from the left edge along the path toward the net; Leo looks toward him."),
    # Scene 13: the mouse offers help
    P("s13_arrives", 13, RW, "s13_arrives_start", "s13_arrives_end", L(13, 1), reuse="s13_arrives_closed_r01"),
    P("s13_sees_lion", 13, RW, "s13_arrives_end", "s13_arrives_end", L(13, 2),
      "Milo stands still looking at the lion under the net; Leo looks back at him; both breathe."),
    P("s13_little_one", 13, RL, "s13_leo_doubtful_start", "s13_leo_warns_open", L(13, 3, 4),
      f"Leo, concerned, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s13_stay_back", 13, RL, "s13_leo_warns_open", "s13_leo_doubtful_start", L(13, 4, 5),
      f"Leo, concerned, {TALK}.", mode="mouth"),
    P("s13_looks_ropes", 13, RW, "s13_arrives_end", "s13_milo_confident_start", L(13, 6),
      "Milo takes a few small steps closer along the ground and studies the ropes thoughtfully.", **CUT("close_up")),
    P("s13_ropes_big", 13, RW, "s13_milo_confident_start", "s13_milo_confident_start", L(13, 7),
      "Milo studies the ropes, tilting his head slightly; Leo watches him."),
    P("s13_not_nothing", 13, RW, "s13_milo_confident_start", "s13_milo_confident_end", L(13, 8),
      "Milo's expression becomes quietly confident while his body stays still."),
    P("s13_leo_doubts", 13, RL, "s13_leo_doubtful_start", "s13_leo_doubtful_end", L(13, 8),
      "Leo raises one brow gently in doubt.", **CUT("close_up")),
    P("s13_steps_closer", 13, RW, "s13_milo_confident_end", "s13_milo_at_net", L(13, 9),
      "Milo steps forward to the edge of the net and looks up at Leo.", **CUT("close_up")),
    P("s13_too_strong", 13, RM, "s13_milo_cu", "s13_milo_cu_open", L(13, 10),
      f"Milo, calm and confident, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s13_my_teeth", 13, RM, "s13_milo_cu_open", "s13_milo_cu", L(13, 11),
      f"Milo, calm and confident, {TALK}.", mode="mouth"),
    P("s13_your_teeth", 13, RL, "s13_leo_doubtful_end", "s13_leo_doubtful_open", L(13, 12),
      f"Leo, doubtful with one brow raised, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s13_lots_of_them", 13, RM, "s13_milo_cu_open", "s13_milo_cu", L(13, 13, 14),
      f"Milo {TALK} with a cheeky little smile.", mode="mouth", **CUT("close_up")),
    # Scene 14: the rescue
    P("s14_takes_rope", 14, RB, "s14_milo_holds_rope", "s14_gnaw_fray_start", L(14, 1),
      "Milo holds one strand of the net steady with both paws and begins to bite it with his two small front teeth.",
      **CUT("close_up")),
    P("s14_gnaw_fray", 14, RB, "s14_gnaw_fray_start", "s14_gnaw_fray_end", L(14, 1), reuse="s14_gnaw_fray_functional_r01"),
    P("s14_nibble_gnaw", 14, RB, "s14_gnaw_fray_end", "s14_gnaw_fray_end", L(14, 2, 3),
      "Milo keeps nibbling at the same spot on the strand, holding it steady with both paws."),
    P("s14_gnaw_wide", 14, RW, "s14_gnaw_wide", "s14_gnaw_wide", L(14, 4, 5),
      "Milo gnaws steadily at one strand at the edge of the net; Leo lies low under the net and watches.",
      **CUT("close_up")),
    P("s14_leo_doubts", 14, RL, "s13_leo_doubtful_end", "s13_leo_doubtful_end", L(14, 6, 7),
      "Leo watches through the net with one brow raised, breathing slowly.", **CUT("close_up")),
    P("s14_keeps_going", 14, RB, "s14_gnaw_fray_end", "s14_sever_R01_start", L(14, 7, 8),
      "Milo keeps gnawing at the one bite point; more fibres fray.", **CUT("close_up")),
    P("s14_fibres", 14, RB, "s14_sever_R01_start", "s14_sever_R01_start", L(14, 9),
      "Milo keeps nibbling at the badly frayed strand, holding it steady."),
    P("s14_parted", 14, RB, "s14_sever_R01_start", "s14_sever_R01_end", L(14, 10),
      "The last fibres part at the bite point, leaving two frayed ends; Milo settles his jaw."),
    P("s14_steps_aside", 14, RW, "s14_milo_clear_start", "s14_milo_clear_end", L(14, 11), reuse="s14_milo_clear_closed_r01",
      **CUT("close_up")),
    P("s14_widens", 14, RW, "s14_milo_clear_end", "s14_step_clear_start", L(14, 12),
      "The loosened net sags open at Leo's front and Leo rises, putting one front paw forward through the opening."),
    P("s14_step_clear", 14, RW, "s14_step_clear_start", "s14_step_clear_end", L(14, 13), reuse="s14_step_clear_closed_r01"),
    P("s14_free", 14, RW, "s14_step_clear_end", "s14_free_hold_start", L(14, 14),
      "Leo turns his head and looks down toward the little mouse at the left."),
    # Scene 15: kindness is not a debt
    P("s15_you_did_it", 15, RL, "s15_leo_amazed_start", "s15_leo_amazed_open", L(15, 1, 2),
      f"Leo, amazed, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s15_told_you", 15, RM, "s15_milo_modest_start", "s15_milo_modest_open", L(15, 3),
      f"Milo, warm and modest, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s15_looked", 15, RW, "s14_free_hold_start", "s14_free_hold_end", L(15, 4), reuse="s14_free_hold_closed_r01",
      **CUT("close_up")),
    P("s15_rescued", 15, RW, "s14_free_hold_end", "s14_free_hold_end", L(15, 5),
      "Leo stands free and looks down at the tiny mouse; Milo looks up at him; both smile softly and breathe."),
    P("s15_grateful_look", 15, RL, "s15_leo_amazed_end", "s15_leo_amazed_end", L(15, 5),
      "Leo looks at the little mouse with deep gratitude, breathing slowly.", **CUT("close_up")),
    P("s15_came_to_help", 15, RL, "s15_leo_amazed_end", "s15_leo_grateful_open", L(15, 6),
      f"Leo, grateful, {TALK}.", mode="mouth"),
    P("s15_didnt_have_to", 15, RL, "s15_leo_grateful_open", "s15_leo_amazed_end", L(15, 6),
      f"Leo, grateful, {TALK}.", mode="mouth"),
    P("s15_kind_to_me", 15, RM, "s15_milo_modest_open", "s15_milo_modest_end", L(15, 7),
      f"Milo {TALK} with a proud, relieved little smile.", mode="mouth", **CUT("close_up")),
    P("s15_repaid", 15, RL, "s15_leo_amazed_end", "s15_leo_grateful_open", L(15, 8),
      f"Leo, grateful and thoughtful, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s15_not_like_that", 15, RM, "s15_milo_sincere_start", "s15_milo_sincere_open", L(15, 9),
      f"Milo, calm and sincere, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s15_what_mean", 15, RL, "s15_leo_grateful_open", "s15_leo_amazed_end", L(15, 10, 11),
      f"Leo {TALK}, then listens with soft eyes.", mode="mouth", **CUT("close_up")),
    P("s15_no_debt", 15, RM, "s15_milo_sincere_open", "s15_milo_sincere_start", L(15, 11, 12),
      f"Milo, calm and sincere, {TALK}.", mode="mouth", **CUT("close_up")),
    P("s15_saw_someone", 15, RM, "s15_milo_sincere_start", "s15_milo_sincere_open", L(15, 13),
      f"Milo, calm and sincere, {TALK}.", mode="mouth"),
    P("s15_so_i_helped", 15, RM, "s15_milo_sincere_open", "s15_milo_sincere_end", L(15, 14, 15),
      f"Milo, sincere, {TALK}, ending with a small warm smile.", mode="mouth"),
    P("s15_quiet", 15, RL, "s15_leo_reflects_start", "s15_leo_reflects_end", L(15, 16),
      "Leo becomes quiet and thoughtful and lowers his gaze a little.", **CUT("close_up")),
    P("s15_thinks", 15, RL, "s15_leo_reflects_end", "s15_leo_reflects_end", L(15, 17),
      "Leo thinks quietly with lowered eyes, breathing slowly; he blinks once."),
    P("s15_sits", 15, RW, "s14_free_hold_end", "s15_leo_sits", L(15, 17),
      "Leo sits down slowly on his haunches on the path, looking down at the little mouse.", **CUT("close_up")),
    P("s15_claws_roar", 15, RW, "s15_leo_sits", "s15_leo_sits", L(15, 18, 19),
      "Leo sits calmly looking down at Milo; Milo looks up; both breathe; leaf tips stir."),
    P("s15_understood", 15, RL, "s15_leo_reflects_end", "s15_leo_amazed_end", L(15, 19, 20),
      "Leo slowly lifts his gaze; his eyes become soft and warm.", **CUT("close_up")),
    P("s15_understands", 15, RL, "s15_leo_amazed_end", "s15_leo_amazed_end", L(15, 20),
      "Leo looks ahead with soft, warm eyes, breathing slowly."),
    P("s15_gentleness", 15, RW, "s15_leo_sits", "s15_leo_bows", L(15, 21),
      "Leo slowly and gently lowers his big head toward the little mouse.", **CUT("close_up")),
    P("s15_gentle_hold", 15, RW, "s15_leo_bows", "s15_leo_bows", L(15, 21),
      "Leo holds his head low and close to Milo; both smile softly and breathe."),
    P("s15_not_powerless", 15, RM, "s15_milo_modest_end", "s15_milo_modest_end", L(15, 22),
      "Milo smiles with quiet pride, breathing calmly; he blinks once.", **CUT("close_up")),
    P("s15_smiled", 15, RL, "s15_leo_amazed_end", "s15_leo_smiles", L(15, 23),
      "Leo's face opens into a warm smile.", **CUT("close_up")),
    # Scene 16: friends
    P("s16_tree_landscape", 16, DW, "PL_tree_day", "PL_tree_day", L(16, 1),
      "The great old tree in daylight: leaves sway softly, light and shadows move gently on the grass.",
      mode="ambient", **CUT("location_change", "crossfade")),
    P("s16_you_know", 16, DW, "s16_friends_start", "s16_friends_start", L(16, 2, 3),
      f"Leo {TALK} with a happy closed smile between words; Milo listens.", mode="mouth", **CUT("dissolve", "crossfade")),
    P("s16_large_ideas", 16, DW, "s16_friends_start", "s16_friends_start", L(16, 3),
      f"Leo {TALK} with a happy smile; Milo listens.", mode="mouth"),
    P("s16_useful_teeth", 16, DW, "s16_friends_start", "s16_friends_start", L(16, 4),
      f"Milo {TALK} with a cheeky smile; Leo listens.", mode="mouth"),
    P("s16_laugh", 16, DW, "s16_friends_start", "s16_friends_end", L(16, 5, 6), reuse="s16_friends_closed_r01"),
    P("s16_laughter_settles", 16, DW, "s16_friends_end", "s16_friends_end", L(16, 6, 7),
      "Leo and Milo rest together with happy faces, breathing calmly; leaves sway softly."),
    P("s16_old_tree", 16, DW, "PL_tree_day", "PL_tree_day", L(16, 7),
      "The great old tree in daylight: leaves sway softly, light and shadows move gently on the grass.",
      mode="ambient", **CUT("dissolve", "crossfade")),
    P("s16_net_memory", 16, RW, "s10_trap_set", "s10_trap_set", L(16, 8),
      "The quiet forest path in morning light with the bundled net in the branches above; leaves sway softly.",
      mode="ambient", **CUT("location_change", "crossfade")),
    P("s16_stream_memory", 16, SA, "PL_stream_afternoon", "PL_stream_afternoon", L(16, 9),
      "The stream bank in warm afternoon light: the stream ripples and sparkles, leaf and grass tips sway gently.",
      mode="ambient", **CUT("location_change", "crossfade")),
    P("s16_friends_again", 16, DW, "s16_friends_end", "s16_friends_end", L(16, 10),
      "Leo and Milo rest together under the great tree with happy faces, breathing calmly.",
      **CUT("location_change", "crossfade")),
    P("s16_rest", 16, DW, "s16_friends_end", "s16_friends_resting", L(16, 11),
      "Leo slowly lays his head down on his front paws and closes his eyes; Milo curls up against the paw and closes "
      "his eyes too."),
    P("s16_resting", 16, DW, "s16_friends_resting", "s16_friends_resting", L(16, 12),
      "Leo and Milo rest peacefully with closed eyes, breathing slowly; leaves sway softly."),
    P("s16_final_landscape", 16, DW, "PL_tree_day", "PL_tree_day", L(16, 12),
      "The great old tree in daylight: leaves sway softly, light and shadows move gently on the grass.",
      mode="ambient", **CUT("dissolve", "crossfade")),
]

README = """# The Lion and the Mouse, v6 (chained coverage)

The v5 story and narration, re-planned so the pictures last exactly as long as the audio (owner, 2026-10-08):
{pieces} pieces of 2.45 to 6.33 s cover all 11:23.7 of the v5 English narration, and each piece starts on the
image the previous one ended on, unless a planned cut is marked (a face close-up, another place or time, a dissolve).
Rules: `docs/creation-rules.md` CR-21; workflow: `.claude/skills/audio-chained-coverage/SKILL.md`; every change:
`docs/changelog.md`.

## Status (2026-10-08)

- **Plan only: nothing generated.** {pieces} pieces: {reuse} reuse a v5 render (same endpoints, prompt and 81 frames),
  {renders} need new renders; {holds} are holds or landscapes (start = end: breathing, blinking, ambient motion).
- **{new} new images** are needed (bold in `SHOT_PLAN.md`): open-mouth key frames for the talking chains (CR-19),
  entrances onto empty plates, the empty trap path with the net, and a few new beats (Leo's sleeping face, Leo
  sitting and bowing, the friends resting). Everything else reuses the v5 images, which keep their files.
- **Defaults the agent took (owner to confirm):** reuse the v5 English narration (no new TTS) and the v5 images.
- Prompts: `python3 production/image_prompts.py --story lion_and_mouse_v6 lint` must report 0 errors.

## Read in this order

1. `SHOT_PLAN.md`: every piece, its join (chain or the reason for the cut), its images and lines; the new images.
2. `TIMING_SHEET.md`: when each piece plays, its length, frame count and speed (from `chain_plan.py`).
3. `prompts/scene-NN.md`: the exact prompt and ordered references of every new image and every clip.
4. `chain_source.py`: the source of the plan (edit this, then rebuild; see its docstring).

## Rebuild after a change to `chain_source.py`

```bash
python3 production/chain_packet.py stories/lion_and_mouse_v6/chain_source.py
python3 production/image_prompts.py --story lion_and_mouse_v6 build
python3 production/image_prompts.py --story lion_and_mouse_v6 lint
python3 production/image_prompts.py --story lion_and_mouse_v6 md
python3 production/chain_plan.py --story lion_and_mouse_v6 --audio-story lion_and_mouse_v5 apply
```

## Next steps (each needs the owner)

1. Owner reviews `SHOT_PLAN.md` (the sequence, the holds and landscapes, the cuts).
2. The {new} new images, made in film order; each reviewed against both pieces it joins (CR-21 item 8).
3. Join test before any GPU time: `production/chain_preview.py --story lion_and_mouse_v6 --stills` (CPU).
4. Pilot: render scenes 1 to 3, owner chooses takes, then `chain_preview.py --until 104` measures every join of
   the start of the film; repair flagged joins (`continue_from`) before rendering the rest.

## Known risks carried from v5

- Scene 5: Leo's pose differs between the wide frames (one paw stretched across the path) and the two-shot at his nose
  (head on crossed paws); v6 cuts between them (`close_up`) instead of the v5 bridge, which zoomed.
- Scene 8: v5 `s08_milo_surprised` takes show Milo closing his eyes and clasping his paws; v6 does not reuse them.
- Scene 15: the v5 close-up clips drew branches, leaves and paws (prompts named absent things); v6 renders them anew
  with prompts that describe only what is in frame.
"""
