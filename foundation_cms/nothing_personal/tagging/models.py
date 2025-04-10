from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, ItemBase
from wagtail.models import Page


@register_snippet
class BlogTag(TagBase):
    free_tagging = False

    class Meta:
        verbose_name = "blog tag"
        verbose_name_plural = "blog tags"


class TaggedBlog(ItemBase):
    tag = models.ForeignKey(
        BlogTag, related_name="tagged_blogs", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        to='',  # TODO: Define BlogPage path
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class BlogPage(Page):

    tags = ClusterTaggableManager(through='demo.TaggedBlog', blank=True)
