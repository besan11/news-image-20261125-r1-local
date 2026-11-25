"""Copy the pre-rendered entry image into the harness output directory.

The image is rendered by render.py (Pillow, local run, committed as
entry.png). This entrypoint does no rendering of its own: it only verifies
the PNG magic bytes and copies the file, so the submitted artifact is
exactly the image reviewed locally.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR not set", file=sys.stderr)
        return 1
    src = os.path.join(HERE, "entry.png")
    with open(src, "rb") as f:
        magic = f.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a valid PNG", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    print("wrote entry.png to", out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
