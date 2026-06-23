#!/usr/bin/env python3
"""Generate a video with fal.ai and save it to assets/.

Usage:
  # text → video
  python scripts/gen_video.py "slow dolly across a futuristic lab, cinematic" \
      --model kling --aspect 16:9 --duration 5 --out assets/hero.mp4

  # image → video (animate a still)
  python scripts/gen_video.py "camera pushes in, subtle motion" \
      --image assets/hero.png --model seedance --out assets/hero_anim.mp4
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
import fal          # noqa: E402
import fal_video    # noqa: E402

fal.load_env(str(ROOT / ".env"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--model", default="kling", help="kling | seedance | veo3")
    ap.add_argument("--image", help="still to animate (image→video)")
    ap.add_argument("--aspect", default="16:9", help="16:9 | 9:16 | 1:1")
    ap.add_argument("--duration", default="5", help="seconds: 5 | 10")
    ap.add_argument("--resolution", default="1080p")
    ap.add_argument("--out", default="assets/out.mp4")
    args = ap.parse_args()

    url = fal_video.generate_video(
        args.prompt,
        model=args.model,
        image=args.image,
        aspect_ratio=args.aspect,
        duration=args.duration,
        resolution=args.resolution,
    )
    print(f"✓ generated: {url}")
    out = ROOT / args.out
    n = fal.download(url, str(out))
    print(f"✓ saved {n:,} bytes → {out}")


if __name__ == "__main__":
    main()
