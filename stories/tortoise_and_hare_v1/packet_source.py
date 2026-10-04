"""The Tortoise and the Hare (tortoise_and_hare_v1): story content for the builder.

Everything a prompt says about a character, place or size is defined once here and written into
the story's visual_bible.json; shots only say what is unique to a frame.
"""

SLUG = "tortoise_and_hare_v1"
TITLE = "The Tortoise and the Hare"
MORAL = ("Keep going, step by step, and you can reach places you never thought you could; "
         "and a kind friend cheers for you whether you win or lose.")

# ---------------------------------------------------------------- script
# (scene, speaker, direction, text, coverage shots)
N, H, T, OW, P, B = "NARRATOR", "HATTIE", "TOBY", "OLIVE", "PIP", "BRAMBLE"
WARM = "warm, gentle storyteller for small children, unhurried, smiling"
LINES = [
    # 1 Two neighbours
    (1, N, WARM, "Once upon a time, in a sunny meadow at the edge of the Whispering Wood, lived two neighbours who were as different as can be.", ["s01_meadow"]),
    (1, N, WARM, "Every morning the dew sparkled on the grass, the daisies opened their little white faces, and the birds sang their first songs of the day.", ["s01_meadow"]),
    (1, N, WARM + ", a little bouncy", "Hattie the Hare was quick and bouncy. She could hop over a log before you could even say hop!", ["s01_hattie_bounces"]),
    (1, H, "excited, playful, full of energy, proud but friendly", "Wheee! Look at me! I'm the fastest hopper in the whole wide wood!", ["s01_hattie_bounces"]),
    (1, N, WARM, "Hattie loved to race the wind. She raced the falling leaves, she raced the bumblebees, and she always, always won.", ["s01_hattie_bounces"]),
    (1, N, WARM + ", slowing down", "And Toby the Tortoise was slow and calm. He liked to sit in the warm sun and watch the daisies sway.", ["s01_toby_rests"]),
    (1, T, "slow, calm, kind, a gentle smile in the voice", "Good morning, sunshine. Good morning, daisies. What a lovely day to take my time.", ["s01_toby_rests"]),
    (1, N, WARM, "Toby never hurried. He noticed the ladybirds on the leaves and the shapes of the clouds, and he always took one step, and then another.", ["s01_toby_rests"]),
    # 2 The challenge
    (2, N, WARM, "One bright morning, Hattie came bouncing across the meadow and stopped right next to Toby.", ["s02_hattie_boasts"]),
    (2, H, "bright, teasing but not mean, a little cheeky", "Good morning, Toby! Goodness, you're slow. Do you ever actually get anywhere?", ["s02_hattie_boasts"]),
    (2, T, "calm, steady, patient, not hurt", "I always get where I'm going, Hattie. One step, and then another step.", ["s02_toby_replies"]),
    (2, H, "laughing lightly, playful", "One step at a time? I can do a hundred hops in that time!", ["s02_hattie_boasts"]),
    (2, T, "gentle, thoughtful", "Being fast is a wonderful thing, Hattie. But being fast isn't the only way to get somewhere.", ["s02_toby_replies"]),
    (2, H, "sudden bright idea, excited", "Oh really? I know! Let's have a race! Then everyone will see who is the fastest.", ["s02_challenge"]),
    (2, N, WARM, "Toby thought for a moment. He looked at the long path into the wood, and he looked at Hattie's long, strong legs. Then he smiled a slow, steady smile.", ["s02_toby_thinks"]),
    (2, T, "calm, friendly, quietly confident", "All right, Hattie. Let's race.", ["s02_challenge"]),
    (2, H, "surprised, then delighted", "Really? Hooray! This is going to be the easiest race ever!", ["s02_challenge"]),
    # 3 Ready, steady, go
    (3, N, WARM + ", lively", "News of the race spread through the meadow faster than a breeze.", ["s03_crowd_gathers"]),
    (3, N, WARM, "Pip the Squirrel came scampering down from the trees, and Bramble the Hedgehog came trundling out of the ferns.", ["s03_crowd_gathers"]),
    (3, P, "squeaky, excited, quick", "A race! A race! Hattie against Toby!", ["s03_crowd_gathers"]),
    (3, B, "slow, cosy, a little fussy, kind", "Oh my, oh my. I must find a good place to watch.", ["s03_crowd_gathers"]),
    (3, P, "squeaky, giggling", "Hattie is sure to win. She's the fastest in the wood!", ["s03_crowd_gathers"]),
    (3, B, "cosy, wise for a little one", "Maybe so, Pip. But a race isn't over until it's over.", ["s03_crowd_gathers"]),
    (3, N, WARM, "Wise old Olive the Owl fluffed her feathers and hooted for quiet.", ["s03_olive_announces"]),
    (3, OW, "wise, clear, kind, like a friendly teacher", "The race goes along the forest path, up the hill past the big shady tree, and all the way to the daisy ribbon by the old oak.", ["s03_olive_announces"]),
    (3, OW, "kind, firm", "Remember, racers: stay on the path, be kind, and do your very best.", ["s03_olive_announces"]),
    (3, OW, "clear and exciting, building up", "Racers, take your places. Ready... steady... go!", ["s03_go"]),
    # 4 Off they go
    (4, N, WARM + ", fast and fun", "Whoosh! Hattie shot off like an arrow. All anyone could see was a puff of dust and the tips of her long ears.", ["s04_hattie_zooms"]),
    (4, N, WARM + ", slow and warm", "And Toby? Toby took one careful step. And then another.", ["s04_toby_steps"]),
    (4, P, "squeaky, cheering", "Go, Toby, go!", ["s04_toby_steps"]),
    (4, B, "cheerful, slow", "Good luck, both of you!", ["s04_toby_steps"]),
    # 5 Far ahead
    (5, N, WARM, "Hattie raced along the forest path, past the ferns and the mushrooms and the mossy stones.", ["s04_hattie_zooms"]),
    (5, N, WARM, "After a while, she stopped and looked back. There was no one there at all.", ["s05_hattie_looks_back"]),
    (5, H, "pleased with herself, laughing", "Ha! Toby's so far behind, I can't even see him!", ["s05_hattie_smug"]),
    (5, H, "smug, relaxed", "This race is too easy. I could stop for a snack and still win.", ["s05_hattie_smug"]),
    (5, N, WARM, "Beside the path grew a patch of sweet pink clover, Hattie's very favourite treat.", ["s05_hattie_clover"]),
    (5, H, "happy, munching", "Mmm, yummy! Just one more bite. And maybe one more.", ["s05_hattie_clover"]),
    (5, N, WARM, "One bite became ten bites, and ten bites became a whole tummy full of clover.", ["s05_hattie_clover"]),
    # 6 A little nap
    (6, N, WARM, "At last Hattie hopped on, up the hill. At the top stood a big shady tree, with soft cool grass all around it.", ["s06_hattie_arrives_tree"]),
    (6, H, "sleepy, content, yawning a little", "Mmm, this looks comfy. My tummy is full, and I have plenty of time. I'll rest my eyes for just one minute.", ["s06_hattie_lies_down"]),
    (6, N, WARM + ", soft and sleepy", "Hattie lay down in the shade. She yawned a great big yawn...", ["s06_hattie_lies_down"]),
    (6, N, WARM + ", whispering", "...and before she knew it, she was fast asleep.", ["s06_hattie_sleeps"]),
    # 7 One step, and then another
    (7, N, WARM, "Meanwhile, back on the forest path, Toby kept walking.", ["s07_toby_walks"]),
    (7, T, "steady, rhythmic, calm, almost a little song", "One step, and then another step. One step, and then another step.", ["s07_toby_walks"]),
    (7, N, WARM, "Soon Toby came to the patch of sweet pink clover. It smelled delicious.", ["s07_toby_clover"]),
    (7, T, "tempted, then gently firm", "Oh, that does look tasty. But I'm in a race. I'll come back for some tomorrow.", ["s07_toby_clover"]),
    (7, N, WARM, "And on he went. The sun climbed high in the sky. Toby's legs felt tired, but he did not stop.", ["s07_toby_determined"]),
    (7, T, "singing softly, slow and cheerful", "Slow and steady, step by step, I'm not fast, but I'm not finished yet.", ["s07_toby_song"]),
    (7, N, WARM, "Pip had raced ahead along the branches to see how Toby was doing.", ["s07_pip_cheers"]),
    (7, P, "squeaky, encouraging", "You can do it, Toby! Keep going!", ["s07_pip_cheers"]),
    (7, T, "warm, grateful, determined", "Thank you, Pip. I'm not fast, but I'm not stopping.", ["s07_toby_determined"]),
    # 8 Past the sleeping hare
    (8, N, WARM, "Then came the hill. It was steep, and it was long, and for a little tortoise it looked like a mountain.", ["s08_toby_climbs"]),
    (8, T, "puffing a little, but determined", "Phew. That's a big hill. But a big hill is just a lot of little steps.", ["s08_toby_tired"]),
    (8, N, WARM, "Up, up the hill went Toby, slow and steady.", ["s08_toby_climbs"]),
    (8, N, WARM, "At the top, he saw Hattie, curled up asleep under the big shady tree.", ["s08_toby_climbs"]),
    (8, T, "whispering softly, kind", "Sleep well, Hattie. I'll keep going.", ["s08_toby_whispers"]),
    (8, N, WARM + ", quiet", "And so, very quietly, so as not to wake her, Toby walked on past.", ["s08_toby_passes"]),
    # 9 Hattie wakes up
    (9, N, WARM, "The shadows grew long, and the air grew cool. Hattie's nose twitched. Her eyes popped open.", ["s09_hattie_wakes"]),
    (9, H, "waking, confused, then worried", "Oh! How long did I sleep? The sun is nearly going down!", ["s09_hattie_wakes"]),
    (9, N, WARM + ", a little suspense, never scary", "She jumped up and looked down the hill. Far away, near the old oak, a little round shape was moving towards the daisy ribbon.", ["s09_hattie_sees"]),
    (9, H, "alarmed but funny, not frightened", "Toby?! Oh no, oh no, oh no!", ["s09_hattie_sees"]),
    (9, N, WARM + ", fast", "Hattie ran faster than she had ever run before. She ran so fast her ears flew out behind her like two flags.", ["s09_hattie_dashes"]),
    # 10 The finish
    (10, N, WARM, "At the old oak, everyone was waiting.", ["s10_crowd_waits"]),
    (10, B, "excited, slow", "Look! Here comes someone!", ["s10_crowd_waits"]),
    (10, P, "squeaky, overjoyed", "It's Toby! It's Toby!", ["s10_toby_crosses"]),
    (10, N, WARM + ", building joy", "Step by step, Toby walked right up to the daisy ribbon... and through it!", ["s10_toby_crosses"]),
    (10, OW, "proud, joyful announcement", "The winner is... Toby the Tortoise!", ["s10_olive_winner"]),
    (10, N, WARM, "Everyone cheered. Pip turned a somersault, and Bramble clapped his little paws.", ["s10_crowd_cheers"]),
    (10, N, WARM, "A moment later, Hattie came racing in, puffing and panting.", ["s10_hattie_arrives"]),
    # 11 Friends
    (11, H, "out of breath, surprised, honest", "Toby... you won.", ["s11_hattie_admits"]),
    (11, H, "a little embarrassed, sincere", "I was so sure I was the fastest that I stopped for clover, and then I stopped for a nap. I stopped trying. That wasn't very clever, was it?", ["s11_hattie_admits"]),
    (11, T, "kind, generous, warm", "You are very fast, Hattie. Faster than anyone I know.", ["s11_toby_kind"]),
    (11, T, "gentle, simple", "I just kept going, one step at a time.", ["s11_toby_kind"]),
    (11, H, "sincere, sorry, then warm", "I'm sorry I teased you. Congratulations, Toby. You really earned it.", ["s11_hattie_admits"]),
    (11, OW, "wise, warm, like a grandparent", "Well said, both of you. Being fast is a gift, and so is being steady. But the very best gift is being a good friend.", ["s11_olive_wise"]),
    (11, T, "friendly, inviting", "Thank you, Hattie. Next time, shall we walk the path together? You can show me all the things you see when you're zooming by.", ["s11_friends"]),
    (11, H, "happy, touched", "I'd like that. I'd like that very much. And you can show me all the things I missed!", ["s11_friends"]),
    # 12 Slow and steady
    (12, N, WARM, "And from that day on, Hattie and Toby often walked the forest path together, Hattie hopping slowly, and Toby stepping steadily beside her.", ["s12_walk_together"]),
    (12, N, WARM, "Toby showed Hattie the ladybirds and the cloud shapes, and Hattie showed Toby the best view from the top of the hill.", ["s12_hilltop_view"]),
    (12, N, WARM, "And yes, they shared the sweet pink clover too.", ["s12_hilltop_view"]),
    (12, N, WARM, "Hattie learned that being fast is wonderful, but it is no good if you stop trying.", ["s12_walk_together"]),
    (12, N, WARM, "And Toby showed everyone that when you keep going, step by step, you can reach places you never thought you could.", ["s12_friends_end"]),
    (12, N, WARM + ", the moral, slow and clear", "Slow and steady wins the race.", ["s12_friends_end"]),
    (12, N, WARM + ", closing", "The end.", ["s12_friends_end"]),
]
SCENE_TITLES = {1: "Two neighbours", 2: "The challenge", 3: "Ready, steady, go!", 4: "Off they go",
                5: "Far ahead", 6: "A little nap", 7: "One step, and then another", 8: "Past the sleeping hare",
                9: "Hattie wakes up", 10: "The finish", 11: "Friends", 12: "Slow and steady"}

# ---------------------------------------------------------------- characters (design specs until the canonicals are approved)
CHARACTERS = {
    "toby": {
        "name": "Toby", "folder": "Toby", "canon_id": "TOBY_CANON",
        "identity": (
            "Toby is one small, rounded young wool-felt tortoise who walks on four short sturdy legs. His high domed "
            "shell is warm olive-green felt (#7A8B3C) divided into large honey-tan hexagonal plates (#C9A15A), each "
            "outlined with darker olive-green stitching (#55652A), with a narrow cream-yellow rim (#E6D49A) along the "
            "lower edge of the shell. His head, neck, legs and short pointed tail are soft sage-green felt (#A9B97A); "
            "his chin and throat are pale cream (#EEEACB). His round head is about one third as long as his shell, "
            "with a short blunt snout, two tiny dark nostril dots and a gentle wide mouth line. Two large round glossy "
            "eyes, each about a quarter of the head width: warm dark-brown irises (#5A3A22), black pupils, one white "
            "catch-light at upper right, ivory sclera (#F2EEE2), softly rounded upper lids that make him look calm. "
            "Two short soft olive-green brows (#55652A). Four short legs with three rounded cream toenails each "
            "(#EFE6CF). He has no ears, no hair, no teeth and no clothing. His shell is about 1.6 times as long as he "
            "is tall at the shell top, and his head sits out in front on a short neck. Fine looped felt fibres and "
            "small visible stitches. These intrinsic colours and this mid brightness stay identical in every image; "
            "scene light only tints and shades them. His pose, facing and expression are the ones this prompt states."),
        "sheet": "one small rounded olive-green felt tortoise with a domed shell of honey-tan hexagonal plates, sage-green head and legs, cream chin, two brown eyes, four short legs and a short pointed tail",
        "mouth": ("When Toby's mouth opens, it is a small rounded opening with a dark warm-brown interior and a soft pink "
                  "tongue; he has no teeth."),
        "palette": {"shell": "#7A8B3C", "plates": "#C9A15A", "seams": "#55652A", "rim": "#E6D49A", "skin": "#A9B97A",
                    "chin": "#EEEACB", "iris": "#5A3A22", "sclera": "#F2EEE2", "toenails": "#EFE6CF"},
        "proportions": {"shell_length_to_height": 1.6, "head_length_to_shell_length": 0.33, "eye_to_head_width": 0.25},
        "checklist": ["one tortoise, four legs, one short pointed tail", "domed olive-green shell with large honey-tan hexagonal plates",
                      "darker olive stitching around every plate", "cream-yellow shell rim", "sage-green head, neck and legs",
                      "pale cream chin and throat", "two eyes with warm dark-brown irises and ivory sclera", "two short olive brows",
                      "no ears, no hair, no teeth", "three cream toenails per foot", "head about one third of the shell length",
                      "calm, softly rounded upper eyelids", "felt texture with visible stitches", "colours not shifted by scene light"],
        "drift_phrases": ["turtle", "flipper", "flippers", "spiky shell", "green eyes"],
    },
    "hattie": {
        "name": "Hattie", "folder": "Hattie", "canon_id": "HATTIE_CANON",
        "identity": (
            "Hattie is one tall, slim young wool-felt hare who stands, walks and runs upright on two long hind legs. "
            "Her body felt is warm caramel-tan (#C9955B), with a lighter wheat-beige mask around the eyes (#E2BE8A), a "
            "long oval cream belly and chest (#F3E3C6) and one small round white cotton tail (#FAF6EE) at the lower "
            "back. Two very long upright ears, each as long as her head and neck together, with dusty-pink inner felt "
            "(#E8A3A0) and dark chocolate-brown tips (#4E3426). Her oval head has a short rounded muzzle with two cream "
            "muzzle pads (#F5E8D2), a small rose-brown nose (#A86A5E), a small mouth line and four fine pale whiskers "
            "(#F0E2CC) on each side. Two large almond-shaped glossy eyes, each about a fifth of the head width: "
            "amber-brown irises (#8A5A22), black pupils, one white catch-light at upper right, ivory sclera (#F4ECE4). "
            "Two short dark-brown brows (#5A3A22). Two slim arms with small rounded paws; two long hind feet with three "
            "toes each, each foot about as long as her shin. Her ears make up about two fifths of her height from feet "
            "to ear tips; her head is about one sixth. Fine looped felt fibres and small visible stitches. These "
            "intrinsic colours and this mid brightness stay identical in every image; scene light only tints and "
            "shades them. Her pose, facing and expression are the ones this prompt states."),
        "sheet": "one tall slim caramel-tan felt hare standing upright, very long ears with pink insides and chocolate-brown tips, cream belly, two amber-brown eyes, a rose-brown nose and one small round white tail",
        "mouth": ("When Hattie's mouth opens, it is a small rounded opening with a dark warm-brown interior, a soft pink "
                  "tongue and two small ivory upper front teeth just showing."),
        "palette": {"body": "#C9955B", "mask": "#E2BE8A", "belly": "#F3E3C6", "tail": "#FAF6EE", "inner_ear": "#E8A3A0",
                    "ear_tips": "#4E3426", "muzzle": "#F5E8D2", "nose": "#A86A5E", "iris": "#8A5A22", "brows": "#5A3A22"},
        "proportions": {"ears_to_height": 0.4, "head_to_height": 0.17, "eye_to_head_width": 0.2},
        "checklist": ["one hare standing upright, two arms, two long hind feet", "two very long upright ears with pink insides and chocolate-brown tips",
                      "caramel-tan body with a lighter wheat-beige eye mask", "long oval cream belly", "one small round white cotton tail",
                      "two almond eyes with amber-brown irises and ivory sclera", "two short dark-brown brows", "small rose-brown nose",
                      "four pale whiskers on each side", "cream muzzle pads", "three toes on each long hind foot",
                      "ears about two fifths of her height", "felt texture with visible stitches", "colours not shifted by scene light"],
        "drift_phrases": ["rabbit", "bunny", "floppy ears", "lop", "grey hare"],
    },
    "olive": {
        "name": "Olive", "folder": "Olive", "canon_id": "OLIVE_CANON",
        "identity": (
            "Olive is one small, round, wise wool-felt tawny owl who stands upright on two feet. Her body feathers are "
            "warm tawny-brown felt (#9A6A3C) with small cream speckles (#EAD9B8), and her round chest is lighter "
            "buff-cream (#E3CBA0) with soft brown chevron stitches. Her round face is a pale buff-cream disc (#E8D2A8) "
            "edged with a thin chocolate-brown rim (#5A3A22), with two short soft feather tufts on top of the head. "
            "Two very large round glossy eyes, each about a third of the face width: golden-amber irises (#D69A2A), "
            "black pupils, one white catch-light at upper right, ivory sclera only at the edges (#F4ECE0); two small "
            "chocolate-brown brow feathers above them; a small hooked dark-brown beak (#4A3426) between and below the "
            "eyes. Two folded wings with darker brown bars (#6E4A2A), and two short feet with three ochre-tan toes "
            "each (#C9A15A). She is about as wide as she is tall, without the tufts. Fine looped felt fibres and small "
            "visible stitches. These intrinsic colours and this mid brightness stay identical in every image; scene "
            "light only tints and shades them. Her pose, facing and expression are the ones this prompt states."),
        "sheet": "one small round tawny-brown felt owl with cream speckles, a buff-cream face disc, two big golden-amber eyes, a small brown beak and two folded wings",
        "mouth": ("When Olive speaks, her small hooked beak opens slightly to show a dark warm-brown inside; she has no "
                  "teeth and no lips."),
        "palette": {"feathers": "#9A6A3C", "speckles": "#EAD9B8", "chest": "#E3CBA0", "face_disc": "#E8D2A8",
                    "rim": "#5A3A22", "iris": "#D69A2A", "beak": "#4A3426", "wing_bars": "#6E4A2A", "toes": "#C9A15A"},
        "proportions": {"width_to_height": 1.0, "eye_to_face_width": 0.33},
        "checklist": ["one owl, two folded wings, two feet", "tawny-brown body with cream speckles", "buff-cream round face disc with a thin brown rim",
                      "two short feather tufts on the head", "two big eyes with golden-amber irises", "small hooked dark-brown beak",
                      "lighter chest with chevron stitches", "three toes on each foot", "about as wide as tall",
                      "felt texture with visible stitches", "colours not shifted by scene light"],
        "drift_phrases": ["spectacles", "glasses", "horned owl", "snowy owl"],
    },
    "pip": {
        "name": "Pip", "folder": "Pip", "canon_id": "PIP_CANON",
        "identity": (
            "Pip is one small, quick young wool-felt red squirrel who stands upright on two hind feet. His body felt "
            "is warm rust-orange (#B5562A), with a cream belly and chest (#F1DFC2) and one big bushy tail (#C2622E) "
            "that curls up behind him almost as tall as he is. Two small rounded ears with short darker rust-orange "
            "tips (#8E3F1E). His round head has a short muzzle with cream cheeks (#F1DFC2), a tiny dark-brown nose "
            "(#4A2E22), a small mouth line and three fine pale whiskers (#F0E2CC) on each side. Two large round "
            "glossy eyes: dark-brown irises (#4A2E22), black pupils, one white catch-light at upper right, ivory "
            "sclera (#F2EEE2); two short dark-brown brows. Two small arms with tiny paws and two hind feet with "
            "four toes each. Fine looped felt fibres and small visible stitches. These intrinsic colours and this mid "
            "brightness stay identical in every image; scene light only tints and shades them. His pose, facing and "
            "expression are the ones this prompt states."),
        "sheet": "one small rust-orange felt squirrel with a cream belly, a big bushy curled tail, small rounded ears and two dark-brown eyes",
        "mouth": "When Pip's mouth opens, it is a tiny rounded opening with a dark warm-brown interior and two small ivory front teeth.",
        "palette": {"body": "#B5562A", "belly": "#F1DFC2", "tail": "#C2622E", "ear_tips": "#8E3F1E", "nose": "#4A2E22"},
        "proportions": {"tail_to_height": 0.9},
        "checklist": ["one squirrel standing upright", "rust-orange body, cream belly and cheeks", "one big bushy curled tail",
                      "two small rounded ears", "two dark-brown eyes", "three whiskers on each side", "felt texture"],
        "drift_phrases": ["chipmunk", "grey squirrel", "stripes"],
    },
    "bramble": {
        "name": "Bramble", "folder": "Bramble", "canon_id": "BRAMBLE_CANON",
        "identity": (
            "Bramble is one small, round, cosy young wool-felt hedgehog who walks on four short legs and can stand up "
            "on two. His back is covered with soft rounded felt spines in chestnut-brown (#6E4A30) with cream tips "
            "(#EADBC0), like a round brush; they are soft and friendly, never sharp. His face, tummy and legs are "
            "pale biscuit-beige felt (#E7CBA4). His pointed little snout ends in a round black nose (#2A1E18). Two "
            "small round ears (#D8B88E). Two small round glossy eyes: dark-brown irises (#3E2A1E), black pupils, one "
            "white catch-light, ivory sclera (#F2EEE2); two short brown brows. A small smiling mouth line. Four "
            "short legs with tiny paws. Fine looped felt fibres and small visible stitches. These intrinsic colours "
            "and this mid brightness stay identical in every image; scene light only tints and shades them. His pose, "
            "facing and expression are the ones this prompt states."),
        "sheet": "one small round felt hedgehog with soft chestnut-brown cream-tipped spines, a biscuit-beige face and tummy, a black nose and two small brown eyes",
        "mouth": "When Bramble's mouth opens, it is a small rounded opening with a dark warm-brown interior and a soft pink tongue.",
        "palette": {"spines": "#6E4A30", "tips": "#EADBC0", "face": "#E7CBA4", "nose": "#2A1E18"},
        "proportions": {},
        "checklist": ["one hedgehog", "soft rounded chestnut-brown spines with cream tips", "biscuit-beige face and tummy",
                      "round black nose", "two small brown eyes", "two small round ears", "felt texture"],
        "drift_phrases": ["porcupine", "quills", "sharp spikes"],
    },
}
ORDER = ["hattie", "toby", "olive", "pip", "bramble"]   # identity order in a prompt (tallest first)

CAST_SCALE_BLOCK = (
    "Relative size (fixed for the whole story, the same at the same distance from the camera): Hattie standing, from "
    "feet to ear tips, is the tallest; Toby's shell top reaches about one third of Hattie's height and his shell is "
    "about half her height long; Olive standing is about two fifths of Hattie's height; Pip standing, to his ear tips, "
    "is about one third of Hattie's height, his tail reaching about half; Bramble is about one quarter of Hattie's "
    "height. Sitting, lying or running changes a silhouette but never the size of a head, shell, ear or limb.")
CAST_SCALE = {
    "rule": "At equal depth, with Hattie's height from feet to ear tips as 1.0: Toby's shell top 0.33 and shell length 0.50; Olive 0.40; Pip 0.33 to the ear tips (tail top 0.50); Bramble 0.25.",
    "anchor_record": "LINEUP",
    "status": "design targets; measure them on the approved LINEUP image and update every setup's sizes",
}

# ---------------------------------------------------------------- locations (one locked plate each)
LOC = {
    "meadow_morning": dict(folder="meadow", stem="meadow_morning", label="the sunny meadow in morning light",
        description=("A sunny felt meadow at the edge of a wood: a wide flat lane of short green grass fills the lower half, "
                     "with clumps of white daisies; a mossy tree stump stands at the left; a line of small round grey "
                     "pebbles crosses the grass as the start line; the forest path opens between two trees at the far right; "
                     "rounded felt trees and a soft blue sky behind."),
        landmarks=["the forest path entrance between two trees at the far right (x 0.85-0.98)", "the mossy stump at the left (x 0.08-0.22, top near y=0.55)",
                   "the pebble start line across the grass (y 0.80-0.83, x 0.25-0.70)", "daisy clumps at the lower right and lower left corners",
                   "the grass lane where characters stand (y 0.70-0.90)"],
        light="Fresh morning sunlight from the upper left; soft shadows to the right.",
        ambient="Grass tips and daisies sway gently in a light breeze; leaves flutter; the stump, trees and pebbles stay fixed."),
    "path_morning": dict(folder="forest_path", stem="path_morning", label="the forest path in late-morning light",
        description=("A side view of a winding felt forest path: a flat earth lane crosses the whole frame left to right in "
                     "the lower third, with ferns, red-capped mushrooms, a patch of clover and mossy stones in front of it and tall "
                     "felt trees with soft green canopies behind it."),
        landmarks=["the earth lane across the frame (y 0.72-0.86)", "a cluster of red-capped mushrooms at the lower left (x 0.08-0.18)",
                   "a patch of clover with small pink flowers beside the lane at the lower right (x 0.62-0.78, y 0.84-0.94)",
                   "a mossy stone at the lower right (x 0.80-0.92, y 0.80-0.92)", "a large trunk behind the lane at the centre (x 0.46-0.54)",
                   "ferns along the bottom edge"],
        light="Bright late-morning sunlight from the upper left through the leaves, dappled light on the lane.",
        ambient="Fern tips and leaves move gently; sun dapples drift slightly; trunks, stones and mushrooms stay fixed."),
    "path_sunset": dict(folder="forest_path", stem="path_sunset", derived_from="path_morning", label="the forest path at sunset",
        description=("The same side view of the forest path as the late-morning plate, with every tree, stone, fern and "
                     "mushroom and the clover patch in exactly the same place, in warm golden sunset light."),
        landmarks=["the earth lane across the frame (y 0.72-0.86)", "a cluster of red-capped mushrooms at the lower left (x 0.08-0.18)",
                   "a patch of clover with small pink flowers beside the lane at the lower right (x 0.62-0.78, y 0.84-0.94)",
                   "a mossy stone at the lower right (x 0.80-0.92, y 0.80-0.92)", "a large trunk behind the lane at the centre (x 0.46-0.54)"],
        light="Low warm golden sunset light from the right; long soft shadows to the left; a pink-orange glow between the trunks.",
        ambient="Leaves move gently; warm light flickers softly; trunks, stones and mushrooms stay fixed."),
    "hill_noon": dict(folder="hilltop", stem="hill_noon", label="the hilltop with the big shady tree at midday",
        description=("A grassy felt hilltop: one big round shady tree stands left of centre with a thick trunk and a wide "
                     "canopy, soft cool grass beneath it; the path comes up the slope from the lower left and continues "
                     "over the crest at the right; far below at the right, a small old oak and a tiny daisy ribbon "
                     "are just visible in the distance."),
        landmarks=["the big tree trunk left of centre (x 0.30-0.40, base near y=0.70)", "its canopy across the upper left (x 0.05-0.65, y 0.00-0.45)",
                   "the path rising from the lower left to the crest at the right (y 0.72-0.88)", "the shady grass under the tree (x 0.15-0.55, y 0.68-0.82)",
                   "the distant old oak at the right edge (x 0.85-0.95, y 0.45-0.55)"],
        light="Bright midday sunlight from above; a deep cool shadow under the tree.",
        ambient="Canopy leaves and grass sway gently; the shadow stays still; trunk and path stay fixed."),
    "hill_afternoon": dict(folder="hilltop", stem="hill_afternoon", derived_from="hill_noon", label="the hilltop with the big shady tree in late afternoon",
        description=("The same hilltop as the midday plate, with the tree, path and distant oak in exactly the same "
                     "places, in late-afternoon light."),
        landmarks=["the big tree trunk left of centre (x 0.30-0.40, base near y=0.70)", "the path rising from the lower left to the crest at the right (y 0.72-0.88)",
                   "the distant old oak at the right edge (x 0.85-0.95, y 0.45-0.55)"],
        light="Warm late-afternoon light from the low right; long shadows to the left.",
        ambient="Leaves and grass sway gently; trunk and path stay fixed."),
    "finish_afternoon": dict(folder="finish", stem="finish_afternoon", label="the old oak clearing with the finish ribbon in late afternoon",
        description=("A round grassy felt clearing in front of a wide old oak: the path enters from the left; two small "
                     "upright sticks stand in the grass at the centre, one at each side of the path, ready for the finish "
                     "ribbon; ferns and flowers around the edges."),
        landmarks=["the old oak trunk at the right (x 0.70-0.92, base near y=0.62)", "the path entering from the left edge (y 0.74-0.88)",
                   "the left finish stick at x=0.42 and the right finish stick at x=0.58, both from y=0.62 to y=0.82",
                   "ferns at the lower left and lower right corners"],
        light="Warm golden late-afternoon light from the left; soft long shadows to the right.",
        ambient="Ferns, grass and leaves sway gently; sticks, oak and path stay fixed."),
}

CLOSE_TREATMENT = ("The background is the same place, very strongly blurred into soft shapes of colour, as with a "
                   "portrait lens at f/1.4; nothing stands in front of the character except what this frame states. "
                   "The blurred place:")


def closeup(loc, who, label, top_word="ear tips", top=0.05):
    name = CHARACTERS[who]["name"]
    return dict(location=loc, framing="dialogue_close_up", label=label,
                camera=(f"Close-up, 16:9: {name}'s head and upper chest are centred, {top_word} near y={top:.2f} and chin "
                        f"near y=0.70, facing the camera."),
                background_treatment=CLOSE_TREATMENT)


WIDE = "Fixed normal-height wide camera, 16:9, exactly the framing of the locked plate."
SIDE = "Fixed normal-height side camera, 16:9, exactly the framing of the locked plate; characters travel left to right along the lane."
# design-target sizes (fractions of the frame height), from CAST_SCALE with Hattie = 0.42 in wides
SZ = {
    "hattie": "Hattie standing measures about 0.42 of the frame height from feet to ear tips, her feet on the ground line.",
    "toby": "Toby measures about 0.14 of the frame height to the top of his shell and about 0.21 of the frame height long.",
    "olive": "Olive standing measures about 0.17 of the frame height.",
    "pip": "Pip standing measures about 0.14 of the frame height to his ear tips, his tail reaching about 0.21.",
    "bramble": "Bramble measures about 0.10 of the frame height.",
}
REL = ("At the same distance from the camera, Toby's shell top reaches about one third of Hattie's height; every "
       "character keeps the story's size lineup.")
SETUPS = {
    "meadow_plate": dict(location="meadow_morning", framing="empty_plate", label="the empty meadow in morning light", camera=WIDE),
    "meadow_wide": dict(location="meadow_morning", framing="scene_wide", label="a wide shot of the sunny meadow in morning light",
                        camera=WIDE + " The characters stand on the grass lane between y=0.80 and y=0.88.", size=dict(SZ), relation=REL),
    "meadow_hattie_closeup": closeup("meadow_morning", "hattie", "a close-up of Hattie in the meadow", "ear tips", 0.02),
    "meadow_toby_closeup": closeup("meadow_morning", "toby", "a close-up of Toby in the meadow", "the top of his shell", 0.12),
    "meadow_olive_closeup": closeup("meadow_morning", "olive", "a close-up of Olive on her stump in the meadow", "the top of her head", 0.08),
    "path_side": dict(location="path_morning", framing="scene_wide", label="a side-on wide shot of the forest path in late-morning light",
                      camera=SIDE + " Feet and shells rest on the lane near y=0.84.",
                      size={"hattie": "Hattie standing or running measures about 0.42 of the frame height from feet to ear tips.",
                            "toby": SZ["toby"], "pip": SZ["pip"]}, relation=REL),
    "path_hattie_closeup": closeup("path_morning", "hattie", "a close-up of Hattie on the forest path", "ear tips", 0.02),
    "path_toby_closeup": closeup("path_morning", "toby", "a close-up of Toby on the forest path", "the top of his shell", 0.12),
    "hill_wide": dict(location="hill_noon", framing="scene_wide", label="a wide shot of the hilltop with the big shady tree at midday",
                      camera=WIDE + " Characters stand on the path or the shady grass near y=0.80.",
                      size={"hattie": "Hattie standing measures about 0.38 of the frame height from feet to ear tips; lying down asleep, she is about 0.42 of the frame width long.",
                            "toby": "Toby measures about 0.13 of the frame height to the top of his shell and about 0.19 of the frame height long."},
                      relation=REL),
    "hill_hattie_closeup": closeup("hill_noon", "hattie", "a close-up of Hattie under the shady tree", "ear tips", 0.02),
    "hill_toby_closeup": closeup("hill_noon", "toby", "a close-up of Toby on the hilltop", "the top of his shell", 0.12),
    "hill_late_wide": dict(location="hill_afternoon", framing="scene_wide", label="a wide shot of the hilltop in late afternoon",
                           camera=WIDE + " Characters stand on the path or the shady grass near y=0.80.",
                           size={"hattie": "Hattie standing measures about 0.38 of the frame height from feet to ear tips; lying down, she is about 0.42 of the frame width long; sitting, she keeps the same head and ear size.",
                                 "toby": "Toby measures about 0.13 of the frame height to the top of his shell and about 0.19 of the frame height long."},
                           relation=REL),
    "hill_late_hattie_closeup": closeup("hill_afternoon", "hattie", "a close-up of Hattie on the hilltop in late afternoon", "ear tips", 0.02),
    "finish_wide": dict(location="finish_afternoon", framing="scene_wide", label="a wide shot of the old oak clearing with the finish ribbon",
                        camera=WIDE + " The characters stand on the grass near y=0.84.", size=dict(SZ), relation=REL),
    "finish_hattie_closeup": closeup("finish_afternoon", "hattie", "a close-up of Hattie at the finish", "ear tips", 0.02),
    "finish_olive_closeup": closeup("finish_afternoon", "olive", "a close-up of Olive at the finish", "the top of her head", 0.08),
    "finish_toby_closeup": closeup("finish_afternoon", "toby", "a close-up of Toby at the finish", "the top of his shell", 0.12),
    "path_sunset_side": dict(location="path_sunset", framing="scene_wide", label="a side-on wide shot of the forest path at sunset",
                             camera=SIDE + " Feet and shells rest on the lane near y=0.84.",
                             size={"hattie": SZ["hattie"], "toby": SZ["toby"]}, relation=REL),
}

RIBBON_OBJECT = ("The finish ribbon: one daisy chain of small white felt daisies with yellow centres on a thin green "
                 "felt stem, tied between the two finish sticks at about two thirds of their height.")
RIBBON_WORLD = {
    "tied": RIBBON_OBJECT + " It hangs across the path, whole and unbroken.",
    "parted": RIBBON_OBJECT + " It has just parted in the middle where Toby walked through; its two halves hang from the sticks.",
    "down": RIBBON_OBJECT + " Its two parted halves hang from the sticks after Toby walked through it.",
}

# ---------------------------------------------------------------- shots
# id: (scene, setup, cast, start frame, end frame, video action, ribbon state or None, expressions {char: (start, end)})
SHOTS = [
    ("s01_meadow", 1, "meadow_plate", [], "The empty meadow in fresh morning light, daisies open in the grass",
     "The same empty meadow; a light breeze has bent the daisies slightly", "A gentle breeze moves the grass and daisies; nothing else moves.", None, {}),
    ("s01_hattie_bounces", 1, "meadow_wide", ["hattie"],
     "Hattie bounds in from the left in a big upright hop, both long hind feet off the ground near x=0.25, ears streaming back, arms out, laughing with a wide open smile",
     "Hattie lands near x=0.45 on both long hind feet, standing tall and proud, arms raised in joy, wide happy smile, ears upright",
     "Hattie bounds from the left to the centre of the meadow in one big upright hop and lands proudly.", None,
     {"hattie": ("H_EXPR_PROUD", "H_EXPR_PROUD")}),
    ("s01_toby_rests", 1, "meadow_wide", ["toby"],
     "Toby rests on the grass near x=0.62, facing left in three-quarter view, head out, eyes half closed in the sun, a calm small smile",
     "Same place and pose; Toby has lifted his head a little and opened his eyes, looking up at the sky with a calm small smile",
     "Toby slowly lifts his head and opens his eyes, enjoying the sunshine.", None,
     {"toby": ("T_EXPR_CALM", "T_EXPR_CALM")}),
    ("s02_hattie_boasts", 2, "meadow_hattie_closeup", ["hattie"],
     "Hattie looks down toward the camera with a teasing grin: brows raised, eyes bright, mouth closed in a wide cheeky smile",
     "Hattie laughs: eyes squeezed half closed with joy, brows up, mouth open in a light laugh",
     "Hattie grins and laughs lightly, her ears bobbing a little.", None,
     {"hattie": ("H_EXPR_CHEEKY", "H_EXPR_CHEEKY")}),
    ("s02_toby_replies", 2, "meadow_toby_closeup", ["toby"],
     "Toby looks up toward the camera, calm and patient: brows relaxed, eyes soft and steady, mouth closed in a small gentle smile",
     "Toby smiles a slow, steady smile: brows relaxed, eyes warm, the mouth line widening slightly",
     "Toby's small smile slowly widens into a steady, friendly smile.", None,
     {"toby": ("T_EXPR_CALM", "T_EXPR_KIND")}),
    ("s02_toby_thinks", 2, "meadow_toby_closeup", ["toby"],
     "Toby looks off to the right toward the forest path, thinking: brows slightly drawn together, eyes looking to the side, mouth closed in a flat line",
     "Toby looks back toward the camera with a slow, steady smile: brows relaxed, eyes warm",
     "Toby looks toward the path, thinks, then smiles slowly.", None, {"toby": ("T_EXPR_THINKING", "T_EXPR_KIND")}),
    ("s02_challenge", 2, "meadow_wide", ["hattie", "toby"],
     "Hattie stands at the left near x=0.38 facing right, leaning toward Toby with one paw pointing toward the forest path at the right, excited grin; Toby rests near x=0.60 facing left, looking up at her calmly",
     "Same places; Hattie bounces on her toes with both paws clenched in excitement; Toby nods with a small steady smile",
     "Hattie points and bounces with excitement; Toby gives one slow nod.", None,
     {"hattie": ("H_EXPR_CHEEKY", "H_EXPR_PROUD"), "toby": ("T_EXPR_CALM", "T_EXPR_KIND")}),
    ("s03_crowd_gathers", 3, "meadow_wide", ["hattie", "toby", "olive", "pip", "bramble"],
     "Olive stands on top of the mossy stump at the left; Pip stands on the grass near x=0.30 waving both paws, Bramble near x=0.40 shuffling in; Hattie near x=0.56 and Toby near x=0.66 behind the pebble start line, both facing left toward Olive",
     "Same places; Pip hops up with both paws raised, Bramble has settled near x=0.40 and looks on happily, Hattie and Toby still at the start line",
     "Pip waves and hops with excitement while Bramble shuffles into place next to him.", None,
     {"hattie": ("H_EXPR_PROUD", "H_EXPR_PROUD"), "toby": ("T_EXPR_CALM", "T_EXPR_CALM")}),
    ("s03_olive_announces", 3, "meadow_olive_closeup", ["olive"],
     "Olive on her stump looks at the camera with a wise, kind face: brows level, big eyes steady, beak closed",
     "Olive lifts one wing like a teacher pointing the way, eyes bright, beak slightly open as she announces",
     "Olive raises one wing and announces the race.", None,
     {"olive": ("O_EXPR_WISE", "O_EXPR_ANNOUNCE")}),
    ("s03_go", 3, "meadow_wide", ["hattie", "toby", "olive", "pip", "bramble"],
     "Hattie crouches behind the pebble start line near x=0.58, ready to spring, ears back, facing right toward the forest path; Toby stands beside her near x=0.48, facing right; Olive on the stump at the left with one wing raised; Pip near x=0.30 and Bramble near x=0.40 watch from the grass",
     "Hattie is mid-leap off the line toward the right, already near x=0.86; Toby has taken his first small step over the pebbles near x=0.51; Olive's wing is down; Pip and Bramble cheer with their paws raised",
     "Olive drops her wing; Hattie springs off toward the forest path while Toby takes his first slow step.", None,
     {"hattie": ("H_EXPR_PROUD", "H_EXPR_PROUD"), "toby": ("T_EXPR_DETERMINED", "T_EXPR_DETERMINED")}),
    ("s04_hattie_zooms", 4, "path_side", ["hattie"],
     "Hattie runs upright at full speed near x=0.15 on the lane, long hind feet stretched in a big stride, ears streaming back, delighted grin",
     "Hattie is near x=0.85 in the same running stride, about to leave the frame at the right",
     "Hattie races along the lane from left to right in big upright bounds.", None,
     {"hattie": ("H_EXPR_PROUD", "H_EXPR_PROUD")}),
    ("s04_toby_steps", 4, "meadow_wide", ["toby", "olive", "pip", "bramble"],
     "Toby has just crossed the pebble start line near x=0.62, facing right, one front foot forward; Olive on the stump at the left; Pip near x=0.30 and Bramble near x=0.40 cheering with their paws raised",
     "Toby is near x=0.67, one step further toward the forest path; Pip jumps as he cheers, Olive and Bramble watch happily",
     "Toby takes one slow, careful step toward the forest path; Pip jumps and cheers.", None,
     {"toby": ("T_EXPR_DETERMINED", "T_EXPR_DETERMINED")}),
    ("s05_hattie_looks_back", 5, "path_side", ["hattie"],
     "Hattie stands near x=0.70 on the lane, having stopped, body facing right and head turned back over her shoulder to look left along the empty path",
     "Same place; Hattie has turned fully to look back left along the empty path, one paw shading her eyes",
     "Hattie stops, turns and peers back along the empty path.", None,
     {"hattie": ("H_EXPR_PROUD", "H_EXPR_SMUG")}),
    ("s05_hattie_smug", 5, "path_hattie_closeup", ["hattie"],
     "Hattie smiles smugly: one brow raised, eyes half lowered, mouth closed in a satisfied grin",
     "Hattie gives a little laugh: brows up, eyes squeezed with amusement, mouth slightly open",
     "Hattie grins and laughs to herself.", None, {"hattie": ("H_EXPR_SMUG", "H_EXPR_CHEEKY")}),
    ("s05_hattie_clover", 5, "path_side", ["hattie"],
     "Hattie sits on the lane near x=0.70 beside the clover patch, holding a sprig of clover in both paws at her mouth, eyes half closed with delight",
     "Same place; Hattie's cheeks are round and full, a few bare clover stems on the ground beside her, and she pats her tummy with one paw",
     "Hattie munches clover happily and pats her full tummy.", None, {"hattie": ("H_EXPR_HAPPY", "H_EXPR_SLEEPY")}),
    ("s06_hattie_arrives_tree", 6, "hill_wide", ["hattie"],
     "Hattie hops up the path near x=0.20, standing tall, looking toward the big shady tree with interest",
     "Hattie stands in the shady grass under the tree near x=0.42, looking at the soft grass with a pleased smile",
     "Hattie hops up the hill and stops in the cool shade under the big tree.", None,
     {"hattie": ("H_EXPR_PROUD", "H_EXPR_SLEEPY")}),
    ("s06_hattie_lies_down", 6, "hill_wide", ["hattie"],
     "Hattie sits in the shady grass under the tree near x=0.42, stretching her arms up in a big yawn, eyes closed",
     "Hattie lies on her side in the shady grass near x=0.42, curled up, head resting on her arm, ears lying back along her body, eyes closed",
     "Hattie yawns, stretches and lies down in the shade.", None,
     {"hattie": ("H_EXPR_SLEEPY", "H_EXPR_ASLEEP")}),
    ("s06_hattie_sleeps", 6, "hill_hattie_closeup", ["hattie"],
     "Hattie's sleepy face lying on the grass: eyelids almost closed, brows relaxed, mouth closed in a tiny content smile",
     "Hattie is fast asleep: eyes fully closed, brows relaxed, mouth closed and soft",
     "Hattie's eyes slowly close and she falls fast asleep.", None,
     {"hattie": ("H_EXPR_SLEEPY", "H_EXPR_ASLEEP")}),
    ("s07_toby_walks", 7, "path_side", ["toby"],
     "Toby walks along the lane near x=0.20, facing right, one front foot lifted mid-step, calm and steady",
     "Toby near x=0.32, the other front foot lifted mid-step, the same calm face",
     "Toby walks slowly and steadily from left to right.", None, {"toby": ("T_EXPR_DETERMINED", "T_EXPR_DETERMINED")}),
    ("s07_toby_song", 7, "path_toby_closeup", ["toby"],
     "Toby walks and sings softly: eyes half closed with contentment, brows relaxed, mouth slightly open in a little song",
     "Toby keeps walking, mouth closed in a small cheerful smile, eyes looking ahead",
     "Toby sings softly to himself as he walks.", None, {"toby": ("T_EXPR_CALM", "T_EXPR_HAPPY")}),
    ("s07_toby_clover", 7, "path_side", ["toby"],
     "Toby has stopped on the lane near x=0.56 beside the clover patch, head turned down toward the clover, sniffing it",
     "Toby has turned his head back to face right along the lane and lifts one front foot to walk on, a small determined smile",
     "Toby sniffs the clover, then turns away and walks on.", None, {"toby": ("T_EXPR_CALM", "T_EXPR_DETERMINED")}),
    ("s07_pip_cheers", 7, "path_side", ["toby", "pip"],
     "Toby walks near x=0.62 facing right, just past the clover patch; Pip stands on the mossy stone at the lower right, waving both paws at Toby",
     "Toby near x=0.70, still walking; Pip jumps on the stone with both paws up, cheering",
     "Pip cheers and jumps while Toby keeps walking.", None, {"toby": ("T_EXPR_KIND", "T_EXPR_KIND")}),
    ("s07_toby_determined", 7, "path_toby_closeup", ["toby"],
     "Toby looks ahead with gentle determination: brows slightly lowered and level, eyes steady and focused, mouth closed in a firm small smile",
     "Toby looks up toward the camera with warm thanks: brows lifted slightly, eyes soft, a small grateful smile",
     "Toby keeps his steady look, then glances up with a grateful smile.", None,
     {"toby": ("T_EXPR_DETERMINED", "T_EXPR_KIND")}),
    ("s08_toby_tired", 8, "hill_toby_closeup", ["toby"],
     "Toby looks up the steep hill, a little tired: brows tilted up in the middle, eyes looking upward, mouth slightly open as he puffs",
     "Toby sets his face with gentle determination: brows level, eyes steady, a small firm smile",
     "Toby puffs, looks up the hill, then sets his face and carries on.", None, {"toby": ("T_EXPR_TIRED", "T_EXPR_DETERMINED")}),
    ("s08_toby_climbs", 8, "hill_wide", ["hattie", "toby"],
     "Hattie lies asleep on her side in the shady grass under the tree near x=0.42, curled up, ears back, eyes closed; Toby walks up the path at the lower left near x=0.15, facing right",
     "Same Hattie, still asleep; Toby has come up the path to near x=0.28, looking at Hattie",
     "Toby climbs the last steps of the hill and sees Hattie asleep under the tree.", None,
     {"toby": ("T_EXPR_CALM", "T_EXPR_KIND")}),
    ("s08_toby_whispers", 8, "hill_toby_closeup", ["toby"],
     "Toby looks toward the sleeping Hattie off-screen to the left with a soft, kind face: brows relaxed, eyes gentle, mouth closed",
     "Toby whispers with a tiny smile: eyes gentle, mouth slightly open",
     "Toby looks at his sleeping friend and whispers softly.", None, {"toby": ("T_EXPR_KIND", "T_EXPR_KIND")}),
    ("s08_toby_passes", 8, "hill_wide", ["hattie", "toby"],
     "Hattie still asleep under the tree near x=0.42; Toby walks quietly along the path near x=0.55, facing right",
     "Hattie still asleep; Toby near x=0.72, walking toward the crest at the right",
     "Toby tiptoes past the sleeping Hattie toward the crest of the hill.", None, {"toby": ("T_EXPR_KIND", "T_EXPR_DETERMINED")}),
    ("s09_hattie_wakes", 9, "hill_late_hattie_closeup", ["hattie"],
     "Hattie asleep, lying on the grass, eyes closed; her nose twitches",
     "Hattie's eyes have popped wide open in surprise: brows high, eyes round, mouth a small open O",
     "Hattie's nose twitches and her eyes pop open.", None, {"hattie": ("H_EXPR_ASLEEP", "H_EXPR_STARTLED")}),
    ("s09_hattie_sees", 9, "hill_late_wide", ["hattie"],
     "Hattie stands up quickly in the grass under the tree near x=0.42, looking toward the distant oak at the far right, ears straight up",
     "Same place; Hattie has both paws on her cheeks in dismay, ears straight up, staring at the distant oak",
     "Hattie jumps up, stares into the distance and clasps her cheeks.", None, {"hattie": ("H_EXPR_STARTLED", "H_EXPR_STARTLED")}),
    ("s09_hattie_dashes", 9, "hill_late_wide", ["hattie"],
     "Hattie springs off from near x=0.45 in a huge upright leap toward the right, ears streaming back",
     "Hattie is near x=0.85, running flat out down the path over the crest at the right",
     "Hattie dashes off down the hill as fast as she can.", None, {"hattie": ("H_EXPR_STARTLED", "H_EXPR_DETERMINED")}),
    ("s10_crowd_waits", 10, "finish_wide", ["olive", "pip", "bramble"],
     "Olive stands at the right finish stick, Pip near x=0.66 and Bramble near x=0.74 on the grass, all looking left toward the path",
     "Same places; Bramble points one paw toward the path at the left, Pip leans forward on tiptoe",
     "Bramble spots someone coming and points; Pip leans forward to see.", "tied", {}),
    ("s10_toby_crosses", 10, "finish_wide", ["toby", "olive", "pip", "bramble"],
     "Toby walks up the path toward the ribbon near x=0.38, facing right, his head just touching the ribbon; Olive, Pip and Bramble cheer on the right",
     "Toby has walked through the ribbon and stands near x=0.52; Olive raises both wings, Pip jumps with joy, Bramble claps",
     "Toby walks through the daisy ribbon and everyone cheers.", "tied->parted", {"toby": ("T_EXPR_DETERMINED", "T_EXPR_HAPPY")}),
    ("s10_olive_winner", 10, "finish_olive_closeup", ["olive"],
     "Olive stands proudly with both wings lifted high, eyes bright, beak open in a joyful announcement",
     "Olive beams: eyes smiling and narrowed with joy, beak closed, wings still raised",
     "Olive raises her wings high and announces the winner.", None, {"olive": ("O_EXPR_ANNOUNCE", "O_EXPR_HAPPY")}),
    ("s10_crowd_cheers", 10, "finish_wide", ["toby", "olive", "pip", "bramble"],
     "Toby stands near x=0.52 beyond the parted ribbon, smiling; Pip near x=0.66 is upside down in the middle of a somersault; Bramble near x=0.74 claps his paws; Olive by the right finish stick with wings raised",
     "Pip has landed on his feet with both paws up; Bramble still clapping; Toby smiling widely",
     "Pip turns a somersault and Bramble claps while Toby smiles.", "parted", {"toby": ("T_EXPR_HAPPY", "T_EXPR_HAPPY")}),
    ("s10_hattie_arrives", 10, "finish_wide", ["hattie", "toby", "olive", "pip", "bramble"],
     "Hattie skids in from the left near x=0.20, ears flying, puffing; Toby stands near x=0.52 beyond the parted ribbon; Olive, Pip and Bramble at the right",
     "Hattie stands near x=0.32 bent forward with her paws on her knees, panting; everyone else in the same places",
     "Hattie races in and stops, puffing and panting.", "parted", {"hattie": ("H_EXPR_STARTLED", "H_EXPR_EMBARRASSED"), "toby": ("T_EXPR_HAPPY", "T_EXPR_KIND")}),
    ("s11_hattie_admits", 11, "finish_hattie_closeup", ["hattie"],
     "Hattie looks down toward the camera, a little embarrassed: brows tilted up in the middle, eyes lowered, mouth closed in a shy small line",
     "Hattie looks up sincerely with a warm, sorry smile: brows relaxed, eyes soft and honest",
     "Hattie looks down, embarrassed, then looks up with a sincere smile.", "down",
     {"hattie": ("H_EXPR_EMBARRASSED", "H_EXPR_SINCERE")}),
    ("s11_toby_kind", 11, "finish_toby_closeup", ["toby"],
     "Toby looks up toward the camera with a kind, generous face: brows relaxed, eyes warm, mouth closed in a gentle smile",
     "Toby smiles more widely, eyes crinkling with friendliness",
     "Toby's gentle smile grows warmer.", "down", {"toby": ("T_EXPR_KIND", "T_EXPR_HAPPY")}),
    ("s11_olive_wise", 11, "finish_olive_closeup", ["olive"],
     "Olive looks at the camera with a wise, warm face: brows level, eyes soft, beak closed",
     "Olive speaks gently with her beak slightly open, eyes kind",
     "Olive speaks a few wise, warm words.", "down", {"olive": ("O_EXPR_WISE", "O_EXPR_WISE")}),
    ("s11_friends", 11, "finish_wide", ["hattie", "toby", "olive", "pip", "bramble"],
     "Hattie kneels on the grass near x=0.42 to be closer to Toby, reaching out one paw; Toby near x=0.52 looks up at her; Olive, Pip and Bramble watch from the right",
     "Hattie's paw rests gently on top of Toby's shell; both smile happily; Olive, Pip and Bramble smile",
     "Hattie kneels down and gently places her paw on Toby's shell; both smile.", "down",
     {"hattie": ("H_EXPR_SINCERE", "H_EXPR_HAPPY"), "toby": ("T_EXPR_KIND", "T_EXPR_HAPPY")}),
    ("s12_walk_together", 12, "path_sunset_side", ["hattie", "toby"],
     "Hattie walks slowly upright near x=0.25 facing right beside Toby near x=0.35, both smiling, Hattie looking down at Toby",
     "Hattie near x=0.40 and Toby near x=0.50, walking side by side, Hattie pointing at something in the trees",
     "Hattie and Toby walk slowly along the path together, chatting happily.", None,
     {"hattie": ("H_EXPR_HAPPY", "H_EXPR_HAPPY"), "toby": ("T_EXPR_HAPPY", "T_EXPR_HAPPY")}),
    ("s12_hilltop_view", 12, "hill_late_wide", ["hattie", "toby"],
     "Another day: Hattie sits in the grass at the hilltop near x=0.55 beside Toby near x=0.66, both facing right toward the view, Hattie pointing into the distance",
     "Same places; they look at each other and laugh, a few sprigs of clover on the grass between them",
     "Hattie points out the view and the two friends laugh together.", None,
     {"hattie": ("H_EXPR_HAPPY", "H_EXPR_HAPPY"), "toby": ("T_EXPR_HAPPY", "T_EXPR_HAPPY")}),
    ("s12_friends_end", 12, "path_sunset_side", ["hattie", "toby"],
     "Hattie sits on the lane near x=0.45 beside Toby near x=0.55, both facing the camera with warm smiles in the golden light",
     "Same places; both have closed their eyes in happy smiles",
     "Hattie and Toby sit together and smile in the sunset.", None,
     {"hattie": ("H_EXPR_HAPPY", "H_EXPR_HAPPY"), "toby": ("T_EXPR_HAPPY", "T_EXPR_HAPPY")}),
]

# ---------------------------------------------------------------- expression studies (edit of the closed-mouth portrait)
EXPR = {
    "hattie": {"PROUD": "proud and happy: brows raised, eyes bright and wide, a big closed smile",
               "CHEEKY": "cheeky and teasing: one brow raised, eyes bright, a wide lopsided closed grin",
               "SMUG": "smug: one brow raised, eyelids half lowered, a satisfied closed grin",
               "SLEEPY": "sleepy: eyelids drooping half closed, brows relaxed, a small content closed smile",
               "ASLEEP": "fast asleep: eyes fully closed, brows relaxed, mouth closed and soft",
               "STARTLED": "startled: brows high, eyes round and wide, mouth a small open O",
               "DETERMINED": "determined: brows lowered and level, eyes focused, mouth closed in a firm line",
               "EMBARRASSED": "embarrassed: brows tilted up in the middle, eyes looking down, mouth a small shy closed line",
               "SINCERE": "sincere and sorry: brows relaxed and slightly raised, eyes soft and honest, a small warm closed smile",
               "HAPPY": "happy: brows relaxed, eyes smiling and slightly narrowed, a wide closed smile"},
    "toby": {"THINKING": "thinking: brows slightly drawn together, eyes looking to one side, mouth closed in a flat line",
             "TIRED": "a little tired: brows tilted up in the middle, eyes looking upward, mouth slightly open as he puffs",
             "CALM": "calm: brows relaxed, eyelids softly half lowered, a small closed smile",
             "KIND": "kind: brows relaxed and slightly raised, eyes warm and soft, a gentle closed smile",
             "DETERMINED": "gently determined: brows slightly lowered and level, eyes steady and focused, a firm small closed smile",
             "HAPPY": "happy: brows raised a little, eyes crinkled with joy, a wide closed smile"},
    "olive": {"WISE": "wise and kind: brows level, big eyes steady and calm, beak closed",
              "ANNOUNCE": "announcing: brows raised, eyes bright, beak slightly open",
              "HAPPY": "happy: eyes smiling and narrowed with joy, beak closed"},
}
PREFIX = {"hattie": "H", "toby": "T", "olive": "O", "pip": "P", "bramble": "B"}

# ---------------------------------------------------------------- story-specific builder settings
CANON_VIEW = {
    "hattie": "a neutral front view, standing upright with both arms resting at her sides, ears upright, mouth closed in a soft neutral smile, looking at the camera",
    "toby": "a neutral three-quarter view facing left, standing on all four legs with his head out, mouth closed in a soft neutral smile, looking at the camera",
    "olive": "a neutral front view, standing upright on both feet with wings folded, beak closed, looking at the camera",
    "pip": "a neutral front view, standing upright with both paws at his chest and his tail curled up behind him, mouth closed in a soft smile, looking at the camera",
    "bramble": "a neutral three-quarter view facing left, standing on all four legs, mouth closed in a soft smile, looking at the camera"}
POSE_VIEWS = [
    ("H_SIDE_R", "hattie", "Full-body side view facing screen-right, standing upright, arms relaxed, ears upright, mouth closed.", "Hattie's side view facing right"),
    ("H_RUN_R", "hattie", "Full-body running pose facing screen-right: upright torso leaning slightly forward, long hind legs in a big mid-stride with one foot on the ground, arms swinging, ears streaming back. Head size equals the neutral pose.", "Hattie running, facing right"),
    ("H_ASLEEP", "hattie", "Full body lying asleep on her side in three-quarter view, curled up, head resting on one arm, both long ears lying back along her body, eyes closed, mouth closed. Head and ears keep the neutral size.", "Hattie lying asleep"),
    ("T_SIDE_R", "toby", "Full-body side view facing screen-right, walking: one front foot lifted mid-step, head out on his neck, mouth closed. The shell keeps exactly its canonical size and plate pattern.", "Toby walking, facing right"),
]
# (character, regex on the frame text, pose record, setups where it applies or None for all); first match wins per character
POSE_RULES = [
    ("hattie", r"hattie[^;.]*\b(lies|lying|asleep)", "H_ASLEEP", None),
    ("hattie", r"hattie[^;.]*\b(runs|running|leap|bounds|springs|races|skids|dashes)", "H_RUN_R", None),
    ("hattie", r".", "H_SIDE_R", ("path_side", "path_sunset_side")),
    ("toby", r"toby[^;.]*\b(walks|walking|step)", "T_SIDE_R", None),
]
PORTRAIT_CHARS = ["hattie", "toby", "olive"]
LINEUP_SIZE = "Hattie measures 0.75 of the frame height from feet to ear tips; every other character follows the size lineup above."
FINAL_CHECK = None   # None: the generic check (each visible character exactly once)
PROP_BLOCKS = {"ribbon_object": RIBBON_OBJECT, **{f"ribbon_{k}": v for k, v in RIBBON_WORLD.items()}}
PROP_STATE_PREFIX = "ribbon_"
PROPS = [("PROP_RIBBON", "prop_ribbon", "the finish ribbon",
          "{{block:ribbon_object}} Show it tied between its two sticks.")]
COUNTS = {}          # character -> number of identical members (a flock); default 1
INTRO = ("Second story of *Big Lessons, Little Tales*: Aesop's tortoise and hare for ages 3 to 7, in the felt "
         "stop-motion style of the channel, made with the consistency rules learnt on The Lion and the Mouse "
         "(`docs/creation-rules.md` CR-01 to CR-18).")
ROLES = {"hattie": "the hare, fast and proud, learns not to stop trying", "toby": "the tortoise, slow, calm and kind, wins by keeping going",
         "olive": "the owl, wise race starter", "pip": "the squirrel, excited cheerleader", "bramble": "the hedgehog, cosy spectator"}
TRAVEL_NOTE = ("Travel is always left to right (meadow → forest path → hilltop → finish), so screen direction holds "
               "across cuts.")
STATE_ROWS = [
    "| s01-s02 | Hattie and Toby in the meadow; the others not yet there | start line of pebbles in the meadow; finish ribbon tied at the old oak (unseen) |",
    "| s03 | everyone in the meadow: Olive on her stump, Pip and Bramble watching, racers at the start line | same |",
    "| s03_go / s04 | Hattie gone along the forest path; Toby just past the start line; Olive, Pip, Bramble stay in the meadow | same |",
    "| s05 | Hattie far ahead on the forest path, eating clover beside the path | some clover eaten (bare stems) |",
    "| s06 | Hattie asleep under the big shady tree on the hilltop (midday) | same |",
    "| s07 | Toby on the forest path, past the clover without stopping; Pip has run ahead along the trees to cheer him, then returns to the finish | same |",
    "| s08 | Toby climbs the hill, passes the sleeping Hattie and goes over the crest | same |",
    "| s09 | late afternoon: Hattie wakes and dashes after Toby | same |",
    "| s10 | Olive, Pip and Bramble waiting at the finish; Toby walks through the ribbon; Hattie arrives just after | ribbon tied → parted in the middle, both halves hang from the sticks |",
    "| s11 | everyone at the finish; Hattie kneels, paw on Toby's shell | ribbon parted |",
    "| s12 | another day, then sunset: Hattie and Toby on the hilltop and walking the forest path together | no ribbon |"]
PROP_REF = "PROP_RIBBON"
DECISIONS = [
    "- 2026-10-04: names approved: Hattie (hare), Toby (tortoise), Olive (owl), Pip (squirrel), Bramble (hedgehog).",
    "- 2026-10-04: cast of five approved, including the start and finish scenes with all five at once (the hardest frames for image models; check counts carefully).",
    "- 2026-10-04: narration 7 to 10 minutes; the script was expanded to about 9 minutes.",
    "- 2026-10-04: narrator: reuse the saved narrator voice for now (`voice/narrators/moonlight_storyteller_1`, the default of `voice/narrate_scenes.py`); character voices are decided later.",
]
REVISION = "tortoise_and_hare_v1-2026-10-04"
