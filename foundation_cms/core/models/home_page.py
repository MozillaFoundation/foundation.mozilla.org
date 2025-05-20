from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail_localize.fields import TranslatableField

from foundation_cms.base.models.abstract_home_page import AbstractHomePage

hero_intro_heading_default_text = "A healthy internet is one in which privacy, openness, and inclusion are the norms."
hero_intro_body_default_text = (
    "Mozilla empowers consumers to demand better online privacy, trustworthy AI, "
    "and safe online experiences from Big Tech and governments. We work across "
    "borders, disciplines, and technologies to uphold principles like privacy, "
    "inclusion and decentralization online."
)


class HomePage(AbstractHomePage):
    hero_headline = models.CharField(
        max_length=120,
        help_text="Hero story headline",
        blank=True,
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_intro_heading = models.CharField(max_length=100, blank=True, default=hero_intro_heading_default_text)

    hero_intro_body = models.TextField(max_length=300, blank=True, default=hero_intro_body_default_text)

    content_panels = AbstractHomePage.content_panels + [
        FieldPanel("hero_headline"),
        FieldPanel("hero_image"),
        FieldPanel("hero_intro_heading"),
        FieldPanel("hero_intro_body"),
        FieldPanel("body"),
    ]

    translatable_fields = [
        TranslatableField("hero_headline"),
        TranslatableField("hero_intro_heading"),
        TranslatableField("hero_intro_body"),
    ]

    template = "patterns/pages/core/home_page.html"

    subpage_types = [
        "GeneralPage",
        "articles.ArticleAdviceColumn",
        "articles.ArticleCollectionPage",
        "articles.ArticleEditorialFeature",
        "articles.ArticleProductReview",

    ]

    class Meta:
        verbose_name = "Home Page (new)"

    def get_context(self, request):
        context = super().get_context(request)
        return context
