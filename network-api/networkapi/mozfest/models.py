from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from networkapi.wagtailpages.utils import get_page_tree_information
from networkapi.wagtailpages.models import (
    base_fields,
    FoundationMetadataPageMixin,
    Signup
)


class MozfestPrimaryPage(FoundationMetadataPageMixin, Page):
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

    body = StreamField(base_fields)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        ImageChooserPanel('banner'),
        FieldPanel('intro'),
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

    def get_template(self, request):
        if self.use_wide_template:
            return 'mozfest/mozfest_primary_page_wide.html'

        return 'mozfest/mozfest_primary_page.html'

    def get_context(self, request, bypass_menu_buildstep=False):
        context = super().get_context(request)
        context = get_page_tree_information(self, context)

        # Also make sure that these pages always tap into the mozfest newsletter for the footer!
        mozfest_footer = Signup.objects.filter(name__iexact='mozfest').first()
        context['mozfest_footer'] = mozfest_footer

        # Find the homepage, and then record all pages that should end up as nav items. Note
        # that subclasses can bypass this, because the MozfestHomepage doesn't need any of
        # this work to be done.
        if not bypass_menu_buildstep:
            homepage = list(filter(
                lambda x: x.specific.__class__.__name__ is 'MozfestHomepage',
                self.get_ancestors()
            ))[0]
            context['menu_root'] = homepage
            context['menu_items'] = homepage.get_children().filter(live=True, show_in_menus=True)

        return context


class MozfestHomepage(MozfestPrimaryPage):
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

    banner_video_url = models.URLField(
        max_length=2048,
        blank=True,
        help_text='The video to play when users click "watch video"'
    )

    prefooter_text = RichTextField(
        help_text='Pre-footer content',
        blank=True
    )

    subpage_types = [
        'MozfestPrimaryPage'
    ]

    # Put everything except `prefooter_text` above the body
    parent_panels = MozfestPrimaryPage.content_panels
    panel_count = len(parent_panels)
    n = panel_count - 1

    content_panels = parent_panels[:n] + [
        FieldPanel('banner_heading'),
        FieldPanel('banner_guide_text'),
        FieldPanel('banner_video_url'),
    ] + parent_panels[n:] + [
        FieldPanel('prefooter_text'),
    ]

    # Because we inherit from PrimaryPage, but the "use_wide_templatae" property does nothing
    # we should hide it and make sure we use the right template
    settings_panels = Page.settings_panels

    def get_template(self, request):
        return 'mozfest/mozfest_homepage.html'

    def get_context(self, request):
        context = super().get_context(request, bypass_menu_buildstep=True)
        context['menu_root'] = self
        context['menu_items'] = self.get_children().filter(live=True, show_in_menus=True)
        return context
