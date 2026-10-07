# Question to Google: Gemini API narration in Made-for-Kids YouTube videos

Status: ready to send (updated 2026-10-07: the podcast and the channel's own website were added,
the owner's details filled in). Not sent yet (2026-09-27 first draft). Record the answer here and in the
`voice.yaml` of every voice in use (`licence:` field, as in
`voice/narrators/golden_hour_storyteller_3/voice.yaml`; the story voices are
`voice/narrators/moonlight_storyteller_1/`, `voice/cast/leo/`,
`voice/cast/milo/`) once it arrives. Since 2026-10-02 the same Age
Requirements question also covers the Gemini image models used for the (deleted) v4 stills
(`docs/licensing.md`); current stills are made with ChatGPT Pro, so the question is now about TTS only.

## Where to send it

Google publishes no email address for questions about the Gemini API Terms,
so no address is invented here. The official routes, most direct first:

1. **Google AI Studio, "Send feedback"** (aistudio.google.com, while signed in
   with the account that owns the API key: the "?"/help menu, then Send
   feedback). It reaches the Gemini API team and is tied to your project.
2. **Google AI Developers Forum**, category "Gemini API"
   (https://discuss.ai.google.dev). Public, so Google staff and other
   developers can answer; do not post your API key or project id.
3. **Google Cloud Support** (only if the key's project has a paid Cloud
   support plan): a support case under "Billing / Terms".

For routes 1 and 2 use the subject and message below as they are.

Send it from the Google account that owns the API key (sign in to aistudio.google.com with it).
If that account is not jei.leal.r@gmail.com, put the key-owning address in the last line instead.

## Subject

Gemini API Terms (Age Requirements): pre-rendered TTS narration in children's videos and a podcast

## Message

Hello,

I would like to confirm that my intended use of the Gemini API is permitted
under the Gemini API Additional Terms of Service, specifically the section
"Age Requirements".

I am an adult (over 18). I produce animated fables for children and publish
them on my YouTube channel, where the videos are set as "Made for Kids". I
also plan to publish the same stories as an audio podcast (hosted on Spotify
for Creators and listed in podcast apps such as Apple Podcasts) and on a
simple static website. I use Gemini 3.8 Flash TTS (with voices designed in
Google AI Studio) to generate the narration.

How the API would be used:

- Only I call the API, from my own computer, using my own API key.
- The API generates audio files (narration). I edit them into the finished
  videos and podcast episodes myself, and then upload the finished files to
  YouTube and the podcast host.
- Viewers and listeners, including children, only watch or listen to the
  finished recordings. They never interact with the Gemini API: no website,
  app or other service sends their input to the API or shows them live API
  output. The website only shows finished pages and recordings.
- I disclose that the voices are AI-generated, both spoken at the start of
  each episode and in the descriptions.

The Age Requirements say that the Services must not be used "as part of a
website, application, or other service (collectively, 'API Clients') that is
directed towards or is likely to be accessed by individuals under the age of
18."

My questions:

1. Is producing pre-rendered narration with the Gemini API, and publishing
   it inside finished videos on a YouTube channel for children, in podcast
   episodes and on a static website, permitted under these terms? In other
   words, are a YouTube channel, a podcast and a website that only publish
   such finished recordings not considered "API Clients" under the Age
   Requirements?
2. If this use is permitted, does it make any difference whether I use the
   unpaid tier or the paid tier?
3. Are there any additional requirements (for example attribution,
   disclosure, or SynthID-related) that I should follow for this use?

Thank you for your help.

Kind regards,
[Your name]
Big Lessons, Little Tales (YouTube channel: [channel URL])
jei.leal.r@gmail.com

## Why this is asked (for the record)

- Gemini API Additional Terms, "Age Requirements" (checked 2026-09-27):
  "You must be 18 years of age or older to use the APIs. You also will not
  use the Services as part of a website, application, or other service
  (collectively, 'API Clients') that is directed towards or is likely to be
  accessed by individuals under the age of 18."
- Our reading: the restriction is about API Clients (apps/services built on
  the API that users interact with); pre-rendered audio in a video is content,
  and Google states it "won't claim ownership over that content". The wording
  "or other service" is broad enough that a written confirmation is worth
  having before relying on Gemini for a monetised children's channel.
- Fallback if the answer is no: an open-licence TTS (e.g. Chatterbox, MIT;
  the earlier experiment is in the git history before 2026-09-27).
