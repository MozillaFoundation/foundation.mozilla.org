from django.db import models
from django.conf import settings

from django.template.defaultfilters import slugify

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.snippets.models import register_snippet

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from . import customblocks
from .index import IndexPage
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from ..utils import (
    set_main_site_nav_information,
    get_content_related_by_tag
)

base_fields = [
    ('paragraph', blocks.RichTextBlock(
        features=[
            'bold', 'italic',
            'h2', 'h3', 'h4', 'h5',
            'ol', 'ul',
            'link', 'hr',
        ]
    )),
    ('image', customblocks.AnnotatedImageBlock()),
    ('image_text', customblocks.ImageTextBlock()),
    ('image_text_mini', customblocks.ImageTextMini()),
    ('video', customblocks.VideoBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('spacer', customblocks.BootstrapSpacerBlock()),
    ('quote', customblocks.QuoteBlock()),
]


@register_snippet
class BlogPageCategory(models.Model):
    name = models.CharField(
        max_length=50
    )

    intro = RichTextField(
        features=[
            'bold', 'italic', 'link',
        ],
        blank=True,
    )

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Page Category"
        verbose_name_plural = "Blog Page Categories"


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('wagtailpages.BlogPage', on_delete=models.CASCADE, related_name='tagged_items')


class BlogPage(FoundationMetadataPageMixin, Page):

    author = models.CharField(
        verbose_name='Author',
        max_length=70,
        blank=False,
    )

    body = StreamField(base_fields)

    category = ParentalManyToManyField(
        BlogPageCategory,
        help_text='Which blog categories is this blog page associated with?',
        blank=True,
        verbose_name="Categories",
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    zen_nav = True

    feature_comments = models.BooleanField(
        default=False,
        help_text='Check this box to add a comment section for this blog post.',
    )

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('category'),
        StreamFieldPanel('body'),
        FieldPanel('feature_comments'),
    ]

    promote_panels = FoundationMetadataPageMixin.promote_panels + [
        FieldPanel('tags'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('first_published_at'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['related_posts'] = get_content_related_by_tag(self)
        context['coral_talk_server_url'] = settings.CORAL_TALK_SERVER_URL
        context['coral_talk'] = context['coral_talk_server_url'] and self.feature_comments

        # Pull this object specifically using the English page title
        blog_page = IndexPage.objects.get(title_en__iexact='Blog')

        # If that doesn't yield the blog page, pull using the universal title
        if blog_page is None:
            blog_page = IndexPage.objects.get(title__iexact='Blog')

        if blog_page:
            context['blog_index'] = blog_page

        return set_main_site_nav_information(self, context, 'Homepage')
