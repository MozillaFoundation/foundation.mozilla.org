from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string

from foundation_cms.base.models.abstract_article_page import AbstractArticlePage
from foundation_cms.mixins.hero_image import HeroImageMixin


class NothingPersonalProductReviewPage(AbstractArticlePage, HeroImageMixin):

    body = None
    updated = models.DateField(null=True, blank=True, help_text="When the review was last updated.")
    reviewed = models.DateField(null=True, blank=True, help_text="Date of the product review.")
    research = models.CharField(max_length=255, blank=True, help_text="Amount of time spent on research.")

    content_panels = AbstractArticlePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("updated"),
                FieldPanel("reviewed"),
                FieldPanel("research"),
            ],
            heading="Product Review Meta",
        ),
        FieldPanel("lede_text"),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    class Meta:
        verbose_name = "Nothing Personal Product Review"

    template = "patterns/pages/nothing_personal/product_review_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        return context
