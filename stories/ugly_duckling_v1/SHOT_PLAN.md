# The Ugly Duckling: shot plan and state table

43 shots, each with a start and an end still (Wan animates between them, about 5 s at 81 frames). Every shot keeps one camera setup (never a wide start with a close-up end). Ollie travels away from home left to right (pond → reedy path → lake); the seasons change with the plates (spring pond, autumn lake, winter river, spring lake and pond).

Each image's full prompt and the references to attach, in order: [`prompts/`](prompts/) or `python3 production/image_prompts.py --story ugly_duckling_v1 show <record>`.

| # | Shot | Setup (framing) | Cast | Start | End | Video action |
|---|---|---|---|---|---|---|
| 1 | `s01_pond` | `pond_plate` (empty_plate) | - | The empty farm pond in soft morning mist, the reed nest at the left | The same pond; the mist has thinned a little | Mist drifts slowly over the pond; reeds sway. |
| 2 | `s01_mama_nest` | `nest_wide` (scene_wide) | mama | Mama Duck sits on her reed nest at the left, wings fluffed over her eggs, eyes half closed and calm | Mama Duck lifts her head and looks down at her nest, listening | Mama Duck sits on her nest and lifts her head to listen. |
| 3 | `s01_ducklings_hatch` | `nest_closer` (close_two_shot) | mama, ducklings×3 | Mama Duck stands beside the nest; three cracked eggshells lie in it and three yellow ducklings tumble out, blinking | The three ducklings stand in a row on the edge of the nest, looking up at Mama Duck; one big speckled egg still lies whole in the nest | Three yellow ducklings tumble out of their shells and line up beside the one unhatched egg. |
| 4 | `s01_mama_closeup` | `mama_closeup` (dialogue_close_up) | mama | Mama Duck looks down toward the camera with loving delight: brows raised, eyes shining, beak closed in a smile | Mama Duck speaks warmly, beak slightly open, eyes soft | Mama Duck smiles with joy and speaks warmly. |
| 5 | `s01_big_egg` | `nest_closer` (close_two_shot) | mama, ducklings×3 | Mama Duck and the three ducklings lean over the one big speckled egg in the nest, waiting | A crack runs across the big egg; everyone leans closer with wide eyes | The family leans in as a crack appears in the big egg. |
| 6 | `s01_ollie_hatches` | `nest_closer` (close_two_shot) | mama, ollie, ducklings×3 | Ollie tumbles out of the big broken egg in the nest, blinking and wobbly; Mama Duck and the three ducklings look at him in surprise | Ollie stands up on his big feet in the nest, looking up shyly at Mama Duck; Mama Duck smiles warmly at him | Ollie tumbles out of the big egg, stands up wobbling, and Mama Duck smiles at him. |
| 7 | `s02_ducklings_stare` | `nest_wide` (scene_wide) | mama, ollie, ducklings×3 | The three ducklings stand in a row on the bank near x=0.45 staring at Ollie near x=0.65, one pointing a wing at his big feet; Mama Duck in the nest at the left | The ducklings giggle behind their wings; Ollie looks down at his feet | The ducklings stare and point at Ollie's big feet and giggle. |
| 8 | `s02_ollie_sad` | `pond_day_ollie_closeup` (dialogue_close_up) | ollie | Ollie looks down sadly: brows tilted up in the middle, eyes lowered and shiny, beak closed | Ollie speaks softly with the same sad face, beak slightly open | Ollie looks down sadly and speaks softly. |
| 9 | `s02_mama_comforts` | `nest_wide` (scene_wide) | mama, ollie | Mama Duck waddles over to Ollie on the bank near x=0.55 and bends her head to his, kindly | Mama Duck holds one wing around Ollie; he snuggles against her with his eyes closed | Mama Duck comforts Ollie and tucks him under her wing. |
| 10 | `s03_to_the_water` | `pond_day_wide` (scene_wide) | mama, ollie, ducklings×3 | Mama Duck walks into the water at the left edge of the pond, the three ducklings and Ollie following in a line along the bank | Mama Duck swims near x=0.40 with the three ducklings and Ollie paddling behind her in a line | Mama Duck leads her ducklings into the pond for their first swim. |
| 11 | `s03_ollie_glides` | `pond_day_wide` (scene_wide) | mama, ollie, ducklings×3 | The three ducklings splash and wobble near x=0.35; Ollie glides smoothly ahead near x=0.60, leaving a neat ripple; Mama Duck watches | Ollie glides near x=0.70, calm and graceful; the ducklings still splash; Mama Duck looks proud | The ducklings splash clumsily while Ollie glides smoothly ahead. |
| 12 | `s03_honk` | `pond_day_wide` (scene_wide) | mama, ollie, ducklings×3 | Ollie on the water near x=0.62 opens his beak in a big honk; the three ducklings turn toward him | The ducklings laugh with their wings over their beaks; Ollie looks down, embarrassed; Mama Duck looks worried | Ollie honks and the ducklings laugh at him. |
| 13 | `s03_ollie_alone` | `pond_day_ollie_closeup` (dialogue_close_up) | ollie | Ollie alone among the reeds, head low: brows tilted up, eyes shiny, one tear on his beak | Ollie closes his eyes, a second tear falling, beak closed | Ollie floats alone in the reeds as two tears fall. |
| 14 | `s04_decision` | `pond_evening_ollie_closeup` (dialogue_close_up) | ollie | Ollie looks out across the pond at sunset, thoughtful and sad: brows drawn together, eyes steady, beak closed | Ollie sets his face with quiet courage: brows level, eyes determined | Ollie thinks, then makes a brave decision. |
| 15 | `s04_leaves` | `reed_path_side` (scene_wide) | ollie | Ollie waddles along the reedy path near x=0.20, facing right, his head turned back toward the pond's glow at the left | Ollie near x=0.70, facing right, walking on into the dusk | Ollie looks back once, then waddles away along the reedy path. |
| 16 | `s05_lake` | `lake_autumn_wide` (scene_wide) | ollie | Ollie stands small on the grassy shore at the lower left, looking out over the wide autumn lake | Ollie has stepped to the water's edge, golden leaves floating past him | Ollie gazes at the great autumn lake and steps to the water's edge. |
| 17 | `s05_ollie_lake` | `lake_autumn_ollie_closeup` (dialogue_close_up) | ollie | Ollie looks around, lonely: brows tilted up, eyes searching, beak closed | Ollie speaks quietly to himself, beak slightly open, eyes lowered | Ollie looks around, lonely, and wonders aloud. |
| 18 | `s05_swans_fly` | `lake_autumn_wide` (scene_wide) | swans×2, ollie | Two white swans fly across the sky from the left near y=0.20, long necks stretched, wings wide; Ollie on the shore looks up | The two swans fly near the right side of the sky; Ollie still looks up, stretching his neck after them | Two swans fly across the autumn sky while Ollie watches from the shore. |
| 19 | `s05_ollie_watches` | `lake_autumn_ollie_closeup` (dialogue_close_up) | ollie | Ollie gazes up at the sky in wonder: brows raised, eyes wide and shining, beak slightly open | Ollie whispers his wish, eyes still on the sky, a small hopeful smile | Ollie gazes up in wonder and whispers his wish. |
| 20 | `s06_winter` | `river_wide` (scene_wide) | - | The empty frozen river in soft falling snow, the burrow glowing at the right | The same scene; a little more snow has fallen | Snow falls gently on the frozen river. |
| 21 | `s06_ollie_cold` | `river_wide` (scene_wide) | ollie | Ollie curls up on the snow bank near x=0.40, head tucked, shivering, snowflakes on his back | Same place; Ollie lifts his head a little, eyes half open, still shivering | Ollie shivers in the snow and lifts his head weakly. |
| 22 | `s06_ottie_finds` | `river_wide` (scene_wide) | ottie, ollie | Ottie pops her head out of the burrow entrance at the right, looking toward Ollie curled in the snow near x=0.40 | Ottie has scampered out onto the snow near x=0.58 and leans toward Ollie, one paw held out | Ottie pops out of her burrow and hurries to Ollie, holding out a paw. |
| 23 | `s06_ottie_closeup` | `river_ottie_closeup` (dialogue_close_up) | ottie | Ottie looks toward the camera with warm concern: brows tilted up, eyes kind, mouth open as she speaks | Ottie laughs kindly, eyes crinkled, a big friendly smile | Ottie speaks kindly, then laughs warmly. |
| 24 | `s06_ollie_shy` | `river_ollie_closeup` (dialogue_close_up) | ollie | Ollie looks up shyly: brows raised a little, eyes wide and unsure, beak slightly open | Ollie's face softens into a small, hopeful smile | Ollie looks up shyly, then smiles with hope. |
| 25 | `s07_sliding` | `river_wide` (scene_wide) | ottie, ollie | Ottie slides on her belly across the ice near x=0.35, arms out, laughing; Ollie slides beside her on his big feet near x=0.50, wings spread | Both have slid to near x=0.65, laughing together, Ollie's wings still spread | Ollie and Ottie slide across the ice together, laughing. |
| 26 | `s07_ollie_grows` | `river_wide` (scene_wide) | ottie, ollie | Ollie sits on the snow bank near x=0.45 beside Ottie near x=0.58, both watching the snow fall, Ollie stretching his neck upward | Same places; Ollie's neck is stretched tall, his wings opened wide, Ottie looking up at him with a smile | Ollie stretches his neck and opens his wings as Ottie watches. |
| 27 | `s08_spring` | `lake_spring_wide` (scene_wide) | - | The empty great lake in spring sunshine, blossoms on the trees | The same lake; a few blossoms have drifted onto the water | Blossoms drift down onto the sparkling spring lake. |
| 28 | `s08_goodbye` | `river_wide` (scene_wide) | ottie, ollie | The snow has nearly melted; Ollie stands near x=0.45 facing Ottie near x=0.60, both smiling, Ollie bowing his head in thanks | Ottie waves one paw; Ollie turns toward the right, wings slightly raised, ready to go | Ollie thanks Ottie and turns to go as she waves goodbye. |
| 29 | `s08_flies` | `lake_spring_wide` (scene_wide) | ollie_swan | Ollie the swan flies low over the spring lake from the left near x=0.15, wings wide | Ollie the swan glides down toward the water near x=0.60, wings still wide | Ollie the swan flies over the lake and glides down toward the water. |
| 30 | `s09_swans_lake` | `lake_spring_wide` (scene_wide) | swans×2 | Two adult swans glide on the lake near x=0.55 and x=0.68, necks curved gracefully | The two swans turn their heads toward the left, noticing someone arriving | Two swans glide on the lake and turn their heads. |
| 31 | `s09_ollie_nervous` | `lake_spring_ollie_closeup` (dialogue_close_up) | ollie_swan | Ollie the swan looks toward the swans off-screen, nervous: brows tilted up, eyes unsure, beak closed | Ollie the swan takes a small brave breath: brows level, eyes hopeful | Ollie looks nervous, then gathers his courage. |
| 32 | `s09_ollie_bows` | `lake_spring_wide` (scene_wide) | swans×2, ollie_swan | Ollie the swan lands softly on the water near x=0.35; the two swans near x=0.55 and x=0.68 look at him | Ollie the swan bows his long neck low toward the water; the two swans glide closer | Ollie lands on the water and bows his head as the swans come closer. |
| 33 | `s10_reflection` | `lake_spring_reflection` (close_two_shot) | ollie_swan | Ollie the swan bows over the still water; his mirror reflection below shows a white swan, both blurred by a small ripple | The ripple has calmed; the reflection is clear: the same white swan looking up at him | The ripple calms and Ollie sees his own clear reflection. |
| 34 | `s10_ollie_amazed` | `lake_spring_ollie_closeup` (dialogue_close_up) | ollie_swan | Ollie the swan is astonished: brows high, eyes wide and shining, beak slightly open | Ollie the swan's astonishment turns into a joyful smile, eyes bright | Ollie stares in astonishment, then smiles with joy. |
| 35 | `s10_swan_welcomes` | `lake_spring_swan_closeup` (dialogue_close_up) | swans | One adult swan looks kindly toward the camera: brows relaxed, eyes warm, beak closed | The swan speaks a gentle welcome, beak slightly open | An adult swan smiles kindly and speaks a gentle welcome. |
| 36 | `s10_swim_together` | `lake_spring_wide` (scene_wide) | swans×2, ollie_swan | Ollie the swan and the two swans swim side by side near x=0.40 to x=0.65, necks curved, all smiling | The three swans swim together toward the right, gliding in a line | Ollie and the swans swim away together across the lake. |
| 37 | `s11_arrives_home` | `pond_spring_wide` (scene_wide) | ollie_swan, mama, ducklings×3 | Ollie the swan glides down onto the farm pond from the right; Mama Duck and the three ducklings on the bank at the left look up | Ollie the swan floats on the pond near x=0.60; Mama Duck and the ducklings stare at him | Ollie lands on the farm pond while Mama Duck and the ducklings watch. |
| 38 | `s11_ducklings_amazed` | `pond_spring_wide` (scene_wide) | ollie_swan, mama, ducklings×3 | The three ducklings at the water's edge stare up at Ollie the swan, beaks open in amazement; Mama Duck behind them | Mama Duck steps forward to the water's edge, one wing raised to her chest | The ducklings gape in amazement and Mama Duck steps forward. |
| 39 | `s11_mama_closeup` | `pond_spring_mama_closeup` (dialogue_close_up) | mama | Mama Duck looks up with dawning recognition: brows high, eyes shining, beak open | Mama Duck smiles with proud, tender love, eyes full of happy tears | Mama Duck recognises Ollie and smiles with tender pride. |
| 40 | `s11_ollie_closeup` | `pond_spring_ollie_closeup` (dialogue_close_up) | ollie_swan | Ollie the swan looks down warmly toward the camera: brows relaxed, eyes kind, a gentle smile | Ollie the swan speaks kindly, beak slightly open, eyes soft | Ollie smiles warmly and speaks kindly. |
| 41 | `s11_ducklings_sorry` | `pond_spring_wide` (scene_wide) | ollie_swan, mama, ducklings×3 | The three ducklings stand at the water's edge with their heads bowed, sorry; Ollie the swan floats close to the bank, bending his neck toward them | Ollie the swan touches his beak gently to the nearest duckling's head; the ducklings smile up at him; Mama Duck watches happily | The ducklings say sorry and Ollie gently forgives them. |
| 42 | `s12_family` | `pond_spring_wide` (scene_wide) | ollie_swan, ottie, mama, ducklings×3 | Ollie the swan swims on the pond with the three ducklings riding on his back; Mama Duck swims beside him; Ottie splashes in the water at the right | Everyone splashes and laughs together on the sunny pond | Everyone splashes and plays together on the sunny pond. |
| 43 | `s12_end` | `pond_spring_wide` (scene_wide) | ollie_swan, ottie, mama, ducklings×3 | Ollie the swan, Mama Duck, the three ducklings and Ottie sit together on the grassy bank in the sunshine, all facing the camera and smiling | Same places; they all close their eyes in happy smiles | The whole family and Ottie sit together, smiling in the sunshine. |

## Cause-and-effect state table

| After shot | Where everyone is | Props and world state |
|---|---|---|
| s01 | spring morning: Mama Duck at the nest; three ducklings hatch, then Ollie from the big egg | eggs → shells |
| s02-s03 | Ollie teased for being different; the swimming lesson on the pond; Ollie alone in the reeds | same |
| s04 | sunset: Ollie leaves along the reedy path | Ollie no longer at the pond |
| s05 | autumn: Ollie alone at the great lake; two swans fly south overhead | same |
| s06-s07 | winter: Ottie shelters Ollie in her burrow; they slide on the ice; Ollie starts to grow | Ollie the cygnet growing |
| s08 | spring: Ollie says goodbye to Ottie and flies (now Ollie the swan) | Ollie the swan from here on |
| s09-s10 | spring lake: the swans; Ollie sees his reflection and is welcomed | same |
| s11-s12 | Ollie the swan visits the farm pond; the ducklings say sorry; everyone plays together, Ottie too | same |

## Camera setups

| Setup | Place | Framing | Size anchor (first frame made there) |
|---|---|---|---|
| `pond_plate` | the farm pond in spring morning light | empty_plate | - |
| `nest_wide` | the farm pond in spring morning light | scene_wide | s01_mama_nest_start |
| `nest_closer` | the farm pond in spring morning light | close_two_shot | s01_ducklings_hatch_start |
| `mama_closeup` | the farm pond in spring morning light | dialogue_close_up | s01_mama_closeup_start |
| `pond_day_wide` | the farm pond on a sunny afternoon | scene_wide | s03_to_the_water_start |
| `pond_day_ollie_closeup` | the farm pond on a sunny afternoon | dialogue_close_up | s02_ollie_sad_start |
| `pond_day_mama_closeup` | the farm pond on a sunny afternoon | dialogue_close_up | - |
| `pond_evening_wide` | the farm pond at sunset | scene_wide | - |
| `pond_evening_ollie_closeup` | the farm pond at sunset | dialogue_close_up | s04_decision_start |
| `reed_path_side` | the reedy path at dusk | scene_wide | s04_leaves_start |
| `lake_autumn_wide` | the great lake in autumn | scene_wide | s05_lake_start |
| `lake_autumn_ollie_closeup` | the great lake in autumn | dialogue_close_up | s05_ollie_lake_start |
| `river_wide` | the frozen river in winter | scene_wide | s06_ollie_cold_start |
| `river_ollie_closeup` | the frozen river in winter | dialogue_close_up | s06_ollie_shy_start |
| `river_ottie_closeup` | the frozen river in winter | dialogue_close_up | s06_ottie_closeup_start |
| `lake_spring_wide` | the great lake in spring | scene_wide | s08_flies_start |
| `lake_spring_reflection` | the great lake in spring | close_two_shot | s10_reflection_start |
| `lake_spring_ollie_closeup` | the great lake in spring | dialogue_close_up | s09_ollie_nervous_start |
| `lake_spring_swan_closeup` | the great lake in spring | dialogue_close_up | s10_swan_welcomes_start |
| `pond_spring_wide` | the farm pond on a sunny afternoon | scene_wide | s11_arrives_home_start |
| `pond_spring_mama_closeup` | the farm pond on a sunny afternoon | dialogue_close_up | s11_mama_closeup_start |
| `pond_spring_ollie_closeup` | the farm pond on a sunny afternoon | dialogue_close_up | s11_ollie_closeup_start |
