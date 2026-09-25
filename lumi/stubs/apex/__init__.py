"""Stub that shadows the container's apex (see deepspeed stub for why).

transformers' T5 tries `import apex` for FusedRMSNorm; the real apex drags in
aiter, which attempts a HIP JIT build and fails after ~70 s. Raising here makes
transformers fall back to its own T5LayerNorm immediately.
"""
raise ImportError("apex is stubbed out in the LTX venv (aiter JIT build is broken)")
