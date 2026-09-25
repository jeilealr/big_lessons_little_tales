"""Stub that shadows the container's deepspeed.

The container's deepspeed pulls in apex -> aiter, which tries to JIT-compile
HIP kernels at import time and fails (no c++ on PATH). transformers imports
deepspeed eagerly when it is importable, so this empty module takes its place.
LTX-Video never uses ZeRO, so nothing in here is ever called.
"""
__version__ = "0.0.0-stub"
