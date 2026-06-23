#!/usr/bin/env python3
"""Generate a single image with fal.ai and save it to assets/.

Usage:
  python scripts/gen_image.py "a cinematic product shot, dramatic light" \
      --model gpt-image-2 --aspect 16:9 --out assets/hero.png

  # image-to-image (use a reference photo):
  python scripts/gen_image.py "same person, neon city background" \
      --ref ~/Desktop/me.jpg --model nano-banana-2 --aspect 9:16
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import fal  # noqa: E402

fal.load_env(str(Path(__file__).resolve().parent.parent / ".env"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--model", default="gpt-image-2", help="gpt-image-2 | nano-banana-2")
    ap.add_argument("--aspect", default="16:9", help="1:1 | 4:5 | 9:16 | 16:9 | 4:3")
    ap.add_argument("--resolution", default="2K", help="nano-banana-2: 0.5K|1K|2K|4K")
    ap.add_argument("--quality", default="high", help="gpt-image-2: low|medium|high")
    ap.add_argument("--ref", action="append", help="reference image path/URL (repeatable)")
    ap.add_argument("--out", default="assets/out.png")
    args = ap.parse_args()

    url = fal.generate_image(
        args.prompt,
        model=args.model,
        aspect_ratio=args.aspect,
        resolution=args.resolution,
        quality=args.quality,
        reference_images=args.ref,
    )
    print(f"✓ generated: {url}")
    out = Path(__file__).resolve().parent.parent / args.out
    n = fal.download(url, str(out))
    print(f"✓ saved {n:,} bytes → {out}")


if __name__ == "__main__":
    main()
