import logging
import os
import subprocess
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image as PILImage
from wagtail.images.models import Filter, SourceImageIOError

logger = logging.getLogger(__name__)


# Storage prefix the conversion Lambda writes converted GIFs to. Mirrors the
# `animated_webp` field's upload_to, and must stay in step with the Lambda.
CONVERTED_WEBP_PREFIX = "images/converted_webp/"


def derive_webp_name(source_name):
    """
    Storage key the conversion Lambda produces for a given source file.

    The Lambda derives the same key from the S3 object key in its event, and neither
    side consults the database.

    AWS_LOCATION environment variable is not included: the storage backend applies
    that prefix itself, so names handled here are always relative to it.
    """
    stem = os.path.splitext(os.path.basename(source_name))[0]
    return f"{CONVERTED_WEBP_PREFIX}{stem}.webp"


def converted_webp_exists(name):
    """
    Results are cached to keep a page of GIFs from issuing one S3 HEAD per
    image per render.

    Never raises an error: a storage failure reads as "not ready", and the caller falls
    back to serving the unconverted GIF.
    """
    cache_key = f"converted-webp-exists:{name}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        exists = default_storage.exists(name)
    except Exception as e:
        logger.warning(f"Could not check for converted WebP {name}: {e}")
        return False

    ttl = getattr(settings, "GIF_WEBP_FOUND_CACHE_SECONDS", 3600)
    if not exists:
        ttl = getattr(settings, "GIF_WEBP_MISSING_CACHE_SECONDS", 30)
    cache.set(cache_key, exists, ttl)
    return exists


def is_animated_webp(file):
    """
    Check if the provided file is an animated WebP.
    """
    try:
        with PILImage.open(file) as im:
            return im.format == "WEBP" and getattr(im, "is_animated", False)
    except Exception:
        return False


def get_custom_webp_spec(spec_str):
    """
    Appends '-webp' to the filter spec for internal tracking and cache uniqueness.
    """
    return (
        "original-webp"
        if spec_str == "original"
        else (f"{spec_str}-webp" if not spec_str.endswith("-webp") else spec_str)
    )


def get_or_create_rendition(image, spec_str, file, width, height):
    """
    Creates or retrieves a rendition with a unique filter + focal point combo.
    """
    return image.renditions.get_or_create(
        filter_spec=spec_str,
        focal_point_key=image.get_focal_point_key(),
        defaults={
            "file": file,
            "width": width,
            "height": height,
        },
    )[0]


def cache_rendition(image, rendition, spec_str):
    """
    Caches the rendition in Wagtail’s backend using the normalized spec.
    """
    filter_obj = Filter(spec=spec_str.replace("-webp", ""))
    Rendition = image.get_rendition_model()
    cache_key = Rendition.construct_cache_key(image, filter_obj.get_cache_key(image), spec_str)
    Rendition.cache_backend.set(cache_key, rendition)


def _run_ffmpeg(args, description):
    """
    Run ffmpeg with a hard timeout.

    Without one, a runaway encode hangs the worker until the gunicorn arbiter
    kills it, which orphans the ffmpeg child and leaves it consuming memory
    after the request is gone.

    Returns True on success, False on any failure (logged, never raised).
    """
    timeout = getattr(settings, "GIF_CONVERSION_TIMEOUT", 20)
    try:
        subprocess.run(
            args,
            check=True,
            timeout=timeout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.TimeoutExpired:
        logger.warning(f"{description} timed out after {timeout}s and was killed")
        return False
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode(errors="replace") if e.stderr else ""
        logger.warning(f"{description} failed: {stderr}")
        return False
    except FileNotFoundError:
        logger.warning(f"{description} failed: ffmpeg is not installed")
        return False


def convert_gif_to_webp(source_file, output_path=None):
    """
    Converts a GIF to an animated WebP using ffmpeg.
    Returns the output path on success, or None on failure.
    """
    return _convert_to_webp_via_ffmpeg(source_file, output_path, input_suffix=".gif")


def _convert_to_webp_via_ffmpeg(source_file, output_path=None, input_suffix=".webp"):
    """
    Generic wrapper around ffmpeg to convert animated image sources to WebP.
    """
    temp_in_path = None
    temp_out_path = None

    try:
        with source_file.open("rb") as f, tempfile.NamedTemporaryFile(delete=False, suffix=input_suffix) as temp_in:
            temp_in.write(f.read())
            temp_in.flush()
            temp_in_path = temp_in.name

        temp_out_path = output_path or tempfile.NamedTemporaryFile(delete=False, suffix=".webp").name

        subprocess.run(
            ["ffmpeg", "-y", "-i", temp_in_path, "-loop", "0", "-f", "webp", temp_out_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return temp_out_path

    except subprocess.CalledProcessError as e:
        logger.warning(f"WebP conversion failed: {e.stderr.decode()}")
        return None

    finally:
        if temp_in_path and os.path.exists(temp_in_path):
            os.remove(temp_in_path)


def generate_webp_rendition(image, source_file, spec_str, width, height):
    """
    Resizes and crops the input (GIF) to the requested size and saves as animated WebP.

    Returns None if the conversion fails; callers must handle that and fall back
    to serving the unconverted source.
    """
    temp_in_path = None
    temp_out_path = None

    try:
        with source_file.open("rb") as f, tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as temp_in:
            temp_in.write(f.read())
            temp_in.flush()

            temp_in_path = temp_in.name
            temp_out_path = temp_in_path.replace(".gif", f"-{width}x{height}.webp")

        aspect_ratio = width / height
        vf_filter = f"crop='min(in_w,in_h*{aspect_ratio})':'min(in_h,in_w/{aspect_ratio})'," f"scale={width}:{height}"

        args = [
            "ffmpeg",
            "-y",
            "-i",
            temp_in_path,
            "-vf",
            vf_filter,
            "-loop",
            "0",
            "-f",
            "webp",
            "-c:v",
            "libwebp_anim",
            temp_out_path,
        ]

        if not _run_ffmpeg(args, f"WebP rendition generation ({spec_str})"):
            return None

        with open(temp_out_path, "rb") as out_file:
            rendition_file = ContentFile(out_file.read(), name=f"{image.pk}-{spec_str}.webp")
            rendition = get_or_create_rendition(image, spec_str, rendition_file, width, height)
            cache_rendition(image, rendition, spec_str)
            return rendition

    finally:
        # Both names stay None if source_file.open() raised. Referencing
        # temp_in.name here used to throw NameError over the top of the real error.
        if temp_out_path and os.path.exists(temp_out_path):
            os.remove(temp_out_path)
        if temp_in_path and os.path.exists(temp_in_path):
            os.remove(temp_in_path)


def serve_or_create_webp(image, spec_str, fallback_file, width=None, height=None):
    """
    Returns an existing .webp rendition if available, otherwise creates one from
    the fallback_file (usually image.animated_webp).
    """
    existing = image.renditions.filter(filter_spec=spec_str).first()
    if existing and existing.file.name.endswith(".webp"):
        return existing

    if not fallback_file or not fallback_file.name or not default_storage.exists(fallback_file.name):
        raise SourceImageIOError(f"WebP fallback file not ready: {fallback_file}")

    with fallback_file.open("rb") as f:
        rendition_file = ContentFile(f.read(), name=f"{image.pk}-{spec_str}.webp")
        rendition = get_or_create_rendition(image, spec_str, rendition_file, width, height)
        cache_rendition(image, rendition, spec_str)
        return rendition
