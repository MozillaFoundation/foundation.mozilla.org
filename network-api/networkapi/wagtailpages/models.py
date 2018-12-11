import json
from django.db import models
from django.conf import settings
from django.http import HttpResponseRedirect

from . import customblocks
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable as WagtailOrderable
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import InlinePanel
from wagtailmetadata.models import MetadataPageMixin

from .utils import get_page_tree_information
from .donation_modal import DonationModals  # noqa: F401

"""
We'll need to figure out which components are truly "base" and
which are bits that should be used in subclassing template-based
page types.
"""
base_fields = [
    ('heading', blocks.CharBlock()),
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
    ('image_text2', customblocks.ImageTextBlock2()),
    ('figure', customblocks.FigureBlock()),
    ('figuregrid', customblocks.FigureGridBlock()),
    ('figuregrid2', customblocks.FigureGridBlock2()),
    ('video', customblocks.VideoBlock()),
    ('iframe', customblocks.iFrameBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('spacer', customblocks.BootstrapSpacerBlock()),
    ('quote', customblocks.QuoteBlock()),
    ('pulse_listing', customblocks.PulseProjectList()),
    ('profile_listing', customblocks.LatestProfileList()),
    ('profile_by_id', customblocks.ProfileById()),
]


class ModularPage(MetadataPageMixin, Page):
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

    # Legacy field for now, necessary to make sure that the
    # actualy <title> element has the correct value in it.
    # This uses page.meta_title in the base.html
    # master template, which is still based on Mezzanine
    # page models, rather than Wagtail pages models.
    @property
    def meta_title(self):
        return self.title

    show_in_menus_default = True


class MiniSiteNameSpace(ModularPage):
    subpage_types = [
        'CampaignPage',
        'OpportunityPage',
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
        context = super(MiniSiteNameSpace, self).get_context(request)
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

    class Meta:
        verbose_name = 'signup snippet'


class OpportunityPage(MiniSiteNameSpace):
    """
    these pages come with sign-up-for-xyz CTAs
    """
    cta = models.ForeignKey(
        'Signup',
        related_name='page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose existing or create new petition form'
    )

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        SnippetChooserPanel('cta'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'OpportunityPage',
        'RedirectingPage',
    ]


@register_snippet
class Petition(CTA):
    legacy_petition = models.BooleanField(
        help_text='Mark this petition as a legacy petition in terms of where the data gets sent.',
        default=False,
    )

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

    google_forms_url = models.URLField(
        help_text='Google form to post petition data to',
        max_length=2048,
        null=True,
        blank=True,
    )

    checkbox_1 = models.CharField(
        max_length=1024,
        help_text='label for the first checkbox option (may contain HTML)',
        blank=True,
    )

    checkbox_2 = models.CharField(
        max_length=1024,
        help_text='label for the second checkbox option (may contain HTML)',
        blank=True,
    )

    checkbox_1_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Checkbox 1',
        verbose_name='First checkbox Google Form field',
        blank=True,
    )

    checkbox_2_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Checkbox 1',
        verbose_name='Second checkbox Google Form field',
        blank=True,
    )

    given_name_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Given Name(s)',
        verbose_name='Given Name(s) Google Form field',
        blank=True,
    )

    surname_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Surname',
        verbose_name='Surname Google Form field',
        blank=True,
    )

    email_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Email',
        verbose_name='Email Google Form field',
        blank=True,
    )

    newsletter_signup_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Mozilla Newsletter checkbox',
        verbose_name='Mozilla Newsletter signup checkbox Google Form field',
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


class PrimaryPage(MetadataPageMixin, Page):
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
        StreamFieldPanel('body'),
    ]

    parent_page_types = [
        'Homepage',
        'PrimaryPage',
    ]

    subpage_types = [
        'PrimaryPage',
        'RedirectingPage'
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super(PrimaryPage, self).get_context(request)
        return get_page_tree_information(self, context)


class NewsPage(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/news_page.html'


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

    panels = [
        ImageChooserPanel('sectionImage'),
        FieldPanel('sectionHeader'),
        FieldPanel('sectionCopy'),
        FieldPanel('sectionButtonTitle'),
        FieldPanel('sectionButtonURL'),
    ]


class InitiativesPage(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/initiatives_page.html'

    subpage_types = [
        'MiniSiteNameSpace',
        'RedirectingPage',
        'OpportunityPage',
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
    template = 'wagtailpages/static/people_page.html'


class Styleguide(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/styleguide.html'


# Code for the new wagtail based homepage


class HomepageFeaturedNews(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='featured_news',
    )
    news = models.ForeignKey('news.News', related_name='+')
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
    highlight = models.ForeignKey('highlights.Highlight', related_name='+')
    panels = [
        SnippetChooserPanel('highlight'),
    ]

    class Meta:
        verbose_name = 'highlight'
        verbose_name_plural = 'highlights'
        ordering = ['sort_order']  # not automatically inherited!

    def __str__(self):
        return self.page.title + '->' + self.highlight.title


class InitiativesHighlights(WagtailOrderable, models.Model):
    page = ParentalKey(
        'wagtailpages.InitiativesPage',
        related_name='featured_highlights',
    )
    highlight = models.ForeignKey('highlights.Highlight', related_name='+')
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
    highlight = models.ForeignKey('highlights.Highlight', related_name='+')
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


class Homepage(MetadataPageMixin, Page):
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
        InlinePanel('featured_highlights', label='Highlights', max_num=5),
        InlinePanel('featured_news', label='News', max_num=4),
    ]

    subpage_types = [
        'PrimaryPage',
        'PeoplePage',
        'InitiativesPage',
        'Styleguide',
        'NewsPage',
        'ParticipatePage',
        'ParticipatePage2',
        'MiniSiteNameSpace',
        'RedirectingPage',
        'OpportunityPage',
    ]

    def get_context(self, request):
        # We need to expose MEDIA_URL so that the s3 images will show up properly
        # due to our custom image upload approach pre-wagtail
        context = super(Homepage, self).get_context(request)
        context['MEDIA_URL'] = settings.MEDIA_URL
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
