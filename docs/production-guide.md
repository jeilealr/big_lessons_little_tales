# Producing a felt-animal fable: the complete guide

How to go from a story idea to a finished, consistent, monetisable children's
video with this repo. Worked example throughout: **The Lion and the Mouse**
(`stories/lion_and_mouse/story.yaml`). Narration, voices and sound are done
outside this repo (ElevenLabs); here we make the pictures, plus optional
background ambience.

## 0. What "professional" means here

A children's fable works when a child can follow it without effort: the same
characters, in recognisable places, doing one clear thing at a time, towards a
kind message. Every technical rule below serves that.

It is also what the platform pays for. YouTube's **quality principles for
kids and family content** reward videos that model *"Looking after yourself
and others"* (kindness, good friendship) and *"Creativity, play, and a sense of
imagination"* (storytelling), and demote content that is *"Hard to follow"*
(jumbled storylines) or *"Sensational or misleading"* ([YouTube Help][yt-kids]).
Channels with a strong focus on low-quality made-for-kids content can be
suspended from the Partner Program ([YouTube Blog][yt-kids-blog]).

Separately, YouTube's **inauthentic-content policy** (renamed from
"repetitious content" in July 2025, clarified in July 2026) removes
monetisation from *"generic, repetitive, or template-based"* videos made with
minimal variation using AI, from *"off-putting or distressing"* content, and
from AI personas on sensitive topics ([TechCrunch][tc-2026], [Tubefilter][tf-2026]).
YouTube's own example of distressing content is **animals in distress followed
by a rescue**, which is the shape of many fables. AI assistance itself is
fine when it *"enhances creativity"* and the result is high quality.

What this means in practice:

| Rule | Why |
|---|---|
| Every story is original in its telling: your script, your direction, your characters | template-made, look-alike videos are what the inauthentic-content policy targets |
| Characters never change appearance between shots | inconsistency makes a story "hard to follow" |
| Peril is brief, mild and resolved kindly; never the thumbnail | "animals in distress then rescue" is YouTube's own example of distressing content |
| No logos, brands, products, recognisable third-party characters | "heavily promotional", "strange use of children's characters" |
| Mark the videos *Made for kids* | required for child-directed content (it disables personalised ads and comments) |

**AI disclosure.** YouTube requires the *altered or synthetic content* label only
for *realistic* content that could be mistaken for a real person, place or
event; clearly unrealistic or animated content is exempt ([YouTube Blog][yt-ai]).
Felt stop-motion animals are clearly unrealistic, so the label is not required;
a line in the description ("Animated with the help of AI tools") is honest and
costs nothing.

## 1. The pipeline at a glance

```
story.yaml ──► design ──► characters ──► locations ──► shot plan ──► render ──► post ──► edit
 (bible)      (stills)   (canonical,    (plates)      (one action   (Wan I2V   (RIFE,    (ElevenLabs
                          turnarounds,                 per shot)     from key-  ESRGAN,   narration,
                          LoRA)                                      frames)    grade)    music, cut)
```

| Stage | Tool | Output |
|---|---|---|
| Story bible | `stories/<slug>/story.yaml` | style, characters, locations, scenes: the only place story facts live |
| Design | `production/design.py candidates / sheet / pick` | candidate stills; the chosen **canonical** still per character and location |
| Character pack | `character/character.py` (turns, angles, dataset) | a pose/angle library, and the LoRA dataset |
| LoRA | `lora/` (musubi-tuner) | a small model per main character |
| Shots | Wan 2.2 image-to-video from keyframes | 5 s clips, one action each |
| Post | `twc/post.py` | 1080p30, learned interpolation and upscaling, grade |
| Edit | your editor + ElevenLabs | the finished episode |

## 2. The story bible (`story.yaml`)

Everything the story needs is written once, here, and pasted verbatim by the
tools into every prompt:

- **style** and **negative**: the look of the whole film. Never change them
  mid-story.
- **characters**: a frozen **sheet** each (the exact description), a trigger
  word for the LoRA, personality, and relative **scale** (Milo is 1/6 of Leo).
- **locations**: a sheet each; every shot set there starts from the same plate.
- **scenes**: the author's text, then the shot breakdown.

Writing a character sheet:
- Name the details that must never change: colours, materials, eye style, the
  one distinctive feature (Leo's burnt-orange mane, Milo's oversized pink ears).
- Materials, not photographic words: "needle-felted", "stitched", "wool".
- One sheet per character, frozen. Change the *action*, never the sheet.

(Sections 3 to 8 follow as each stage is validated on The Lion and the Mouse.)

## Sources

- [yt-kids]: YouTube Help, *Best practices for kids & family content*, https://support.google.com/youtube/answer/10774223
- [yt-kids-blog]: YouTube Blog, *Our responsibility approach to protecting kids and families on YouTube*, https://blog.youtube/news-and-events/our-responsibility-approach-protecting-kids-and-families-youtube/
- [tc-2026]: TechCrunch, *YouTube clarifies policies around AI slop and upsetting videos* (20 Jul 2026), https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/
- [tf-2026]: Tubefilter, *YouTube inauthentic content monetization policy update* (13 Jul 2026), https://www.tubefilter.com/2026/07/13/youtube-inauthentic-content-monetization-policy-update/
- [yt-ai]: YouTube Blog, *How we're helping creators disclose altered or synthetic content*, https://blog.youtube/news-and-events/disclosing-ai-generated-content/

[yt-kids]: https://support.google.com/youtube/answer/10774223
[yt-kids-blog]: https://blog.youtube/news-and-events/our-responsibility-approach-protecting-kids-and-families-youtube/
[tc-2026]: https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/
[tf-2026]: https://www.tubefilter.com/2026/07/13/youtube-inauthentic-content-monetization-policy-update/
[yt-ai]: https://blog.youtube/news-and-events/disclosing-ai-generated-content/
