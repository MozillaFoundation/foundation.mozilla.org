from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail_color_panel.fields import ColorField

from wagtail_localize.fields import SynchronizedField, TranslatableField
from wagtail_color_panel.edit_handlers import NativeColorPanel

from networkapi.wagtailpages.models import Profile
from networkapi.wagtailpages.utils import set_main_site_nav_information
from ..customblocks.base_rich_text_options import base_rich_text_options
from ..mixin.foundation_metadata import FoundationMetadataPageMixin
from django import forms


class PublicationAuthors(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("wagtailpages.PublicationPage", related_name="authors")

    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=False
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

    def __str__(self):
        return f"Author: {self.author.name}"


class PublicationPage(FoundationMetadataPageMixin, Page):
    """
    This is the root page of a publication.

    From here the user can browse to the various sections (called chapters).
    It will have information on the publication, its authors, and metadata from it's children

    Publications are collections of Articles
    Publications can also be broken down into Chapters, which are really just child publication pages
    Each of those Chapters may have several Articles
    An Article can only belong to one Chapter/Publication Page
    """

    subpage_types = ['ArticlePage', 'PublicationPage']

    toc_thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='toc_thumbnail_image',
        verbose_name='Table of Content Thumbnail',
        help_text='Thumbnail image to show on table of content. Use square image of 320×320 pixels or larger.',
    )

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='publication_hero_image',
        verbose_name='Publication Hero Image',
    )

    hero_video = models.CharField(
        blank=True,
        max_length=500,
        help_text='Log into Vimeo using 1Password '
                  'and upload the desired video. '
                  'Then select the video and '
                  'click "Advanced", "Distribution", '
                  'and "Video File Links". Copy and paste the link here.'
    )

    HERO_CONTENT_IMAGE = 'image'
    HERO_CONTENT_VIDEO = 'video'

    displayed_hero_content = models.CharField(
        max_length=25,
        choices=[
            (HERO_CONTENT_IMAGE, 'Image'),
            (HERO_CONTENT_VIDEO, 'Video'),
        ],
        default=HERO_CONTENT_IMAGE
    )

    hero_background_color = ColorField(
        default='#ffffff',
        help_text='Please check your chosen background color with '
                  'https://webaim.org/resources/contrastchecker/ to see if your text and background '
                  'color pass accessibility standards. If your text is black '
                  'enter #000000 in the Foreground Color box and #FFFFFF if '
                  'your text is white. After you have selected your background color, '
                  'please contact the design team for a design review!'
    )

    HERO_TEXT_COLOR_DARK = "black"
    HERO_TEXT_COLOR_LIGHT = "white"

    hero_text_color = models.CharField(
        max_length=25,
        choices=[
            (HERO_TEXT_COLOR_DARK, 'Black'),
            (HERO_TEXT_COLOR_LIGHT, 'White'),
        ],
        default=HERO_TEXT_COLOR_DARK,
        help_text='For proper contrast, we recommend using “White” for dark background colors, '
                  'and “Black” for light background colors.'
    )

    subtitle = models.CharField(
        blank=True,
        max_length=250,
    )

    secondary_subtitle = models.CharField(
        blank=True,
        max_length=250,
    )

    publication_date = models.DateField("Publication date", null=True, blank=True)

    publication_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    HERO_LAYOUT_FULL_SCREEN = 'full_screen'
    HERO_LAYOUT_IMAGE_LEFT = 'image_left'
    HERO_LAYOUT_IMAGE_RIGHT = 'image_right'
    HERO_LAYOUT_STATIC = 'static'

    hero_layout = models.CharField(
        max_length=25,
        choices=[
            (HERO_LAYOUT_FULL_SCREEN, 'Full Screen'),
            (HERO_LAYOUT_IMAGE_LEFT, 'Image Left'),
            (HERO_LAYOUT_IMAGE_RIGHT, 'Image Right'),
            (HERO_LAYOUT_STATIC, 'Static'),
        ],
        default=HERO_LAYOUT_STATIC,
    )

    HERO_BTN_STYLE_PRIMARY = 'primary'
    HERO_BTN_STYLE_SECONDARY = 'secondary'
    HERO_BTN_STYLE_TERTIARY = 'tertiary'

    download_button_style = models.CharField(
        max_length=25,
        choices=[
            (HERO_BTN_STYLE_PRIMARY, 'Primary'),
            (HERO_BTN_STYLE_SECONDARY, 'Secondary'),
            (HERO_BTN_STYLE_TERTIARY, 'Tertiary'),
        ],
        default=HERO_BTN_STYLE_PRIMARY,
    )

    # Since wagtail cannot save SVG files as images,
    # we are instead uploading them as a document.
    download_button_icon = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Custom Icon for download button, please use https://feathericons.com"
    )

    show_authors = models.BooleanField(
        default=True,
        help_text="Display authors in the hero section"
    )

    additional_author_copy = models.CharField(
        help_text="Example: with contributing authors",
        max_length=100,
        blank=True,
    )

    intro_notes = RichTextField(
        blank=True,
        features=base_rich_text_options + ['h4']
    )

    notes = RichTextField(
        blank=True,
        features=base_rich_text_options + ['h4', 'ol', 'ul']
    )

    contents_title = models.CharField(
        blank=True,
        default="Table of Contents",
        max_length=250,
    )

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            InlinePanel("authors", label="Author", min_num=0)
        ], heading="Author(s)"),
        MultiFieldPanel([
            ImageChooserPanel("toc_thumbnail_image")
        ], heading="Table of Content Thumbnail"),
        MultiFieldPanel(
            [
                FieldPanel('hero_layout', widget=forms.RadioSelect),
                FieldPanel('show_authors'),
                FieldPanel('additional_author_copy'),
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_video'),
                FieldPanel('displayed_hero_content', widget=forms.RadioSelect),
                NativeColorPanel('hero_background_color'),
                FieldPanel('hero_text_color', widget=forms.RadioSelect),
                FieldPanel('subtitle'),
                FieldPanel('secondary_subtitle'),
                FieldPanel('publication_date'),
                FieldPanel('download_button_style', widget=forms.RadioSelect),
                DocumentChooserPanel('download_button_icon'),
                DocumentChooserPanel('publication_file', heading="Download button file"),
            ],
            heading='Hero',
        ),
        FieldPanel('intro_notes'),
        FieldPanel('contents_title'),
        FieldPanel('notes'),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField('slug'),
        TranslatableField('seo_title'),
        SynchronizedField('show_in_menus'),
        TranslatableField('search_description'),
        SynchronizedField('search_image'),
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("subtitle"),
        TranslatableField('secondary_subtitle'),
        SynchronizedField('toc_thumbnail_image'),
        SynchronizedField('hero_image'),
        SynchronizedField('publication_date'),
        SynchronizedField('publication_file'),
        SynchronizedField('authors'),
        TranslatableField('additional_author_copy'),
        TranslatableField('intro_notes'),
        TranslatableField('contents_title'),
        TranslatableField('notes'),
    ]

    @property
    def is_publication_page(self):
        """
        Returning true to let publication_hero.html to show breadcrumbs
        """
        return True

    @property
    def is_chapter_page(self):
        """
        A PublicationPage nested under a PublicationPage is considered to be a
        "ChapterPage". The templates used very similar logic and structure, and
        all the fields are the same.
        """
        parent = self.get_parent().specific
        return parent.__class__ is PublicationPage

    @property
    def next_page(self):
        """
        Only applies to Chapter Publication (sub-Publication Pages).
        Returns a Page object or None.
        """
        next_page = self.get_parent()
        if self.is_chapter_page:
            sibling = self.get_siblings().filter(path__gt=self.path, live=True).first()
            if sibling:
                # If there is no more chapters. Return the parent page.
                next_page = sibling
        return next_page

    @property
    def prev_page(self):
        """
        Only applies to Chapter Publication (sub-Publication Pages).
        Returns a Page object or None.
        """
        prev_page = self.get_parent()
        if self.is_chapter_page:
            sibling = self.get_siblings().filter(path__lt=self.path, live=True).reverse().first()
            if sibling:
                # If there is no more chapters. Return the parent page.
                prev_page = sibling
        return prev_page

    @property
    def zen_nav(self):
        return True

    def breadcrumb_list(self):
        """
        Get all the parent PublicationPages and return a QuerySet
        """
        return Page.objects.ancestor_of(self).type(PublicationPage).live()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        pages = []
        for page in self.get_children():
            if request.user.is_authenticated:
                # User is logged in, and can preview a page. Get all pages, even drafts.
                pages.append({
                    'child': page,
                    'grandchildren': page.get_children()
                })
            elif page.live:
                # User is not logged in AND this page is live. Only fetch live grandchild pages.
                pages.append({
                    'child': page,
                    'grandchildren': page.get_children().live()
                })
        context['child_pages'] = pages
        return set_main_site_nav_information(self, context, 'Homepage')
