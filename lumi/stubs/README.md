# Import stubs

The LUMI PyTorch container ships `deepspeed`, `apex` and `aiter`. Their import
chain (`deepspeed -> apex -> aiter`) JIT-compiles HIP kernels at import time and
fails because there is no C++ compiler on PATH. `transformers` imports deepspeed
eagerly whenever it is installed, so every model import broke.

These files go into a venv's site-packages, which comes before the container's
packages on `sys.path`:

- `deepspeed/__init__.py`: an empty module (nothing here uses ZeRO)
- `apex/__init__.py`: raises ImportError, so `transformers` immediately falls
  back to its own T5LayerNorm instead of waiting ~70 s for the failed build
- `sitecustomize.py`: makes `importlib.util.find_spec()` report deepspeed, apex
  and aiter as not installed. Needed from accelerate 1.6 on, which imports real
  symbols (`DeepSpeedEngine`) from the empty deepspeed stub.

| venv | gets | installed by |
|---|---|---|
| generation (`ltx_env`, transformers 4.51) | the two stubs | `../setup_env.sh` |

A rebuilt generation venv gets the newest accelerate (`setup_env.sh` does not
pin it); if model imports then fail with "cannot import name
'DeepSpeedEngine'", copy `sitecustomize.py` into it as well.
