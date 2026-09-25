"""Prompts for the five keyframe-to-keyframe transitions of the TWC intro.

Lifted verbatim from the LTX-era script (legacy/ltx/generate_intro_v3.py); the
first one is the rewritten "cover hinges open" version. Each transition goes
from reference still `start` to `end` in Intro/reference_img/.
"""

SEGMENTS = [
    {
        "name": "01_book_awakens",
        "start": "1.png",
        "end": "2.png",
        "weight": 3.5,
        # Rewritten 2026-09-22: the original listed ~8 events (levitate,
        # particles, open, fan, light burst, pages tearing, vortex...) and the
        # model resolved that as an explosion/morph. One physical action in
        # order, and the cover actually hinges open (13B, 49 frames, seed+1).
        "prompt": (
            "Slow cinematic push-in on an ornate closed book resting on a wooden "
            "desk in a candlelit library. The glowing TWC emblem on the front "
            "cover pulses gently. The front cover slowly lifts by itself and "
            "swings open like a door, hinging on the spine, revealing bright "
            "pages inside. Warm golden light spills out from between the pages "
            "as the cover opens. Loose illustrated pages begin to lift out of the "
            "open book and float upward, with blue and violet magical particles "
            "gathering around it. Smooth, continuous, realistic motion. The book "
            "stays on the desk in the same position; same book, same cover "
            "design, same emblem throughout."
        ),
    },
    {
        "name": "02_page_tornado",
        "start": "2.png",
        "end": "3.png",
        "weight": 4.0,
        "prompt": (
            "The camera begins rapidly pulling backward away from the open magical "
            "book. Hundreds of illustrated manga and webtoon pages spiral outward "
            "from the book, forming a massive tunnel-shaped vortex. The book remains "
            "floating at the exact center of the vortex while becoming progressively "
            "smaller as the camera moves farther away. The loose pages rotate around "
            "the book in a powerful organized spiral, like a hurricane made entirely "
            "from illustrated stories. Bright electric blue, violet and magenta "
            "energy streams trace the circular motion of the vortex. Pages pass very "
            "close to the camera with strong natural motion blur and parallax, while "
            "distant pages remain sharper. The vortex grows enormous as the camera "
            "continues retreating through it. Maintain the same book, same magical "
            "environment and same visual identity. Epic cinematic scale, fluid camera "
            "movement, realistic flexible paper motion, deep perspective, volumetric "
            "light."
        ),
    },
    {
        "name": "03_vortex_rotation",
        "start": "3.png",
        "end": "4.png",
        "weight": 3.5,
        "prompt": (
            "Continue seamlessly from the enormous page vortex. The camera maintains "
            "approximately the same distance from the floating book while slowly "
            "orbiting around it. The book rotates smoothly in three-dimensional "
            "space, changing from the previous exterior-facing orientation until the "
            "open illustrated pages become clearly visible to the camera. The book "
            "remains centered inside the eye of the vortex. Hundreds of manga and "
            "webtoon pages continue flowing around it in a circular hurricane motion. "
            "Blue, violet and magenta energy streams follow the vortex. The loose "
            "pages contain varied fantasy illustrations and different scenes rather "
            "than repeating identical images. Strong depth and parallax as foreground "
            "pages sweep past the lens while distant pages spiral deeper into the "
            "tunnel. Smooth continuous cinematic rotation. Preserve the exact same "
            "book shape, scale and environment."
        ),
    },
    {
        "name": "04_dive_toward_stories",
        "start": "4.png",
        "end": "5.png",
        "weight": 3.5,
        "prompt": (
            "The open illustrated book remains floating at the center of the swirling "
            "page vortex. The camera pauses briefly, then begins accelerating forward "
            "toward the book. The book grows progressively larger as the camera flies "
            "through the eye of the vortex. Loose illustrated pages sweep past both "
            "sides of the camera at increasing speed, creating strong parallax and "
            "controlled motion blur. As the camera approaches, the individual "
            "illustrated panels printed across the open book become increasingly "
            "detailed and visible. The magical vortex continues spinning behind the "
            "book with intense blue, violet and magenta energy. A brilliant warm "
            "white light begins glowing from the center binding of the book and "
            "gradually becomes stronger. The camera moves extremely close to the open "
            "pages until the book fills most of the frame. Cinematic forward flight, "
            "smooth acceleration, realistic paper physics, dramatic depth of field."
        ),
    },
    {
        "name": "05_twc_reveal",
        "start": "5.png",
        "end": "6.png",
        "weight": 3.5,
        "prompt": (
            "Continue the forward camera movement directly toward the open book. The "
            "camera pushes closer and closer between the illustrated pages toward the "
            "brilliant light emerging from the center binding. The manga panels rush "
            "past the edges of the frame as the camera appears to enter the world "
            "inside the book. The central light rapidly intensifies into brilliant "
            "white, electric blue and magenta until it fills the entire screen. For a "
            "brief moment the screen becomes an almost complete luminous white-blue "
            "flash. From inside the light, the glowing TWC emblem gradually resolves "
            "into focus. The book itself is no longer visible. As the brightness "
            "fades, reveal a clean deep cosmic blue background filled with subtle "
            "blue and violet energy, tiny stars and drifting particles. A controlled "
            "number of manga and webtoon pages continue floating slowly around the "
            "outer edges of the frame, framing the logo without obscuring it. The TWC "
            "emblem remains perfectly centered, large, sharp and stable. The final "
            "composition becomes calm and elegant after the chaotic vortex. Camera "
            "movement gradually stops completely. Hold on the finished logo."
        ),
    },
]
