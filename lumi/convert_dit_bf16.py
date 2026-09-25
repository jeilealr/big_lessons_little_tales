#!/usr/bin/env python3
"""Convert the ComfyUI-repackaged Wan 2.2 experts from fp16 to bf16, streaming.

musubi-tuner ties the training precision to the weight dtype: fp16 weights
require --mixed_precision fp16, which its own code notes can produce NaNs. The
MI250X runs bf16 natively, so we train in bf16 on converted weights (fp16 ->
bf16 keeps the range and drops mantissa bits to bf16 precision, the dtype Wan
was trained in).

Streams one tensor at a time instead of memory-mapping the 28 GB file (the
login node's per-user memory limit refused the mmap). fp16 and bf16 are both
2 bytes, so every tensor keeps its size and offset; only the header's dtype
strings change. Peak memory = the largest single tensor.
"""
import json
import struct
import sys
from pathlib import Path

import numpy as np
import torch

for src in map(Path, sys.argv[1:]):
    dst = src.with_name(src.name.replace("_fp16", "_bf16"))
    if dst.is_file():
        print("exists", dst); continue
    tmp = dst.with_suffix(".partial")
    with open(src, "rb") as fin:
        (hlen,) = struct.unpack("<Q", fin.read(8))
        header = json.loads(fin.read(hlen))
        base = 8 + hlen
        converted = 0
        for key, info in header.items():
            if key != "__metadata__" and info["dtype"] == "F16":
                info["dtype"] = "BF16"; converted += 1
        new_header = json.dumps(header, separators=(",", ":")).encode()
        new_header += b" " * ((8 - len(new_header) % 8) % 8)     # keep 8-byte alignment
        items = sorted(((k, v) for k, v in header.items() if k != "__metadata__"),
                       key=lambda kv: kv[1]["data_offsets"][0])
        with open(tmp, "wb") as fout:
            fout.write(struct.pack("<Q", len(new_header))); fout.write(new_header)
            written = 0
            for key, info in items:
                start, end = info["data_offsets"]
                assert start == written, f"gap before {key}"
                fin.seek(base + start)
                raw = fin.read(end - start)
                if info["dtype"] == "BF16":           # was F16 in the source
                    t = torch.from_numpy(np.frombuffer(raw, dtype=np.float16).copy())
                    raw = t.to(torch.bfloat16).view(torch.int16).numpy().tobytes()
                fout.write(raw); written += len(raw)
    tmp.rename(dst)
    print(f"{src.name} -> {dst.name}: {len(items)} tensors, {converted} fp16 -> bf16", flush=True)
