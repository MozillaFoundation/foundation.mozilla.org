from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable, Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel
from django import forms

from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages.models import Profile, PublicationPage
from networkapi.wagtailpages.utils import get_plaintext_titles, set_main_site_nav_information, TitleWidget

from ..mixin.foundation_metadata import FoundationMetadataPageMixin
from ..article_fields import article_fields


class ArticleAuthors(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("wagtailpages.ArticlePage", related_name="authors")

    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=False
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

    def __str__(self):
        return self.author.name


class ArticlePage(FoundationMetadataPageMixin, Page):

    """

    Articles can belong to any page in the Wagtail Tree.
    An ArticlePage can have no children
    If not a child of a Publication Page, page nav at bottom of page
    and breadcrumbs will not render.
    """
    subpage_types = []
    body = StreamField(article_fields)

    toc_thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Table of Content Thumbnail',
        help_text='Thumbnail image to show on table of content. Use square image of 320×320 pixels or larger.',
    )

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
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

    article_file = models.ForeignKey(
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

    show_side_share_buttons = models.BooleanField(
        default=True,
        help_text="Show social share buttons on the side"
    )

    show_authors = models.BooleanField(
        default=True,
        help_text="Display authors in the hero section"
    )

    content_panels = [
        FieldPanel(
            "title",
            classname="full title",
            widget=TitleWidget(attrs={"class": "max-length-warning", "data-max-length": 60})
        ),
        MultiFieldPanel([
            InlinePanel("authors", label="Author", min_num=0)
        ], heading="Author(s)"),
        MultiFieldPanel([
            ImageChooserPanel("toc_thumbnail_image"),
        ], heading="Table of Content Thumbnail"),
        MultiFieldPanel([
            FieldPanel('hero_layout', widget=forms.RadioSelect),
            FieldPanel('show_authors'),
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
            DocumentChooserPanel('article_file', heading="Download button file"),
        ], heading="Hero"),
        FieldPanel('show_side_share_buttons'),
        StreamFieldPanel('body'),
        InlinePanel("footnotes", label="Footnotes"),
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
        SynchronizedField('authors'),
        SynchronizedField('toc_thumbnail_image'),
        SynchronizedField('hero_image'),
        TranslatableField('subtitle'),
        SynchronizedField('article_file'),
        TranslatableField('body'),
        TranslatableField('footnotes'),
    ]

    @property
    def is_publication_article(self):
        parent = self.get_parent().specific
        return parent.__class__ is PublicationPage

    @property
    def next_page(self):
        """
        Get the next page for a publication. Details below:

        Check the parent page type. If the parent page type is a "Chapter Page",
        then look for siblings of `this` page. If no next sibling can be found
        look for the parent page next sibling. And if that cannot be found,
        return the Chapter Page's parent (Publication Page).
        Otherwise if the parent page is a Publication page: look for the next sibling,
        if there is no next sibling page, return this pages' parent.
        """

        parent = self.get_parent().specific
        next_page = self.get_siblings().filter(path__gt=self.path, live=True).first()
        if parent.is_chapter_page:
            # if there is no next page look for the next chapter
            if not next_page:
                next_page = parent.get_siblings().filter(path__gt=self.path, live=True).first()
                # if there is no next chapter return to the parent.get_parent()
                if not next_page:
                    next_page = parent.get_parent()
        else:
            # Parent is a PublicationPage, not a chapter page
            # if there is no next page, return the parent
            if not next_page:
                next_page = parent

        return next_page

    @property
    def prev_page(self):
        """
        Get the previous page for a publication. Details below:

        Check the parent page type. If the parent page type is a "Chapter Page",
        then look for siblings of `this` page. If no previous sibling can be found
        look for the parent page previous sibling. And if that cannot be found,
        return the Chapter Page's parent (Publication Page).
        Otherwise if the parent page is a Publication page: look for the previous sibling,
        if there is no previous sibling page, return this pages' parent.
        """

        parent = self.get_parent().specific
        prev_page = self.get_siblings().filter(path__lt=self.path, live=True).reverse().first()
        if parent.is_chapter_page:
            # look for the previous page in this chapter
            # if there is no previous page look for the previous chapter
            if not prev_page:
                prev_page = parent.get_siblings().filter(path__lt=self.path, live=True).reverse().first()
                # if there is no previous chapter return to the parent.get_parent()
                if not prev_page:
                    prev_page = parent.get_parent()
        else:
            # Parent is a PublicationPage, not a chapter page
            # look for the previous page in this publication
            # if there is no previous page, return the parent
            if not prev_page:
                prev_page = parent

        return prev_page

    def breadcrumb_list(self):
        """
        Get all the parent PublicationPages and return a QuerySet
        """
        return Page.objects.ancestor_of(self).type(PublicationPage).live()

    @property
    def zen_nav(self):
        return True

    @property
    def get_page_titles(self):
        return get_plaintext_titles(None, self.body, "content")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Add get_titles to the page context. This is in get_context() because
        # we need access to the `request` object
        # menu_items is required for zen_nav in the templates
        context['get_titles'] = get_plaintext_titles(request, self.body, "content")
        return set_main_site_nav_information(self, context, 'Homepage')
