from django.conf import settings
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Page, Orderable as WagtailOrderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import PageChooserPanel

from modelcluster.fields import ParentalKey

from .primary import PrimaryPage
from .mixin.foundation_metadata import FoundationMetadataPageMixin

# TODO:  https://github.com/mozilla/foundation.mozilla.org/issues/2362
from ..donation_modal import DonationModals  # noqa: F401


class NewsPage(PrimaryPage):
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
    template = 'wagtailpages/static/initiatives_page.html'

    subpage_types = [
        'BanneredCampaignPage',
        'MiniSiteNameSpace',
        'OpportunityPage',
        'RedirectingPage',
        # The following additional types are here to ensure
        # that the /initiatives route can house all the pages
        # that originally lived under /opportunity
        'BlogPage',
        'CampaignPage',
        'YoutubeRegretsPage',
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


class ParticipatePage2(PrimaryPage):
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
        MultiFieldPanel(
          [
            ImageChooserPanel('ctaHero'),
            FieldPanel('ctaHeroHeader'),
            FieldPanel('ctaHeroSubhead'),
            FieldPanel('ctaButtonTitle'),
            FieldPanel('ctaButtonURL'),
          ],
          heading="Primary CTA",
          classname="collapsible"
        ),
        FieldPanel('h2'),
        FieldPanel('h2Subheader'),
        InlinePanel('featured_highlights', label='Highlights Group 1', max_num=3),
        MultiFieldPanel(
          [
            ImageChooserPanel('ctaHero2'),
            FieldPanel('ctaHeroHeader2'),
            FieldPanel('ctaHeroSubhead2'),
            FieldPanel('ctaButtonTitle2'),
            FieldPanel('ctaButtonURL2'),
          ],
          heading="CTA 2",
          classname="collapsible"
        ),
        InlinePanel('featured_highlights2', label='Highlights Group 2', max_num=6),
        MultiFieldPanel(
          [
            ImageChooserPanel('ctaHero3'),
            FieldPanel('ctaHeroHeader3'),
            FieldPanel('ctaHeroSubhead3'),
            FieldPanel('ctaFacebook3'),
            FieldPanel('ctaTwitter3'),
            FieldPanel('ctaEmailShareSubject3'),
            FieldPanel('ctaEmailShareBody3'),
          ],
          heading="CTA 3",
          classname="collapsible"
        ),
        InlinePanel('cta4', label='CTA Group 4', max_num=3),
    ]


class Styleguide(PrimaryPage):
    template = 'wagtailpages/static/styleguide.html'


class HomepageSpotlightPosts(WagtailOrderable):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='spotlight_posts',
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


class HomepageNewsYouCanUse(WagtailOrderable):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='news_you_can_use',
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
    panels = [
        SnippetChooserPanel('highlight'),
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


@register_snippet
class FocusArea(models.Model):
    interest_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='interest_icon'
    )

    name = models.CharField(
        max_length=100,
        help_text='The name of this area of focus. Max. 100 characters.',
    )

    description = models.TextField(
        max_length=300,
        help_text='Description of this area of focus. Max. 300 characters.',
    )

    page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        ImageChooserPanel('interest_icon'),
        FieldPanel('name'),
        FieldPanel('description'),
        PageChooserPanel('page'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Area of focus'
        verbose_name_plural = 'Areas of focus'


class HomepageFocusAreas(WagtailOrderable):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='focus_areas',
    )

    area = models.ForeignKey(FocusArea, on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('area'),
    ]


class HomepageTakeActionCards(WagtailOrderable):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='take_action_cards',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    text = models.CharField(max_length=255)
    internal_link = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('text'),
        PageChooserPanel('internal_link'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Take Action Card"
        ordering = ['sort_order']  # not automatically inherited!


class PartnerLogos(WagtailOrderable):
    page = ParentalKey(
        'wagtailpages.Homepage',
        related_name='partner_logos',
    )
    link = models.URLField(blank=True)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    name = models.CharField(
        default='Partner Name',
        blank=False,
        max_length=100,
        help_text='Alt text for the logo image.'
    )
    width = models.PositiveSmallIntegerField(
        default=100,
        help_text='The width of the image. Height will automatically be applied.'
    )
    panels = [
        ImageChooserPanel('logo'),
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('width'),
    ]

    @property
    def image_rendition(self):
        width = self.width * 2
        return self.logo.get_rendition(f'width-{width}')

    class Meta:
        verbose_name = 'Partner Logo'
        ordering = ['sort_order']  # not automatically inherited!


class Homepage(FoundationMetadataPageMixin, Page):
    hero_headline = models.CharField(
        max_length=80,
        help_text='Hero story headline',
        blank=True,
    )

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='hero_image'
    )

    def get_banner(self):
        return self.hero_image

    hero_button_text = models.CharField(
        max_length=50,
        blank=True
    )

    hero_button_url = models.URLField(
        blank=True
    )

    spotlight_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='spotlight_image',
    )

    spotlight_headline = models.CharField(
        max_length=140,
        help_text='Spotlight headline',
        blank=True,
    )

    cause_statement = models.CharField(
        max_length=250,
        default="",
    )

    cause_statement_link_text = models.CharField(
        max_length=80,
        blank=True,
    )

    cause_statement_link_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cause_statement_link'
    )

    quote_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='quote_image',
    )

    quote_text = models.CharField(
        max_length=450,
        default='',
    )

    quote_source_name = models.CharField(
        max_length=100,
        default='',
    )

    quote_source_job_title = models.CharField(
        max_length=100,
        default='',
    )

    # Partner Section
    partner_heading = models.CharField(max_length=75, default='Partner with us')
    partner_intro_text = models.TextField(blank=True)
    partner_page_text = models.CharField(max_length=35, default="Let's work together")
    partner_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='parnter_internal_link',
    )
    partner_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    # Take Action Section
    take_action_title = models.CharField(default='Take action', max_length=50)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
          [
            FieldPanel('hero_headline'),
            FieldPanel('hero_button_text'),
            FieldPanel('hero_button_url'),
            ImageChooserPanel('hero_image'),
          ],
          heading='hero',
          classname='collapsible'
        ),
        MultiFieldPanel(
          [
            FieldPanel('cause_statement'),
            FieldPanel('cause_statement_link_text'),
            PageChooserPanel('cause_statement_link_page'),
          ],
          heading='cause statement',
          classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                InlinePanel('focus_areas', min_num=3, max_num=3),
            ],
            heading='Areas of focus',
            classname='collapsible collapsed',
        ),
        MultiFieldPanel(
            [
                InlinePanel('news_you_can_use', min_num=4, max_num=4),
            ],
            heading='News you can use',
            classname='collapsible'
        ),
        MultiFieldPanel(
          [
            ImageChooserPanel('spotlight_image'),
            FieldPanel('spotlight_headline'),
            InlinePanel('spotlight_posts', label='Posts', min_num=3, max_num=3),
          ],
          heading='spotlight',
          classname='collapsible'
        ),
        MultiFieldPanel(
            [
                FieldPanel('take_action_title'),
                InlinePanel('take_action_cards', label='Take Action Cards', max_num=4),
            ],
            heading='Take Action',
            classname='collapsible',
        ),
        MultiFieldPanel(
          [
            ImageChooserPanel('quote_image'),
            FieldPanel('quote_text'),
            FieldPanel('quote_source_name'),
            FieldPanel('quote_source_job_title'),
          ],
          heading='quote',
          classname='collapsible collapsed',
        ),
        MultiFieldPanel(
          [
            FieldPanel('partner_heading'),
            FieldPanel('partner_intro_text'),
            FieldPanel('partner_page_text'),
            PageChooserPanel('partner_page'),
            ImageChooserPanel('partner_background_image'),
            InlinePanel('partner_logos', label='Partner Logo', max_num=7, min_num=1),
          ],
          heading='Partner',
          classname='collapsible collapsed'
        ),
    ]

    subpage_types = [
        'BanneredCampaignPage',
        'BlogIndexPage',
        'CampaignIndexPage',
        'InitiativesPage',
        'MiniSiteNameSpace',
        'NewsPage',
        'OpportunityPage',
        'ParticipatePage2',
        'PrimaryPage',
        'PublicationPage',
        'RedirectingPage',
        'Styleguide',
        'ProductPage',
        'BuyersGuidePage',
    ]

    def get_context(self, request):
        # We need to expose MEDIA_URL so that the s3 images will show up properly
        # due to our custom image upload approach pre-wagtail
        context = super().get_context(request)
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['menu_root'] = self
        context['menu_items'] = self.get_children().live().in_menu()
        return context
