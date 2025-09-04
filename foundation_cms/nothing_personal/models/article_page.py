from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage


class NothingPersonalArticlePage(AbstractArticlePage):
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Hero Image",
        help_text="Image for page hero section.",
    )

    hero_image_alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt Text",
        help_text="Descriptive text for screen readers. Leave blank to use the image's default title.",
    )

    content_panels = AbstractArticlePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Image",
            classname="collapsible",
        ),
    ]

    parent_page_types = ["core.HomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Article Page"

    template = "patterns/pages/nothing_personal/article_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        return context
