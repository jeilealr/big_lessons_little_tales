# Question to Google: Gemini API narration in Made-for-Kids YouTube videos

Status: draft, not sent (2026-09-27). Record the answer here and in
`voice/gemini/cast/narrator/voice.yaml` (`licence:`) once it arrives.

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

## Subject

Gemini API Terms (Age Requirements): pre-rendered TTS narration in Made-for-Kids YouTube videos

## Message

Hello,

I would like to confirm that my intended use of the Gemini API is permitted
under the Gemini API Additional Terms of Service, specifically the section
"Age Requirements".

I am an adult (over 18). I produce animated fables for children and publish
them on my YouTube channel, where the videos are set as "Made for Kids". I
would like to use Gemini 3.8 Flash TTS (with a voice designed in Google AI
Studio) to generate the narration for these videos.

How the API would be used:

- Only I call the API, from my own computer, using my own API key.
- The API generates audio files (narration). I edit them into the finished
  videos myself, and then upload the finished videos to YouTube.
- Viewers, including children, only watch the finished videos. They never
  interact with the Gemini API, and there is no website, app or other service
  that sends their input to the API or shows them live API output.
- I disclose in the video description that AI tools were used.

The Age Requirements say that the Services must not be used "as part of a
website, application, or other service (collectively, 'API Clients') that is
directed towards or is likely to be accessed by individuals under the age of
18."

My questions:

1. Is producing pre-rendered narration with the Gemini API, and publishing
   it inside finished videos on a YouTube channel for children, permitted
   under these terms? In other words, is a YouTube channel that shows such
   videos not considered an "API Client" under the Age Requirements?
2. If this use is permitted, does it make any difference whether I use the
   unpaid tier or the paid tier?
3. Are there any additional requirements (for example attribution,
   disclosure, or SynthID-related) that I should follow for this use?

Thank you for your help.

Kind regards,
[Your name]
[Channel name and URL]
[Email address of the Google account that owns the API key]

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
- Fallback if the answer is no: Chatterbox (MIT) voices in `voice/`
  (paused, not deleted).
