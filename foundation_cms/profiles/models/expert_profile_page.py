from django.db import models
from django.db.models import CASCADE, CharField, TextField, URLField
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page, TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.widgets import TopicSelectWidget
from foundation_cms.blocks.block_registry import BlockRegistry
from foundation_cms.gallery_hub.models import ProjectPage
from foundation_cms.profiles.blocks import (
    ArticlesSectionBlock,
    LinkSectionBlock,
    ProjectsSectionBlock,
)
from foundation_cms.profiles.models.abstract_profile_page import AbstractProfilePage

EXPERT_PROFILE_BIO_COLLAPSED_CHAR_LIMIT = 600

expert_profile_body_block_options = BlockRegistry.get_blocks(["quote"]) + [
    ("projects_section", ProjectsSectionBlock(skip_default_wrapper=True, group="Profile sections")),
    ("articles_section", ArticlesSectionBlock(skip_default_wrapper=True, group="Profile sections")),
    ("link_section", LinkSectionBlock(skip_default_wrapper=True, group="Profile sections")),
]


class ExpertExternalLink(TranslatableMixin, Orderable):
    page = ParentalKey(
        "profiles.ExpertProfilePage",
        related_name="external_links",
        on_delete=CASCADE,
    )
    title = CharField(max_length=255, help_text="Title of the external link.")
    description = TextField(blank=True, help_text="Brief description of the link.")
    url = URLField(help_text="Full URL including https://")

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("url"),
    ]

    translatable_fields = [
        TranslatableField("title"),
        TranslatableField("description"),
        SynchronizedField("url"),
    ]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Expert External Link"
        verbose_name_plural = "Expert External Links"


class ExpertProfileSelectedProject(Orderable):
    page = ParentalKey(
        "profiles.ExpertProfilePage",
        related_name="selected_projects",
        on_delete=CASCADE,
    )
    project = models.ForeignKey(
        Page,
        related_name="expert_profile_project_selections",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        PageChooserPanel("project", "gallery_hub.ProjectPage"),
    ]


class ExpertProfileSelectedArticle(Orderable):
    page = ParentalKey(
        "profiles.ExpertProfilePage",
        related_name="selected_articles",
        on_delete=CASCADE,
    )
    article = models.ForeignKey(
        Page,
        related_name="expert_profile_article_selections",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panels = [
        PageChooserPanel("article", "nothing_personal.NothingPersonalArticlePage"),
    ]


class ExpertProfilePage(AbstractProfilePage):
    body = StreamField(
        expert_profile_body_block_options,
        block_counts={
            "quote": {"max_num": 1},
            "projects_section": {"max_num": 1},
            "articles_section": {"max_num": 1},
        },
        use_json_field=True,
        blank=True,
    )

    affiliation = CharField(
        max_length=255,
        blank=True,
        help_text="Organization or institution.",
    )

    blurb = CharField(
        max_length=115,
        blank=True,
        help_text="Short promotional summary shown in the Expert Hub landing page visualization (max 115 characters).",
    )
    quote = TextField(
        blank=True,
        help_text="Optional pull quote shown in the profile introduction.",
    )
    quote_attribution = CharField(
        max_length=255,
        blank=True,
        help_text="Optional attribution for the profile introduction quote.",
    )
    linkedin_url = URLField(blank=True, help_text="Full LinkedIn profile URL including https://")
    bluesky_url = URLField(blank=True, help_text="Full Bluesky profile URL including https://")
    facebook_url = URLField(blank=True, help_text="Full Facebook profile URL including https://")
    instagram_url = URLField(blank=True, help_text="Full Instagram profile URL including https://")
    tiktok_url = URLField(blank=True, help_text="Full TikTok profile URL including https://")

    content_panels = Page.content_panels + [
        FieldPanel("title", heading="Full Name", help_text="Full name of the profile."),
        FieldPanel("role"),
        FieldPanel("location"),
        FieldPanel("affiliation"),
        FieldPanel("topics", widget=TopicSelectWidget),
        FieldPanel("bio"),
        FieldPanel("image"),
        FieldPanel("blurb"),
        MultiFieldPanel(
            [
                FieldPanel("linkedin_url"),
                FieldPanel("bluesky_url"),
                FieldPanel("facebook_url"),
                FieldPanel("instagram_url"),
                FieldPanel("tiktok_url"),
            ],
            heading="Where to Find Me",
            classname="collapsible",
        ),
        FieldPanel("body"),
    ]

    translatable_fields = AbstractProfilePage.translatable_fields + [
        TranslatableField("affiliation"),
        TranslatableField("blurb"),
        TranslatableField("quote"),
        TranslatableField("quote_attribution"),
        SynchronizedField("linkedin_url"),
        SynchronizedField("bluesky_url"),
        SynchronizedField("facebook_url"),
        SynchronizedField("instagram_url"),
        SynchronizedField("tiktok_url"),
        SynchronizedField("selected_projects"),
        SynchronizedField("selected_articles"),
        TranslatableField("body"),
    ]

    search_fields = AbstractProfilePage.search_fields + [
        index.SearchField("blurb", boost=5),
        index.SearchField("affiliation", boost=2),
    ]

    parent_page_types = ["profiles.ExpertHubPage"]
    subpage_types: list[str] = []

    template = "patterns/pages/profiles/expert_profile_page.html"

    class Meta:
        verbose_name = "Expert Profile Page"

    def get_context(self, request):
        context = super().get_context(request)
        context["bio_collapsed_char_limit"] = EXPERT_PROFILE_BIO_COLLAPSED_CHAR_LIMIT
        context["social_links"] = [
            {"label": label, "platform": platform, "url": getattr(self, field_name)}
            for label, platform, field_name in [
                ("LinkedIn", "linkedin", "linkedin_url"),
                ("Bluesky", "bluesky", "bluesky_url"),
                ("Facebook", "facebook", "facebook_url"),
                ("Instagram", "instagram", "instagram_url"),
                ("TikTok", "tiktok", "tiktok_url"),
            ]
            if getattr(self, field_name)
        ]

        return context

    def get_related_projects(self):
        return (
            ProjectPage.objects.live()
            .public()
            .filter(expert=self, locale=self.locale)
            .select_related("hero_image")
            .prefetch_related("topics")
            .order_by("-first_published_at", "-id")
        )
