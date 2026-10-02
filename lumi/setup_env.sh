#!/bin/bash
# Create (or update in place) the generation venv, $BLLT_VENV_GEN (LUMI login
# node, ~10 min). The venv sits on top of the LUMI PyTorch container and uses
# its PyTorch (--system-site-packages); see docs/provenance.md.
#   bash lumi/setup_env.sh
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$HERE/site.sh"
VENV=$BLLT_VENV_GEN

# The inner script is expanded twice: $VENV and $HERE here, \$... in the container.
singularity exec -B "$BLLT_BINDS" "$BLLT_SIF" bash -c "
set -euo pipefail
\$WITH_CONDA
python -m venv --system-site-packages '$VENV'
source '$VENV/bin/activate'
python -m pip install --upgrade pip
# diffusers 0.39 runs Wan 2.2; transformers 4.51 matches it. The venv folder is
# still called ltx_env (it once also served LTX-Video); the name does not matter.
python -m pip install 'transformers==4.51.3' 'diffusers==0.39.0' accelerate peft imageio imageio-ffmpeg
python -m pip install ftfy spandrel pyyaml opencv-python-headless kornia timm einops
# shadow the container's deepspeed and apex (their import chain breaks; see stubs/README.md)
SITE=\$(python -c 'import site; print(site.getsitepackages()[0])')
cp -r '$HERE/stubs/deepspeed' '$HERE/stubs/apex' \"\$SITE/\"
python -c 'import diffusers, transformers; print(\"ok: diffusers\", diffusers.__version__, \"transformers\", transformers.__version__)'
"
