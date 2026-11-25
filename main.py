#!/usr/bin/env python3
"""Sum up 24 November 2026 world news in one image.

Stdlib only: copies the pre-rendered entry.png (drawn in-session,
1024x1024 PNG, <1 MiB) to the grader's output path. No network,
no third-party libraries, deterministic bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def out_path():
    if os.environ.get("OUTPUT_PATH"):
        return Path(os.environ["OUTPUT_PATH"])
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(base) / "entry.png"


def main():
    out = out_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out)


if __name__ == "__main__":
    main()
