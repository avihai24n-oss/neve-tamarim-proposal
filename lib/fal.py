"""fal.ai image generator — supports two models:

  • "gpt-image-2"    → openai/gpt-image-2          (sizes via image_size)
  • "nano-banana-2"  → fal-ai/nano-banana-2/edit   (Gemini 3.1 Flash Image)

Both run through fal.ai's queue endpoint (submit → poll status → fetch result)
and return the fal.media-hosted image URL. Instagram's publish API can read
those URLs directly, so the carousel flow never has to re-host.

Pricing (per output image, nano-banana-2): 0.5K=$0.06 · 1K=$0.08 · 2K=$0.12 · 4K=$0.16
gpt-image-2 is billed per request by fal; see https://fal.ai/models/openai/gpt-image-2
"""
import base64
import mimetypes
import os
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import requests


def load_env(env_path: str = ".env") -> None:
    """Minimal .env loader (no dependency on python-dotenv)."""
    p = Path(env_path)
    if not p.exists():
        return
    for ln in p.read_text().splitlines():
        if "=" in ln and not ln.startswith("#"):
            k, v = ln.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


# ── model registry ──────────────────────────────────────────────────────────
# Friendly name → fal queue slug.
MODELS = {
    "gpt-image-2": "openai/gpt-image-2",
    "nano-banana-2": "fal-ai/nano-banana-2/edit",
}
# Image-to-image (reference) endpoints, used when reference_images are supplied.
EDIT_MODELS = {
    "gpt-image-2": "openai/gpt-image-2/edit",
    "nano-banana-2": "fal-ai/nano-banana-2/edit",
}
DEFAULT_MODEL = "gpt-image-2"

# gpt-image-2 /edit takes named size presets rather than width/height.
GPT_SIZE_PRESET = {
    "1:1": "square_hd", "4:5": "portrait_4_3", "3:4": "portrait_4_3",
    "9:16": "portrait_16_9", "16:9": "landscape_16_9", "4:3": "landscape_4_3",
}


def _to_image_ref(path_or_url: str) -> str:
    """Pass through an http(s) URL; turn a local file into a base64 data URI.

    fal's edit endpoints accept either, so local reference images (e.g. a photo
    of yourself) never need a separate upload step.
    """
    if path_or_url.startswith(("http://", "https://", "data:")):
        return path_or_url
    p = Path(path_or_url).expanduser()
    if not p.exists():
        raise FileNotFoundError(f"reference image not found: {p}")
    mime = mimetypes.guess_type(str(p))[0] or "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

# nano-banana-2's /edit endpoint requires at least one reference image, even for
# pure text→image. A neutral blank lets the prompt drive the result entirely.
DEFAULT_BLANK_REF = (
    "https://storage.googleapis.com/falserverless/example_inputs/nano-banana-edit-input.png"
)

# Instagram carousel images: 1:1 (1080×1080) or 4:5 (1080×1350).
DEFAULT_SIZE = {"width": 1024, "height": 1024}   # gpt-image-2
DEFAULT_QUALITY = "medium"                        # gpt-image-2
DEFAULT_ASPECT_RATIO = "1:1"                       # nano-banana-2
DEFAULT_RESOLUTION = "1K"                          # nano-banana-2


def _resolve_slug(model: str) -> str:
    """Accept a friendly name ('nano-banana-2') or a raw fal slug."""
    return MODELS.get(model, model)


def _build_body(
    slug: str,
    prompt: str,
    *,
    size: Optional[dict],
    quality: str,
    aspect_ratio: str,
    resolution: str,
    image_urls: Optional[list[str]],
    num_images: int,
    thinking_level: str,
) -> dict:
    if slug == MODELS["nano-banana-2"]:
        return {
            "prompt": prompt,
            "image_urls": image_urls or [DEFAULT_BLANK_REF],
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "num_images": num_images,
            "output_format": "png",
            "thinking_level": thinking_level,
        }
    # gpt-image-2 (and any other openai/* slug)
    return {
        "prompt": prompt,
        "image_size": size or DEFAULT_SIZE,
        "quality": quality,
        "num_images": num_images,
        "output_format": "png",
    }


def _submit_and_wait(slug: str, body: dict, timeout_seconds: int) -> dict:
    """Submit to the fal queue, poll until COMPLETED, return the result JSON."""
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
        time.sleep(3)
        s = requests.get(status_url, headers=headers, timeout=30).json()
        status = s.get("status")
        if status == "COMPLETED":
            break
        if status in ("FAILED", "ERROR"):
            raise RuntimeError(f"fal.ai job failed: {s}")
    else:
        raise TimeoutError(
            f"fal.ai job {request_id} did not complete within {timeout_seconds}s"
        )

    return requests.get(result_url, headers={"Authorization": f"Key {key}"}, timeout=30).json()


def generate_image(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    # gpt-image-2 knobs
    size: Optional[dict] = None,
    quality: str = DEFAULT_QUALITY,
    # nano-banana-2 knobs
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    image_urls: Optional[list[str]] = None,
    thinking_level: str = "high",
    # reference images (image-to-image) — local paths or URLs
    reference_images: Optional[list[str]] = None,
    # shared
    num_images: int = 1,
    timeout_seconds: int = 180,
) -> str:
    """Submit a prompt to fal.ai, poll until done, return the first image URL.

    model — "gpt-image-2" (default) or "nano-banana-2", or a raw fal slug.
    reference_images — optional local paths/URLs (e.g. a photo of yourself). When
        given, the call routes to the model's image-to-image /edit endpoint so the
        output is conditioned on those references.
    The returned URL is fal.media-hosted and stays live for hours — long enough
    for Instagram to fetch and publish it.
    """
    refs = [_to_image_ref(r) for r in (reference_images or [])]

    if refs:
        slug = EDIT_MODELS.get(model, _resolve_slug(model))
        if slug == MODELS["nano-banana-2"]:
            body = _build_body(
                slug, prompt, size=size, quality=quality,
                aspect_ratio=aspect_ratio, resolution=resolution,
                image_urls=refs, num_images=num_images, thinking_level=thinking_level,
            )
        else:  # gpt-image-2/edit — preset size + image_urls references
            body = {
                "prompt": prompt,
                "image_urls": refs,
                "image_size": GPT_SIZE_PRESET.get(aspect_ratio, "square_hd"),
                "quality": quality,
                "num_images": num_images,
                "output_format": "png",
            }
    else:
        slug = _resolve_slug(model)
        body = _build_body(
            slug, prompt, size=size, quality=quality,
            aspect_ratio=aspect_ratio, resolution=resolution,
            image_urls=image_urls, num_images=num_images, thinking_level=thinking_level,
        )

    result = _submit_and_wait(slug, body, timeout_seconds)
    return result["images"][0]["url"]


def generate_carousel(prompts: list[str], **kwargs) -> list[str]:
    """Generate one image per prompt; return list of fal.media-hosted URLs.

    Instagram carousels support 2–10 images, so len(prompts) must be in [2, 10].
    Pass model=/aspect_ratio=/etc. through **kwargs to control generation.
    """
    if not 2 <= len(prompts) <= 10:
        raise ValueError(f"Instagram carousels require 2–10 images, got {len(prompts)}")
    urls: list[str] = []
    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] generating...", flush=True)
        urls.append(generate_image(prompt, **kwargs))
        print(f"  ✓ {urls[-1][:80]}...", flush=True)
    return urls


def download(url: str, dest: str) -> int:
    """Download a fal.media URL to a local path. Returns bytes written.

    fal.media URLs expire after a while — download right away if you want to keep
    the image (Instagram publishing reads the URL directly, so it's optional there).
    """
    p = Path(dest)
    p.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "carousel-creator/1.0"})
    with urlopen(req, timeout=60) as r:
        data = r.read()
    p.write_bytes(data)
    return len(data)


def _ext_from_url(url: str, fallback: str = ".png") -> str:
    return Path(urlparse(url).path).suffix or fallback
