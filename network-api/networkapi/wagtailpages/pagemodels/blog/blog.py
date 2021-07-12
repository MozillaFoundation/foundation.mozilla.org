from django.db import models
from django.conf import settings

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PrivacyModalPanel,
    PublishingPanel,
    StreamFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import InlinePanel, PageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from .. import customblocks

from ..mixin.foundation_metadata import FoundationMetadataPageMixin

from ...utils import (
    set_main_site_nav_information,
    get_content_related_by_tag
)

from .blog_category import BlogPageCategory
from .blog_index import BlogIndexPage
from ..content_author import ContentAuthor

base_fields = [
    ('paragraph', blocks.RichTextBlock(
        features=[
            'bold', 'italic',
            'h2', 'h3', 'h4', 'h5',
            'ol', 'ul',
            'link', 'hr',
        ]
    )),
    ('iframe', customblocks.iFrameBlock()),
    ('image', customblocks.AnnotatedImageBlock()),
    ('image_text', customblocks.ImageTextBlock()),
    ('image_text_mini', customblocks.ImageTextMini()),
    ('video', customblocks.VideoBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('pulse_listing', customblocks.PulseProjectList()),
    ('quote', customblocks.QuoteBlock()),
    ('spacer', customblocks.BootstrapSpacerBlock()),
]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('wagtailpages.BlogPage', on_delete=models.CASCADE, related_name='tagged_items')


class BlogAuthors(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("wagtailpages.BlogPage", related_name="authors")
    author = models.ForeignKey(
        ContentAuthor,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

    def __str__(self):
        return self.author.name


class RelatedBlogPosts(Orderable):
    page = ParentalKey(
        'wagtailpages.BlogPage',
        related_name='related_posts',
    )

    related_post = models.ForeignKey(
        'wagtailpages.BlogPage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        PageChooserPanel('related_post'),
    ]

    def __str__(self):
        return self.related_post.title

    class Meta:
        verbose_name = "Related blog posts"
        verbose_name_plural = "Related blog posts"


class BlogPage(FoundationMetadataPageMixin, Page):
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

    related_post_count = 3

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel("authors", label="Author", min_num=1)
            ],
            heading="Author(s)"
        ),
        FieldPanel('category'),
        StreamFieldPanel('body'),
        FieldPanel('feature_comments'),
        InlinePanel(
            'related_posts',
            label='Related Blog Posts',
            min_num=related_post_count,
            max_num=related_post_count
        ),
    ]

    promote_panels = FoundationMetadataPageMixin.promote_panels + [
        FieldPanel('tags'),
    ]

    settings_panels = [
        PublishingPanel(),
        FieldPanel('first_published_at'),
        PrivacyModalPanel(),
    ]

    subpage_types = [
        'ArticlePage'
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['show_comments'] = settings.USE_COMMENTO and self.feature_comments

        # Pull this object specifically using the English page title
        blog_page = BlogIndexPage.objects.get(title_en__iexact='Blog')

        # If that doesn't yield the blog page, pull using the universal title
        if blog_page is None:
            blog_page = BlogIndexPage.objects.get(title__iexact='Blog')

        if blog_page:
            context['blog_index'] = blog_page

        return set_main_site_nav_information(self, context, 'Homepage')

    def save(self, *args, **kwargs):
        """
        if a blog page gets saved with fewer than 3 related posts, find
        the most related posts and drop those in to fill out the related
        posts to three, before actually saving.
        """
        print("related count:", self.related_post.all())
        if self.related_post.all().count() < related_post_count:
            print("padding related posts")
        super().save(*args, *kwargs)
