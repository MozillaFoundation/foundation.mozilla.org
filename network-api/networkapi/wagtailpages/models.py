import json
import re

from django.db import models
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.template.defaultfilters import slugify


from . import customblocks

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable as WagtailOrderable
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.snippets.models import register_snippet

from wagtailmetadata.models import MetadataPageMixin

from taggit.models import Tag, TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from .utils import (
    set_main_site_nav_information,
    get_page_tree_information,
    get_content_related_by_tag
)

# TODO:  https://github.com/mozilla/foundation.mozilla.org/issues/2362
from .donation_modal import DonationModals  # noqa: F401


# See https://docs.python.org/3.7/library/stdtypes.html#str.title
# for why this definition exists (basically: apostrophes)
def titlecase(s):
    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda mo: mo.group(0)[0].upper() +
        mo.group(0)[1:].lower(),
        s
    )


"""
We'll need to figure out which components are truly "base" and
which are bits that should be used in subclassing template-based
page types.
"""
base_fields = [field for field in [
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
    ('image_grid', customblocks.ImageGridBlock()),
    ('video', customblocks.VideoBlock()),
    ('iframe', customblocks.iFrameBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('spacer', customblocks.BootstrapSpacerBlock()),
    ('quote', customblocks.QuoteBlock()),
    ('pulse_listing', customblocks.PulseProjectList()),
    ('profile_listing', customblocks.LatestProfileList()),
    ('profile_by_id', customblocks.ProfileById()),
    ('profile_directory', customblocks.ProfileDirectory()),
    ('recent_blog_entries', customblocks.RecentBlogEntries()),
    ('airtable', customblocks.AirTableBlock()),
] if field is not None]


# Override the MetadataPageMixin to allow for a default
# description and image in page metadata for all Pages on the site
class FoundationMetadataPageMixin(MetadataPageMixin):
    def __init__(self, *args, **kwargs):
        # The first Wagtail image returned that has the specified tag name will
        # be the default image URL in social shares when no Image is specified at the Page level
        super().__init__(*args, **kwargs)
        try:
            default_social_share_tag = 'social share image'
            self.social_share_tag = Tag.objects.get(name=default_social_share_tag)
        except Tag.DoesNotExist:
            self.social_share_tag = None

    # Change this string to update the default description of all pages on the site
    default_description = 'Mozilla is a global non-profit dedicated to putting you in control of your online ' \
                          'experience and shaping the future of the web for the public good. '

    def get_meta_description(self):
        if self.search_description:
            return self.search_description

        parent = self.get_parent()

        while parent:
            if parent.search_description:
                return parent.search_description
            parent = parent.get_parent()

        return self.default_description

    def get_meta_image(self):
        if self.search_image:
            return self.search_image

        parent = self.get_parent()

        while parent:
            if hasattr(parent, 'search_image') and parent.search_image:
                return parent.search_image
            if hasattr(parent, 'homepage') and parent.homepage.search_image:
                return parent.homepage.search_image
            parent = parent.get_parent()

        try:
            return Image.objects.filter(tags=self.social_share_tag).first()
        except Image.DoesNotExist:
            return None

    class Meta:
        abstract = True


class ModularPage(FoundationMetadataPageMixin, Page):
    """
    The base class offers universal component picking
    """

    header = models.CharField(
        max_length=250,
        blank=True
    )

    narrowed_page_content = models.BooleanField(
        default=False,
        help_text='For text-heavy pages, turn this on to reduce the overall width of the content on the page.'
    )

    zen_nav = models.BooleanField(
        default=True,
        help_text='For secondary nav pages, use this to collapse the primary nav under a toggle hamburger.'
    )

    body = StreamField(base_fields)

    settings_panels = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('narrowed_page_content'),
        ]),
        MultiFieldPanel([
            FieldPanel('zen_nav'),
        ])
    ]

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        StreamFieldPanel('body'),
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        return set_main_site_nav_information(self, context, 'Homepage')


class MiniSiteNameSpace(ModularPage):
    subpage_types = [
        'BlogPage',
        'CampaignPage',
        'BanneredCampaignPage',
        'OpportunityPage',
        'YoutubeRegretsPage',
    ]

    """
    This is basically an abstract page type for setting up
    minisite namespaces such as "campaign", "opportunity", etc.
    """

    def get_context(self, request):
        """
        Extend the context so that mini-site pages know what kind of tree
        they live in, and what some of their local aspects are:
        """
        context = super().get_context(request)
        updated = get_page_tree_information(self, context)
        updated['mini_site_title'] = updated['root'].title
        return updated


class CTA(models.Model):
    name = models.CharField(
        default='',
        max_length=100,
        help_text='Identify this component for other editors',
    )

    header = models.CharField(
        max_length=500,
        help_text='Heading that will display on page for this component',
        blank=True
    )

    description = RichTextField(
        help_text='Body (richtext) of component',
        blank=True
    )

    newsletter = models.CharField(
        max_length=100,
        help_text='The (pre-existing) SalesForce newsletter to sign up for',
        default='mozilla-foundation'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'CTA'


@register_snippet
class Signup(CTA):

    ask_name = models.BooleanField(
        help_text='Check this box to show (optional) name fields',
        default=False,
    )

    class Meta:
        verbose_name = 'signup snippet'


class OpportunityPage(MiniSiteNameSpace):

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'OpportunityPage',
        'RedirectingPage',
    ]


@register_snippet
class Petition(CTA):
    campaign_id = models.CharField(
        max_length=20,
        help_text='Which campaign identifier should this petition be tied to?',
        null=True,
        blank=True,
    )

    requires_country_code = models.BooleanField(
        default=False,
        help_text='Will this petition require users to specify their country?',
    )

    requires_postal_code = models.BooleanField(
        default=False,
        help_text='Will this petition require users to specify their postal code?',
    )

    COMMENT_CHOICES = (
        ('none', 'No comments'),
        ('optional', 'Optional comments'),
        ('required', 'Required comments'),
    )

    comment_requirements = models.CharField(
        choices=COMMENT_CHOICES,
        default='none',
        help_text='What is the comments policy for this petition?',
        max_length=8,
    )

    checkbox_1 = models.CharField(
        editable=False,
        max_length=1024,
        help_text='label for the first checkbox option (may contain HTML)',
        blank=True,
    )

    checkbox_2 = models.CharField(
        editable=False,
        max_length=1024,
        help_text='label for the second checkbox option (may contain HTML)',
        blank=True,
    )

    share_link = models.URLField(
        max_length=1024,
        help_text='Link that will be put in share button',
        blank=True,
        editable=False,
    )

    share_link_text = models.CharField(
        max_length=20,
        help_text='Text content of the share button',
        default='Share this',
        blank=True,
        editable=False,
    )

    share_twitter = models.CharField(
        max_length=20,
        help_text='Share Progress id for twitter button',
        blank=True,
    )

    share_facebook = models.CharField(
        max_length=20,
        help_text='Share Progress id for facebook button',
        blank=True,
    )

    share_email = models.CharField(
        max_length=20,
        help_text='Share Progress id for email button',
        blank=True,
    )

    thank_you = models.CharField(
        max_length=140,
        help_text='Message to show after thanking people for signing',
        default='Thank you for signing too!',
    )

    class Meta:
        verbose_name = 'petition snippet'


class CampaignPage(MiniSiteNameSpace):
    """
    these pages come with sign-a-petition CTAs
    """
    cta = models.ForeignKey(
        'Petition',
        related_name='page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose existing or create new sign-up form'
    )

    def get_donation_modal_json(self):
        modals = self.donation_modals.all()
        # This is where we can do server-side A/B testing,
        # by either sending all modals down the pipe, or
        # selectively only sending a single one based on
        # things like geolocation, time of day, etc.
        modals_json = [m.to_simple_dict() for m in modals]
        return json.dumps(modals_json)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        SnippetChooserPanel('cta'),
        InlinePanel('donation_modals', label='Donation Modal', max_num=4),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'CampaignPage',
        'RedirectingPage',
    ]


# Code for the new wagtail primary pages (under homepage)


class PrimaryPage(FoundationMetadataPageMixin, Page):
    """
    Basically a straight copy of modular page, but with
    restrictions on what can live 'under it'.

    Ideally this is just PrimaryPage(ModularPage) but
    setting that up as a migration seems to be causing
    problems.
    """
    header = models.CharField(
        max_length=250,
        blank=True
    )

    banner = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='primary_banner',
        verbose_name='Hero Image',
        help_text='Choose an image that\'s bigger than 4032px x 1152px with aspect ratio 3.5:1',
    )

    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text='Intro paragraph to show in hero cutout box'
    )

    narrowed_page_content = models.BooleanField(
        default=False,
        help_text='For text-heavy pages, turn this on to reduce the overall width of the content on the page.'
    )

    zen_nav = models.BooleanField(
        default=False,
        help_text='For secondary nav pages, use this to collapse the primary nav under a toggle hamburger.'
    )

    body = StreamField(base_fields)

    settings_panels = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('narrowed_page_content'),
        ]),
        MultiFieldPanel([
            FieldPanel('zen_nav'),
        ])
    ]

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        ImageChooserPanel('banner'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'PrimaryPage',
        'RedirectingPage',
        'BanneredCampaignPage'
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        context = set_main_site_nav_information(self, context, 'Homepage')
        context = get_page_tree_information(self, context)
        return context


class BanneredCampaignPage(PrimaryPage):
    """
    title, header, intro, and body are inherited from PrimaryPage
    """

    # Note that this is a different related_name, as the `page`
    # name is already taken as back-referenced to CampaignPage.
    cta = models.ForeignKey(
        'Petition',
        related_name='bcpage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose an existing, or create a new, pettition form'
    )

    signup = models.ForeignKey(
        'Signup',
        related_name='bcpage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose an existing, or create a new, sign-up form'
    )

    panel_count = len(PrimaryPage.content_panels)
    n = panel_count - 1

    content_panels = PrimaryPage.content_panels[:n] + [
        SnippetChooserPanel('cta'),
        SnippetChooserPanel('signup'),
    ] + PrimaryPage.content_panels[n:]

    subpage_types = [
        'BanneredCampaignPage',
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        return get_page_tree_information(self, context)


class IndexPage(FoundationMetadataPageMixin, RoutablePageMixin, Page):
    """
    This is a page type for creating "index" pages that
    can show cards for all their child content.
    E.g. a page that list "all blog posts" under it,
    or "all the various campaigns", etc.
    """

    header = models.CharField(
        max_length=250,
        blank=True
    )

    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text='Intro paragraph to show in hero cutout box'
    )

    DEFAULT_PAGE_SIZE = 12

    PAGE_SIZES = (
        (4, '4'),
        (8, '8'),
        (DEFAULT_PAGE_SIZE, str(DEFAULT_PAGE_SIZE)),
        (24, '24'),
    )

    page_size = models.IntegerField(
        choices=PAGE_SIZES,
        default=DEFAULT_PAGE_SIZE,
        help_text='The number of entries to show by default, and per incremental load'
    )

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('intro'),
        FieldPanel('page_size'),
    ]

    def get_context(self, request):
        # bootstrap the render context
        context = super().get_context(request)
        context = set_main_site_nav_information(self, context, 'Homepage')
        context = get_page_tree_information(self, context)

        # perform entry pagination and (optional) filterin
        entries = self.get_entries(context)
        context['has_more'] = self.page_size < len(entries)
        context['entries'] = entries[0:self.page_size]
        return context

    def get_all_entries(self):
        """
        Get all (live) child entries, ordered "newest first"
        """
        return self.get_children().live().public().order_by('-first_published_at')

    def get_entries(self, context=dict()):
        """
        Get all child entries, filtered down if required based on
        the `self.filtered` field being set or not.
        """
        entries = self.get_all_entries()
        if hasattr(self, 'filtered'):
            entries = self.filter_entries(entries, context)
        return entries

    def filter_entries(self, entries, context):
        filter_type = self.filtered.get('type')
        context['filtered'] = filter_type

        if filter_type == 'tags':
            entries = self.filter_entries_for_tag(entries, context)

        if filter_type == 'category':
            entries = self.filter_entries_for_category(entries, context)

        context['total_entries'] = len(entries)
        return entries

    def filter_entries_for_tag(self, entries, context):
        """
        Realise the 'entries' queryset and filter it for tags presences.
        We need to perform this realisation because there is no guarantee
        that all children for this IndexPage in fact have a `tags` field,
        so in order to test this each entry needs to be "cast" into its
        specific model before we can test for whether i) there are tags
        to work with and then ii) those tags match the specified ones.
        """
        terms = self.filtered.get('terms')

        # "unsluggify" all terms. Note that we cannot use list comprehension,
        # as not all terms might be real tags, and list comprehension cannot
        # be made to ignore throws.
        context['terms'] = list()
        for term in terms:
            try:
                tag = Tag.objects.get(slug=term)
                context['terms'].append(str(tag))
            except Tag.DoesNotExist:
                # ignore non-existent tags
                pass

        entries = [
            entry
            for
            entry in entries.specific()
            if
            hasattr(entry, 'tags')
            and not
            # Determine whether there is any overlap between 'all tags' and
            # the tags specified. This effects ANY matching (rather than ALL).
            set([tag.slug for tag in entry.tags.all()]).isdisjoint(terms)
        ]

        return entries

    def filter_entries_for_category(self, entries, context):
        category = self.filtered.get('category')

        # make sure we bypass "x results for Y"
        context['no_filter_ui'] = True

        # and that we don't show the primary tag/category
        context['hide_classifiers'] = True

        # explicitly set the index page title and intro
        context['index_title'] = titlecase(f'{category.name} {self.title}')
        context['index_intro'] = category.intro

        # and then the filtered content
        context['terms'] = [category.name, ]
        entries = [
            entry
            for
            entry in entries.specific()
            if
            hasattr(entry, 'category')
            and
            category in entry.category.all()
        ]

        return entries

    """
    Sub routes
    """

    @route('^entries/')
    def generate_entries_set_html(self, request, *args, **kwargs):
        """
        JSON endpoint for getting a set of (pre-rendered) entries
        """

        page = 1
        if 'page' in request.GET:
            page = int(request.GET['page'])

        page_size = self.page_size
        if 'page_size' in request.GET:
            page_size = int(request.GET['page_size'])

        start = page * page_size
        end = start + page_size
        entries = self.get_entries()
        has_next = end < len(entries)

        hide_classifiers = False
        if hasattr(self, 'filtered'):
            if self.filtered.get('type') == 'category':
                hide_classifiers = True

        html = loader.render_to_string(
            'wagtailpages/fragments/entry_cards.html',
            context={
                'entries': entries[start:end],
                'hide_classifiers': hide_classifiers
            },
            request=request
        )

        return JsonResponse({
            'entries_html': html,
            'has_next': has_next,
        })

    """
    tag routes
    """

    # helper function for /tags/... subroutes
    def extract_tag_information(self, tag):
        terms = list(filter(None, re.split('/', tag)))
        self.filtered = {
            'type': 'tags',
            'terms': terms
        }

    @route(r'^tags/(?P<tag>.+)/entries/')
    def generate_tagged_entries_set_html(self, request, tag, *args, **kwargs):
        """
        JSON endpoint for getting a set of (pre-rendered) tagged entries
        """
        self.extract_tag_information(tag)
        return self.generate_entries_set_html(request, *args, **kwargs)

    @route(r'^tags/(?P<tag>.+)/')
    def entries_by_tag(self, request, tag, *args, **kwargs):
        """
        If this page was called with `/tags/...` as suffix, extract
        the tags to filter prior to rendering this page. Multiple
        tags are specified as subpath: `/tags/tag1/tag2/...`
        """
        self.extract_tag_information(tag)
        return IndexPage.serve(self, request, *args, **kwargs)

    """
    category routes
    """

    # helper function for /category/... subroutes
    def extract_category_information(self, category_object):
        self.filtered = {
            'type': 'category',
            'category': category_object
        }

    @route(r'^category/(?P<category>.+)/entries/')
    def generate_category_entries_set_html(self, request, category, *args, **kwargs):
        """
        JSON endpoint for getting a set of (pre-rendered) category entries
        """
        self.extract_category_information(category)
        return self.generate_entries_set_html(request, *args, **kwargs)

    @route(r'^category/(?P<category>.+)/')
    def entries_by_category(self, request, category, *args, **kwargs):
        """
        If this page was called with `/category/...` as suffix, extract
        the category to filter prior to rendering this page. Only one
        category can be specified (unlike tags)
        """
        category_object = None

        # We can't use .filter for @property fields,
        # so we have to run through all categories =(
        for bpc in BlogPageCategory.objects.all():
            if bpc.slug == category:
                category_object = bpc

        # while tags yield '0 results', an unknown category
        # should redirect to the base index page, instead.
        if category_object is None:
            return redirect(self.full_url)

        self.extract_category_information(category_object)
        return IndexPage.serve(self, request, *args, **kwargs)


class NewsPage(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/news_page.html'


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

    body = StreamField([
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
    ])

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

        return set_main_site_nav_information(self, context, 'Homepage')


class InitiativeSection(models.Model):
    page = ParentalKey(
        'wagtailpages.InitiativesPage',
        related_name='initiative_sections',
    )

    sectionImage = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='section_image',
        verbose_name='Hero Image',
    )

    sectionHeader = models.CharField(
        verbose_name='Header',
        max_length=250,
    )

    sectionCopy = models.TextField(
        verbose_name='Subheader',
    )

    sectionButtonTitle = models.CharField(
        verbose_name='Button Text',
        max_length=250,
    )

    sectionButtonURL = models.TextField(
        verbose_name='Button URL',
    )

    sectionButtonTitle2 = models.CharField(
        verbose_name='Button 2 Text',
        max_length=250,
        blank="True"
    )

    sectionButtonURL2 = models.TextField(
        verbose_name='Button 2 URL',
        blank="True"
    )

    panels = [
        ImageChooserPanel('sectionImage'),
        FieldPanel('sectionHeader'),
        FieldPanel('sectionCopy'),
        FieldPanel('sectionButtonTitle'),
        FieldPanel('sectionButtonURL'),
        FieldPanel('sectionButtonTitle2'),
        FieldPanel('sectionButtonURL2'),
    ]


class InitiativesPage(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/initiatives_page.html'

    subpage_types = [
        'BanneredCampaignPage',
        'MiniSiteNameSpace',
        'OpportunityPage',
        'RedirectingPage',
    ]

    primaryHero = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='primary_hero',
        verbose_name='Primary Hero Image',
    )

    subheader = models.TextField(
        blank=True,
    )

    h3 = models.TextField(
        blank=True,
    )

    sub_h3 = models.TextField(
        blank=True,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('primaryHero'),
        FieldPanel('header'),
        FieldPanel('subheader'),
        FieldPanel('h3'),
        FieldPanel('sub_h3'),
        InlinePanel('initiative_sections', label="Initiatives"),
        InlinePanel('featured_highlights', label='Highlights', max_num=9),
    ]


# TODO: Remove this model after ParticipatePage2 is in use
class ParticipatePage(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/participate_page.html'


class ParticipatePage2(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/participate_page2.html'

    ctaHero = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='primary_hero_participate',
        verbose_name='Primary Hero Image',
    )

    ctaHeroHeader = models.TextField(
        blank=True,
    )

    ctaHeroSubhead = RichTextField(
        features=[
            'bold', 'italic', 'link',
        ],
        blank=True,
    )

    ctaCommitment = models.TextField(
        blank=True,
    )

    ctaButtonTitle = models.CharField(
        verbose_name='Button Text',
        max_length=250,
        blank=True,
    )

    ctaButtonURL = models.TextField(
        verbose_name='Button URL',
        blank=True,
    )

    ctaHero2 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='primary_hero_participate2',
        verbose_name='Primary Hero Image',
    )

    ctaHeroHeader2 = models.TextField(
        blank=True,
    )

    ctaHeroSubhead2 = RichTextField(
        features=[
            'bold', 'italic', 'link',
        ],
        blank=True,
    )

    ctaCommitment2 = models.TextField(
        blank=True,
    )

    ctaButtonTitle2 = models.CharField(
        verbose_name='Button Text',
        max_length=250,
        blank=True,
    )

    ctaButtonURL2 = models.TextField(
        verbose_name='Button URL',
        blank=True,
    )

    ctaHero3 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='primary_hero_participate3',
        verbose_name='Primary Hero Image',
    )

    ctaHeroHeader3 = models.TextField(
        blank=True,
    )

    ctaHeroSubhead3 = RichTextField(
        features=[
            'bold', 'italic', 'link',
        ],
        blank=True,
    )

    ctaCommitment3 = models.TextField(
        blank=True,
    )

    ctaFacebook3 = models.TextField(
        blank=True,
    )

    ctaTwitter3 = models.TextField(
        blank=True,
    )

    ctaEmailShareBody3 = models.TextField(
        blank=True,
    )

    ctaEmailShareSubject3 = models.TextField(
        blank=True,
    )

    h2 = models.TextField(
        blank=True,
    )

    h2Subheader = models.TextField(
        blank=True,
        verbose_name='H2 Subheader',
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('ctaHero'),
            FieldPanel('ctaHeroHeader'),
            FieldPanel('ctaHeroSubhead'),
            FieldPanel('ctaCommitment'),
            FieldPanel('ctaButtonTitle'),
            FieldPanel('ctaButtonURL'),
        ], heading="Primary CTA"),
        FieldPanel('h2'),
        FieldPanel('h2Subheader'),
        InlinePanel('featured_highlights', label='Highlights Group 1', max_num=3),
        MultiFieldPanel([
            ImageChooserPanel('ctaHero2'),
            FieldPanel('ctaHeroHeader2'),
            FieldPanel('ctaHeroSubhead2'),
            FieldPanel('ctaCommitment2'),
            FieldPanel('ctaButtonTitle2'),
            FieldPanel('ctaButtonURL2'),
        ], heading="CTA 2"),
        InlinePanel('featured_highlights2', label='Highlights Group 2', max_num=6),
        MultiFieldPanel([
            ImageChooserPanel('ctaHero3'),
            FieldPanel('ctaHeroHeader3'),
            FieldPanel('ctaHeroSubhead3'),
            FieldPanel('ctaCommitment3'),
            FieldPanel('ctaFacebook3'),
            FieldPanel('ctaTwitter3'),
            FieldPanel('ctaEmailShareSubject3'),
            FieldPanel('ctaEmailShareBody3'),
        ], heading="CTA 3"),
        InlinePanel('cta4', label='CTA Group 4', max_num=3),
    ]


class PeoplePage(PrimaryPage):
    parent_page_types = ['Homepage']


class Styleguide(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/styleguide.html'


# Code for the new wagtail based homepage


class HomepageFeaturedNews(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='featured_news',
    )
    news = models.ForeignKey('news.News', on_delete=models.CASCADE, related_name='+')
    panels = [
        SnippetChooserPanel('news'),
    ]

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'
        ordering = ['sort_order']  # not automatically inherited!

    def __str__(self):
        return self.page.title + '->' + self.news.headline


class HomepageFeaturedHighlights(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='featured_highlights',
    )
    highlight = models.ForeignKey('highlights.Highlight', on_delete=models.CASCADE, related_name='+')
    panels = [
        SnippetChooserPanel('highlight'),
    ]

    class Meta:
        verbose_name = 'highlight'
        verbose_name_plural = 'highlights'
        ordering = ['sort_order']  # not automatically inherited!

    def __str__(self):
        return self.page.title + '->' + self.highlight.title


class HomepageFeaturedBlogs(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='featured_blogs',
    )
    blog = models.ForeignKey('BlogPage', on_delete=models.CASCADE, related_name='+')
    panels = [
        PageChooserPanel('blog'),
    ]

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
        ordering = ['sort_order']  # not automatically inherited!

    def __str__(self):
        return self.page.title + '->' + self.blog.title


class InitiativesHighlights(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.InitiativesPage',
        related_name='featured_highlights',
    )
    highlight = models.ForeignKey('highlights.Highlight', on_delete=models.CASCADE, related_name='+')
    panels = [
        SnippetChooserPanel('highlight'),
    ]

    class Meta:
        verbose_name = 'highlight'
        verbose_name_plural = 'highlights'
        ordering = ['sort_order']  # not automatically inherited!

    def __str__(self):
        return self.page.title + '->' + self.highlight.title


class CTABase(WagtailOrderable, models.Model):
    hero = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cta_hero',
        verbose_name='Hero Image',
    )

    header = models.TextField(
        blank=True,
    )

    subhead = RichTextField(
        features=[
            'bold', 'italic', 'link',
        ],
        blank=True,
    )

    commitment = models.CharField(
        blank=True,
        max_length=256,
        help_text='Amount of time required (eg: "30 min commitment")',
    )

    buttonTitle = models.CharField(
        verbose_name='Button Text',
        max_length=250,
        blank=True,
    )

    buttonURL = models.TextField(
        verbose_name='Button URL',
        blank=True,
    )

    panels = [
        ImageChooserPanel('hero'),
        FieldPanel('header'),
        FieldPanel('subhead'),
        FieldPanel('commitment'),
        FieldPanel('buttonTitle'),
        FieldPanel('buttonURL'),
    ]

    class Meta:
        abstract = True
        verbose_name = 'cta'
        verbose_name_plural = 'ctas'
        ordering = ['sort_order']  # not automatically inherited!

    def __str__(self):
        return self.page.title + '->' + self.highlight.title


class CTA4(CTABase):
    page = ParentalKey(
        'wagtailpages.ParticipatePage2',
        related_name='cta4',
    )


class ParticipateHighlightsBase(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.ParticipatePage2',
        related_name='featured_highlights',
    )
    highlight = models.ForeignKey('highlights.Highlight', on_delete=models.CASCADE, related_name='+')
    commitment = models.CharField(
        blank=True,
        max_length=256,
        help_text='Amount of time required (eg: "30 min commitment")',
    )
    panels = [
        SnippetChooserPanel('highlight'),
        FieldPanel('commitment'),
    ]

    class Meta:
        abstract = True
        verbose_name = 'highlight'
        verbose_name_plural = 'highlights'
        ordering = ['sort_order']  # not automatically inherited!

    def __str__(self):
        return self.page.title + '->' + self.highlight.title


class ParticipateHighlights(ParticipateHighlightsBase):
    page = ParentalKey(
        'wagtailpages.ParticipatePage2',
        related_name='featured_highlights',
    )


class ParticipateHighlights2(ParticipateHighlightsBase):
    page = ParentalKey(
        'wagtailpages.ParticipatePage2',
        related_name='featured_highlights2',
    )


class Homepage(FoundationMetadataPageMixin, Page):
    hero_headline = models.CharField(
        max_length=140,
        help_text='Hero story headline',
        blank=True,
    )

    hero_story_description = RichTextField(
        features=[
            'bold', 'italic', 'link',
        ]
    )

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='hero_image'
    )

    hero_button_text = models.CharField(
        max_length=50,
        blank=True
    )

    hero_button_url = models.URLField(
        blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_headline'),
            FieldPanel('hero_story_description'),
            FieldRowPanel([
                FieldPanel('hero_button_text'),
                FieldPanel('hero_button_url'),
            ]),
            ImageChooserPanel('hero_image'),
        ],
            heading='hero',
            classname='collapsible'
        ),
        InlinePanel('featured_blogs', label='Blogs', max_num=4),
        InlinePanel('featured_highlights', label='Highlights', max_num=5),
    ]

    subpage_types = [
        'BanneredCampaignPage',
        'IndexPage',
        'InitiativesPage',
        'MiniSiteNameSpace',
        'NewsPage',
        'OpportunityPage',
        'ParticipatePage',
        'ParticipatePage2',
        'PeoplePage',
        'PrimaryPage',
        'RedirectingPage',
        'Styleguide',
    ]

    def get_context(self, request):
        # We need to expose MEDIA_URL so that the s3 images will show up properly
        # due to our custom image upload approach pre-wagtail
        context = super().get_context(request)
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['menu_root'] = self
        context['menu_items'] = self.get_children().live().in_menu()
        return context


class RedirectingPage(Page):
    URL = models.URLField(
        help_text='The fully qualified URL that this page should map to.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('URL'),
    ]

    show_in_menus_default = True

    def serve(self, request):
        # Note that due to how this page type works, there is no
        # associated template file in the wagtailpages directory.
        return HttpResponseRedirect(self.URL)


class YoutubeRegretsPage(FoundationMetadataPageMixin, Page):
    headline = models.CharField(
        max_length=500,
        help_text='Page headline',
        blank=True,
    )

    intro_text = StreamField([
        ('text', blocks.CharBlock()),
    ])

    intro_images = StreamField([
        ('image', customblocks.ImageBlock()),
    ])

    faq = StreamField(
        [
            ('paragraph', blocks.RichTextBlock(
                features=[
                    'bold', 'italic',
                    'h2', 'h3', 'h4', 'h5',
                    'ol', 'ul',
                    'link', 'hr',
                ]
            ))
        ],
        blank=True,
    )

    regret_stories = StreamField([
        ('regret_story', customblocks.YoutubeRegretBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('headline'),
        StreamFieldPanel('intro_text'),
        StreamFieldPanel('intro_images'),
        StreamFieldPanel('faq'),
        StreamFieldPanel('regret_stories'),
    ]

    zen_nav = True

    def get_context(self, request):
        context = super().get_context(request)
        return set_main_site_nav_information(self, context, 'Homepage')

    template = 'wagtailpages/pages/youtube_regrets_page.html'
