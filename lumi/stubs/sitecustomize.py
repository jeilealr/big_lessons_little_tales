"""Make deepspeed, apex and aiter look NOT INSTALLED in this venv.

The LUMI PyTorch container ships them, but importing them JIT-compiles HIP
kernels and fails (no C++ compiler on PATH). transformers and accelerate
decide whether to import them with importlib.util.find_spec(); an empty stub
module was enough for transformers 4.51, but accelerate 1.6 then imports real
symbols from it ("cannot import name 'DeepSpeedEngine'"). Reporting the
packages as absent lets every library skip them by its own logic. Nothing
here uses ZeRO, apex or aiter.
"""
import importlib.util as _util

_HIDDEN = {"deepspeed", "apex", "aiter"}
_find_spec = _util.find_spec


def _find_spec_hiding(name, package=None):
    if name.split(".")[0] in _HIDDEN:
        return None
    return _find_spec(name, package)


_util.find_spec = _find_spec_hiding
