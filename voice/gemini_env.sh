# Source to use Gemini TTS (no container, no GPU; any login-node shell):
#   source voice/gemini_env.sh
# Activates the google-genai venv and exports the owner's API key. The key lives
# outside every repo, in ~/.config/gemini/env (chmod 600), written by the owner;
# this file never contains or prints it.
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/../lumi" && pwd)/site.sh"
source "$FELTWILLOW_VENV_GEMINI/bin/activate" || { echo "no venv at $FELTWILLOW_VENV_GEMINI" >&2; return 1; }
if [ -r "$HOME/.config/gemini/env" ]; then
  set -a; source "$HOME/.config/gemini/env"; set +a
else
  echo "no ~/.config/gemini/env: see voice/README.md" >&2
fi
