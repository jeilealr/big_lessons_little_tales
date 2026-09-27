# Source to use Gemini TTS: the google-genai venv + the owner's API key.
# The key lives outside every repo, in ~/.config/gemini/env (chmod 600),
# written by the owner; this file never contains or prints it.
source /scratch/project_465002727/jelealro/gemini_env/venv/bin/activate
if [ -r "$HOME/.config/gemini/env" ]; then
  set -a; source "$HOME/.config/gemini/env"; set +a
else
  echo "no ~/.config/gemini/env: see voice/gemini/README.md" >&2
fi
