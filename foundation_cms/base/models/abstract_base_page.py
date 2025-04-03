from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtailmetadata.models import MetadataPageMixin
from modelcluster.fields import ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django.db import models

from foundation_cms.base.mixins.theme_mixin import ThemedPageMixin

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='author_image'
    )
    bio = models.TextField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        FieldPanel("bio"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"

class AbstractBasePage(MetadataPageMixin, ThemedPageMixin, Page):
    tags = ParentalManyToManyField("taggit.Tag", blank=True)
    author = models.ForeignKey(
        "base.Author",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_pages",
    )

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel("tags"),
            FieldPanel("author"),
        ], heading="Additional Metadata")
    ]

    class Meta:
        abstract = True

