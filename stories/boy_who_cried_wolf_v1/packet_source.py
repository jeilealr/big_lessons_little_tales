"""The Boy Who Cried Wolf (boy_who_cried_wolf_v1): story content for build_story.py."""

SLUG = "boy_who_cried_wolf_v1"
TITLE = "The Boy Who Cried Wolf"
MORAL = ("Always tell the truth, about big things and little things, so that people can believe you when it "
         "matters most; and when you make a mistake, saying sorry and telling the truth is the first step back.")

N, F, R, B, L = "NARRATOR", "FINN", "ROSIE", "BEN", "LENA"
WARM = "warm, gentle storyteller for small children, unhurried, smiling"
LINES = [
    # 1 The village
    (1, N, WARM, "Once upon a time, in a little village tucked between green hills, lived a boy called Finn.", ["s01_village"]),
    (1, N, WARM, "Finn lived with his Grandma Rosie, who baked the warmest, softest bread in the whole village.", ["s01_village_life"]),
    (1, N, WARM, "Every morning the village woke up slowly. Farmer Ben fed his hens, Grandma Rosie opened her bakery, and Finn's friend Lena skipped across the square.", ["s01_village_life"]),
    (1, N, WARM, "And every morning, Finn had a very important job.", ["s01_village_life"]),
    (1, R, "warm, loving grandmother", "Good morning, Finn. Are you ready to look after the sheep today?", ["s01_rosie_reminds"]),
    (1, F, "bright, eager, about eight years old", "Yes, Grandma! I'll take them up the hill to the sweet green grass.", ["s01_finn_promises"]),
    (1, R, "warm, then serious and clear", "Good boy. And remember: if a wolf ever comes, you shout wolf as loud as you can, and we will all come running to help.", ["s01_rosie_reminds"]),
    (1, F, "cheerful, a promise", "I'll remember, Grandma.", ["s01_finn_promises"]),
    # 2 On the hill
    (2, N, WARM, "So Finn led the sheep up the winding path to the top of the hill. There were five fluffy sheep, and one little lamb called Daisy, who had a white heart on her nose.", ["s01_finn_leaves", "s02_flock_arrives"]),
    (2, F, "counting happily, sing-song", "One, two, three, four, five sheep... and Daisy makes six. Everybody's here!", ["s02_counting"]),
    (2, N, WARM, "Daisy was Finn's favourite. She followed him everywhere and nuzzled his hand.", ["s02_daisy_nuzzles"]),
    (2, N, WARM + ", lazy and slow", "The sheep munched the grass. Munch, munch, munch. The clouds drifted by. The sun climbed higher.", ["s02_daisy_nuzzles"]),
    (2, F, "bored, sighing, a little whiny", "Oh, this is so boring. Nothing ever happens up here.", ["s02_finn_bored"]),
    (2, N, WARM, "Finn sat on the big grey rock and sighed. Then he had an idea. It was not a very good idea.", ["s02_finn_bored"]),
    (2, F, "mischievous, whispering to himself", "I know! I'll play a trick. That will make things exciting!", ["s02_finn_bored"]),
    # 3 The first trick
    (3, F, "shouting loudly, pretending to be scared", "Wolf! Wolf! A wolf is chasing the sheep!", ["s03_finn_shouts"]),
    (3, N, WARM + ", quick", "Down in the village, everyone stopped what they were doing, and they ran up the hill path as fast as they could.", ["s03_villagers_run"]),
    (3, N, WARM, "But when they reached the top, there was no wolf at all. Just the sheep, munching grass, and Finn, rolling on the grass with laughter.", ["s03_no_wolf"]),
    (3, F, "laughing, cheeky", "Ha ha! There's no wolf! I tricked you!", ["s03_no_wolf"]),
    (3, B, "big, deep, kind but cross", "Finn, that's not funny. We left our work to help you.", ["s03_ben_cross"]),
    (3, R, "gentle, serious, disappointed", "A shout for help is not a joke, Finn. Please don't do that again.", ["s03_rosie_serious"]),
    (3, N, WARM, "The villagers walked back down the hill, shaking their heads.", ["s03_no_wolf"]),
    # 4 The second trick
    (4, N, WARM, "The next day, Finn was on the hill again. And again, he felt bored.", ["s04_finn_again"]),
    (4, F, "mischievous, giggling", "Last time was so funny. I'll do it one more time.", ["s04_finn_again"]),
    (4, F, "shouting, fake panic", "Wolf! Wolf! Help, help, the wolf is here!", ["s04_finn_again"]),
    (4, N, WARM, "Once again, the villagers ran up the hill, puffing and panting.", ["s04_villagers_run"]),
    (4, N, WARM, "And once again, there was no wolf. Only Finn, giggling behind the big grey rock.", ["s04_finn_giggles"]),
    (4, L, "a girl of nine, upset, hurt", "Finn! You scared us! I thought the sheep were in danger!", ["s04_lena_upset"]),
    (4, B, "slow, serious, not shouting", "Finn, if you keep crying wolf when there is no wolf, nobody will believe you when there really is one.", ["s04_ben_warns"]),
    (4, N, WARM + ", quiet", "The villagers went home, and this time they were not just cross. They were sad.", ["s04_villagers_leave"]),
    (4, N, WARM, "Finn watched them go. For a moment, his tummy felt a little funny, but he shrugged and looked away.", ["s04_villagers_leave"]),
    # 5 The real wolf
    (5, N, WARM, "That evening, as the sun began to set and the sky turned orange and pink, something moved at the edge of the dark woods.", ["s05_wolf_appears"]),
    (5, N, WARM + ", a little suspense, never scary", "It was a wolf. A real one. He was long and grey, with a big bushy tail and a very hungry tummy.", ["s05_wolf_appears"]),
    (5, N, WARM, "The wolf crept closer, licking his lips and looking at the fluffy sheep.", ["s05_wolf_creeps"]),
    (5, F, "frightened, a whisper", "Oh no. Oh no! That's a real wolf!", ["s05_finn_sees"]),
    # 6 Nobody comes
    (6, F, "shouting with all his might, truly scared, begging", "Wolf! Wolf! Please help! There really is a wolf this time!", ["s06_finn_cries_wolf"]),
    (6, N, WARM, "Down in the village, the villagers heard Finn shouting.", ["s06_village_hears"]),
    (6, B, "tired, shaking his head", "Not again. That boy is playing another trick.", ["s06_village_hears"]),
    (6, L, "unsure, worried", "Should we go, Grandma Rosie?", ["s06_village_hears"]),
    (6, R, "sad, torn", "I don't know, Lena. I want to believe him. But he has fooled us twice.", ["s06_rosie_doubts"]),
    (6, N, WARM + ", sad and slow", "And so, nobody came.", ["s06_rosie_doubts"]),
    # 7 The bell
    (7, N, WARM + ", fast, never scary", "The wolf leapt toward the flock. The sheep bleated and scattered in every direction, running into the woods to hide.", ["s07_sheep_scatter"]),
    (7, N, WARM, "Finn was frightened, but he was brave. He ran to the old bell on the hill and rang it with all his might.", ["s07_finn_rings_bell"]),
    (7, N, "playful sound words, ringing and loud", "Clang! Clang! Clang!", ["s07_finn_rings_bell"]),
    (7, N, WARM + ", relieved", "The loud clanging startled the wolf. He tucked his tail between his legs and ran back into the woods, far, far away.", ["s07_wolf_runs"]),
    # 8 The empty hill
    (8, N, WARM + ", quiet", "The wolf was gone. But so were the sheep.", ["s08_empty_hill"]),
    (8, F, "calling, worried", "Daisy? Daisy! Where are you? Where is everybody?", ["s08_empty_hill"]),
    (8, N, WARM + ", tender", "The hill was empty and quiet. Finn sat down on the grass, and big tears rolled down his cheeks.", ["s08_finn_cries"]),
    (8, F, "crying softly, sorry", "This is all my fault. If I hadn't told those fibs, everyone would have come.", ["s08_finn_cries"]),
    # 9 The truth
    (9, N, WARM, "Finn ran all the way down to the village as fast as his legs could carry him.", ["s09_finn_runs_home"]),
    (9, F, "breathless, upset, honest", "Grandma! The wolf came, a real wolf! I rang the bell and he ran away, but the sheep ran into the woods, and Daisy is lost!", ["s09_finn_tells"]),
    (9, B, "doubtful, gentle", "Is this another trick, Finn?", ["s09_finn_tells"]),
    (9, N, WARM, "Grandma Rosie looked at Finn's face. She saw his real tears, and she knelt down beside him.", ["s09_rosie_kneels"]),
    (9, F, "sincere, sorry, through tears", "It's not a trick. I'm so sorry I told fibs before. I won't ever do it again. This time, it's true.", ["s09_finn_sorry"]),
    (9, R, "warm, decisive, kind", "I believe you, Finn. Come on, everyone. Let's find those sheep.", ["s09_rosie_believes"]),
    # 10 The search
    (10, N, WARM, "So the whole village went out to the edge of the woods, just as the first stars began to twinkle.", ["s10_search"]),
    (10, N, WARM, "They searched behind the bushes and under the ferns, calling softly.", ["s10_search"]),
    (10, L, "excited, happy", "Here's one! And another!", ["s10_found_sheep"]),
    (10, B, "pleased, deep", "Three more over here!", ["s10_found_sheep"]),
    (10, N, WARM, "One, two, three, four, five sheep were found. But where was Daisy?", ["s10_found_sheep"]),
    (10, F, "calling, hopeful", "Daisy! Daisy, where are you?", ["s10_daisy_found"]),
    (10, N, WARM + ", soft", "Then, from under a big leafy bush, came a tiny sound. Baa.", ["s10_daisy_found"]),
    (10, F, "overjoyed, relieved", "Daisy! There you are!", ["s10_daisy_found"]),
    (10, N, WARM, "Finn hugged Daisy tight, and Daisy nuzzled his cheek.", ["s10_hug"]),
    # 11 Trust
    (11, N, WARM, "Back home, Grandma Rosie sat with Finn on the step of the little bakery, with Daisy curled up at his feet.", ["s11_together"]),
    (11, R, "wise, gentle, like a bedtime talk", "Finn, trust is like a tower of blocks. Every time you tell the truth, you add a block, and the tower grows tall and strong.", ["s11_rosie_tower"]),
    (11, R, "gentle, honest", "But every fib knocks some blocks down. And it takes a long, long time to build the tower up again.", ["s11_rosie_tower"]),
    (11, F, "small voice, thoughtful", "I knocked my tower down, didn't I?", ["s11_finn_understands"]),
    (11, R, "kind, encouraging", "A little. But you told the truth tonight, and that was a very good block to start with.", ["s11_rosie_tower"]),
    (11, F, "determined, hopeful", "Then I'll build it up again. One true word at a time.", ["s11_finn_understands"]),
    # 12 One true word at a time
    (12, N, WARM, "From that day on, Finn always told the truth, about big things and little things.", ["s12_morning_hill"]),
    (12, N, WARM, "Each morning he led the sheep up the hill, and Daisy trotted right beside him.", ["s12_morning_hill"]),
    (12, N, WARM, "And if he ever felt bored, he played games that didn't fool anybody, like counting clouds, or teaching Daisy to dance.", ["s12_morning_hill"]),
    (12, N, WARM, "Little by little, block by block, the villagers learned to trust Finn again.", ["s12_lena_waves"]),
    (12, L, "cheerful, friendly", "Good morning, Finn! How are the sheep today?", ["s12_lena_waves"]),
    (12, F, "happy, proud, honest", "All six of them are happy and safe. And that's the truth!", ["s12_end"]),
    (12, N, WARM + ", the moral, slow and clear", "Because when you always tell the truth, people will believe you when it matters most.", ["s12_end"]),
    (12, N, WARM + ", closing", "The end.", ["s12_end"]),
]
SCENE_TITLES = {1: "The village", 2: "On the hill", 3: "The first trick", 4: "The second trick", 5: "The real wolf",
                6: "Nobody comes", 7: "The bell", 8: "The empty hill", 9: "The truth", 10: "The search",
                11: "A tower of blocks", 12: "One true word at a time"}

# ---------------------------------------------------------------- characters (design specs until the canonicals are approved)
TAIL = ("Fine looped felt fibres and small visible stitches. These intrinsic colours and this mid brightness stay "
        "identical in every image; scene light only tints and shades them. {p} pose, facing and expression are the "
        "ones this prompt states.")
CHARACTERS = {
    "finn": {"name": "Finn", "folder": "Finn", "canon_id": "FINN_CANON",
        "identity": ("Finn is one young wool-felt boy of about eight, a soft storybook doll with a round head about one "
            "fifth of his height. His skin is warm peach felt (#F2C29B) with rosy-pink cheeks (#E8907E) and a few tiny "
            "cinnamon-brown freckle stitches (#A8653C) across his nose. His hair is a mop of short curly copper-orange "
            "felt (#C86A2C) that covers his ears' tops and his forehead. Two large round glossy eyes, each about a fifth "
            "of the head width: hazel-green irises (#7A8A3A), black pupils, one white catch-light at upper right, ivory "
            "sclera (#F6F0E6); two short copper-orange brows; a small rounded nose and a small mouth line. He wears a "
            "moss-green knitted tunic (#5E7A3A) with a round collar, a short red scarf (#C0392B) knotted at the neck, "
            "brown felt trousers (#7A5236) and small dark-brown boots (#4A3020). Two arms with small four-fingered hands "
            "and two legs; slim, like a child. " + TAIL.format(p="His")),
        "sheet": "one young felt boy with curly copper-orange hair, rosy cheeks and freckles, two hazel-green eyes, a moss-green tunic, a short red scarf, brown trousers and dark-brown boots",
        "mouth": "When Finn's mouth opens, it is a small rounded opening with a dark warm-brown interior, a soft pink tongue and a neat row of small ivory upper teeth.",
        "palette": {"skin": "#F2C29B", "cheeks": "#E8907E", "hair": "#C86A2C", "iris": "#7A8A3A", "tunic": "#5E7A3A", "scarf": "#C0392B", "trousers": "#7A5236", "boots": "#4A3020"},
        "proportions": {"head_to_height": 0.2},
        "checklist": ["one boy, two arms, two legs, four fingers per hand", "curly copper-orange hair", "rosy cheeks and freckles",
                      "two hazel-green eyes", "moss-green tunic with round collar", "short red scarf", "brown trousers and dark-brown boots",
                      "head about one fifth of his height", "felt texture with visible stitches", "colours not shifted by scene light"],
        "drift_phrases": ["blond", "baseball cap", "backpack"]},
    "rosie": {"name": "Grandma Rosie", "folder": "Rosie", "canon_id": "ROSIE_CANON",
        "identity": ("Grandma Rosie is one round, cosy, elderly wool-felt woman, a soft storybook doll, about one and a third "
            "times Finn's height. Her skin is warm peach felt (#EBB896) with rosy-pink cheeks (#E08A7A) and soft smile "
            "lines. Her hair is silver-white felt (#E6E2DA) pulled up into a round bun on top of her head. Two kind round "
            "glossy eyes: warm brown irises (#6A4228), black pupils, one white catch-light at upper right, ivory sclera "
            "(#F6F0E6); two soft silver-white brows; a small rounded nose and a gentle mouth line. She wears a long "
            "lavender-purple dress (#8E7AB5) with short puffed sleeves and a long cream apron (#F2E6CF) with one front "
            "pocket, and small dark-brown shoes (#4A3020). Two arms with small four-fingered hands; a round, plump "
            "figure. " + TAIL.format(p="Her")),
        "sheet": "one round elderly felt grandmother with a silver-white bun, rosy cheeks, two kind brown eyes, a long lavender-purple dress and a cream apron",
        "mouth": "When Grandma Rosie's mouth opens, it is a small rounded opening with a dark warm-brown interior and a soft pink tongue.",
        "palette": {"skin": "#EBB896", "hair": "#E6E2DA", "iris": "#6A4228", "dress": "#8E7AB5", "apron": "#F2E6CF"},
        "proportions": {"height_to_finn": 1.33},
        "checklist": ["one elderly woman, two arms, two legs", "silver-white hair in a round bun", "rosy cheeks", "two kind brown eyes",
                      "long lavender-purple dress with puffed sleeves", "long cream apron with one pocket", "about one and a third of Finn's height",
                      "felt texture", "colours not shifted by scene light"],
        "drift_phrases": ["spectacles", "walking stick", "shawl"]},
    "ben": {"name": "Farmer Ben", "folder": "Ben", "canon_id": "BEN_CANON",
        "identity": ("Farmer Ben is one tall, broad, friendly wool-felt man, a soft storybook doll, about one and a half "
            "times Finn's height. His skin is tan felt (#D69A6E) with ruddy cheeks (#C9785E). He has a short bushy "
            "chestnut-brown beard (#6B4226) and short chestnut-brown hair under a round straw-yellow hat (#D9B75C) with "
            "a brown band. Two friendly round glossy eyes: dark-brown irises (#4A2E1E), black pupils, one white "
            "catch-light at upper right, ivory sclera (#F6F0E6); two thick chestnut-brown brows; a round nose. He wears "
            "denim-blue overalls (#4F6F9E) over a cream shirt (#F2E8D5) with rolled-up sleeves, and big dark-brown "
            "boots (#4A3020). Two strong arms with large four-fingered hands. " + TAIL.format(p="His")),
        "sheet": "one tall broad felt farmer with a chestnut-brown beard, a straw-yellow hat, two dark-brown eyes, denim-blue overalls over a cream shirt and dark-brown boots",
        "mouth": "When Farmer Ben's mouth opens, it is a rounded opening with a dark warm-brown interior and a soft pink tongue, framed by his beard.",
        "palette": {"skin": "#D69A6E", "beard": "#6B4226", "hat": "#D9B75C", "overalls": "#4F6F9E", "shirt": "#F2E8D5"},
        "proportions": {"height_to_finn": 1.5},
        "checklist": ["one tall man, two arms, two legs", "short bushy chestnut-brown beard", "round straw-yellow hat with a brown band",
                      "two dark-brown eyes", "denim-blue overalls over a cream shirt", "about one and a half of Finn's height",
                      "felt texture", "colours not shifted by scene light"],
        "drift_phrases": ["clean-shaven", "pitchfork", "cowboy hat"]},
    "lena": {"name": "Lena", "folder": "Lena", "canon_id": "LENA_CANON",
        "identity": ("Lena is one young wool-felt girl of about nine, a soft storybook doll, a little taller than Finn. "
            "Her skin is warm caramel-brown felt (#B07A52) with rosy cheeks (#C97A6A). Her hair is dark-brown felt "
            "(#3E2A1E) in two long braids tied with small sunflower-yellow ribbons (#F2C230). Two large round glossy "
            "eyes: dark-brown irises (#3E2A1E), black pupils, one white catch-light at upper right, ivory sclera "
            "(#F6F0E6); two short dark-brown brows; a small nose and a bright mouth line. She wears a sky-blue dress "
            "(#7FB2DA) with a white collar (#F8F4EC) and small red shoes (#B8433A). Two arms with small four-fingered "
            "hands and two slim legs. " + TAIL.format(p="Her")),
        "sheet": "one young felt girl with two long dark-brown braids tied with sunflower-yellow ribbons, two dark-brown eyes, a sky-blue dress with a white collar and red shoes",
        "mouth": "When Lena's mouth opens, it is a small rounded opening with a dark warm-brown interior, a soft pink tongue and small ivory upper teeth.",
        "palette": {"skin": "#B07A52", "hair": "#3E2A1E", "ribbons": "#F2C230", "dress": "#7FB2DA", "collar": "#F8F4EC", "shoes": "#B8433A"},
        "proportions": {"height_to_finn": 1.05},
        "checklist": ["one girl, two arms, two legs", "two long dark-brown braids with sunflower-yellow ribbons", "two dark-brown eyes",
                      "sky-blue dress with a white collar", "red shoes", "a little taller than Finn", "felt texture"],
        "drift_phrases": ["ponytail", "blonde"]},
    "daisy": {"name": "Daisy", "folder": "Daisy", "canon_id": "DAISY_CANON",
        "identity": ("Daisy is one small young wool-felt lamb who walks on four thin legs. Her fleece is a fluffy cloud of "
            "cream-white curly felt (#F4EEDF). Her face, ears and lower legs are soft charcoal-black felt (#2E2A28), "
            "with one white heart-shaped patch (#FBF8F2) on her forehead above her nose. Two small ears stick out "
            "sideways with rosy-pink insides (#E8A3A0). Two large round glossy eyes: warm amber-brown irises (#8A5A22), "
            "black pupils, one white catch-light at upper right, ivory sclera (#F6F0E6); a small rosy-pink nose "
            "(#E8A3A0) and a small smiling mouth line. A short fluffy cream-white tail. Four little dark hooves. She is "
            "about a third of Finn's height. " + TAIL.format(p="Her")),
        "sheet": "one small fluffy cream-white felt lamb with a charcoal-black face and legs, a white heart-shaped patch on her forehead, rosy-pink ear insides and two amber-brown eyes",
        "mouth": "When Daisy bleats, her mouth opens in a small rounded shape with a soft pink inside.",
        "palette": {"fleece": "#F4EEDF", "face_legs": "#2E2A28", "heart": "#FBF8F2", "ears_inside": "#E8A3A0", "iris": "#8A5A22"},
        "proportions": {"height_to_finn": 0.35},
        "checklist": ["one lamb, four legs, one short tail", "fluffy cream-white fleece", "charcoal-black face and lower legs",
                      "white heart-shaped patch on the forehead", "ears sticking out sideways with pink insides", "two amber-brown eyes",
                      "about a third of Finn's height", "felt texture"],
        "drift_phrases": ["white-faced lamb", "goat"]},
    "sheep": {"name": "the Sheep", "plural": "sheep", "folder": "Sheep", "canon_id": "SHEEP_CANON",
        "identity": ("Each of the flock's sheep is the same: one round, friendly wool-felt ewe who walks on four legs, "
            "with a big fluffy body of cream-white curly felt (#EFE6D2), a smooth pale biscuit-beige face and lower legs "
            "(#D9C3A0), two small soft ears sticking out sideways with rosy-pink insides (#E3A39A), two round glossy eyes "
            "with dark-brown irises (#4A2E1E), black pupils, ivory sclera and one white catch-light, a small rosy-pink "
            "nose (#E3A39A), a small smiling mouth line, a short fluffy tail and four little dark hooves. Each sheep is "
            "about half of Finn's height to the top of her head and has no horns. " + TAIL.format(p="Their")),
        "sheet": "a round fluffy cream-white felt sheep with a biscuit-beige face and legs, small ears with rosy-pink insides and two dark-brown eyes",
        "mouth": "When a sheep bleats, its mouth opens in a small rounded shape with a soft pink inside.",
        "palette": {"fleece": "#EFE6D2", "face_legs": "#D9C3A0", "ears_inside": "#E3A39A", "iris": "#4A2E1E"},
        "proportions": {"height_to_finn": 0.55},
        "checklist": ["every sheep identical", "round fluffy cream-white fleece", "biscuit-beige face and legs, no horns",
                      "ears with rosy-pink insides", "two dark-brown eyes", "count matches the cast line"],
        "drift_phrases": ["horned", "black sheep"]},
    "wolf": {"name": "the Wolf", "folder": "Wolf", "canon_id": "WOLF_CANON",
        "identity": ("The Wolf is one long, lanky, rather silly wool-felt wolf who walks on four long legs, more funny than "
            "frightening. His fur felt is soft smoke-grey (#8A8D93), lighter pale-grey on the muzzle, chest and belly "
            "(#D3D5D8), with darker charcoal-grey tips on his two tall pointed ears and his back (#4E5157). His long "
            "rounded muzzle ends in a big round black nose (#222222). Two round glossy eyes: golden-yellow irises "
            "(#D9A93A), black pupils, one white catch-light at upper right, ivory sclera (#F4EEE2); two expressive "
            "charcoal-grey brows. His mouth is a long wavy closed line, and his teeth are hidden. One big bushy "
            "smoke-grey tail with a pale-grey tip. Long thin legs with soft round paws. Standing on four legs he is "
            "about three quarters of Finn's height to his ear tips. Rounded soft shapes everywhere, no sharp edges. "
            + TAIL.format(p="His")),
        "sheet": "one long lanky smoke-grey felt wolf with a pale-grey muzzle and chest, tall pointed ears, two golden-yellow eyes, a big black nose and a big bushy tail, more silly than scary",
        "mouth": "When the Wolf's mouth opens, it is a long rounded opening with a dark warm-brown interior and a long pink tongue; his teeth stay hidden.",
        "palette": {"fur": "#8A8D93", "muzzle": "#D3D5D8", "tips": "#4E5157", "nose": "#222222", "iris": "#D9A93A"},
        "proportions": {"height_to_finn": 0.75},
        "checklist": ["one wolf, four legs, one bushy tail", "soft smoke-grey fur with a pale-grey muzzle and chest",
                      "two tall pointed ears with charcoal tips", "two golden-yellow eyes", "big round black nose",
                      "teeth hidden, rounded soft shapes", "silly rather than scary", "about three quarters of Finn's height"],
        "drift_phrases": ["fangs", "snarling", "blood", "red eyes", "drooling"]},
}
ORDER = ["ben", "rosie", "lena", "finn", "wolf", "sheep", "daisy"]
COUNTS = {"sheep": 5}
PREFIX = {"finn": "F", "rosie": "R", "ben": "B", "lena": "L", "daisy": "D", "sheep": "SH", "wolf": "W"}

CAST_SCALE_BLOCK = (
    "Relative size (fixed for the whole story, the same at the same distance from the camera), with Finn's height as "
    "1: Farmer Ben 1.5 (1.6 with his hat), Grandma Rosie 1.33, Lena 1.05, the Wolf 0.75 to his ear tips on four legs, "
    "each sheep 0.55 to the top of her head, Daisy 0.35. The adults are clearly taller than the children, and Daisy is "
    "clearly smaller than every sheep. Sitting, kneeling, crouching or running changes a silhouette but never the size "
    "of a head or limb.")
CAST_SCALE = {"rule": "At equal depth, with Finn's height as 1.0: Ben 1.5 (1.6 with hat), Rosie 1.33, Lena 1.05, Wolf 0.75 (to ear tips, on four legs), each sheep 0.55, Daisy 0.35.",
              "anchor_record": "LINEUP",
              "status": "design targets; measure them on the approved LINEUP image and update every setup's sizes"}
LINEUP_SIZE = "Farmer Ben with his hat measures 0.78 of the frame height; every other character follows the size lineup above."
FINAL_CHECK = ("Before finishing, check: each named character appears exactly once and the flock has exactly the number "
               "of sheep the cast line states; every character has exactly two eyes and two eyebrows (one above each "
               "eye, drawn once), its canonical ears, hair, clothes, limbs and hands or hooves, and each animal exactly "
               "one tail attached at its root; no text, letters, labels or watermark anywhere.")

# ---------------------------------------------------------------- locations
P_VILLAGE = ("A small felt village square: round cottages with soft thatched roofs around a cobbled square with a stone "
             "well in the middle; Grandma Rosie's bakery at the left with a round window and a wooden bench by its "
             "door; a low wooden fence and a few hens' feeding trough at the right; the path to the hill leaves the "
             "square at the far right; green hills behind.")
L_VILLAGE = ["the bakery at the left (x 0.02-0.30) with its door and bench (bench x 0.18-0.30, y 0.74-0.82)",
             "the stone well in the middle of the square (x 0.44-0.56, y 0.55-0.78)", "the low wooden fence at the right (x 0.70-0.95, y 0.62-0.74)",
             "the hill path leaving the square at the far right (x 0.88-1.00)", "the cobbled ground where characters stand (y 0.75-0.92)"]
P_PASTURE = ("A wide grassy felt hilltop pasture: soft green grass with small flowers; a big round grey rock at the left "
             "where Finn sits; a wooden post with a small brass bell hanging from a little roof at the right of centre; "
             "far below at the left, the thatched roofs of the village; the dark edge of the woods along the far right.")
L_PASTURE = ["the big grey rock at the left (x 0.08-0.28, top near y=0.62)", "the bell post right of centre (x 0.62-0.67, from y=0.40 to y=0.80), the bell near its top",
             "the village roofs far below at the left (x 0.00-0.25, y 0.38-0.48)", "the edge of the woods along the far right (x 0.85-1.00)",
             "the open grass where the flock grazes (y 0.68-0.92)"]
P_PATH = ("A side view of a winding felt path climbing a grassy hillside from the lower left to the upper right, with "
          "a low stone wall along it, wildflowers and a lone small tree.")
L_PATH = ["the path rising from the lower left (y 0.86) to the upper right (y 0.62)", "the low stone wall below the path along its length",
          "a lone small tree at the upper middle (x 0.48-0.58, y 0.20-0.60)", "wildflowers along the bottom edge"]
LOC = {
    "village_morning": dict(folder="village", stem="village_morning", label="the village square in morning light",
        description=P_VILLAGE, landmarks=L_VILLAGE, light="Fresh morning sunlight from the upper right; soft shadows to the left.",
        ambient="Smoke curls gently from a chimney; grass and flowers sway; buildings, well and fence stay fixed."),
    "village_evening": dict(folder="village", stem="village_evening", derived_from="village_morning", label="the village square at dusk",
        description="The same village square as the morning plate, with every cottage, the well, the bakery and the fence in exactly the same place, at dusk with warm lit windows.",
        landmarks=L_VILLAGE, light="Dusk: deep blue sky with the first stars, warm yellow light from the cottage windows and the bakery door.",
        ambient="Window light flickers softly; buildings, well and fence stay fixed."),
    "pasture_morning": dict(folder="pasture", stem="pasture_morning", label="the hilltop pasture in morning light",
        description=P_PASTURE, landmarks=L_PASTURE, light="Bright morning sunlight from the upper left; a clear blue sky with small round clouds.",
        ambient="Grass and flowers sway; clouds drift slowly; rock, post and bell stay fixed."),
    "pasture_noon": dict(folder="pasture", stem="pasture_noon", derived_from="pasture_morning", label="the hilltop pasture at midday",
        description="The same hilltop pasture as the morning plate, every rock, post and tree in exactly the same place, at midday.",
        landmarks=L_PASTURE, light="Bright midday sunlight from above; short shadows; a warm blue sky.",
        ambient="Grass and flowers sway; clouds drift slowly; rock, post and bell stay fixed."),
    "pasture_evening": dict(folder="pasture", stem="pasture_evening", derived_from="pasture_morning", label="the hilltop pasture at sunset",
        description="The same hilltop pasture as the morning plate, every rock, post and tree in exactly the same place, at sunset.",
        landmarks=L_PASTURE, light="Sunset: orange and pink sky, warm low light from the left, the woods at the right in soft blue shadow.",
        ambient="Grass sways; the sky glows; rock, post and bell stay fixed."),
    "path_morning": dict(folder="hill_path", stem="path_morning", label="the hill path in morning light",
        description=P_PATH, landmarks=L_PATH, light="Morning sunlight from the upper left.",
        ambient="Grass and wildflowers sway; the wall, tree and path stay fixed."),
    "path_noon": dict(folder="hill_path", stem="path_noon", derived_from="path_morning", label="the hill path at midday",
        description="The same hill path as the morning plate, every stone, flower and the tree in exactly the same place, at midday.",
        landmarks=L_PATH, light="Bright midday sunlight from above.", ambient="Grass and wildflowers sway; the wall, tree and path stay fixed."),
    "path_evening": dict(folder="hill_path", stem="path_evening", derived_from="path_morning", label="the hill path at sunset",
        description="The same hill path as the morning plate, every stone, flower and the tree in exactly the same place, at sunset.",
        landmarks=L_PATH, light="Sunset: warm orange light from the left, long shadows, a pink sky.",
        ambient="Grass sways; the wall, tree and path stay fixed."),
    "woods_evening": dict(folder="woods", stem="woods_evening", label="the edge of the woods at dusk",
        description=("The edge of a soft felt wood at dusk: big leafy bushes and ferns in front of round-topped trees, a "
                     "grassy clearing in the middle where characters stand, the first stars in a deep blue sky between "
                     "the treetops."),
        landmarks=["a big leafy bush at the lower left (x 0.02-0.25, y 0.55-0.90)", "a big leafy bush at the right (x 0.72-0.98, y 0.55-0.90)",
                   "ferns along the bottom edge", "the grassy clearing in the middle (x 0.25-0.72, y 0.70-0.92)"],
        light="Dusk: deep blue light with a warm glow low on the horizon; soft and calm, not dark.",
        ambient="Leaves and ferns stir gently; stars twinkle; bushes and trees stay fixed."),
}

CLOSE_TREATMENT = ("The background is the same place, very strongly blurred into soft shapes of colour, as with a "
                   "portrait lens at f/1.4; nothing stands in front of the character except what this frame states. "
                   "The blurred place:")


def closeup(loc, who, label, top_word="the top of the head", top=0.05):
    name = CHARACTERS[who]["name"]
    return dict(location=loc, framing="dialogue_close_up", label=label,
                camera=(f"Close-up, 16:9: {name}'s head and upper chest are centred, {top_word} near y={top:.2f} and chin "
                        f"near y=0.70, facing the camera."),
                background_treatment=CLOSE_TREATMENT)


WIDE = "Fixed normal-height wide camera, 16:9, exactly the framing of the locked plate."
SIDE = "Fixed normal-height side camera, 16:9, exactly the framing of the locked plate; characters climb the path from left to right and come down from right to left."
RATIO = {"finn": 1.0, "rosie": 1.33, "ben": 1.6, "lena": 1.05, "wolf": 0.75, "sheep": 0.55, "daisy": 0.35}
WHAT = {"finn": "Finn standing measures about {h:.2f} of the frame height",
        "rosie": "Grandma Rosie standing measures about {h:.2f} of the frame height",
        "ben": "Farmer Ben standing, with his hat, measures about {h:.2f} of the frame height",
        "lena": "Lena standing measures about {h:.2f} of the frame height",
        "wolf": "the Wolf on four legs measures about {h:.2f} of the frame height to his ear tips",
        "sheep": "each sheep measures about {h:.2f} of the frame height to the top of her head",
        "daisy": "Daisy measures about {h:.2f} of the frame height"}


def sizes(finn_h, chars):
    return {c: WHAT[c].format(h=finn_h * RATIO[c])[0].upper() + WHAT[c].format(h=finn_h * RATIO[c])[1:] + "." for c in chars}


REL = "Every character keeps the story's size lineup; the adults are clearly taller than the children, and Daisy is smaller than every sheep."
ALL = list(RATIO)
SETUPS = {
    "village_plate": dict(location="village_morning", framing="empty_plate", label="the empty village square in morning light", camera=WIDE),
    "village_wide": dict(location="village_morning", framing="scene_wide", label="a wide shot of the village square in morning light",
                         camera=WIDE + " Characters stand on the cobbles near y=0.86.", size=sizes(0.30, ALL), relation=REL),
    "village_rosie_closeup": closeup("village_morning", "rosie", "a close-up of Grandma Rosie in the village square", "the top of her bun"),
    "village_finn_closeup": closeup("village_morning", "finn", "a close-up of Finn in the village square", "the top of his hair"),
    "pasture_wide": dict(location="pasture_morning", framing="scene_wide", label="a wide shot of the hilltop pasture in morning light",
                         camera=WIDE + " Characters stand on the grass near y=0.86.", size=sizes(0.30, ALL), relation=REL),
    "pasture_finn_closeup": closeup("pasture_morning", "finn", "a close-up of Finn on the hilltop pasture", "the top of his hair"),
    "pasture_ben_closeup": closeup("pasture_morning", "ben", "a close-up of Farmer Ben on the hilltop pasture", "the top of his hat"),
    "pasture_rosie_closeup": closeup("pasture_morning", "rosie", "a close-up of Grandma Rosie on the hilltop pasture", "the top of her bun"),
    "path_side": dict(location="path_morning", framing="scene_wide", label="a side-on wide shot of the hill path in morning light",
                      camera=SIDE, size=sizes(0.30, ALL), relation=REL),
    "pasture_noon_wide": dict(location="pasture_noon", framing="scene_wide", label="a wide shot of the hilltop pasture at midday",
                              camera=WIDE + " Characters stand on the grass near y=0.86.", size=sizes(0.30, ALL), relation=REL),
    "pasture_noon_lena_closeup": closeup("pasture_noon", "lena", "a close-up of Lena on the hilltop pasture at midday", "the top of her head"),
    "pasture_noon_ben_closeup": closeup("pasture_noon", "ben", "a close-up of Farmer Ben on the hilltop pasture at midday", "the top of his hat"),
    "path_noon_side": dict(location="path_noon", framing="scene_wide", label="a side-on wide shot of the hill path at midday",
                           camera=SIDE, size=sizes(0.30, ALL), relation=REL),
    "pasture_evening_wide": dict(location="pasture_evening", framing="scene_wide", label="a wide shot of the hilltop pasture at sunset",
                                 camera=WIDE + " Characters stand on the grass near y=0.86.", size=sizes(0.30, ALL), relation=REL),
    "pasture_evening_finn_closeup": closeup("pasture_evening", "finn", "a close-up of Finn on the hilltop at sunset", "the top of his hair"),
    "pasture_evening_wolf_closeup": closeup("pasture_evening", "wolf", "a close-up of the Wolf at the edge of the woods at sunset", "his ear tips"),
    "village_evening_wide": dict(location="village_evening", framing="scene_wide", label="a wide shot of the village square at dusk",
                                 camera=WIDE + " Characters stand on the cobbles near y=0.86.", size=sizes(0.30, ALL), relation=REL),
    "village_evening_rosie_closeup": closeup("village_evening", "rosie", "a close-up of Grandma Rosie in the village at dusk", "the top of her bun"),
    "village_evening_finn_closeup": closeup("village_evening", "finn", "a close-up of Finn in the village at dusk", "the top of his hair"),
    "path_evening_side": dict(location="path_evening", framing="scene_wide", label="a side-on wide shot of the hill path at sunset",
                              camera=SIDE, size=sizes(0.30, ALL), relation=REL),
    "woods_wide": dict(location="woods_evening", framing="scene_wide", label="a wide shot of the edge of the woods at dusk",
                       camera=WIDE + " Characters stand in the clearing near y=0.88.", size=sizes(0.30, ALL), relation=REL),
    "woods_two_shot": dict(location="woods_evening", framing="close_two_shot", label="a closer two-shot of Finn and Daisy by the bush at dusk",
                           camera=("Fixed closer camera at the edge of the woods, 16:9: one shared crop of the wide setup that "
                                   "magnifies Finn, Daisy and the bush equally; the plate is softly blurred behind them."),
                           size={"finn": "Finn kneeling fills about 0.70 of the frame height.", "daisy": "Daisy measures about 0.33 of the frame height."},
                           relation="Daisy is about a third of Finn's standing height; kneeling, Finn's head stays the same size."),
}

# ---------------------------------------------------------------- shots
# (id, scene, setup, cast, start frame, end frame, video action, prop state, expressions {char: (start, end)})
FLOCK = ["sheep*5", "daisy"]
SHOTS = [
    ("s01_village", 1, "village_plate", [], "The empty village square in fresh morning light, smoke rising from one chimney",
     "The same empty square; the smoke has drifted a little to the left", "Smoke drifts gently from a chimney; nothing else moves.", None, {}),
    ("s01_village_life", 1, "village_wide", ["ben", "rosie", "lena"],
     "Farmer Ben stands by the fence at the right scattering grain toward the ground with one hand; Grandma Rosie stands in the open bakery door at the left, smiling; Lena skips across the middle of the square near x=0.40, one foot raised",
     "Ben still by the fence; Rosie waves from her door; Lena has skipped to near x=0.55 and waves back",
     "Lena skips across the square while Ben scatters grain and Grandma Rosie waves from her bakery door.", None,
     {"rosie": ("R_EXPR_WARM", "R_EXPR_WARM"), "lena": ("L_EXPR_CHEERFUL", "L_EXPR_CHEERFUL")}),
    ("s01_rosie_reminds", 1, "village_rosie_closeup", ["rosie"],
     "Grandma Rosie looks down toward the camera with a warm loving smile: brows relaxed, eyes crinkled, mouth closed",
     "Grandma Rosie becomes gently serious: brows slightly raised and level, eyes steady, mouth closed in a firm kind line",
     "Grandma Rosie smiles, then becomes gently serious as she gives her reminder.", None, {"rosie": ("R_EXPR_WARM", "R_EXPR_SERIOUS")}),
    ("s01_finn_promises", 1, "village_finn_closeup", ["finn"],
     "Finn looks up toward the camera, eager and happy: brows raised, eyes bright, a big closed smile",
     "Finn nods with a cheerful promise: eyes bright, mouth open in a happy answer",
     "Finn smiles and nods eagerly.", None, {"finn": ("F_EXPR_HAPPY", "F_EXPR_HAPPY")}),
    ("s01_finn_leaves", 1, "village_wide", ["rosie", "finn"] + FLOCK,
     "Finn walks toward the hill path at the right near x=0.60, looking back and waving; five sheep and Daisy walk ahead of him toward the path; Grandma Rosie waves from her bakery door at the left",
     "Finn near x=0.78 with the five sheep and Daisy just ahead of him, reaching the hill path at the right; Rosie still waving",
     "Finn leads the flock across the square toward the hill path, waving to Grandma Rosie.", None,
     {"finn": ("F_EXPR_HAPPY", "F_EXPR_HAPPY"), "rosie": ("R_EXPR_WARM", "R_EXPR_WARM")}),
    ("s02_flock_arrives", 2, "pasture_wide", ["finn"] + FLOCK,
     "Finn walks onto the pasture from the left near x=0.20, the five sheep and Daisy trotting ahead of him onto the grass",
     "The five sheep spread out grazing on the grass in the middle; Daisy stands beside Finn near x=0.35; Finn looks around happily",
     "Finn and the flock arrive on the hilltop and the sheep start to graze.", None, {"finn": ("F_EXPR_HAPPY", "F_EXPR_HAPPY")}),
    ("s02_counting", 2, "pasture_finn_closeup", ["finn"],
     "Finn counts with one finger raised, looking off to the right at the flock, brows raised, mouth open mid-word",
     "Finn smiles proudly, counting finished: brows relaxed, eyes bright, a big closed smile",
     "Finn counts the sheep on his fingers and smiles.", None, {"finn": ("F_EXPR_HAPPY", "F_EXPR_HAPPY")}),
    ("s02_daisy_nuzzles", 2, "pasture_wide", ["finn"] + FLOCK,
     "Finn kneels on the grass near x=0.38; Daisy nuzzles his outstretched hand; the five sheep graze in the middle and at the right",
     "Same places; Finn strokes Daisy's head and smiles; the sheep keep grazing",
     "Daisy nuzzles Finn's hand and he strokes her head while the sheep graze.", None, {"finn": ("F_EXPR_HAPPY", "F_EXPR_HAPPY")}),
    ("s02_finn_bored", 2, "pasture_finn_closeup", ["finn"],
     "Finn sits with his chin in his hand, bored: brows drooping, eyelids half lowered, mouth pushed into a pout",
     "Finn gets a mischievous idea: one brow raised, eyes narrowed and sparkling, a sly closed grin",
     "Finn sighs with boredom, then a sly idea lights up his face.", None, {"finn": ("F_EXPR_BORED", "F_EXPR_MISCHIEVOUS")}),
    ("s03_finn_shouts", 3, "pasture_wide", ["finn"] + FLOCK,
     "Finn stands on top of the big grey rock at the left, hands cupped around his mouth, shouting toward the village below; the sheep and Daisy graze calmly",
     "Same places; Finn leans forward shouting even louder; the sheep and Daisy keep grazing",
     "Finn stands on the rock and shouts toward the village while the sheep graze calmly.", None, {"finn": ("F_EXPR_SHOUTING", "F_EXPR_SHOUTING")}),
    ("s03_villagers_run", 3, "path_side", ["ben", "rosie", "lena"],
     "Farmer Ben, Grandma Rosie and Lena run up the path from the lower left, Ben in front near x=0.30, Rosie and Lena just behind, all looking worried",
     "The three are near the upper right of the path, Ben near x=0.70, still running, Rosie holding her apron",
     "Farmer Ben, Grandma Rosie and Lena hurry up the hill path.", None,
     {"ben": ("B_EXPR_WORRIED", "B_EXPR_WORRIED"), "rosie": ("R_EXPR_WORRIED", "R_EXPR_WORRIED"), "lena": ("L_EXPR_WORRIED", "L_EXPR_WORRIED")}),
    ("s03_no_wolf", 3, "pasture_wide", ["ben", "rosie", "lena", "finn"] + FLOCK,
     "Ben, Rosie and Lena have just arrived at the left, out of breath, looking around; Finn rolls on the grass near x=0.45 laughing; the sheep and Daisy graze at the right",
     "Same places; Ben stands with his hands on his hips, Rosie shakes her head, Lena frowns; Finn sits up, still laughing",
     "The villagers look around for the wolf while Finn laughs on the grass.", None,
     {"finn": ("F_EXPR_LAUGHING", "F_EXPR_LAUGHING"), "ben": ("B_EXPR_CROSS", "B_EXPR_CROSS"), "rosie": ("R_EXPR_SERIOUS", "R_EXPR_SERIOUS")}),
    ("s03_ben_cross", 3, "pasture_ben_closeup", ["ben"],
     "Farmer Ben looks down toward the camera, cross but kind: brows lowered, eyes firm, mouth closed in a frown under his beard",
     "Farmer Ben speaks firmly: brows lowered, mouth slightly open",
     "Farmer Ben frowns and speaks firmly.", None, {"ben": ("B_EXPR_CROSS", "B_EXPR_CROSS")}),
    ("s03_rosie_serious", 3, "pasture_rosie_closeup", ["rosie"],
     "Grandma Rosie looks down toward the camera, gently serious and disappointed: brows tilted up in the middle, eyes sad, mouth closed",
     "Grandma Rosie speaks softly with the same serious, disappointed face, mouth slightly open",
     "Grandma Rosie speaks softly, disappointed.", None, {"rosie": ("R_EXPR_SERIOUS", "R_EXPR_SERIOUS")}),
    ("s04_finn_again", 4, "pasture_noon_wide", ["finn"] + FLOCK,
     "Finn stands by the big grey rock at the left with a sly grin, hands cupped around his mouth; the sheep and Daisy graze",
     "Same places; Finn shouts with his arms waving wildly",
     "Finn grins, then shouts and waves his arms toward the village.", None, {"finn": ("F_EXPR_MISCHIEVOUS", "F_EXPR_SHOUTING")}),
    ("s04_villagers_run", 4, "path_noon_side", ["ben", "rosie", "lena"],
     "Farmer Ben, Grandma Rosie and Lena hurry up the path from the lower left again, Ben in front near x=0.30, all puffing",
     "The three are near the upper right of the path, Ben near x=0.70, Rosie holding her side, Lena close behind",
     "The villagers hurry up the hill path again, puffing.", None,
     {"ben": ("B_EXPR_WORRIED", "B_EXPR_WORRIED"), "rosie": ("R_EXPR_WORRIED", "R_EXPR_WORRIED"), "lena": ("L_EXPR_WORRIED", "L_EXPR_WORRIED")}),
    ("s04_finn_giggles", 4, "pasture_noon_wide", ["ben", "rosie", "lena", "finn"] + FLOCK,
     "Ben, Rosie and Lena arrive at the left, panting; Finn peeks out from behind the big grey rock, giggling with both hands over his mouth; the sheep and Daisy graze at the right",
     "Same places; the villagers stare at Finn, unhappy; Finn still giggles",
     "The villagers arrive panting and find Finn giggling behind the rock.", None,
     {"finn": ("F_EXPR_LAUGHING", "F_EXPR_LAUGHING"), "ben": ("B_EXPR_CROSS", "B_EXPR_CROSS"), "lena": ("L_EXPR_UPSET", "L_EXPR_UPSET")}),
    ("s04_lena_upset", 4, "pasture_noon_lena_closeup", ["lena"],
     "Lena looks at the camera, upset: brows drawn together and up, eyes shiny, mouth closed in a wobbly line",
     "Lena speaks, hurt: brows up, mouth open",
     "Lena looks hurt and speaks up.", None, {"lena": ("L_EXPR_UPSET", "L_EXPR_UPSET")}),
    ("s04_ben_warns", 4, "pasture_noon_ben_closeup", ["ben"],
     "Farmer Ben looks down toward the camera, slow and serious: brows level, eyes steady, mouth closed",
     "Farmer Ben speaks his warning: one finger raised beside his face, brows level, mouth slightly open",
     "Farmer Ben raises one finger and gives his warning.", None, {"ben": ("B_EXPR_STERN", "B_EXPR_STERN")}),
    ("s04_villagers_leave", 4, "pasture_noon_wide", ["ben", "rosie", "lena", "finn"] + FLOCK,
     "Ben, Rosie and Lena walk away toward the left edge, heads down and sad; Finn stands by the rock watching them, his smile fading; the sheep and Daisy graze",
     "The villagers have nearly left the frame at the left; Finn shrugs and looks away to the right",
     "The villagers walk sadly away; Finn watches them go, then shrugs.", None,
     {"finn": ("F_EXPR_GUILTY", "F_EXPR_GUILTY")}),
    ("s05_wolf_appears", 5, "pasture_evening_wide", ["finn", "wolf"] + FLOCK,
     "Finn sits on the big grey rock at the left looking at the sunset; the sheep and Daisy graze in the middle; the Wolf peeks out from the edge of the woods at the far right, crouched low",
     "Same places; the Wolf has stepped out onto the grass at the right, crouched low, looking at the sheep",
     "The Wolf creeps out of the woods at the edge of the pasture while Finn watches the sunset.", None, {}),
    ("s05_wolf_creeps", 5, "pasture_evening_wolf_closeup", ["wolf"],
     "The Wolf looks off to the left at the sheep with a silly hungry grin: brows raised, eyes wide and greedy, mouth closed in a long wavy smile",
     "The Wolf licks his lips with the tip of his tongue, eyes still on the sheep",
     "The Wolf grins and licks his lips, looking at the sheep.", None, {"wolf": ("W_EXPR_HUNGRY", "W_EXPR_HUNGRY")}),
    ("s05_finn_sees", 5, "pasture_evening_finn_closeup", ["finn"],
     "Finn turns his head toward the right and sees the Wolf: brows high, eyes round, mouth a small open O",
     "Finn is frightened: brows tilted up in the middle, eyes wide, both hands at his cheeks",
     "Finn turns, sees the Wolf and puts his hands to his cheeks.", None, {"finn": ("F_EXPR_STARTLED", "F_EXPR_WORRIED")}),
    ("s06_finn_cries_wolf", 6, "pasture_evening_wide", ["finn", "wolf"] + FLOCK,
     "Finn stands on the big grey rock shouting with his hands cupped toward the village; the Wolf creeps toward the flock from the right, near x=0.78; the sheep and Daisy huddle together in the middle",
     "Finn waves both arms, still shouting; the Wolf is closer, near x=0.70; the sheep huddle tighter",
     "Finn shouts and waves for help while the Wolf creeps closer to the huddled sheep.", None,
     {"finn": ("F_EXPR_SHOUTING", "F_EXPR_SHOUTING"), "wolf": ("W_EXPR_HUNGRY", "W_EXPR_HUNGRY")}),
    ("s06_village_hears", 6, "village_evening_wide", ["ben", "rosie", "lena"],
     "Farmer Ben, Grandma Rosie and Lena stand in the square near the well, looking up toward the hill at the right, listening",
     "Ben shakes his head and turns away; Lena looks up at Rosie; Rosie looks at the hill, unsure",
     "The villagers hear the shouting; Ben shakes his head and Lena looks up at Grandma Rosie.", None,
     {"ben": ("B_EXPR_DOUBTFUL", "B_EXPR_DOUBTFUL"), "rosie": ("R_EXPR_DOUBTFUL", "R_EXPR_DOUBTFUL"), "lena": ("L_EXPR_WORRIED", "L_EXPR_WORRIED")}),
    ("s06_rosie_doubts", 6, "village_evening_rosie_closeup", ["rosie"],
     "Grandma Rosie looks toward the hill off-screen to the right, torn and sad: brows tilted up, eyes worried, mouth closed",
     "Grandma Rosie lowers her eyes sadly, mouth closed in a small unhappy line",
     "Grandma Rosie looks toward the hill, torn, then lowers her eyes.", None, {"rosie": ("R_EXPR_DOUBTFUL", "R_EXPR_DOUBTFUL")}),
    ("s07_sheep_scatter", 7, "pasture_evening_wide", ["finn", "wolf"] + FLOCK,
     "The Wolf leaps toward the flock from the right, all four paws off the ground; the five sheep and Daisy start to run in different directions toward the woods at the right; Finn on the rock, frightened",
     "The sheep and Daisy are running into the edge of the woods at the far right, only their tails still visible; the Wolf has landed in the middle, looking around; Finn jumps down from the rock",
     "The Wolf leaps and the sheep scatter into the woods while Finn jumps down from the rock.", None,
     {"finn": ("F_EXPR_WORRIED", "F_EXPR_WORRIED"), "wolf": ("W_EXPR_HUNGRY", "W_EXPR_HUNGRY")}),
    ("s07_finn_rings_bell", 7, "pasture_evening_wide", ["finn", "wolf"],
     "Finn runs to the bell post and grabs the bell rope with both hands; the Wolf in the middle of the grass turns his head toward Finn",
     "Finn rings the bell hard, the bell swinging; the Wolf jumps in surprise, ears straight up",
     "Finn rings the bell with all his might and the Wolf jumps in surprise.", None,
     {"finn": ("F_EXPR_BRAVE", "F_EXPR_BRAVE"), "wolf": ("W_EXPR_HUNGRY", "W_EXPR_STARTLED")}),
    ("s07_wolf_runs", 7, "pasture_evening_wide", ["finn", "wolf"],
     "The Wolf runs toward the woods at the right with his tail tucked between his legs; Finn still holds the bell rope by the post",
     "The Wolf disappears into the woods at the far right, only the tip of his tail showing; Finn lets go of the rope, breathing hard",
     "The Wolf runs off into the woods with his tail tucked between his legs.", None,
     {"finn": ("F_EXPR_BRAVE", "F_EXPR_WORRIED"), "wolf": ("W_EXPR_STARTLED", "W_EXPR_STARTLED")}),
    ("s08_empty_hill", 8, "pasture_evening_wide", ["finn"],
     "Finn stands alone in the middle of the empty pasture, looking toward the woods, calling with his hands cupped; no sheep anywhere",
     "Finn sits down on the grass in the middle, alone, head drooping",
     "Finn calls for the sheep on the empty hill, then sits down sadly.", None, {"finn": ("F_EXPR_WORRIED", "F_EXPR_CRYING")}),
    ("s08_finn_cries", 8, "pasture_evening_finn_closeup", ["finn"],
     "Finn cries softly: brows tilted up in the middle, eyes shiny with tears, one tear on his cheek, mouth wobbling",
     "Finn wipes a tear with the back of his hand, looking down, sorry",
     "Finn cries softly and wipes away a tear.", None, {"finn": ("F_EXPR_CRYING", "F_EXPR_CRYING")}),
    ("s09_finn_runs_home", 9, "path_evening_side", ["finn"],
     "Finn runs down the path from the upper right near x=0.75, facing left, arms pumping",
     "Finn is near the lower left near x=0.25, still running down toward the village",
     "Finn runs down the hill path toward the village as fast as he can.", None, {"finn": ("F_EXPR_WORRIED", "F_EXPR_WORRIED")}),
    ("s09_finn_tells", 9, "village_evening_wide", ["ben", "rosie", "lena", "finn"],
     "Finn has just run into the square from the right, breathless, talking and pointing back at the hill; Rosie, Ben and Lena stand by the well listening",
     "Same places; Ben folds his arms, doubtful; Lena watches Finn; Rosie looks closely at Finn's face",
     "Finn bursts into the square and tells everyone what happened; Ben folds his arms.", None,
     {"finn": ("F_EXPR_CRYING", "F_EXPR_CRYING"), "ben": ("B_EXPR_DOUBTFUL", "B_EXPR_DOUBTFUL"), "rosie": ("R_EXPR_DOUBTFUL", "R_EXPR_KIND")}),
    ("s09_rosie_kneels", 9, "village_evening_wide", ["ben", "rosie", "lena", "finn"],
     "Grandma Rosie steps toward Finn near the well; Ben and Lena watch",
     "Grandma Rosie kneels down beside Finn, one hand on his shoulder, looking into his face; Ben unfolds his arms",
     "Grandma Rosie kneels down beside Finn and puts a hand on his shoulder.", None,
     {"finn": ("F_EXPR_CRYING", "F_EXPR_SINCERE"), "rosie": ("R_EXPR_KIND", "R_EXPR_KIND")}),
    ("s09_finn_sorry", 9, "village_evening_finn_closeup", ["finn"],
     "Finn looks at the camera through his tears, sincere and sorry: brows tilted up, eyes shiny, mouth closed in a small wobbly line",
     "Finn speaks honestly, eyes steady now, mouth slightly open",
     "Finn says sorry through his tears, then speaks steadily.", None, {"finn": ("F_EXPR_SINCERE", "F_EXPR_SINCERE")}),
    ("s09_rosie_believes", 9, "village_evening_rosie_closeup", ["rosie"],
     "Grandma Rosie looks at the camera with warm, kind belief: brows relaxed, eyes soft, a small closed smile",
     "Grandma Rosie looks up, decisive: brows level, eyes bright, mouth open as she calls everyone",
     "Grandma Rosie smiles kindly, then calls everyone to help.", None, {"rosie": ("R_EXPR_KIND", "R_EXPR_KIND")}),
    ("s10_search", 10, "woods_wide", ["ben", "rosie", "lena", "finn"],
     "Finn, Grandma Rosie, Farmer Ben and Lena search the clearing at the edge of the woods, bending to look behind the bushes and under the ferns",
     "Same people, spread a little further; Lena points at the bush at the right, Ben looks behind the bush at the left",
     "Everyone searches behind the bushes and under the ferns.", None, {"finn": ("F_EXPR_WORRIED", "F_EXPR_WORRIED")}),
    ("s10_found_sheep", 10, "woods_wide", ["ben", "rosie", "lena", "finn", "sheep*5"],
     "Two sheep step out of the bush at the right toward Lena; three sheep step out of the bush at the left toward Ben; Finn and Rosie in the middle",
     "All five sheep stand together in the middle of the clearing; Lena and Ben smile; Finn looks around, still searching",
     "The five sheep come out of the bushes and gather in the clearing.", None,
     {"lena": ("L_EXPR_EXCITED", "L_EXPR_EXCITED"), "finn": ("F_EXPR_WORRIED", "F_EXPR_WORRIED")}),
    ("s10_daisy_found", 10, "woods_two_shot", ["finn", "daisy"],
     "Finn kneels beside the big leafy bush at the right; Daisy's head peeks out from under the leaves",
     "Daisy has stepped out from under the bush toward Finn; Finn's face lights up with joy",
     "Daisy peeks out from under the bush and steps toward Finn, who lights up with joy.", None,
     {"finn": ("F_EXPR_WORRIED", "F_EXPR_RELIEVED")}),
    ("s10_hug", 10, "woods_two_shot", ["finn", "daisy"],
     "Finn kneels and wraps both arms gently around Daisy; Daisy's head rests against his cheek",
     "Same hug; Finn's eyes are closed with happiness and Daisy nuzzles his cheek",
     "Finn hugs Daisy and she nuzzles his cheek.", None, {"finn": ("F_EXPR_RELIEVED", "F_EXPR_RELIEVED")}),
    ("s11_together", 11, "village_evening_wide", ["rosie", "finn", "daisy"],
     "Grandma Rosie and Finn sit side by side on the bench by the bakery door at the left; Daisy lies curled at Finn's feet",
     "Same places; Rosie puts her arm around Finn's shoulders",
     "Grandma Rosie and Finn sit together on the bench, and she puts her arm around him.", None,
     {"rosie": ("R_EXPR_KIND", "R_EXPR_KIND"), "finn": ("F_EXPR_SINCERE", "F_EXPR_SINCERE")}),
    ("s11_rosie_tower", 11, "village_evening_rosie_closeup", ["rosie"],
     "Grandma Rosie looks at the camera, wise and gentle: brows relaxed, eyes warm, mouth closed in a soft smile; one hand raised, fingers showing a little tower shape",
     "Grandma Rosie speaks gently, same warm face, mouth slightly open",
     "Grandma Rosie explains gently, shaping a little tower with her hand.", None, {"rosie": ("R_EXPR_KIND", "R_EXPR_KIND")}),
    ("s11_finn_understands", 11, "village_evening_finn_closeup", ["finn"],
     "Finn looks up thoughtfully: brows slightly drawn together, eyes looking up, mouth closed",
     "Finn smiles with new determination: brows level, eyes bright, a small brave closed smile",
     "Finn thinks, then smiles with new determination.", None, {"finn": ("F_EXPR_SINCERE", "F_EXPR_BRAVE")}),
    ("s12_morning_hill", 12, "pasture_wide", ["finn"] + FLOCK,
     "Another morning: Finn lies on the grass near x=0.40 pointing up at the clouds; Daisy stands beside him; the five sheep graze",
     "Finn stands and holds Daisy's front hooves as if dancing, both happy; the sheep graze",
     "Finn counts clouds, then dances with Daisy while the sheep graze.", None, {"finn": ("F_EXPR_HAPPY", "F_EXPR_HAPPY")}),
    ("s12_lena_waves", 12, "pasture_wide", ["lena", "finn"] + FLOCK,
     "Lena comes onto the pasture from the left, waving; Finn near x=0.50 turns toward her; the sheep and Daisy graze",
     "Lena near x=0.30 and Finn near x=0.45 wave to each other, smiling; the sheep and Daisy graze",
     "Lena arrives waving and Finn waves back.", None,
     {"lena": ("L_EXPR_CHEERFUL", "L_EXPR_CHEERFUL"), "finn": ("F_EXPR_HAPPY", "F_EXPR_HAPPY")}),
    ("s12_end", 12, "pasture_finn_closeup", ["finn"],
     "Finn looks at the camera, happy and proud: brows relaxed, eyes bright, a big honest closed smile",
     "Finn gives a little nod, eyes crinkled with happiness, smile even wider",
     "Finn smiles proudly and gives a little nod.", None, {"finn": ("F_EXPR_HAPPY", "F_EXPR_HAPPY")}),
]

EXPR = {
    "finn": {"HAPPY": "happy: brows raised, eyes bright, a big closed smile",
             "BORED": "bored: brows drooping, eyelids half lowered, mouth pushed into a pout",
             "MISCHIEVOUS": "mischievous: one brow raised, eyes narrowed and sparkling, a sly closed grin",
             "SHOUTING": "shouting: brows raised high, eyes wide, mouth wide open in a big round shout",
             "LAUGHING": "laughing: eyes squeezed shut with laughter, brows up, mouth wide open in a laugh",
             "GUILTY": "a little guilty: brows tilted up in the middle, eyes glancing sideways, mouth closed in a small uncertain line",
             "STARTLED": "startled: brows high, eyes round, mouth a small open O",
             "WORRIED": "worried: brows tilted up in the middle, eyes wide, mouth closed in a wobbly line",
             "BRAVE": "brave: brows lowered and level, eyes determined, mouth closed in a firm line",
             "CRYING": "crying softly: brows tilted up in the middle, eyes shiny with tears and one tear on the cheek, mouth wobbling",
             "SINCERE": "sincere and sorry: brows slightly raised, eyes soft and honest, mouth closed in a small line",
             "RELIEVED": "relieved and joyful: brows relaxed, eyes smiling, a wide open happy smile"},
    "rosie": {"WARM": "warm: brows relaxed, eyes crinkled, a loving closed smile",
              "SERIOUS": "gently serious and disappointed: brows tilted up in the middle, eyes sad and steady, mouth closed",
              "WORRIED": "worried: brows drawn up, eyes wide, mouth slightly open",
              "DOUBTFUL": "torn and sad: brows tilted up, eyes unsure, mouth closed in a small unhappy line",
              "KIND": "kind and believing: brows relaxed, eyes soft, a small warm closed smile"},
    "ben": {"CROSS": "cross but kind: brows lowered, eyes firm, mouth closed in a frown under his beard",
            "STERN": "serious and steady: brows level, eyes steady, mouth closed",
            "WORRIED": "worried: brows drawn up, eyes wide, mouth slightly open",
            "DOUBTFUL": "doubtful: one brow raised, eyes narrowed, mouth closed in a flat line"},
    "lena": {"CHEERFUL": "cheerful: brows raised, eyes bright, a big closed smile",
             "WORRIED": "worried: brows drawn up, eyes wide, mouth slightly open",
             "UPSET": "upset: brows drawn together and up, eyes shiny, mouth closed in a wobbly line",
             "EXCITED": "excited: brows high, eyes wide and happy, mouth open in a delighted smile"},
    "wolf": {"HUNGRY": "silly and hungry: brows raised, eyes wide and greedy, mouth closed in a long wavy grin",
             "STARTLED": "startled: brows shot up, eyes round, ears straight up, mouth a small open O"},
}
CANON_VIEW = {
    "finn": "a neutral front view, standing with both arms relaxed at his sides, mouth closed in a soft smile, looking at the camera",
    "rosie": "a neutral front view, standing with her hands folded in front of her apron, mouth closed in a soft smile, looking at the camera",
    "ben": "a neutral front view, standing with his arms relaxed at his sides, mouth closed in a friendly smile under his beard, looking at the camera",
    "lena": "a neutral front view, standing with her arms relaxed at her sides, mouth closed in a soft smile, looking at the camera",
    "daisy": "a neutral three-quarter view facing left, standing on all four legs, mouth closed, looking at the camera",
    "sheep": "a neutral three-quarter view facing left of one sheep, standing on all four legs, mouth closed, looking at the camera",
    "wolf": "a neutral three-quarter view facing left, standing on all four legs, mouth closed in a long wavy line, tail relaxed, looking at the camera",
}
POSE_VIEWS = [
    ("F_WALK_R", "finn", "Full-body side view facing screen-right, walking, one foot forward, arms swinging gently, mouth closed.", "Finn walking, facing right"),
    ("F_RUN_L", "finn", "Full-body running pose facing screen-left, leaning forward, one foot off the ground, arms pumping. Head size equals the neutral pose.", "Finn running, facing left"),
    ("F_SIT", "finn", "Full body sitting on a low round rock, three-quarter view, elbows on his knees, chin resting in one hand. Head size equals the neutral pose.", "Finn sitting with his chin in his hand"),
    ("F_KNEEL", "finn", "Full body kneeling on one knee, three-quarter view facing left, one hand held out low in front of him. Head size equals the neutral pose.", "Finn kneeling"),
    ("W_CREEP_L", "wolf", "Full-body side view facing screen-left, creeping low on four legs, head forward, tail held low, a silly sly look.", "the Wolf creeping, facing left"),
    ("W_RUN_R", "wolf", "Full-body running pose facing screen-right, long legs stretched, ears back, tail tucked between his legs.", "the Wolf running away, facing right"),
    ("SH_GRAZE", "sheep", "One sheep in side view facing screen-left, head down grazing the ground.", "a sheep grazing"),
    ("D_WALK_R", "daisy", "Full-body side view facing screen-right, trotting on four legs, head up.", "Daisy trotting, facing right"),
]
POSE_RULES = [
    ("finn", r"finn[^;.]*\b(sits|sitting)\b", "F_SIT", None),
    ("finn", r"finn[^;.]*\bknee", "F_KNEEL", None),
    ("finn", r"finn[^;.]*\bruns down\b", "F_RUN_L", None),
    ("finn", r"finn[^;.]*\b(walks|leads)\b", "F_WALK_R", None),
    ("wolf", r"wolf[^;.]*\b(peeks|creeps|crouched)\b", "W_CREEP_L", None),
    ("wolf", r"wolf[^;.]*\b(runs|disappears)\b", "W_RUN_R", None),
    ("sheep", r"\bgraz", "SH_GRAZE", None),
]
PORTRAIT_CHARS = ["finn", "rosie", "ben", "lena", "wolf"]
PROP_BLOCKS = {}
PROP_STATE_PREFIX = ""
PROPS = []
PROP_REF = None
INTRO = ("Third story of *Big Lessons, Little Tales*: Aesop's boy who cried wolf for ages 3 to 7, with a gentle ending "
         "(the wolf is silly rather than scary and runs away from a bell; no animal is hurt; the lost sheep are found "
         "and Finn learns to rebuild trust). Felt storybook style of the channel, made with the consistency rules of "
         "`docs/creation-rules.md` CR-01 to CR-18.")
ROLES = {"finn": "the shepherd boy, about eight; plays tricks, learns honesty", "rosie": "Finn's grandmother, the village baker; wise and kind",
         "ben": "the farmer, big and fair; warns Finn", "lena": "Finn's friend, about nine", "daisy": "Finn's favourite lamb, with a white heart on her forehead",
         "sheep": "the flock: five identical ewes", "wolf": "a lanky, silly, hungry wolf; never hurts anyone"}
TRAVEL_NOTE = ("Going up the hill is always left to right on the hill path, coming down is right to left; the village "
               "square has the hill path at its right, so cuts between village, path and pasture keep screen direction.")
STATE_ROWS = [
    "| s01 | morning: everyone in the village; Finn leaves with the five sheep and Daisy toward the hill path at the right | bell on its post on the hilltop |",
    "| s02 | Finn, five sheep and Daisy on the hilltop pasture | same |",
    "| s03 | first false alarm: Ben, Rosie and Lena run up the path, find no wolf, go home | same |",
    "| s04 | next day, midday: second false alarm; the villagers leave sad | same |",
    "| s05-s06 | sunset: the Wolf comes out of the woods at the right; Finn shouts; in the village nobody comes | same |",
    "| s07 | the sheep and Daisy scatter into the woods at the right; Finn rings the bell; the Wolf runs away into the woods | bell rung |",
    "| s08 | the pasture is empty except Finn | no sheep on the hill |",
    "| s09 | dusk: Finn runs down to the village and tells the truth; Rosie believes him | same |",
    "| s10 | dusk at the edge of the woods: the villagers and Finn find the five sheep, then Daisy under a bush | flock complete again |",
    "| s11 | night: Rosie and Finn on the bench by the bakery, Daisy at his feet | same |",
    "| s12 | another morning: Finn, the flock and Daisy on the pasture; Lena visits | same |"]
DECISIONS = [
    "- 2026-10-04: names approved: Finn, Grandma Rosie, Farmer Ben, Lena, Daisy (and the Wolf).",
    "- 2026-10-04: narration 7 to 10 minutes; narrator: reuse the saved narrator voice for now (`voice/narrators/moonlight_storyteller_1`); character voices are decided later.",
    "- Gentle ending as asked: the Wolf is silly, never touches a sheep, and runs from the bell; the sheep are found; Finn apologises and rebuilds trust.",
]
OPEN = ["- Cast style (assumption, owner to confirm): Finn and the villagers are felt-doll humans, as the title needs a boy; an all-animal cast (for example a young goat as shepherd) is possible.",
        "- Frames with the whole flock (five sheep and Daisy) and up to four people are the hardest for image models; count sheep on every review."]
REVISION = "boy_who_cried_wolf_v1-2026-10-04"
