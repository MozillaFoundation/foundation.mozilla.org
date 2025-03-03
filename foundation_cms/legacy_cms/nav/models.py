from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from modelcluster import fields as cluster_fields
from modelcluster.models import ClusterableModel
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.legacy_cms.nav import blocks as nav_blocks
from foundation_cms.legacy_cms.nav import utils as nav_utils
from foundation_cms.legacy_cms.nav.forms import NavMenuForm
from foundation_cms.legacy_cms.utility.images import SVGImageFormatValidator
from foundation_cms.legacy_cms.wagtailpages.models import (
    BlogIndexPage,
    BlogPage,
    BlogPageTopic,
)
from foundation_cms.legacy_cms.wagtailpages.utils import localize_queryset


class NavMenuFeaturedBlogTopicRelationship(wagtail_models.TranslatableMixin, wagtail_models.Orderable):
    menu = cluster_fields.ParentalKey(
        "nav.NavMenu",
        on_delete=models.CASCADE,
        related_name="featured_blog_topics",
        verbose_name="Navigation Menu",
    )
    topic = models.ForeignKey(
        "wagtailpages.BlogPageTopic",
        on_delete=models.CASCADE,
        related_name="nav_menu_featured_topics",
        verbose_name="Featured Blog Topic",
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name="Icon",
        help_text="Please use SVG format",
    )

    panels = [
        panels.FieldPanel("topic"),
        panels.FieldPanel("icon"),
    ]

    class Meta(wagtail_models.TranslatableMixin.Meta, wagtail_models.Orderable.Meta):
        verbose_name = "Featured Blog Topic"
        verbose_name_plural = "Featured Blog Topics"

    def __str__(self) -> str:
        return f"{self.menu} - {self.topic}"

    def clean(self):
        clean_data = super().clean()

        # Using _id to check the database field directly, to avoid fetching the object.
        # Fetching using "self.icon" will return a 500 error if a user does not upload an image.
        if self.icon_id:
            icon_image_file = self.icon.file
            # Use SVGImageFormatValidator util to check if the uploaded image is an SVG.
            try:
                SVGImageFormatValidator(icon_image_file)
            except ValidationError as error:
                raise ValidationError({"icon": error})
        return clean_data


class NavMenu(
    wagtail_models.PreviewableMixin,
    wagtail_models.DraftStateMixin,
    wagtail_models.RevisionMixin,
    wagtail_models.TranslatableMixin,
    ClusterableModel,
):
    title = models.CharField(max_length=100, help_text="For internal identification only")

    dropdowns = StreamField(
        [
            ("dropdown", nav_blocks.NavDropdown(label="Dropdown")),
        ],
        use_json_field=True,
        min_num=1,
        max_num=5,
        help_text="Add up to 5 dropdown menus",
    )

    enable_blog_dropdown = models.BooleanField(
        default=False,
        verbose_name="Enable Blog Dropdown?",
    )

    blog_button_label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Blog button label",
    )

    panels = [
        panels.HelpPanel(content="To enable a navigation menu on a site, go to Settings > Navigation Menus."),
        panels.FieldPanel("title"),
        panels.FieldPanel("dropdowns"),
        panels.MultiFieldPanel(
            [
                panels.FieldPanel("enable_blog_dropdown"),
                panels.InlinePanel(
                    "featured_blog_topics",
                    label="Featured Blog Topics",
                    help_text="Choose up to 4 featured topics",
                    min_num=0,
                    max_num=4,
                ),
                panels.FieldPanel("blog_button_label"),
            ],
            heading="Blog",
        ),
    ]
    base_form_class = NavMenuForm

    translatable_fields = [
        SynchronizedField("title"),
        TranslatableField("dropdowns"),
        SynchronizedField("enable_blog_dropdown"),
        TranslatableField("blog_button_label"),
        TranslatableField("featured_blog_topics"),
    ]

    search_fields = [
        index.SearchField("title"),
    ]

    class Meta(wagtail_models.TranslatableMixin.Meta):
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"

    def __str__(self) -> str:
        return self.title

    def get_preview_template(self, request, mode_name):
        return "previews/nav/menu.html"

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        context["localized_featured_blog_topics"] = self.featured_blog_topics.all().order_by("sort_order")
        return context

    @cached_property
    def blog_index_page(self):
        return BlogIndexPage.objects.live().get(locale=wagtail_models.Locale.get_active())

    @property
    def localized_featured_blog_topics(self):
        en_locale = wagtail_models.Locale.objects.get(language_code="en")
        active_locale = wagtail_models.Locale.get_active()

        # Get localized blog_topics
        featured_topics_relationships = self.featured_blog_topics.all().select_related("topic", "icon")

        # If not in the en locale, build a cache of en_topics to efficiently get the topics's en slug
        # @TODO Localize Slugs TP1-690 / #12367
        if active_locale != en_locale:
            # Get topics from the en_menu
            en_featured_topics_relationships = self.get_translation(en_locale).featured_blog_topics

            # Build a cache of the en topics:
            en_topic_ids = list(en_featured_topics_relationships.values_list("topic_id", flat=True))
            en_topics = BlogPageTopic.objects.filter(id__in=en_topic_ids).order_by(
                "nav_menu_featured_topics__sort_order"
            )
            en_topics_cache = {en_topic.translation_key: en_topic for en_topic in en_topics}

        # Build featured topics slugs
        blog_index_page = self.blog_index_page
        for relationship in featured_topics_relationships:
            if relationship.topic:
                # Use the en slug only until slugs are localized @TODO TP1-690 / #12367
                if active_locale != en_locale:
                    topic_slug = en_topics_cache.get(relationship.topic.translation_key).slug
                else:
                    topic_slug = relationship.topic.slug

                relationship.topic.url = blog_index_page.url + blog_index_page.reverse_subpage(
                    "entries_by_topic", args=[topic_slug]
                )

        return featured_topics_relationships

    @property
    def localized_featured_blog_posts(self):
        default_locale = settings.LANGUAGE_CODE
        posts = BlogPage.objects.filter(
            featured_pages_relationship__page=self.blog_index_page, locale__language_code=default_locale
        ).order_by("featured_pages_relationship__sort_order")
        posts = localize_queryset(posts, preserve_order=True).prefetch_related("topics")
        return posts[:3]

    @cached_property
    def blog_button_url(self):
        return self.blog_index_page.url

    @cached_property
    def page_references_per_dropdown(self):
        """Get CMS page objects per dropdown id."""
        dropdown_page_links = {}
        for dropdown in self.dropdowns.raw_data:
            local_page_ids = list(nav_utils.find_key_values(dropdown, "page"))
            local_page_ids = [id for id in local_page_ids if id]  # filter out empty values
            dropdown_page_links[dropdown["id"]] = {"page_ids": local_page_ids, "self_page_id": None}
            dropdown_button_page_link = dropdown["value"]["button"]["page"]
            dropdown_button_link_to = dropdown["value"]["button"]["link_to"]
            if dropdown_button_page_link and (dropdown_button_link_to == "page"):
                dropdown_page_links[dropdown["id"]]["self_page_id"] = dropdown_button_page_link

        # Get a flat list of ids:
        page_ids = []
        for dropdown in dropdown_page_links.values():
            page_ids.extend(dropdown["page_ids"])

        # Get all paths for the pages:
        paths = wagtail_models.Page.objects.filter(id__in=page_ids).values("id", "path")
        paths = {p["id"]: p["path"] for p in paths}

        # Map the paths to the dropdowns:
        for dropdown in dropdown_page_links.values():
            for id in dropdown["page_ids"]:
                dropdown[id] = paths[id]

        return dropdown_page_links

    @cached_property
    def page_references(self):
        """Get all the CMS page objects referenced in the dropdowns."""
        page_ids = []
        for dropdown in self.dropdowns.raw_data:
            page_ids.extend(list(nav_utils.find_key_values(dropdown, "page")))

        # Filter out empty values
        page_ids = [id for id in page_ids if id]

        # Get all paths for the pages:
        paths = wagtail_models.Page.objects.filter(id__in=page_ids).values("id", "path")
        paths = {p["id"]: p["path"] for p in paths}

        return paths


@register_setting(icon="nav-menu")
class SiteNavMenu(BaseSiteSetting):
    select_related = ["active_nav_menu"]

    active_nav_menu = models.ForeignKey(
        "nav.NavMenu",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="site_nav_menu",
        verbose_name="Active Navigation Menu",
    )

    content_panels = [
        panels.FieldPanel("active_nav_menu"),
    ]

    class Meta:
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"
