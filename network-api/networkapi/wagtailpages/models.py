from django.db import models
from django.conf import settings

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
    ('image', customblocks.AlignedImageBlock()),
    ('image_text', customblocks.ImageTextBlock()),
    ('figure', customblocks.FigureBlock()),
    ('figuregrid', customblocks.FigureGridBlock()),
    ('video', customblocks.VideoBlock()),
    ('iframe', customblocks.iFrameBlock()),
    ('linkbutton', customblocks.LinkButtonBlock()),
    ('spacer', customblocks.BootstrapSpacerBlock()),
]


class ModularPage(MetadataPageMixin, Page):
    """
    The base class offers universal component picking
    """

    header = models.CharField(
        max_length=250,
        blank=True
    )

    body = StreamField(base_fields)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        StreamFieldPanel('body'),
    ]

    # Legacy field for now, necessary to make sure that the
    # actualy <title> element has the correct value in it.
    # This uses page.meta_title in the base-compiled.html
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
        ancestors = self.get_ancestors()
        root = next((n for n in ancestors if n.specific_class == self.specific_class), self)
        context['root'] = root
        context['mini_site_title'] = root.title

        is_top_page = (root == self)
        context['is_top_page'] = is_top_page

        children = self.get_children().live()
        has_children = len(children) > 0
        context['singleton_page'] = (is_top_page and not has_children)

        return context


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
        help_text="Choose existing or create new petition form"
    )

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        SnippetChooserPanel('cta'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'OpportunityPage',
    ]


@register_snippet
class Petition(CTA):
    google_forms_url = models.URLField(
        help_text='Google form to post petition data to',
        max_length=2048,
        null=True
    )

    checkbox_1 = models.CharField(
        max_length=1024,
        help_text='label for the first checkbox option (may contain HTML)',
        blank=True
    )

    checkbox_1_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Checkbox 1',
        verbose_name='First checkbox Google Form field',
        blank=True
    )

    checkbox_2 = models.CharField(
        max_length=1024,
        help_text='label for the second checkbox option (may contain HTML)',
        blank=True
    )

    checkbox_2_form_field = models.CharField(
        max_length=1024,
        help_text='Google form field name for Checkbox 1',
        verbose_name='Second checkbox Google Form field',
        blank=True
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
        blank=True
    )

    share_link_text = models.CharField(
        max_length=20,
        help_text='Text content of the share button',
        default='Share this',
        blank=True
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
        help_text="Choose existing or create new sign-up form"
    )

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        SnippetChooserPanel('cta'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'CampaignPage',
    ]

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
        verbose_name = "news"
        verbose_name_plural = "news"

    def __str__(self):
        return self.page.title + "->" + self.news.headline


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
        verbose_name = "highlight"
        verbose_name_plural = "highlights"

    def __str__(self):
        return self.page.title + "->" + self.highlight.title


class PrimaryPage(Page):
    body = StreamField(base_fields)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['Homepage']


class Homepage(Page):

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
            heading="hero",
            classname="collapsible"
        ),
        InlinePanel('featured_highlights', label="Highlights", max_num=5),
        InlinePanel('featured_news', label="News", max_num=4),
    ]

    def get_context(self, request):
        # We need to expose MEDIA_URL so that the s3 images will show up properly
        # due to our custom image upload approach pre-wagtail
        context = super(Homepage, self).get_context(request)
        print(settings.MEDIA_URL)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context
