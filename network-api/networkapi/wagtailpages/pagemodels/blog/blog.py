from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import truncatechars
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    PrivacyModalPanel,
    PublishingPanel,
    StreamFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.models import Orderable, Locale, Page
from wagtail.core.fields import StreamField
from wagtail.core.rich_text import get_text_for_indexing
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail_localize.fields import TranslatableField, SynchronizedField

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from .. import customblocks
from ..customblocks.full_content_rich_text_options import full_content_rich_text_options


from ..mixin.foundation_metadata import FoundationMetadataPageMixin

from ...utils import (
    set_main_site_nav_information,
    get_content_related_by_tag,
    TitleWidget
)

from networkapi.wagtailpages.models import Profile
from .blog_topic import BlogPageTopic
from .blog_index import BlogIndexPage

base_fields = [
    ('accordion', customblocks.AccordionBlock()),
    ('paragraph', blocks.RichTextBlock(
        features=full_content_rich_text_options,
        template='wagtailpages/blocks/rich_text_block.html',
    )),
    ('card_grid', customblocks.CardGridBlock()),
    ('image_grid', customblocks.ImageGridBlock()),
    ('iframe', customblocks.iFrameBlock()),
    ('image', customblocks.AnnotatedImageBlock()),
    ('audio', customblocks.AudioBlock()),
    ('image_text', customblocks.ImageTextBlock()),
    ('image_text_mini', customblocks.ImageTextMini()),
    ('video', customblocks.VideoBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('looping_video', customblocks.LoopingVideoBlock()),
    ('pulse_listing', customblocks.PulseProjectList()),
    ('single_quote', customblocks.SingleQuoteBlock()),
    ('slider', customblocks.FoundationSliderBlock()),
    ('spacer', customblocks.BootstrapSpacerBlock()),
    ('airtable', customblocks.AirTableBlock()),
    ('datawrapper', customblocks.DatawrapperBlock()),
    ('typeform', customblocks.TypeformBlock()),
]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('wagtailpages.BlogPage', on_delete=models.CASCADE, related_name='tagged_items')


class BlogAuthors(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey('wagtailpages.BlogPage', related_name='authors')
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel('author'),
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
        blank=False,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        PageChooserPanel('related_post'),
    ]

    def __str__(self):
        return self.related_post.title

    class Meta:
        verbose_name = 'Related blog posts'
        verbose_name_plural = 'Related blog posts'
        ordering = ['sort_order']


class BlogPage(FoundationMetadataPageMixin, Page):
    body = StreamField(
        base_fields,
        block_counts={'typeform': {'max_num': 1}},
    )

    topics = ParentalManyToManyField(
        BlogPageTopic,
        help_text='Which blog topics is this blog page associated with?',
        blank=True,
        verbose_name='Topics',
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    zen_nav = False

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='hero_banner_image',
        verbose_name='Hero Image',
        help_text='Image for the blog page hero section.',
    )
    hero_video = models.CharField(
        blank=True,
        max_length=500,
        help_text='URL to video for blog page hero section.',

    )

    feature_comments = models.BooleanField(
        default=False,
        help_text='Check this box to add a comment section for this blog post.',
    )

    related_post_count = 3

    content_panels = [
        FieldPanel(
            'title',
            classname='full title',
            widget=TitleWidget(attrs={"class": "max-length-warning", "data-max-length": 60})
        ),
        MultiFieldPanel(
            [
                InlinePanel('authors', label='Author', min_num=1)
            ],
            heading='Author(s)'
        ),
        FieldPanel('topics'),
        MultiFieldPanel(
            [
                FieldPanel("hero_video"),
                ImageChooserPanel('hero_image'),
            ],
            heading="Hero Video/Image"
        ),
        StreamFieldPanel('body'),
        FieldPanel('feature_comments'),
        InlinePanel(
            'related_posts',
            label='Related Blog Posts',
            help_text='Pick three other posts that are related to this post. '
                      'If you pick fewer than three (or none), saving will '
                      'automatically bind some related posts based on tag matching.',
            min_num=0,
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

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('body'),
        TranslatableField('title'),
        SynchronizedField('authors'),
        SynchronizedField('hero_video'),
        SynchronizedField('hero_image'),
        SynchronizedField('related_posts'),
        SynchronizedField('first_published_at'),
    ]

    subpage_types = [
        'ArticlePage'
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['show_comments'] = settings.USE_COMMENTO and self.feature_comments

        related_posts = [post.related_post for post in self.related_posts.all()]
        if request.is_preview:
            # While we automatically pad out the related posts during save, we want to
            # see that same padded list during preview, but *without* actually updating
            # the model, so we control this property at render context retrieval time:
            related_posts = related_posts + self.get_missing_related_posts()

        # Make sure to filter out any None entries, which may happen if the
        # self.ensure_related_posts() function was unable to find any related
        # posts to pad the related posts set with.
        context['related_posts'] = list(filter(None, related_posts))

        # Pull this object specifically using the English page title
        default_locale = Locale.objects.get(language_code=settings.LANGUAGE_CODE)
        blog_page = BlogIndexPage.objects.get(title__iexact='Blog', locale=default_locale)

        if blog_page:
            context['blog_index'] = blog_page

        return set_main_site_nav_information(self, context, 'Homepage')

    def get_missing_related_posts(self):
        """
        Check how many related posts are missing, and generate a list of
        posts that can be added in to fill that list up. We do this in its
        own function so that both publishing a page and previewing a page
        can present the full list of related posts, while making sure that
        previewing does not save the amended list into the model, as previews
        shouldn't change the model in any way.
        """
        additional_posts = list()
        post_count = self.related_posts.all().count()
        missing_count = self.related_post_count - post_count

        if missing_count == 0:
            return additional_posts

        related_posts = get_content_related_by_tag(self)

        if len(related_posts) > 0:
            # Add as many posts as there are missing, or until
            # we run out of related posts, whichever comes first.
            for post in related_posts:
                if missing_count == 0:
                    break
                if self.related_posts.filter(related_post=post).count() > 0:
                    # Make sure to skip over duplicates
                    continue
                additional_posts.append(post)
                missing_count = missing_count - 1

        return additional_posts

    def ensure_related_posts(self):
        """
        If a blog page gets saved with fewer than 3 related posts, we
        want to find the most-related posts and drop those in to fill
        out the related posts to three, before actually saving.
        """
        for post in self.get_missing_related_posts():
            self.related_posts.add(
                RelatedBlogPosts(
                    page=self,
                    related_post=post
                )
            )

    def clean(self):
        if self.hero_image and self.hero_video:
            raise ValidationError({
                'hero_image': ValidationError("Please select a video OR an image for the hero section."),
                'hero_video': ValidationError("Please select a video OR an image for the hero section.")
                })

        # Ensure that we've tried to fill in three related posts
        # for this blog post if fewer than three were set by staff
        self.ensure_related_posts()

        return super().clean()

    def get_meta_description(self):
        # TODO: refactor this out as part of: https://github.com/mozilla/foundation.mozilla.org/issues/7828
        if self.search_description:
            return self.search_description

        for block in self.body:
            if block.block_type == "paragraph":
                text = get_text_for_indexing(str(block))
                return truncatechars(text, 153)

        return super().get_meta_description()
