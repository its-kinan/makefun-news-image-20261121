#!/usr/bin/env python3
"""news-image-20261121 entry: copy the built front page to /output/entry.png.

The image (entry.png beside this file) is the agent-built front page for
21 November 2026: masthead with the date plus four stories — the Banda Sea
M6.8 quake, a tanker hit off Oman in the Strait of Hormuz, Denmark pushing
EU travel curbs on Russians, COP31 running overtime. The program only copies bytes, so both grader runs
write identical output. Outside the grader, MAKEFUN_OUTPUT_DIR stands in
for /output:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def check_png(path):
    """Refuse to ship a file the gate would reject: bad magic, oversize,
    or over 1024 px a side. A corrupt copy fails silently in v1; here it
    fails loudly before anything is written."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png: not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png: %d bytes, over the 1 MiB cap" % size)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit("entry.png: %dx%d, over 1024 px a side"
                         % (width, height))
    return width, height, size


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(HERE, "entry.png")
    width, height, size = check_png(src)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    print("entry.png %dx%d %d bytes -> %s"
          % (width, height, size, out_dir))


if __name__ == "__main__":
    main()
