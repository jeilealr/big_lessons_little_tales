# Import stubs

The LUMI PyTorch container ships `deepspeed` and `apex`. Their import chain
(`deepspeed -> apex -> aiter`) JIT-compiles HIP kernels at import time and fails
because there is no C++ compiler on PATH. `transformers` imports deepspeed
eagerly whenever it is installed, so every model import broke.

These two files are copied into the venv's site-packages by `../setup_env.sh`
and shadow the container's packages:

- `deepspeed/__init__.py`: an empty module (nothing here uses ZeRO)
- `apex/__init__.py`: raises ImportError, so `transformers` immediately falls
  back to its own T5LayerNorm instead of waiting ~70 s for the failed build
