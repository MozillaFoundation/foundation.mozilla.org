import hashlib
import logging
import os
import re

from django.conf import settings
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

logger = logging.getLogger(__name__)


# The custom image model for the Foundation site
class FoundationCustomImage(AbstractImage):
    # Add an animated_webp field to the Image model, where webp versions of
    # .gif files are stored and linked to the image.

    # store the original GIF (if the upload was a GIF) so we can link to it
    original_gif = models.FileField(
        upload_to="images/original_gif/",
        blank=True,
        null=True,
        help_text="Original uploaded GIF (stored for reference).",
    )

    # WebP versions of .gif files are stored here.
    animated_webp = models.FileField(upload_to="images/converted_webp/", blank=True, null=True)

    admin_form_fields = Image.admin_form_fields + ("animated_webp", "original_gif")

    @cached_property
    def animated_webp_ready(self):
        """
        The animated WebP for this image, or None if there isn't one (yet).

        Resolved in priority order:

        1. The `animated_webp` field, if already populated. Covers rows written
           before conversion moved off the request cycle, whose keys are not
           derivable (they were named after a temp file).
        2. A directly-uploaded animated WebP: the file is its own conversion.
        3. The key the conversion Lambda writes to. Asynchronous, so absence is
           an ordinary "not converted yet" rather than an error.

        Case 3 persists the key once found, which both saves every later request
        an S3 HEAD and lets the pre_delete signal clean the file up -- an
        unpopulated field would orphan the Lambda's output on delete.
        """
        if not self.pk:
            return None  # Not yet saved, can't safely assign

        if self.animated_webp:
            return self.animated_webp

        name = self.file.name.lower()

        if name.endswith(".webp") and webp_utils.is_animated_webp(self.file):
            self.animated_webp = self.file
            self._persist_animated_webp()
            return self.animated_webp

        if name.endswith(".gif"):
            derived = webp_utils.derive_webp_name(self.file.name)
            if webp_utils.converted_webp_exists(derived):
                # Assign the path, not the file: the Lambda already wrote the
                # object, so this records where it is without re-uploading it.
                self.animated_webp = derived
                self._persist_animated_webp()
                return self.animated_webp

        return None

    def _persist_animated_webp(self):
        """
        Record the resolved WebP without letting a write failure break a render.

        This runs during template rendering, so it must never raise an error.
        """
        try:
            super().save(update_fields=["animated_webp"])
        except Exception as e:
            logger.warning(f"Could not persist animated_webp for image {self.pk}: {e}")

    class Meta:
        app_label = "images"

    def save(self, *args, **kwargs):
        """
        Custom self.save() method for when the image is an animated gif.
        Save the image the wagtail way first then extend to generate a .webp file.
        """

        # wagtail image save
        super().save(*args, **kwargs)

        is_gif = self.file and self.file.name.lower().endswith(".gif")
        is_webp = self.file and self.file.name.lower().endswith(".webp")

        # if an animated WebP is uploaded directly, ensure it is also saved to the animated_webp field
        if is_webp and not self.animated_webp and webp_utils.is_animated_webp(self.file):
            self.animated_webp = self.file
            super().save(update_fields=["animated_webp"])

        # capture original gif
        if is_gif and not self.original_gif:
            # Ensure we read from the start
            try:
                self.file.open("rb")
                self.file.seek(0)
                original_name = os.path.basename(self.file.name)
                self.original_gif.save(
                    original_name,
                    ContentFile(self.file.read()),
                    save=False,
                )
            finally:
                try:
                    self.file.close()
                except Exception:
                    pass
            super().save(update_fields=["original_gif"])

        # gif -> animated WebP conversion step
        #
        # In deployed environments an S3 event triggers a Lambda that writes the
        # WebP to the key derive_webp_name() computes, and get_rendition serves
        # the GIF until it lands.
        #
        # Local development and tests have no S3 and therefore no Lambda, so they
        # still convert inline.
        if is_gif and not self.animated_webp and settings.GIF_CONVERT_SYNCHRONOUSLY:
            webp_path = webp_utils.convert_gif_to_webp(self.file)
            if webp_path:
                with open(webp_path, "rb") as f:
                    # write file to storage but do not save model yet
                    self.animated_webp.save(os.path.basename(webp_path), ContentFile(f.read()), save=False)
                super().save(update_fields=["animated_webp"])

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
            webp_spec = webp_utils.get_custom_webp_spec(spec_str)

            try:
                # try to match fills and create renditions from that
                match = re.match(r"^fill-(\d+)x(\d+)", webp_spec)
                if match:
                    width, height = map(int, match.groups())
                    rendition = webp_utils.generate_webp_rendition(self, self.file, webp_spec, width, height)
                else:
                    # fallback to serving full animated_webp under the same spec, useful if original
                    rendition = webp_utils.serve_or_create_webp(self, webp_spec, self.animated_webp)
            except (FileNotFoundError, SourceImageIOError):
                # WebP source is missing or not ready yet.
                rendition = None

            if rendition is not None:
                return rendition

            # Conversion failed, or the WebP is not ready.

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
    image = models.ForeignKey(get_image_model_string(), on_delete=models.CASCADE, related_name="renditions")

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
    # Check and also delete derived files
    if instance.animated_webp:
        instance.animated_webp.delete(False)
    if instance.original_gif:
        instance.original_gif.delete(False)


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=FoundationCustomRendition)
def rendition_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
