from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.utils import (
    set_main_site_nav_information,
    get_page_tree_information
)

from networkapi.wagtailpages.models import (
    base_fields,
    FoundationMetadataPageMixin,
    FoundationBannerInheritanceMixin,
    Signup
)

from networkapi.wagtailpages.pagemodels import customblocks


class MozfestPrimaryPage(FoundationMetadataPageMixin, FoundationBannerInheritanceMixin, Page):
    header = models.CharField(
        max_length=250,
        blank=True
    )

    banner = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='mozfest_primary_banner',
        verbose_name='Hero Image',
        help_text='Choose an image that\'s bigger than 4032px x 1152px with aspect ratio 3.5:1',
    )

    intro = RichTextField(
        help_text='Page intro content',
        blank=True
    )

    signup = models.ForeignKey(
        Signup,
        related_name='mozfestpage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Choose an existing, or create a new, sign-up form'
    )

    body = StreamField(
        base_fields + [
            ('session_slider_list_block', customblocks.SessionSliderListBlock()),
            ('space_card_list', customblocks.SpaceCardListBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        ImageChooserPanel('banner'),
        FieldPanel('intro'),
        SnippetChooserPanel('signup'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'MozfestPrimaryPage',
    ]

    show_in_menus_default = True

    use_wide_template = models.BooleanField(
        default=False,
        help_text="Make the body content wide, useful for components like directories"
    )

    settings_panels = Page.settings_panels + [
       FieldPanel('use_wide_template')
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('title'),
        TranslatableField('header'),
        SynchronizedField('banner'),
        TranslatableField('intro'),
        TranslatableField('signup'),
        TranslatableField('body'),
    ]

    def get_template(self, request):
        if self.use_wide_template:
            return 'mozfest/mozfest_primary_page_wide.html'

        return 'mozfest/mozfest_primary_page.html'

    def get_context(self, request, bypass_menu_buildstep=False):
        context = super().get_context(request)
        context = set_main_site_nav_information(self, context, 'MozfestHomepage')
        context = get_page_tree_information(self, context)

        # primary nav information
        context['menu_root'] = self
        context['menu_items'] = self.get_children().live().in_menu()

        # Also make sure that these pages always tap into the mozfest newsletter for the footer!
        mozfest_footer = Signup.objects.filter(name__iexact='mozfest').first()
        context['mozfest_footer'] = mozfest_footer

        if not bypass_menu_buildstep:
            context = set_main_site_nav_information(self, context, 'MozfestHomepage')

        return context


class MozfestHomepage(MozfestPrimaryPage):
    """
    MozFest Homepage

    'banner_video_type' determines what version of banner design the page should load

    If the value of `banner_video_type` is `hardcoded`, it displays a hardcoded,
    predefined video in the banner background.

    If the value of `banner_video_type` is `featured`, it displays a carousel of
    cards with their associated headings and body content (`banner_carousel`),
    and an embedded user-defined video (`banner_video`).
    """
    banner_video_type = "featured"

    cta_button_label = models.CharField(
        max_length=250,
        blank=True,
        help_text='Label text for the CTA button in the primary nav bar',
    )

    cta_button_destination = models.CharField(
        max_length=2048,
        blank=True,
        help_text='The URL for the page that the CTA button in the primary nav bar should redirect to.'
                  'E.g., /proposals, https://example.com/external-link',
    )

    banner_heading = models.CharField(
        max_length=250,
        blank=True,
        help_text='A banner heading specific to the homepage'
    )

    banner_guide_text = models.CharField(
        max_length=1000,
        blank=True,
        help_text='A banner paragraph specific to the homepage'
    )

    # For banner_video_type == 'hardcoded'
    banner_video_url = models.URLField(
        max_length=2048,
        blank=True,
        help_text='The video to play when users click "watch video"'
    )

    # For banner_video_type == 'featured'
    banner_carousel = StreamField(
        [
            ('slide', customblocks.BannerCarouselSlideBlock()),
        ],
        max_num=3,
        help_text='The slides shown on the new Hero. Please ensure that there '
                  'are exactly 3 slides. The old Hero will be shown if there '
                  'are no slides present.',
        blank=True,
        null=True,
    )

    # For banner_video_type == 'featured'
    banner_video = StreamField(
        [
            ('CMS_video', customblocks.WagtailVideoChooserBlock()),
            ('external_video', customblocks.ExternalVideoBlock()),
        ],
        max_num=1,
        help_text='The video to play when users click "Watch Video". This is '
                  'only shown on the new Hero.',
        blank=True,
        null=True,
    )

    subpage_types = [
        'MozfestPrimaryPage',
        'MozfestHomepage',
    ]

    # Put everything above the body
    parent_panels = MozfestPrimaryPage.content_panels
    panel_count = len(parent_panels)
    n = panel_count - 1

    all_panels = parent_panels[:n] + [
        FieldPanel('cta_button_label'),
        FieldPanel('cta_button_destination'),
        FieldPanel('banner_heading'),
        StreamFieldPanel('banner_carousel'),
        FieldPanel('banner_guide_text'),
        FieldPanel('banner_video_url'),
        StreamFieldPanel('banner_video'),
    ] + parent_panels[n:]

    if banner_video_type == "hardcoded":
        # Hide all the panels that aren't relevant for the video banner version of the MozFest Homepage
        content_panels = [
            field for field in all_panels
            if field.field_name not in [
                'banner', 'header', 'intro', 'banner_carousel', 'banner_guide_text',
                'banner_video', 'banner_video_url',
            ]
        ]
    elif banner_video_type == "featured":
        # Hide all the panels that aren't relevant for the video banner version of the MozFest Homepage
        content_panels = [
            field for field in all_panels
            if field.field_name not in [
                'banner', 'banner_guide_text', 'banner_video_url', 'cta_button_destination',
                'cta_button_label', 'header', 'hero_image', 'intro',
            ]
        ]
    else:
        content_panels = all_panels

    # Because we inherit from PrimaryPage, but the "use_wide_template" property does nothing
    # we should hide it and make sure we use the right template
    settings_panels = Page.settings_panels

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField('title'),
        TranslatableField('cta_button_label'),
        SynchronizedField('cta_button_destination'),
        TranslatableField('banner_heading'),
        TranslatableField('banner_guide_text'),
        SynchronizedField('banner_video_url'),
        TranslatableField('signup'),
        TranslatableField('body'),
        TranslatableField('footnotes'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['banner_video_type'] = self.specific.banner_video_type

        return context

    def get_template(self, request):
        return 'mozfest/mozfest_homepage.html'
