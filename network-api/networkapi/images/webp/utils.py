import os
import subprocess
import tempfile
import logging
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image as PILImage
from wagtail.images.models import Filter, SourceImageIOError

logger = logging.getLogger("networkapi")

def convert_gif_to_webp(source_file, output_path=None):
    """
    Converts the original GIF to a fully animated WebP and saves it to the
    `animated_webp` field.
    """
    with source_file.open("rb") as f:
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as gif_temp:
            gif_temp.write(f.read())
            gif_temp.flush()
            try:
                webp_path = output_path or gif_temp.name.replace('.gif', '.webp')
                subprocess.run(
                    ['ffmpeg', '-y', '-i', gif_temp.name, '-loop', '0', '-f', 'webp', webp_path],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                return webp_path

            except subprocess.CalledProcessError as e:
                logger.warning(f"WebP conversion failed: {e.stderr.decode()}")
                return None
            
            finally:
                os.remove(gif_temp.name)


def generate_webp_rendition(image, source_file, spec_str, width, height):
    """
    Resizes and crops the original GIF using ffmpeg to match the specified
    `fill-WxH` filter spec, then stores it as a .webp CustomRendition
    """
    with source_file.open("rb") as f:
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as temp_in:
            temp_in.write(f.read())
            temp_in.flush()

            temp_out_path = temp_in.name.replace(".gif", f"-{width}x{height}.webp")
            aspect_ratio = width / height
            vf_filter = (
                f"crop='min(in_w,in_h*{aspect_ratio})':'min(in_h,in_w/{aspect_ratio})',"
                f"scale={width}:{height}"
            )

            try:
                subprocess.run(
                    [
                        "ffmpeg", "-y",
                        "-i", temp_in.name,
                        "-vf", vf_filter,
                        "-loop", "0",
                        "-f", "webp",
                        "-c:v", "libwebp_anim",
                        temp_out_path
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
                logger.warning(f"WebP conversion failed: {e.stderr.decode()}")

            finally:
                os.remove(temp_in.name)
                if os.path.exists(temp_out_path):
                    os.remove(temp_out_path)


def serve_or_create_webp(image, spec_str, fallback_file, width=None, height=None):
    """
    Serves an existing .webp rendition if available, otherwise creates one
    from the provided fallback file (`animated_webp`).
    Used for 'original-webp' and fallback filters that don’t require resizing.
    """
    existing = image.renditions.filter(filter_spec=spec_str).first()
    if existing and existing.file.name.endswith(".webp"):
        return existing

    if (
        not fallback_file or
        not fallback_file.name or
        not default_storage.exists(fallback_file.name)
    ):
        raise SourceImageIOError(f"WebP fallback file not ready: {fallback_file}")

    with fallback_file.open("rb") as f:
        rendition_file = ContentFile(f.read(), name=f"{image.pk}-{spec_str}.webp")
        rendition = get_or_create_rendition(image, spec_str, rendition_file, width, height)
        cache_rendition(image, rendition, spec_str)
        return rendition


def cache_rendition(image, rendition, spec_str):
    """
    Mimics Wagtail’s internal rendition caching.
    """
    filter_obj = Filter(spec=spec_str.replace("-webp", ""))
    Rendition = image.get_rendition_model()
    cache_key = Rendition.construct_cache_key(
        image, filter_obj.get_cache_key(image), spec_str
    )
    Rendition.cache_backend.set(cache_key, rendition)


def get_webp_spec(spec_str):
    return "original-webp" if spec_str == "original" else (
        f"{spec_str}-webp" if not spec_str.endswith("-webp") else spec_str
    )

def get_or_create_rendition(image, spec_str, file, width, height):
    """
    Creates or returns a Wagtail rendition with a unique key (spec + focal point).
    Used by both resized and fallback .webp handlers.
    """
    return image.renditions.get_or_create(
        filter_spec=spec_str,
        focal_point_key=image.get_focal_point_key(),
        defaults={
            'file': file,
            'width': width,
            'height': height,
        }
    )[0]

def is_animated_webp(file):
    """
    Will check if the webp is animated. If it is then we can consider it as the
    raw animated_webp file.
    """
    try:
        with PILImage.open(file) as im:
            return im.format == "WEBP" and getattr(im, "is_animated", False)
    except Exception:
        return False
