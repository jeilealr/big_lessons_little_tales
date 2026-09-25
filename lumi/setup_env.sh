#!/bin/bash
# Rebuild the Python environment this repo runs in (LUMI login node, ~10 min).
# The venv sits on top of the LUMI PyTorch container; see docs/provenance.md.
set -euo pipefail
ROOT=/scratch/project_465002727/jelealro
SIF=/appl/local/containers/sif-images/lumi-pytorch-rocm-6.2.4-python-3.12-pytorch-v2.7.1.sif
VENV=$ROOT/ltx_env/venv
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

singularity exec -B /scratch,/pfs,/project "$SIF" bash -c "
set -euo pipefail
\$WITH_CONDA
python -m venv --system-site-packages $VENV
source $VENV/bin/activate
python -m pip install --upgrade pip
# LTX-Video (legacy intro scripts) plus the pins it needs; diffusers 0.39 also runs Wan 2.2
python -m pip install -e '$ROOT/LTX-Video[inference]' 'transformers==4.51.3' 'diffusers==0.39.0'
python -m pip install ftfy spandrel pyyaml
# shadow the container's deepspeed and apex (their import chain breaks; see stubs/README.md)
SITE=\$(python -c 'import site; print(site.getsitepackages()[0])')
cp -r '$HERE/stubs/deepspeed' '$HERE/stubs/apex' \"\$SITE/\"
python -c 'import diffusers, transformers; print(\"ok: diffusers\", diffusers.__version__, \"transformers\", transformers.__version__)'
"
