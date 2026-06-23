"""fal.ai video generator — text→video and image→video.

Same queue pattern as lib/fal.py (submit → poll status → fetch result), but for
the video models. Returns the fal.media-hosted MP4 URL.

Friendly model names → fal slugs (text2video / image2video pairs):

  • "kling"      → kling-video v2.5 turbo pro   (best motion + prompt adherence)
  • "seedance"   → bytedance seedance v1 pro     (cinematic, fast)
  • "veo3"       → google veo 3                  (audio + dialogue, premium)
  • "infinitalk" → talking-avatar lipsync        (image + audio → talking head)

Pricing is roughly per-second of output. veo3 ≈ premium, kling/seedance mid,
check https://fal.ai/models for live numbers before a big render.
"""
import os
import time
from pathlib import Path
from typing import Optional

import requests

from fal import _to_image_ref, load_env, download  # reuse helpers from lib/fal.py


# ── model registry ──────────────────────────────────────────────────────────
# Each model maps to its text→video and image→video queue slugs.
VIDEO_MODELS = {
    "kling": {
        "t2v": "fal-ai/kling-video/v2.5-turbo/pro/text-to-video",
        "i2v": "fal-ai/kling-video/v2.5-turbo/pro/image-to-video",
    },
    "seedance": {
        "t2v": "fal-ai/bytedance/seedance/v1/pro/text-to-video",
        "i2v": "fal-ai/bytedance/seedance/v1/pro/image-to-video",
    },
    "veo3": {
        "t2v": "fal-ai/veo3",
        "i2v": "fal-ai/veo3/image-to-video",
    },
}
DEFAULT_MODEL = "kling"
# Lipsync / talking avatar is its own thing (image + audio in, video out).
LIPSYNC_MODEL = "fal-ai/infinitalk"


def _submit_and_wait(slug: str, body: dict, timeout_seconds: int) -> dict:
    """Submit to the fal queue, poll until COMPLETED, return the result JSON.

    Video jobs are slow, so the default timeout is generous (10 min) and we poll
    every 5s instead of 3s.
    """
    key = os.environ["FAL_KEY"]
    headers = {"Authorization": f"Key {key}", "Content-Type": "application/json"}

    submit = requests.post(
        f"https://queue.fal.run/{slug}", headers=headers, json=body, timeout=60
    )
    submit.raise_for_status()
    request_id = submit.json()["request_id"]

    status_url = f"https://queue.fal.run/{slug}/requests/{request_id}/status"
    result_url = f"https://queue.fal.run/{slug}/requests/{request_id}"
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        time.sleep(5)
        s = requests.get(status_url, headers=headers, timeout=30).json()
        status = s.get("status")
        if status == "COMPLETED":
            break
        if status in ("FAILED", "ERROR"):
            raise RuntimeError(f"fal.ai video job failed: {s}")
        print(f"  … {status}", flush=True)
    else:
        raise TimeoutError(
            f"fal.ai video job {request_id} did not finish within {timeout_seconds}s"
        )

    return requests.get(result_url, headers={"Authorization": f"Key {key}"}, timeout=30).json()


def generate_video(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    image: Optional[str] = None,        # local path or URL → triggers image→video
    duration: str = "5",                # seconds (model-dependent: "5" / "10")
    aspect_ratio: str = "16:9",         # "16:9" | "9:16" | "1:1"
    resolution: str = "1080p",          # model-dependent
    negative_prompt: str = "blur, distort, low quality",
    timeout_seconds: int = 600,
) -> str:
    """Generate a video, poll until done, return the fal.media MP4 URL.

    Pass image= (a still or a fal.media URL from lib/fal.py) to animate a frame
    instead of pure text→video. Returns a URL that stays live for hours; call
    download() to keep it.
    """
    spec = VIDEO_MODELS.get(model)
    if spec is None:
        # allow a raw fal slug too
        slug = model
        body = {"prompt": prompt, "duration": duration, "aspect_ratio": aspect_ratio}
        if image:
            body["image_url"] = _to_image_ref(image)
    elif image:
        slug = spec["i2v"]
        body = {
            "prompt": prompt,
            "image_url": _to_image_ref(image),
            "duration": duration,
            "negative_prompt": negative_prompt,
        }
    else:
        slug = spec["t2v"]
        body = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "negative_prompt": negative_prompt,
        }

    print(f"[video] {model} → {slug}", flush=True)
    result = _submit_and_wait(slug, body, timeout_seconds)
    # most fal video models return {"video": {"url": ...}}
    if "video" in result:
        return result["video"]["url"]
    if "videos" in result:
        return result["videos"][0]["url"]
    raise RuntimeError(f"unexpected fal response shape: {list(result)}")


def lipsync(image: str, audio: str, *, prompt: str = "A person talking naturally, realistic expressions",
            resolution: str = "480p", num_frames: int = 145, timeout_seconds: int = 600) -> str:
    """Talking-avatar lipsync: a still portrait + an audio track → a talking video.

    image / audio — local paths or URLs. Cost ≈ $0.10/s (480p), $0.14/s (720p).
    num_frames 41-721 at 25fps drives the clip length.
    """
    body = {
        "image_url": _to_image_ref(image),
        "audio_url": audio if audio.startswith("http") else _to_image_ref(audio),
        "prompt": prompt,
        "resolution": resolution,
        "num_frames": num_frames,
        "acceleration": "regular",
    }
    result = _submit_and_wait(LIPSYNC_MODEL, body, timeout_seconds)
    if "video" in result:
        return result["video"]["url"]
    raise RuntimeError(f"unexpected lipsync response: {list(result)}")
