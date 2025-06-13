import hashlib
import os
import re

from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.functional import cached_property
from wagtail.images import get_image_model_string
from wagtail.images.models import (
    AbstractImage,
    AbstractRendition,
    Filter,
    Image,
    SourceImageIOError,
)

from .webp import utils as webp_utils


# The custom image model for the Foundation site
class FoundationCustomImage(AbstractImage):

    # Add an animated_webp field to the Image model, where webp versions of
    # .gif files are stored and linked to the image.
    animated_webp = models.FileField(upload_to="images/converted_webp/", blank=True, null=True)

    admin_form_fields = Image.admin_form_fields + ("animated_webp",)

    @cached_property
    def animated_webp_ready(self):
        if not self.pk:
            return None  # Not yet saved, can't safely assign
        if not self.animated_webp and self.file.name.lower().endswith(".webp"):
            if webp_utils.is_animated_webp(self.file):
                self.animated_webp = self.file
                self.save(update_fields=["animated_webp"])
        return self.animated_webp

    class Meta:
        app_label = "images"

    def save(self, *args, **kwargs):
        """
        Save the image the wagtail way then extend to generate a .webp file if the
        image is a gif.
        """

        super().save(*args, **kwargs)

        # A temporary flag for migrate_legacy_images.py to skip the webp conversion
        skip_webp = getattr(self, "_skip_webp", False)

        # If it's a .gif, convert a copy to .webp and save that to animated_webp.
        if not skip_webp and self.file.name.lower().endswith((".gif")) and not self.animated_webp:
            webp_path = webp_utils.convert_gif_to_webp(self.file)
            if webp_path:
                with open(webp_path, "rb") as f:
                    self.animated_webp.save(os.path.basename(webp_path), ContentFile(f.read()), save=False)
                self.save(update_fields=["animated_webp"])

    def get_rendition(self, *args, **kwargs):
        """
        Main Wagtail image rendition entrypoint.
        If image is a GIF with an animated WebP version and no forced format, attempts:
        - `original` → use 'original-webp' rendition
        - `fill-WxH` → create resized animated WebP
        - fallback → serve original .animated_webp
        Otherwise falls back to Wagtail default behavior.
        """
        filter_spec = args[0] if args else kwargs.get("filter_spec") or kwargs.get("filter")
        spec_str = filter_spec.spec if isinstance(filter_spec, Filter) else str(filter_spec)

        # Cases to use webp = if file gif, if it has an animated_web, and not in a
        # format string like format-jpeg, but allow format-webp
        use_webp = (
            self.file.name.lower().endswith((".gif", ".webp"))
            and self.animated_webp_ready
            and not re.search(r"format-(?!webp)", spec_str)
        )

        # enter the webp utils
        if use_webp:
            # Normalize the spec string for webp caching
            spec_str = webp_utils.get_custom_webp_spec(spec_str)

            # try to match fills and create renditions from that
            match = re.match(r"^fill-(\d+)x(\d+)", spec_str)
            if match:
                width, height = map(int, match.groups())
                return webp_utils.generate_webp_rendition(self, self.file, spec_str, width, height)

            # fallback to serving full animated_webp under the same spec_str, useful if original
            return webp_utils.serve_or_create_webp(self, spec_str, self.animated_webp)
        # else, handle using wagtail default
        else:
            try:
                return super().get_rendition(filter_spec)
            except (FileNotFoundError, SourceImageIOError):
                # Gracefully display a missing image if file not found, useful for local w/ prod db
                return NullRendition(self)

    def get_focal_point_key(self):
        """
        Returns a string key representing the focal point, or an empty string if no focal point.
        Used to uniquely identify renditions based on crop origin.
        """
        if self.focal_point_x is None or self.focal_point_y is None:
            return ""
        key_str = f"{self.focal_point_x},{self.focal_point_y},{self.focal_point_width},{self.focal_point_height}"
        return hashlib.sha1(key_str.encode("utf-8")).hexdigest()


# Custom rendition for the Custom Image class
class FoundationCustomRendition(AbstractRendition):
    image = models.ForeignKey(get_image_model_string(), on_delete=models.CASCADE, related_name="+")

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class NullRendition:
    """
    A dummy rendition returned when the actual image file is missing.
    Prevents Wagtail from crashing on {% image %} tags.
    """

    def __init__(self, image):
        self.image = image
        self.url = image.file.url if image.file else ""
        self.width = image.width or 1
        self.height = image.height or 1
        self.alt = image.title or "Missing image"

    def img_tag(self, attrs=None):
        attrs = attrs or {}
        attr_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
        return f'<img src="{self.url}" width="{self.width}" height="{self.height}" alt="{self.alt}" {attr_str}>'


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=FoundationCustomImage)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=FoundationCustomRendition)
def rendition_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
