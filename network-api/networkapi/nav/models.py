from django.conf import settings
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

from networkapi.nav import blocks as nav_blocks
from networkapi.nav.forms import NavMenuForm
from networkapi.wagtailpages.models import BlogIndexPage, BlogPage, BlogPageTopic
from networkapi.wagtailpages.utils import localize_queryset


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
        TranslatableField("title"),
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
        featured_topics_relationships = self.featured_blog_topics.all().select_related("topic", "icon")

        # Build a cache of the local topics:
        topic_ids = list(featured_topics_relationships.values_list("topic_id", flat=True))
        topics = BlogPageTopic.objects.filter(id__in=topic_ids).order_by("nav_menu_featured_topics__sort_order")
        topics = localize_queryset(topics, preserve_order=True)
        topics_cache = {topic.translation_key: topic for topic in topics}

        # Replace topics with localized versions:
        for relationship in featured_topics_relationships:
            if relationship.topic:
                local_topic = topics_cache.get(relationship.topic.translation_key)
                if local_topic:
                    relationship.topic = local_topic

        # Annotate with its url:
        blog_index_page = self.blog_index_page
        for relationship in featured_topics_relationships:
            if relationship.topic:
                relationship.topic.url = blog_index_page.reverse_subpage(
                    "entries_by_topic", args=[relationship.topic.slug]
                )

        return featured_topics_relationships

    @property
    def localized_featured_blog_posts(self):
        default_locale = settings.LANGUAGE_CODE
        posts = BlogPage.objects.filter(
            featured_pages_relationship__isnull=False, locale__language_code=default_locale
        ).order_by("featured_pages_relationship__sort_order")
        posts = localize_queryset(posts, preserve_order=True).prefetch_related("topics")
        return posts[:3]

    @cached_property
    def blog_button_url(self):
        return self.blog_index_page.url


@register_setting
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