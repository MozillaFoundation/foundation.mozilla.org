from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtailmetadata.models import MetadataPageMixin
from taggit.models import TagBase, ItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from foundation_cms.base.mixins.theme_mixin import ThemedPageMixin


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="author_image"
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


@register_snippet
class PageTag(TagBase):
    free_tagging = False

    class Meta:
        verbose_name = "Page Tag (new)"
        verbose_name_plural = "Page Tags (new)"


class AbstractBasePage(MetadataPageMixin, ThemedPageMixin, Page):
    tags = ClusterTaggableManager(through='base.TaggedPage', blank=True)
    author = models.ForeignKey(
        "base.Author",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_pages",
    )

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("author"),
            ],
            heading="Additional Metadata",
        )
    ]

    class Meta:
        abstract = True


class TaggedPage(ItemBase):
    tag = models.ForeignKey(
        PageTag, related_name="tagged_pages", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to='wagtailcore.Page',
        on_delete=models.CASCADE,
        related_name='base_tagged_items'
    )
