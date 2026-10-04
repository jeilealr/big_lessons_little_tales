"""The Ugly Duckling (ugly_duckling_v1): story content for production/story_packet.py."""

SLUG = "ugly_duckling_v1"
REVISION = "ugly_duckling_v1-2026-10-04"
TITLE = "The Ugly Duckling"
MORAL = ("Everyone grows in their own way and in their own time; being different is nothing to be ashamed of, and "
         "kindness to someone who feels different can help them find where they belong.")

N, OL, M, D, OT, S = "NARRATOR", "OLLIE", "MAMA", "DUCKLINGS", "OTTIE", "SWAN"
WARM = "warm, gentle storyteller for small children, unhurried, smiling"
LINES = [
    # 1 Hatching
    (1, N, WARM, "Once upon a time, beside a quiet pond on a little farm, Mama Duck sat on her nest among the tall green reeds.", ["s01_pond"]),
    (1, N, WARM, "She had been keeping her eggs warm for a long, long time, and today was a very special day.", ["s01_mama_nest"]),
    (1, N, WARM + ", playful sound words", "Crack! Crack! Crack! One, two, three fluffy yellow ducklings popped out of their shells.", ["s01_ducklings_hatch"]),
    (1, M, "loving, delighted mother", "Hello, my little darlings! Welcome to the world!", ["s01_mama_closeup"]),
    (1, N, WARM, "But one egg was still waiting. It was bigger than the others, and a little bit speckled.", ["s01_big_egg"]),
    (1, N, WARM + ", a little suspense, gentle", "Mama Duck waited, and waited. And then... crack!", ["s01_big_egg"]),
    (1, N, WARM, "Out tumbled a big, grey, fluffy duckling with long legs and big flat feet.", ["s01_ollie_hatches"]),
    (1, M, "surprised, then warm and welcoming", "Oh! Well, aren't you a big one! Welcome, little one. I shall call you Ollie.", ["s01_mama_closeup"]),
    # 2 Different
    (2, N, WARM, "The next morning, the ducklings looked at Ollie with big round eyes.", ["s02_ducklings_stare"]),
    (2, D, "three small ducklings speaking together, curious and a little rude, not mean", "Why are you so grey? Why are your feet so big? You don't look like us at all!", ["s02_ducklings_stare"]),
    (2, N, WARM, "Ollie looked at his grey feathers, and he looked at their bright yellow ones, and he felt a little lump in his throat.", ["s02_ollie_sad"]),
    (2, OL, "a small, soft voice, hurt and unsure", "Maybe there's something wrong with me.", ["s02_ollie_sad"]),
    (2, M, "gentle, firm, loving", "There is nothing wrong with you, Ollie. Every one of my ducklings is special in their own way.", ["s02_mama_comforts"]),
    (2, N, WARM, "Mama Duck tucked him under her wing, and for a little while Ollie felt warm and safe.", ["s02_mama_comforts"]),
    # 3 The swimming lesson
    (3, N, WARM, "That afternoon, Mama Duck led her ducklings down to the pond for their very first swim.", ["s03_to_the_water"]),
    (3, M, "cheerful, encouraging teacher", "Paddle, paddle, little ones! Kick your feet, just like me!", ["s03_to_the_water"]),
    (3, N, WARM, "The yellow ducklings wobbled and splashed. But Ollie glided across the water as smoothly as a leaf on the breeze.", ["s03_ollie_glides"]),
    (3, M, "proud, delighted", "Look at Ollie! What a wonderful swimmer!", ["s03_ollie_glides"]),
    (3, N, WARM, "But when Ollie tried to quack, out came a funny honk instead. Honk!", ["s03_honk"]),
    (3, D, "giggling together, teasing", "Honk? Ducks don't honk! You're a funny-looking, funny-sounding duck!", ["s03_honk"]),
    (3, N, WARM + ", tender", "Ollie paddled away into the reeds, all by himself. Two big tears dripped off the end of his beak.", ["s03_ollie_alone"]),
    # 4 Leaving
    (4, N, WARM, "That evening, as the sun went down, Ollie made a big decision.", ["s04_decision"]),
    (4, OL, "quiet, brave but sad", "I don't fit in here. I'll go and find a place where I belong.", ["s04_decision"]),
    (4, N, WARM, "So while everyone was sleeping, Ollie waddled away along the reedy path, out into the big wide world.", ["s04_leaves"]),
    (4, N, WARM, "He looked back just once, at the little pond glowing in the evening light. Then he kept on walking.", ["s04_leaves"]),
    # 5 Autumn
    (5, N, WARM, "Ollie walked for days and days, until he came to a great big lake. The leaves on the trees turned red and gold, and they floated down onto the water.", ["s05_lake"]),
    (5, N, WARM, "Ollie asked the frogs if he could live with them, but frogs live in the mud. He asked the hens on a farm, but hens don't swim.", ["s05_ollie_lake"]),
    (5, OL, "lonely, wondering", "Isn't there anyone like me, anywhere?", ["s05_ollie_lake"]),
    (5, N, WARM + ", full of wonder", "Then, high above him, came a sound like gentle music. A family of beautiful white swans was flying south, their long necks stretched out and their wings shining in the sun.", ["s05_swans_fly"]),
    (5, OL, "amazed, longing, whispering", "Oh... they're the most beautiful birds I've ever seen. I wish I could be like them.", ["s05_ollie_watches"]),
    # 6 Winter
    (6, N, WARM, "Then winter came. Snow covered the ground, and the river turned to ice.", ["s06_winter"]),
    (6, N, WARM + ", tender", "Ollie was cold and hungry, and very, very lonely. He curled up in the snow by the frozen river and shivered.", ["s06_ollie_cold"]),
    (6, N, WARM, "Just then, a little round face popped out of a hole in the riverbank. It was Ottie the Otter.", ["s06_ottie_finds"]),
    (6, OT, "kind, bubbly, warm-hearted", "Oh, you poor thing! You're shivering! Come inside, quickly. My burrow is warm and cosy.", ["s06_ottie_closeup"]),
    (6, OL, "shy, surprised", "You want me to come in? Even though I'm grey, and gangly, and I honk?", ["s06_ollie_shy"]),
    (6, OT, "laughing kindly", "Of course! You don't have to look like anyone else to be my friend. Come on!", ["s06_ottie_closeup"]),
    # 7 Friends in the snow
    (7, N, WARM, "All winter long, Ollie stayed with Ottie. They shared fish soup, told stories, and slid on the ice together.", ["s07_sliding"]),
    (7, OT, "playful, laughing", "Wheee! Your big feet are perfect for sliding, Ollie!", ["s07_sliding"]),
    (7, OL, "laughing, happy for the first time", "Honk! Honk! This is the most fun I've ever had!", ["s07_sliding"]),
    (7, N, WARM, "And slowly, without even noticing, Ollie grew. His neck grew longer, his wings grew stronger, and his grey feathers began to change.", ["s07_ollie_grows"]),
    # 8 Spring
    (8, N, WARM, "At last, spring arrived. The ice melted, the flowers bloomed, and the birds sang again.", ["s08_spring"]),
    (8, OL, "grateful, warm", "Thank you, Ottie. You were my friend when I had nobody. I'll never forget it.", ["s08_goodbye"]),
    (8, OT, "warm, encouraging", "Go and find your place, Ollie. And come back to visit!", ["s08_goodbye"]),
    (8, N, WARM, "Ollie stretched his wings, and to his surprise they lifted him up into the sky. He was flying!", ["s08_flies"]),
    # 9 The swans
    (9, N, WARM, "Ollie flew until he came back to the great lake, sparkling in the spring sunshine. And there, gliding on the water, were the beautiful white swans.", ["s09_swans_lake"]),
    (9, OL, "nervous, small voice", "They'll probably laugh at me, like everyone else. But I want to say hello, just once.", ["s09_ollie_nervous"]),
    (9, N, WARM, "So Ollie landed softly on the water and bowed his head, waiting for them to laugh.", ["s09_ollie_bows"]),
    # 10 The reflection
    (10, N, WARM + ", full of wonder", "But as he bowed his head, he saw his reflection in the clear, still water.", ["s10_reflection"]),
    (10, N, WARM, "He wasn't a grey, gangly duckling any more. Looking back at him was a beautiful white swan, with a long graceful neck and shining feathers.", ["s10_reflection"]),
    (10, OL, "astonished, whispering", "Is that... is that me?", ["s10_ollie_amazed"]),
    (10, S, "graceful, kind, welcoming", "Welcome, young swan! We have been waiting for you. Will you swim with us?", ["s10_swan_welcomes"]),
    (10, OL, "joyful, emotional", "Yes! Oh yes, I'd love to!", ["s10_swim_together"]),
    (10, N, WARM, "For the first time, Ollie knew exactly where he belonged.", ["s10_swim_together"]),
    # 11 Home again
    (11, N, WARM, "But Ollie had not forgotten the little pond, or Mama Duck. One sunny morning, he flew home to visit.", ["s11_arrives_home"]),
    (11, D, "amazed, together", "Wow! Look at that beautiful swan!", ["s11_ducklings_amazed"]),
    (11, M, "recognising him, overjoyed", "Ollie? Is that you? My Ollie!", ["s11_mama_closeup"]),
    (11, OL, "warm, happy", "Hello, Mama. I'm a swan! I was a swan all along.", ["s11_ollie_closeup"]),
    (11, D, "sorry, sincere, together", "We're sorry we teased you, Ollie. We didn't understand that you were just different.", ["s11_ducklings_sorry"]),
    (11, OL, "kind, forgiving", "That's all right. Being different isn't wrong. It just means growing in your own way.", ["s11_ollie_closeup"]),
    (11, M, "proud, tender", "I always knew you were special, Ollie. Not because you are a swan, but because you are you.", ["s11_mama_closeup"]),
    # 12 Everyone belongs
    (12, N, WARM, "From then on, Ollie spent his days gliding on the great lake with the swans, and visiting the little pond with Mama Duck and the ducklings.", ["s12_family"]),
    (12, N, WARM, "And Ottie the Otter came to visit too, and they all splashed and played together in the sunshine.", ["s12_family"]),
    (12, N, WARM, "Because everyone grows in their own way, and in their own time.", ["s12_end"]),
    (12, N, WARM + ", the moral, slow and clear", "And a little kindness can help anyone find the place where they belong.", ["s12_end"]),
    (12, N, WARM + ", closing", "The end.", ["s12_end"]),
]
SCENE_TITLES = {1: "Hatching day", 2: "Different", 3: "The swimming lesson", 4: "Leaving the pond", 5: "The great lake",
                6: "Winter", 7: "Friends in the snow", 8: "Spring", 9: "The swans", 10: "The reflection",
                11: "Home again", 12: "Everyone belongs"}

TAIL = ("Fine looped felt fibres and small visible stitches. These intrinsic colours and this mid brightness stay "
        "identical in every image; scene light only tints and shades them. {p} pose, facing and expression are the "
        "ones this prompt states.")
CHARACTERS = {
    "mama": {"name": "Mama Duck", "folder": "MamaDuck", "canon_id": "MAMA_CANON",
        "identity": ("Mama Duck is one plump, gentle wool-felt mother duck who stands on two webbed feet. Her body feathers "
            "are soft warm-brown felt (#9C6B43) with lighter speckles of buff-cream (#E3C9A0) and a pale cream chest "
            "(#EADBBE). Her head is the same warm-brown with a thin cream stripe above each eye. Her flat rounded beak "
            "is warm orange-yellow (#E8A33A) and her two webbed feet are the same orange-yellow. Two round glossy eyes: "
            "dark-brown irises (#3E2A1E), black pupils, one white catch-light at upper right, ivory sclera (#F4EEE2); "
            "two short soft dark-brown brow stitches. Two folded wings, each with a small teal-blue patch (#3E8A93) "
            "edged in white near its back edge, and one short pointed tail of feathers. " + TAIL.format(p="Her")),
        "sheet": "one plump warm-brown felt mother duck with buff-cream speckles, a pale cream chest, an orange-yellow beak and feet, two dark-brown eyes and a teal-blue wing patch",
        "mouth": "When Mama Duck speaks, her flat beak opens slightly to show a soft pink inside; she has no teeth.",
        "palette": {"body": "#9C6B43", "speckles": "#E3C9A0", "chest": "#EADBBE", "beak_feet": "#E8A33A", "wing_patch": "#3E8A93"},
        "proportions": {}, "checklist": ["one duck, two wings, two webbed feet, one short tail", "warm-brown body with buff-cream speckles",
                      "orange-yellow beak and feet", "teal-blue wing patch", "two dark-brown eyes", "felt texture"],
        "drift_phrases": ["mallard", "green head"]},
    "ducklings": {"name": "the Ducklings", "plural": "ducklings", "folder": "Ducklings", "canon_id": "DUCKLINGS_CANON",
        "identity": ("Each of the three ducklings is the same: one small, round, fluffy wool-felt duckling who stands on two "
            "little webbed feet, with bright buttercup-yellow down (#F5D04A), a slightly paler lemon-yellow chest "
            "(#F8E27C), a small flat orange beak (#EE9A3A), two tiny orange webbed feet, two little stubby wings and "
            "two round glossy eyes with dark-brown irises (#3E2A1E), black pupils, one white catch-light and ivory "
            "sclera; two tiny brown brow stitches. Each duckling is about one third of Mama Duck's height. "
            + TAIL.format(p="Their")),
        "sheet": "a small round fluffy buttercup-yellow felt duckling with a small orange beak and feet and two dark-brown eyes",
        "mouth": "When a duckling speaks, its little beak opens slightly to show a soft pink inside.",
        "palette": {"down": "#F5D04A", "chest": "#F8E27C", "beak_feet": "#EE9A3A"},
        "proportions": {}, "checklist": ["every duckling identical", "bright buttercup-yellow down", "small orange beak and feet",
                      "two dark-brown eyes", "count matches the cast line"],
        "drift_phrases": ["chick", "chicken"]},
    "ollie": {"name": "Ollie", "folder": "Ollie", "canon_id": "OLLIE_CANON",
        "identity": ("Ollie is one young wool-felt cygnet, a baby swan who looks like a big, gangly duckling and stands on two "
            "big flat webbed feet. His fluffy down is soft dove-grey felt (#9A9893) with lighter pale-grey cheeks and "
            "chest (#C9C7C1); he is about half of Mama Duck's height, taller and longer-legged than the yellow "
            "ducklings, with a slightly longer neck. His beak is flat and slate-grey (#6C6B68) with a darker tip, and "
            "his two big webbed feet and long legs are charcoal-grey (#4A4946). Two large round glossy eyes: "
            "dark-brown irises (#3E2A1E), black pupils, one white catch-light at upper right, ivory sclera (#F4EEE2); "
            "two short soft grey brow stitches. Two small fluffy wings and a short fluffy tail. " + TAIL.format(p="His")),
        "sheet": "one gangly young dove-grey felt cygnet with pale-grey cheeks, a slate-grey beak, big charcoal-grey webbed feet and two dark-brown eyes",
        "mouth": "When Ollie speaks, his flat beak opens slightly to show a soft pink inside; he has no teeth.",
        "palette": {"down": "#9A9893", "cheeks_chest": "#C9C7C1", "beak": "#6C6B68", "feet": "#4A4946"},
        "proportions": {"height_to_mama": 0.55}, "checklist": ["one cygnet, two small wings, two big webbed feet", "dove-grey fluffy down",
                      "pale-grey cheeks and chest", "slate-grey beak", "charcoal-grey legs and feet", "two dark-brown eyes",
                      "about half of Mama Duck's height", "felt texture"],
        "drift_phrases": ["ugly", "dirty", "black duckling"]},
    "ollie_swan": {"name": "Ollie the swan", "folder": "OllieSwan", "canon_id": "OLLIE_SWAN_CANON",
        "identity": ("Ollie the swan is one young, graceful wool-felt swan, Ollie grown up: a snow-white felt body (#F7F5EF) "
            "with soft pearl-grey shading under the wings (#DCDAD3), a long elegant curved neck and a small round "
            "head. His beak is warm coral-orange (#E2784A) with a black knob and black base (#1E1E1E), and his two webbed "
            "feet are charcoal-grey (#4A4946). Two round glossy eyes: dark-brown irises (#3E2A1E), black pupils, one "
            "white catch-light at upper right, ivory sclera (#F4EEE2), each framed by a small black patch between eye "
            "and beak; two soft pearl-grey brow stitches. Two large folded wings with layered feather stitches and one "
            "short pointed tail. With his neck up he is about twice Mama Duck's height. " + TAIL.format(p="His")),
        "sheet": "one young graceful snow-white felt swan with a long curved neck, a coral-orange beak with a black knob, charcoal-grey feet and two dark-brown eyes",
        "mouth": "When Ollie the swan speaks, his beak opens slightly to show a soft pink inside; he has no teeth.",
        "palette": {"body": "#F7F5EF", "shading": "#DCDAD3", "beak": "#E2784A", "knob": "#1E1E1E", "feet": "#4A4946"},
        "proportions": {"height_to_mama": 1.9}, "checklist": ["one swan, two large wings, two webbed feet", "snow-white body",
                      "long curved neck", "coral-orange beak with a black knob", "two dark-brown eyes with small black patches",
                      "about twice Mama Duck's height", "felt texture"],
        "drift_phrases": ["black swan", "goose"]},
    "swans": {"name": "the Swans", "plural": "swans", "folder": "Swans", "canon_id": "SWANS_CANON",
        "identity": ("Each adult swan of the swan family is the same: one large, graceful wool-felt swan with a snow-white "
            "felt body (#F8F6F0), soft pearl-grey shading under the wings (#DCDAD3), a long elegant curved neck, a "
            "warm coral-orange beak (#E2784A) with a black knob and base (#1E1E1E), two charcoal-grey webbed feet "
            "(#4A4946), two kind round glossy eyes with dark-brown irises (#3E2A1E), black pupils, one white "
            "catch-light and ivory sclera, two large folded wings and one short pointed tail. With its neck up, each "
            "swan is a little taller than Ollie the swan. " + TAIL.format(p="Their")),
        "sheet": "a large graceful snow-white felt swan with a long curved neck, a coral-orange beak with a black knob and two kind dark-brown eyes",
        "mouth": "When a swan speaks, its beak opens slightly to show a soft pink inside.",
        "palette": {"body": "#F8F6F0", "beak": "#E2784A", "knob": "#1E1E1E"},
        "proportions": {"height_to_mama": 2.1}, "checklist": ["every adult swan identical", "snow-white body, long curved neck",
                      "coral-orange beak with a black knob", "count matches the cast line", "felt texture"],
        "drift_phrases": ["black swan"]},
    "ottie": {"name": "Ottie", "folder": "Ottie", "canon_id": "OTTIE_CANON",
        "identity": ("Ottie is one cheerful, round-faced wool-felt river otter who can stand upright on her two hind feet "
            "and runs on four. Her fur felt is warm chocolate-brown (#6B4A32) with a creamy-beige face, throat and "
            "chest (#E2CBA8). Her round head has two tiny rounded ears, a broad muzzle with a big round dark-brown nose "
            "(#2E1E16), a smiling mouth line and four long pale whiskers (#EFE3CF) on each side. Two round glossy eyes: "
            "dark-brown irises (#3E2A1E), black pupils, one white catch-light at upper right, ivory sclera (#F4EEE2); "
            "two short dark-brown brows. Short arms with small webbed paws, two webbed hind feet and one long thick "
            "tapering tail. Standing upright she is a little taller than Mama Duck. " + TAIL.format(p="Her")),
        "sheet": "one cheerful chocolate-brown felt otter with a creamy-beige face and chest, a big dark-brown nose, long whiskers, two dark-brown eyes and a long thick tail",
        "mouth": "When Ottie's mouth opens, it is a rounded opening with a dark warm-brown interior, a soft pink tongue and small ivory teeth.",
        "palette": {"fur": "#6B4A32", "face_chest": "#E2CBA8", "nose": "#2E1E16"},
        "proportions": {"height_to_mama": 1.1}, "checklist": ["one otter, four legs, one long thick tail", "chocolate-brown fur",
                      "creamy-beige face, throat and chest", "two tiny round ears", "big dark-brown nose", "four whiskers on each side",
                      "two dark-brown eyes", "felt texture"],
        "drift_phrases": ["beaver", "weasel"]},
}
ORDER = ["swans", "ollie_swan", "ottie", "mama", "ollie", "ducklings"]
COUNTS = {"ducklings": 3, "swans": 2}
PREFIX = {"mama": "M", "ducklings": "D", "ollie": "O", "ollie_swan": "OS", "swans": "S", "ottie": "OT"}

CAST_SCALE_BLOCK = (
    "Relative size (fixed for the whole story, the same at the same distance from the camera), with Mama Duck's height "
    "as 1: each yellow duckling 0.35, Ollie the grey cygnet 0.55, Ottie standing upright 1.1, Ollie the grown swan with "
    "his neck up 1.9, each adult swan 2.1. The cygnet Ollie is clearly bigger than the yellow ducklings and clearly "
    "smaller than Mama Duck. Swimming, sitting or curling up changes a silhouette but never the size of a head, beak "
    "or wing.")
CAST_SCALE = {"rule": "At equal depth, with Mama Duck's height as 1.0: each duckling 0.35, Ollie the cygnet 0.55, Ottie upright 1.1, Ollie the swan 1.9 (neck up), each adult swan 2.1.",
              "anchor_record": "LINEUP",
              "status": "design targets; measure them on the approved LINEUP image and update every setup's sizes"}
LINEUP_SIZE = "Each adult swan with its neck up measures 0.75 of the frame height; every other character follows the size lineup above."
FINAL_CHECK = ("Before finishing, check: each named character appears exactly once and every group has exactly the "
               "number the cast line states; every bird has exactly two eyes, one beak, two wings and two webbed feet, "
               "Ottie has four limbs and one tail, and every character has two eyebrow stitches, one above each eye; "
               "no text, letters, labels or watermark anywhere.")

L_POND = ["the reed nest at the left (x 0.08-0.32, y 0.58-0.80)", "the pond water across the middle and right (x 0.35-1.00, y 0.55-0.80)",
          "tall reeds along the far bank (y 0.35-0.55)", "a small wooden farm fence and barn roof far behind at the right (x 0.70-0.95, y 0.20-0.40)",
          "the grassy bank in front where characters stand (y 0.78-0.92)"]
L_LAKE = ["the wide lake water filling the middle (y 0.48-0.85)", "trees along the far shore (y 0.22-0.48)",
          "a flat grassy shore at the lower left where characters stand (x 0.00-0.35, y 0.78-0.95)",
          "a few rounded stones at the water's edge at the lower right (x 0.80-0.95, y 0.82-0.92)"]
LOC = {
    "pond_morning": dict(folder="pond", stem="pond_morning", label="the farm pond in spring morning light",
        description=("A quiet felt farm pond in spring: a cosy reed nest on the bank at the left, calm water with lily pads "
                     "across the middle and right, tall reeds and soft round trees on the far bank, a little wooden fence and "
                     "a red barn roof far behind at the right, a grassy bank in front."),
        landmarks=L_POND, light="Soft fresh morning light from the left; gentle mist on the water.",
        ambient="Reeds sway; the water ripples softly; lily pads bob; nest, fence and barn stay fixed."),
    "pond_day": dict(folder="pond", stem="pond_day", derived_from="pond_morning", label="the farm pond on a sunny afternoon",
        description="The same farm pond as the morning plate, with the nest, reeds, fence and barn in exactly the same places, on a sunny afternoon.",
        landmarks=L_POND, light="Warm bright afternoon sunlight from above; sparkles on the water.",
        ambient="Reeds sway; the water sparkles and ripples; nest, fence and barn stay fixed."),
    "pond_evening": dict(folder="pond", stem="pond_evening", derived_from="pond_morning", label="the farm pond at sunset",
        description="The same farm pond as the morning plate, with the nest, reeds, fence and barn in exactly the same places, at sunset.",
        landmarks=L_POND, light="Sunset: golden-pink light low from the right, long shadows, the water glowing.",
        ambient="Reeds sway slowly; the water glows; nest, fence and barn stay fixed."),
    "reed_path": dict(folder="reed_path", stem="reed_path_evening", label="the reedy path at dusk",
        description=("A side view of a narrow earth path winding between tall felt reeds and cattails at dusk, travel from "
                     "left to right, with the soft glow of the farm pond far behind at the left."),
        landmarks=["the earth path across the frame (y 0.76-0.88)", "tall reeds and cattails behind the path (y 0.25-0.76)",
                   "the pond's glow far behind at the left (x 0.00-0.20, y 0.45-0.60)", "the first stars in the sky"],
        light="Dusk: soft blue light with a warm glow at the left.", ambient="Reeds and cattails sway; stars twinkle; the path stays fixed."),
    "lake_autumn": dict(folder="lake", stem="lake_autumn", label="the great lake in autumn",
        description=("A great wide felt lake in autumn: still water reflecting trees with red, orange and golden leaves on the "
                     "far shore, a few leaves floating on the water, a grassy shore at the lower left and big open sky."),
        landmarks=L_LAKE, light="Golden autumn afternoon light from the right; soft warm reflections.",
        ambient="Leaves drift down and float; the water ripples gently; trees and shore stay fixed."),
    "lake_spring": dict(folder="lake", stem="lake_spring", derived_from="lake_autumn", label="the great lake in spring",
        description="The same great lake as the autumn plate, with the shore, stones and treeline in exactly the same places, in spring: fresh green leaves, blossoms and sparkling water.",
        landmarks=L_LAKE, light="Bright fresh spring sunlight from the upper left; sparkles on the water.",
        ambient="Blossoms drift; the water sparkles; trees and shore stay fixed."),
    "river_winter": dict(folder="river", stem="river_winter", label="the frozen river in winter",
        description=("A snowy felt riverbank in winter: a frozen river of smooth pale-blue ice across the middle, soft snow "
                     "banks, bare trees, and in the bank at the right a round burrow entrance framed by roots with a warm "
                     "glow inside."),
        landmarks=["the frozen river across the middle (y 0.55-0.75)", "the snow bank in front where characters stand (y 0.76-0.94)",
                   "the burrow entrance in the bank at the right (x 0.72-0.88, y 0.55-0.75) with a warm glow", "bare trees on the far bank"],
        light="Soft cool winter daylight, gently falling snow; warm light from the burrow.",
        ambient="Snow falls gently; the burrow glow flickers; ice, trees and bank stay fixed."),
}

CLOSE_TREATMENT = ("The background is the same place, very strongly blurred into soft shapes of colour, as with a "
                   "portrait lens at f/1.4; nothing stands in front of the character except what this frame states. "
                   "The blurred place:")


def closeup(loc, who, label, top_word="the top of the head", top=0.05):
    name = CHARACTERS[who]["name"]
    return dict(location=loc, framing="dialogue_close_up", label=label,
                camera=(f"Close-up, 16:9: {name}'s head and upper chest are centred, {top_word} near y={top:.2f} and the "
                        "chest near y=0.80, facing the camera."),
                background_treatment=CLOSE_TREATMENT)


WIDE = "Fixed normal-height wide camera, 16:9, exactly the framing of the locked plate."
RATIO = {"mama": 1.0, "ducklings": 0.35, "ollie": 0.55, "ottie": 1.1, "ollie_swan": 1.9, "swans": 2.1}
WHAT = {"mama": "Mama Duck measures about {h:.2f} of the frame height",
        "ducklings": "each duckling measures about {h:.2f} of the frame height",
        "ollie": "Ollie the cygnet measures about {h:.2f} of the frame height",
        "ottie": "Ottie standing upright measures about {h:.2f} of the frame height",
        "ollie_swan": "Ollie the swan with his neck up measures about {h:.2f} of the frame height",
        "swans": "each adult swan with its neck up measures about {h:.2f} of the frame height"}


def sizes(mama_h, chars=tuple(RATIO)):
    out = {}
    for c in chars:
        t = WHAT[c].format(h=mama_h * RATIO[c])
        out[c] = t[0].upper() + t[1:] + "."
    return out


REL = "Every character keeps the story's size lineup; the yellow ducklings are the smallest, and the grey cygnet is bigger than them and smaller than Mama Duck."
SETUPS = {
    "pond_plate": dict(location="pond_morning", framing="empty_plate", label="the empty farm pond in morning light", camera=WIDE),
    "nest_wide": dict(location="pond_morning", framing="scene_wide", label="a wide shot of the nest by the farm pond in morning light",
                      camera=WIDE + " The nest sits at the left; characters stand on the bank near y=0.86.", size=sizes(0.26), relation=REL),
    "nest_closer": dict(location="pond_morning", framing="close_two_shot", label="a closer shot of the nest in the reeds",
                        camera=("Fixed closer camera at the nest, 16:9: one shared crop of the wide setup that magnifies the nest, "
                                "Mama Duck and the eggs equally; the plate is softly blurred behind them."),
                        size=sizes(0.60, ("mama", "ducklings", "ollie")), relation=REL),
    "mama_closeup": closeup("pond_morning", "mama", "a close-up of Mama Duck by the nest"),
    "pond_day_wide": dict(location="pond_day", framing="scene_wide", label="a wide shot of the farm pond on a sunny afternoon",
                          camera=WIDE + " Characters stand on the bank near y=0.86 or swim on the water near y=0.70.", size=sizes(0.26), relation=REL),
    "pond_day_ollie_closeup": closeup("pond_day", "ollie", "a close-up of Ollie by the pond"),
    "pond_day_mama_closeup": closeup("pond_day", "mama", "a close-up of Mama Duck by the pond"),
    "pond_evening_wide": dict(location="pond_evening", framing="scene_wide", label="a wide shot of the farm pond at sunset",
                              camera=WIDE + " Characters stand on the bank near y=0.86.", size=sizes(0.26), relation=REL),
    "pond_evening_ollie_closeup": closeup("pond_evening", "ollie", "a close-up of Ollie by the pond at sunset"),
    "reed_path_side": dict(location="reed_path", framing="scene_wide", label="a side-on wide shot of the reedy path at dusk",
                           camera="Fixed normal-height side camera, 16:9, exactly the framing of the locked plate; Ollie walks along the path from left to right.",
                           size=sizes(0.40, ("ollie",)), relation=REL),
    "lake_autumn_wide": dict(location="lake_autumn", framing="scene_wide", label="a wide shot of the great lake in autumn",
                             camera=WIDE + " Characters stand on the shore at the lower left or swim on the water.",
                             size={**sizes(0.30, ("ollie",)), "swans": "The flying swans are small in the sky, each about 0.10 of the frame width."}, relation=REL),
    "lake_autumn_ollie_closeup": closeup("lake_autumn", "ollie", "a close-up of Ollie at the great lake in autumn"),
    "river_wide": dict(location="river_winter", framing="scene_wide", label="a wide shot of the frozen river in winter",
                       camera=WIDE + " Characters stand on the snow bank near y=0.88 or slide on the ice.", size=sizes(0.28, ("ollie", "ottie")), relation=REL),
    "river_ollie_closeup": closeup("river_winter", "ollie", "a close-up of Ollie in the snow"),
    "river_ottie_closeup": closeup("river_winter", "ottie", "a close-up of Ottie at her burrow"),
    "lake_spring_wide": dict(location="lake_spring", framing="scene_wide", label="a wide shot of the great lake in spring",
                             camera=WIDE + " Characters stand on the shore at the lower left or swim on the water near y=0.70.",
                             size=sizes(0.22, ("ollie", "ollie_swan", "swans")), relation=REL),
    "lake_spring_reflection": dict(location="lake_spring", framing="close_two_shot", label="a closer shot of Ollie and his reflection on the spring lake",
                                   camera=("Fixed closer camera low over the water, 16:9: Ollie the swan in the upper half, his clear "
                                           "mirror reflection in the still water in the lower half; the far shore softly blurred."),
                                   size={"ollie_swan": "Ollie the swan, head bowed, fills about 0.45 of the frame height above the waterline, and his reflection the same below it."},
                                   relation="The reflection is the same swan, mirrored, at the same size."),
    "lake_spring_ollie_closeup": closeup("lake_spring", "ollie_swan", "a close-up of Ollie the swan on the spring lake"),
    "lake_spring_swan_closeup": closeup("lake_spring", "swans", "a close-up of one adult swan on the spring lake"),
    "pond_spring_wide": dict(location="pond_day", framing="scene_wide", label="a wide shot of the farm pond on a sunny spring day",
                             camera=WIDE + " Characters stand on the bank near y=0.86 or swim on the water near y=0.70.",
                             size=sizes(0.20, ("mama", "ducklings", "ollie_swan", "ottie")), relation=REL),
    "pond_spring_mama_closeup": closeup("pond_day", "mama", "a close-up of Mama Duck on a spring day"),
    "pond_spring_ollie_closeup": closeup("pond_day", "ollie_swan", "a close-up of Ollie the swan at the farm pond"),
}

D3 = "ducklings*3"
SHOTS = [
    ("s01_pond", 1, "pond_plate", [], "The empty farm pond in soft morning mist, the reed nest at the left",
     "The same pond; the mist has thinned a little", "Mist drifts slowly over the pond; reeds sway.", None, {}),
    ("s01_mama_nest", 1, "nest_wide", ["mama"],
     "Mama Duck sits on her reed nest at the left, wings fluffed over her eggs, eyes half closed and calm",
     "Mama Duck lifts her head and looks down at her nest, listening", "Mama Duck sits on her nest and lifts her head to listen.", None,
     {"mama": ("M_EXPR_CALM", "M_EXPR_CALM")}),
    ("s01_ducklings_hatch", 1, "nest_closer", ["mama", D3],
     "Mama Duck stands beside the nest; three cracked eggshells lie in it and three yellow ducklings tumble out, blinking",
     "The three ducklings stand in a row on the edge of the nest, looking up at Mama Duck; one big speckled egg still lies whole in the nest",
     "Three yellow ducklings tumble out of their shells and line up beside the one unhatched egg.", None,
     {"mama": ("M_EXPR_JOY", "M_EXPR_JOY")}),
    ("s01_mama_closeup", 1, "mama_closeup", ["mama"],
     "Mama Duck looks down toward the camera with loving delight: brows raised, eyes shining, beak closed in a smile",
     "Mama Duck speaks warmly, beak slightly open, eyes soft", "Mama Duck smiles with joy and speaks warmly.", None,
     {"mama": ("M_EXPR_JOY", "M_EXPR_JOY")}),
    ("s01_big_egg", 1, "nest_closer", ["mama", D3],
     "Mama Duck and the three ducklings lean over the one big speckled egg in the nest, waiting",
     "A crack runs across the big egg; everyone leans closer with wide eyes", "The family leans in as a crack appears in the big egg.", None,
     {"mama": ("M_EXPR_CALM", "M_EXPR_SURPRISED")}),
    ("s01_ollie_hatches", 1, "nest_closer", ["mama", D3, "ollie"],
     "Ollie tumbles out of the big broken egg in the nest, blinking and wobbly; Mama Duck and the three ducklings look at him in surprise",
     "Ollie stands up on his big feet in the nest, looking up shyly at Mama Duck; Mama Duck smiles warmly at him",
     "Ollie tumbles out of the big egg, stands up wobbling, and Mama Duck smiles at him.", None,
     {"mama": ("M_EXPR_SURPRISED", "M_EXPR_JOY"), "ollie": ("O_EXPR_SHY", "O_EXPR_SHY")}),
    ("s02_ducklings_stare", 2, "nest_wide", ["mama", D3, "ollie"],
     "The three ducklings stand in a row on the bank near x=0.45 staring at Ollie near x=0.65, one pointing a wing at his big feet; Mama Duck in the nest at the left",
     "The ducklings giggle behind their wings; Ollie looks down at his feet", "The ducklings stare and point at Ollie's big feet and giggle.", None,
     {"ollie": ("O_EXPR_SHY", "O_EXPR_SAD")}),
    ("s02_ollie_sad", 2, "pond_day_ollie_closeup", ["ollie"],
     "Ollie looks down sadly: brows tilted up in the middle, eyes lowered and shiny, beak closed",
     "Ollie speaks softly with the same sad face, beak slightly open", "Ollie looks down sadly and speaks softly.", None,
     {"ollie": ("O_EXPR_SAD", "O_EXPR_SAD")}),
    ("s02_mama_comforts", 2, "nest_wide", ["mama", "ollie"],
     "Mama Duck waddles over to Ollie on the bank near x=0.55 and bends her head to his, kindly",
     "Mama Duck holds one wing around Ollie; he snuggles against her with his eyes closed", "Mama Duck comforts Ollie and tucks him under her wing.", None,
     {"mama": ("M_EXPR_KIND", "M_EXPR_KIND"), "ollie": ("O_EXPR_SAD", "O_EXPR_CONTENT")}),
    ("s03_to_the_water", 3, "pond_day_wide", ["mama", D3, "ollie"],
     "Mama Duck walks into the water at the left edge of the pond, the three ducklings and Ollie following in a line along the bank",
     "Mama Duck swims near x=0.40 with the three ducklings and Ollie paddling behind her in a line", "Mama Duck leads her ducklings into the pond for their first swim.", None,
     {"mama": ("M_EXPR_JOY", "M_EXPR_JOY")}),
    ("s03_ollie_glides", 3, "pond_day_wide", ["mama", D3, "ollie"],
     "The three ducklings splash and wobble near x=0.35; Ollie glides smoothly ahead near x=0.60, leaving a neat ripple; Mama Duck watches",
     "Ollie glides near x=0.70, calm and graceful; the ducklings still splash; Mama Duck looks proud", "The ducklings splash clumsily while Ollie glides smoothly ahead.", None,
     {"mama": ("M_EXPR_JOY", "M_EXPR_PROUD"), "ollie": ("O_EXPR_CONTENT", "O_EXPR_CONTENT")}),
    ("s03_honk", 3, "pond_day_wide", ["mama", D3, "ollie"],
     "Ollie on the water near x=0.62 opens his beak in a big honk; the three ducklings turn toward him",
     "The ducklings laugh with their wings over their beaks; Ollie looks down, embarrassed; Mama Duck looks worried", "Ollie honks and the ducklings laugh at him.", None,
     {"ollie": ("O_EXPR_SURPRISED", "O_EXPR_SAD"), "mama": ("M_EXPR_KIND", "M_EXPR_KIND")}),
    ("s03_ollie_alone", 3, "pond_day_ollie_closeup", ["ollie"],
     "Ollie alone among the reeds, head low: brows tilted up, eyes shiny, one tear on his beak",
     "Ollie closes his eyes, a second tear falling, beak closed", "Ollie floats alone in the reeds as two tears fall.", None,
     {"ollie": ("O_EXPR_CRYING", "O_EXPR_CRYING")}),
    ("s04_decision", 4, "pond_evening_ollie_closeup", ["ollie"],
     "Ollie looks out across the pond at sunset, thoughtful and sad: brows drawn together, eyes steady, beak closed",
     "Ollie sets his face with quiet courage: brows level, eyes determined", "Ollie thinks, then makes a brave decision.", None,
     {"ollie": ("O_EXPR_SAD", "O_EXPR_BRAVE")}),
    ("s04_leaves", 4, "reed_path_side", ["ollie"],
     "Ollie waddles along the reedy path near x=0.20, facing right, his head turned back toward the pond's glow at the left",
     "Ollie near x=0.70, facing right, walking on into the dusk", "Ollie looks back once, then waddles away along the reedy path.", None,
     {"ollie": ("O_EXPR_SAD", "O_EXPR_BRAVE")}),
    ("s05_lake", 5, "lake_autumn_wide", ["ollie"],
     "Ollie stands small on the grassy shore at the lower left, looking out over the wide autumn lake",
     "Ollie has stepped to the water's edge, golden leaves floating past him", "Ollie gazes at the great autumn lake and steps to the water's edge.", None,
     {"ollie": ("O_EXPR_WONDER", "O_EXPR_WONDER")}),
    ("s05_ollie_lake", 5, "lake_autumn_ollie_closeup", ["ollie"],
     "Ollie looks around, lonely: brows tilted up, eyes searching, beak closed",
     "Ollie speaks quietly to himself, beak slightly open, eyes lowered", "Ollie looks around, lonely, and wonders aloud.", None,
     {"ollie": ("O_EXPR_SAD", "O_EXPR_SAD")}),
    ("s05_swans_fly", 5, "lake_autumn_wide", ["ollie", "swans*2"],
     "Two white swans fly across the sky from the left near y=0.20, long necks stretched, wings wide; Ollie on the shore looks up",
     "The two swans fly near the right side of the sky; Ollie still looks up, stretching his neck after them", "Two swans fly across the autumn sky while Ollie watches from the shore.", None,
     {"ollie": ("O_EXPR_WONDER", "O_EXPR_WONDER")}),
    ("s05_ollie_watches", 5, "lake_autumn_ollie_closeup", ["ollie"],
     "Ollie gazes up at the sky in wonder: brows raised, eyes wide and shining, beak slightly open",
     "Ollie whispers his wish, eyes still on the sky, a small hopeful smile", "Ollie gazes up in wonder and whispers his wish.", None,
     {"ollie": ("O_EXPR_WONDER", "O_EXPR_WONDER")}),
    ("s06_winter", 6, "river_wide", [], "The empty frozen river in soft falling snow, the burrow glowing at the right",
     "The same scene; a little more snow has fallen", "Snow falls gently on the frozen river.", None, {}),
    ("s06_ollie_cold", 6, "river_wide", ["ollie"],
     "Ollie curls up on the snow bank near x=0.40, head tucked, shivering, snowflakes on his back",
     "Same place; Ollie lifts his head a little, eyes half open, still shivering", "Ollie shivers in the snow and lifts his head weakly.", None,
     {"ollie": ("O_EXPR_SAD", "O_EXPR_SAD")}),
    ("s06_ottie_finds", 6, "river_wide", ["ollie", "ottie"],
     "Ottie pops her head out of the burrow entrance at the right, looking toward Ollie curled in the snow near x=0.40",
     "Ottie has scampered out onto the snow near x=0.58 and leans toward Ollie, one paw held out", "Ottie pops out of her burrow and hurries to Ollie, holding out a paw.", None,
     {"ottie": ("OT_EXPR_CONCERNED", "OT_EXPR_KIND")}),
    ("s06_ottie_closeup", 6, "river_ottie_closeup", ["ottie"],
     "Ottie looks toward the camera with warm concern: brows tilted up, eyes kind, mouth open as she speaks",
     "Ottie laughs kindly, eyes crinkled, a big friendly smile", "Ottie speaks kindly, then laughs warmly.", None,
     {"ottie": ("OT_EXPR_KIND", "OT_EXPR_HAPPY")}),
    ("s06_ollie_shy", 6, "river_ollie_closeup", ["ollie"],
     "Ollie looks up shyly: brows raised a little, eyes wide and unsure, beak slightly open",
     "Ollie's face softens into a small, hopeful smile", "Ollie looks up shyly, then smiles with hope.", None,
     {"ollie": ("O_EXPR_SHY", "O_EXPR_CONTENT")}),
    ("s07_sliding", 7, "river_wide", ["ollie", "ottie"],
     "Ottie slides on her belly across the ice near x=0.35, arms out, laughing; Ollie slides beside her on his big feet near x=0.50, wings spread",
     "Both have slid to near x=0.65, laughing together, Ollie's wings still spread", "Ollie and Ottie slide across the ice together, laughing.", None,
     {"ottie": ("OT_EXPR_HAPPY", "OT_EXPR_HAPPY"), "ollie": ("O_EXPR_HAPPY", "O_EXPR_HAPPY")}),
    ("s07_ollie_grows", 7, "river_wide", ["ollie", "ottie"],
     "Ollie sits on the snow bank near x=0.45 beside Ottie near x=0.58, both watching the snow fall, Ollie stretching his neck upward",
     "Same places; Ollie's neck is stretched tall, his wings opened wide, Ottie looking up at him with a smile", "Ollie stretches his neck and opens his wings as Ottie watches.", None,
     {"ollie": ("O_EXPR_CONTENT", "O_EXPR_WONDER"), "ottie": ("OT_EXPR_HAPPY", "OT_EXPR_HAPPY")}),
    ("s08_spring", 8, "lake_spring_wide", [], "The empty great lake in spring sunshine, blossoms on the trees",
     "The same lake; a few blossoms have drifted onto the water", "Blossoms drift down onto the sparkling spring lake.", None, {}),
    ("s08_goodbye", 8, "river_wide", ["ollie", "ottie"],
     "The snow has nearly melted; Ollie stands near x=0.45 facing Ottie near x=0.60, both smiling, Ollie bowing his head in thanks",
     "Ottie waves one paw; Ollie turns toward the right, wings slightly raised, ready to go", "Ollie thanks Ottie and turns to go as she waves goodbye.", None,
     {"ollie": ("O_EXPR_HAPPY", "O_EXPR_BRAVE"), "ottie": ("OT_EXPR_KIND", "OT_EXPR_HAPPY")}),
    ("s08_flies", 8, "lake_spring_wide", ["ollie_swan"],
     "Ollie the swan flies low over the spring lake from the left near x=0.15, wings wide",
     "Ollie the swan glides down toward the water near x=0.60, wings still wide", "Ollie the swan flies over the lake and glides down toward the water.", None,
     {"ollie_swan": ("OS_EXPR_WONDER", "OS_EXPR_WONDER")}),
    ("s09_swans_lake", 9, "lake_spring_wide", ["swans*2"],
     "Two adult swans glide on the lake near x=0.55 and x=0.68, necks curved gracefully",
     "The two swans turn their heads toward the left, noticing someone arriving", "Two swans glide on the lake and turn their heads.", None, {}),
    ("s09_ollie_nervous", 9, "lake_spring_ollie_closeup", ["ollie_swan"],
     "Ollie the swan looks toward the swans off-screen, nervous: brows tilted up, eyes unsure, beak closed",
     "Ollie the swan takes a small brave breath: brows level, eyes hopeful", "Ollie looks nervous, then gathers his courage.", None,
     {"ollie_swan": ("OS_EXPR_NERVOUS", "OS_EXPR_NERVOUS")}),
    ("s09_ollie_bows", 9, "lake_spring_wide", ["ollie_swan", "swans*2"],
     "Ollie the swan lands softly on the water near x=0.35; the two swans near x=0.55 and x=0.68 look at him",
     "Ollie the swan bows his long neck low toward the water; the two swans glide closer", "Ollie lands on the water and bows his head as the swans come closer.", None,
     {"ollie_swan": ("OS_EXPR_NERVOUS", "OS_EXPR_NERVOUS")}),
    ("s10_reflection", 10, "lake_spring_reflection", ["ollie_swan"],
     "Ollie the swan bows over the still water; his mirror reflection below shows a white swan, both blurred by a small ripple",
     "The ripple has calmed; the reflection is clear: the same white swan looking up at him", "The ripple calms and Ollie sees his own clear reflection.", None,
     {"ollie_swan": ("OS_EXPR_NERVOUS", "OS_EXPR_AMAZED")}),
    ("s10_ollie_amazed", 10, "lake_spring_ollie_closeup", ["ollie_swan"],
     "Ollie the swan is astonished: brows high, eyes wide and shining, beak slightly open",
     "Ollie the swan's astonishment turns into a joyful smile, eyes bright", "Ollie stares in astonishment, then smiles with joy.", None,
     {"ollie_swan": ("OS_EXPR_AMAZED", "OS_EXPR_HAPPY")}),
    ("s10_swan_welcomes", 10, "lake_spring_swan_closeup", ["swans*1"],
     "One adult swan looks kindly toward the camera: brows relaxed, eyes warm, beak closed",
     "The swan speaks a gentle welcome, beak slightly open", "An adult swan smiles kindly and speaks a gentle welcome.", None,
     {"swans": ("S_EXPR_KIND", "S_EXPR_KIND")}),
    ("s10_swim_together", 10, "lake_spring_wide", ["ollie_swan", "swans*2"],
     "Ollie the swan and the two swans swim side by side near x=0.40 to x=0.65, necks curved, all smiling",
     "The three swans swim together toward the right, gliding in a line", "Ollie and the swans swim away together across the lake.", None,
     {"ollie_swan": ("OS_EXPR_HAPPY", "OS_EXPR_HAPPY")}),
    ("s11_arrives_home", 11, "pond_spring_wide", ["mama", D3, "ollie_swan"],
     "Ollie the swan glides down onto the farm pond from the right; Mama Duck and the three ducklings on the bank at the left look up",
     "Ollie the swan floats on the pond near x=0.60; Mama Duck and the ducklings stare at him", "Ollie lands on the farm pond while Mama Duck and the ducklings watch.", None,
     {"mama": ("M_EXPR_SURPRISED", "M_EXPR_SURPRISED")}),
    ("s11_ducklings_amazed", 11, "pond_spring_wide", ["mama", D3, "ollie_swan"],
     "The three ducklings at the water's edge stare up at Ollie the swan, beaks open in amazement; Mama Duck behind them",
     "Mama Duck steps forward to the water's edge, one wing raised to her chest", "The ducklings gape in amazement and Mama Duck steps forward.", None,
     {"mama": ("M_EXPR_SURPRISED", "M_EXPR_JOY")}),
    ("s11_mama_closeup", 11, "pond_spring_mama_closeup", ["mama"],
     "Mama Duck looks up with dawning recognition: brows high, eyes shining, beak open",
     "Mama Duck smiles with proud, tender love, eyes full of happy tears", "Mama Duck recognises Ollie and smiles with tender pride.", None,
     {"mama": ("M_EXPR_SURPRISED", "M_EXPR_PROUD")}),
    ("s11_ollie_closeup", 11, "pond_spring_ollie_closeup", ["ollie_swan"],
     "Ollie the swan looks down warmly toward the camera: brows relaxed, eyes kind, a gentle smile",
     "Ollie the swan speaks kindly, beak slightly open, eyes soft", "Ollie smiles warmly and speaks kindly.", None,
     {"ollie_swan": ("OS_EXPR_HAPPY", "OS_EXPR_KIND")}),
    ("s11_ducklings_sorry", 11, "pond_spring_wide", ["mama", D3, "ollie_swan"],
     "The three ducklings stand at the water's edge with their heads bowed, sorry; Ollie the swan floats close to the bank, bending his neck toward them",
     "Ollie the swan touches his beak gently to the nearest duckling's head; the ducklings smile up at him; Mama Duck watches happily",
     "The ducklings say sorry and Ollie gently forgives them.", None,
     {"ollie_swan": ("OS_EXPR_KIND", "OS_EXPR_KIND"), "mama": ("M_EXPR_PROUD", "M_EXPR_PROUD")}),
    ("s12_family", 12, "pond_spring_wide", ["mama", D3, "ollie_swan", "ottie"],
     "Ollie the swan swims on the pond with the three ducklings riding on his back; Mama Duck swims beside him; Ottie splashes in the water at the right",
     "Everyone splashes and laughs together on the sunny pond", "Everyone splashes and plays together on the sunny pond.", None,
     {"ollie_swan": ("OS_EXPR_HAPPY", "OS_EXPR_HAPPY"), "ottie": ("OT_EXPR_HAPPY", "OT_EXPR_HAPPY"), "mama": ("M_EXPR_JOY", "M_EXPR_JOY")}),
    ("s12_end", 12, "pond_spring_wide", ["mama", D3, "ollie_swan", "ottie"],
     "Ollie the swan, Mama Duck, the three ducklings and Ottie sit together on the grassy bank in the sunshine, all facing the camera and smiling",
     "Same places; they all close their eyes in happy smiles", "The whole family and Ottie sit together, smiling in the sunshine.", None,
     {"ollie_swan": ("OS_EXPR_HAPPY", "OS_EXPR_HAPPY"), "mama": ("M_EXPR_JOY", "M_EXPR_JOY"), "ottie": ("OT_EXPR_HAPPY", "OT_EXPR_HAPPY")}),
]

EXPR = {
    "mama": {"CALM": "calm: brows relaxed, eyelids softly lowered, beak closed in a gentle smile",
             "JOY": "joyful: brows raised, eyes shining, beak closed in a big smile",
             "SURPRISED": "surprised: brows high, eyes round, beak slightly open",
             "KIND": "kind: brows tilted up a little, eyes soft and warm, beak closed in a gentle smile",
             "PROUD": "proud and tender: brows relaxed, eyes shining with happy tears, beak closed in a warm smile"},
    "ollie": {"SHY": "shy: brows raised a little, eyes wide and unsure, beak closed",
              "SAD": "sad: brows tilted up in the middle, eyes lowered and shiny, beak closed",
              "CRYING": "crying softly: brows tilted up, eyes shiny with tears, one tear on his beak",
              "CONTENT": "content: brows relaxed, eyes soft, a small closed smile",
              "SURPRISED": "surprised: brows high, eyes round, beak open",
              "BRAVE": "quietly brave: brows level, eyes determined, beak closed",
              "WONDER": "full of wonder: brows raised, eyes wide and shining, beak slightly open",
              "HAPPY": "happy: brows raised, eyes smiling, beak open in a big smile"},
    "ollie_swan": {"WONDER": "full of wonder: brows raised, eyes wide and shining, beak slightly open",
                   "NERVOUS": "nervous: brows tilted up, eyes unsure, beak closed",
                   "AMAZED": "astonished: brows high, eyes wide and shining, beak slightly open",
                   "HAPPY": "happy: brows raised, eyes bright, a joyful smile",
                   "KIND": "kind: brows relaxed, eyes warm, a gentle smile"},
    "ottie": {"CONCERNED": "concerned: brows tilted up, eyes wide, mouth slightly open",
              "KIND": "kind: brows relaxed, eyes warm, mouth open in a friendly word",
              "HAPPY": "happy: eyes crinkled with laughter, a big open smile"},
    "swans": {"KIND": "kind and welcoming: brows relaxed, eyes warm, beak closed in a gentle smile"},
}
CANON_VIEW = {
    "mama": "a neutral three-quarter view facing left, standing on both webbed feet, wings folded, beak closed in a soft smile, looking at the camera",
    "ducklings": "a neutral three-quarter view facing left of one duckling, standing on both feet, beak closed, looking at the camera",
    "ollie": "a neutral three-quarter view facing left, standing on his big webbed feet, wings folded, beak closed, looking at the camera",
    "ollie_swan": "a neutral three-quarter view facing left, standing on both webbed feet with his neck curved up, wings folded, beak closed, looking at the camera",
    "swans": "a neutral three-quarter view facing left of one adult swan, standing on both feet with its neck curved up, wings folded, looking at the camera",
    "ottie": "a neutral front view, standing upright on her hind feet with her paws together at her chest, tail curled beside her, mouth closed in a smile, looking at the camera",
}
POSE_VIEWS = [
    ("O_SWIM", "ollie", "Ollie swimming, side view facing screen-right: body low in a hint of water at the bottom, neck up, calm. Head size equals the neutral pose.", "Ollie swimming"),
    ("O_WALK_R", "ollie", "Full-body side view facing screen-right, waddling on his big webbed feet, one foot lifted.", "Ollie waddling, facing right"),
    ("O_CURL", "ollie", "Full body curled up on the ground, head tucked against his body, three-quarter view. Head size equals the neutral pose.", "Ollie curled up"),
    ("M_SWIM", "mama", "Mama Duck swimming, side view facing screen-right: body low in a hint of water at the bottom, neck up.", "Mama Duck swimming"),
    ("OS_SWIM", "ollie_swan", "Ollie the swan swimming, side view facing screen-left, neck gracefully curved, wings folded, a hint of water at the bottom.", "Ollie the swan swimming"),
    ("OS_FLY", "ollie_swan", "Ollie the swan flying, side view facing screen-right, wings spread wide, neck stretched forward, feet tucked.", "Ollie the swan flying"),
    ("S_SWIM", "swans", "One adult swan swimming, side view facing screen-left, neck gracefully curved, a hint of water at the bottom.", "an adult swan swimming"),
    ("OT_SLIDE", "ottie", "Ottie sliding on her belly, side view facing screen-right, arms stretched forward, tail out behind, laughing.", "Ottie sliding on her belly"),
]
POSE_RULES = [
    ("ollie", r"ollie[^;.]*\b(glides|paddl|swim|floats)", "O_SWIM", None),
    ("ollie", r"ollie[^;.]*\b(waddles|walking)", "O_WALK_R", None),
    ("ollie", r"ollie[^;.]*\bcurls", "O_CURL", None),
    ("mama", r"mama duck[^;.]*\bswim", "M_SWIM", None),
    ("ollie_swan", r"ollie the swan[^;.]*\bfl(y|ies)", "OS_FLY", None),
    ("ollie_swan", r"ollie the swan[^;.]*\b(swim|floats|lands softly)", "OS_SWIM", None),
    ("swans", r"swans?[^;.]*\b(glide|swim)", "S_SWIM", None),
    ("ottie", r"ottie slides", "OT_SLIDE", None),
]
PORTRAIT_CHARS = ["mama", "ollie", "ollie_swan", "ottie", "swans"]
PROP_BLOCKS = {}
PROP_STATE_PREFIX = ""
PROPS = []
PROP_REF = None
INTRO = ("Fourth story of *Big Lessons, Little Tales*: Hans Christian Andersen's ugly duckling (public domain) for "
         "ages 3 to 7, retold gently: the ducklings' teasing is mild and they say sorry, a kind otter shelters Ollie "
         "through the winter, and Ollie finds both the swans and his first family again. Felt storybook style of the "
         "channel, made with the consistency rules of `docs/creation-rules.md` CR-01 to CR-18.")
ROLES = {"mama": "the mother duck, loving and kind", "ducklings": "Ollie's three yellow duckling siblings; tease a little, later say sorry",
         "ollie": "the 'ugly duckling', a grey cygnet who feels different", "ollie_swan": "Ollie grown up into a white swan (a separate visual state)",
         "swans": "the swan family: two identical adult swans", "ottie": "a kind otter who shelters Ollie through the winter"}
TRAVEL_NOTE = ("Ollie travels away from home left to right (pond → reedy path → lake); the seasons change with the "
               "plates (spring pond, autumn lake, winter river, spring lake and pond).")
STATE_ROWS = [
    "| s01 | spring morning: Mama Duck at the nest; three ducklings hatch, then Ollie from the big egg | eggs → shells |",
    "| s02-s03 | Ollie teased for being different; the swimming lesson on the pond; Ollie alone in the reeds | same |",
    "| s04 | sunset: Ollie leaves along the reedy path | Ollie no longer at the pond |",
    "| s05 | autumn: Ollie alone at the great lake; two swans fly south overhead | same |",
    "| s06-s07 | winter: Ottie shelters Ollie in her burrow; they slide on the ice; Ollie starts to grow | Ollie the cygnet growing |",
    "| s08 | spring: Ollie says goodbye to Ottie and flies (now Ollie the swan) | Ollie the swan from here on |",
    "| s09-s10 | spring lake: the swans; Ollie sees his reflection and is welcomed | same |",
    "| s11-s12 | Ollie the swan visits the farm pond; the ducklings say sorry; everyone plays together, Ottie too | same |",
]
DECISIONS = [
    "- 2026-10-04: owner chose The Ugly Duckling as the fourth story; narration 7 to 10 minutes; narrator: the saved narrator voice for now.",
]
OPEN = [
    "- Names (Ollie, Mama Duck, Ottie) are proposals.",
    "- Ollie has two canonicals: the grey cygnet (scenes 1-7) and the white swan (scenes 8-12); the change happens off-screen over the winter.",
    "- The reflection shot (s10_reflection) asks an image model for a mirror image in water; check that the reflection matches the swan exactly.",
]
