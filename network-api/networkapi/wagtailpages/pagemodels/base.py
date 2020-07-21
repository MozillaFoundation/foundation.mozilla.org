from django.db import models
from django.conf import settings

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Page, Orderable as WagtailOrderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import PageChooserPanel

from modelcluster.fields import ParentalKey

from .primary import PrimaryPage
from .mixin.foundation_metadata import FoundationMetadataPageMixin

# TODO:  https://github.com/mozilla/foundation.mozilla.org/issues/2362
from ..donation_modal import DonationModals  # noqa: F401


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


class PeoplePage(PrimaryPage):
    parent_page_types = ['Homepage']


class Styleguide(PrimaryPage):
    parent_page_types = ['Homepage']
    template = 'wagtailpages/static/styleguide.html'


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

    content_panels = Page.content_panels + [
        MultiFieldPanel(
          [
            FieldPanel('hero_headline'),
            FieldPanel('hero_story_description'),
            FieldRowPanel([
              FieldPanel('hero_button_text'),
              FieldPanel('hero_button_url'),
            ],
            ),
            ImageChooserPanel('hero_image'),
          ],
          heading='hero',
          classname='collapsible'
        ),
        InlinePanel('featured_blogs', label='Blogs', max_num=4),
        InlinePanel('featured_highlights', label='Highlights', max_num=5),
        MultiFieldPanel(
          [
            ImageChooserPanel('quote_image'),
            FieldPanel('quote_text'),
            FieldPanel('quote_source_name'),
            FieldPanel('quote_source_job_title'),
          ],
          heading='quote',
          classname='collapsible'
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
