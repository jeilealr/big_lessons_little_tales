#!/bin/bash
# Build the image-edit venv, $BLLT_VENV_QWEN (Qwen-Image-Edit-2511,
# production/edit_image.py), on the LUMI login node, ~5 min. Its own venv
# because Qwen2.5-VL (the text encoder) needs transformers >= 4.57, while the
# Wan generation venv pins 4.51. Not run yet: edit_image.py is untested.
#   bash lumi/setup_env_qwen.sh;  BLLT_ENV=qwen lumi/run_in_container.sh python production/edit_image.py ...
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$HERE/site.sh"
VENV=$BLLT_VENV_QWEN

# The inner script is expanded twice: $VENV and $HERE here, \$... in the container.
singularity exec -B "$BLLT_BINDS" "$BLLT_SIF" bash -c "
set -euo pipefail
\$WITH_CONDA
python -m venv --system-site-packages '$VENV'
source '$VENV/bin/activate'
python -m pip install --upgrade pip
python -m pip install 'transformers==4.57.1' 'diffusers==0.39.0' accelerate pillow pyyaml
# shadow the container's deepspeed and apex, and hide them from find_spec: the
# empty deepspeed stub alone broke accelerate 1.6 in the (transformers 4.57)
# musubi venv (see stubs/README.md)
SITE=\$(python -c 'import site; print(site.getsitepackages()[0])')
cp -r '$HERE/stubs/deepspeed' '$HERE/stubs/apex' '$HERE/stubs/sitecustomize.py' \"\$SITE/\"
python -c 'import diffusers, transformers; from diffusers import QwenImageEditPlusPipeline; print(\"ok: diffusers\", diffusers.__version__, \"transformers\", transformers.__version__)'
"
