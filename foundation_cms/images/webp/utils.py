import logging
import os
import subprocess
import tempfile

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image as PILImage
from wagtail.images.models import Filter, SourceImageIOError

logger = logging.getLogger(__name__)


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
    """
    temp_out_path = None

    try:
        with source_file.open("rb") as f, tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as temp_in:
            temp_in.write(f.read())
            temp_in.flush()

            temp_out_path = temp_in.name.replace(".gif", f"-{width}x{height}.webp")

        aspect_ratio = width / height
        vf_filter = f"crop='min(in_w,in_h*{aspect_ratio})':'min(in_h,in_w/{aspect_ratio})'," f"scale={width}:{height}"

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                temp_in.name,
                "-vf",
                vf_filter,
                "-loop",
                "0",
                "-f",
                "webp",
                "-c:v",
                "libwebp_anim",
                temp_out_path,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        with open(temp_out_path, "rb") as out_file:
            rendition_file = ContentFile(out_file.read(), name=f"{image.pk}-{spec_str}.webp")
            rendition = get_or_create_rendition(image, spec_str, rendition_file, width, height)
            cache_rendition(image, rendition, spec_str)
            return rendition

    except subprocess.CalledProcessError as e:
        logger.warning(f"WebP rendition generation failed: {e.stderr.decode()}")

    finally:
        if os.path.exists(temp_out_path or ""):
            os.remove(temp_out_path)
        if os.path.exists(temp_in.name):
            os.remove(temp_in.name)


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
