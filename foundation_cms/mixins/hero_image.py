from django.db import models
from wagtail.images import get_image_model_string


class HeroImageMixin(models.Model):
    hero_title = models.TextField(
        help_text="Hero Title",
        blank=True,
    )

    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Hero Image",
        help_text="Image for page hero section.",
    )

    hero_image_alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt Text",
        help_text="Descriptive text for screen readers. Leave blank to use the image's default title.",
    )

    class Meta:
        abstract = True
