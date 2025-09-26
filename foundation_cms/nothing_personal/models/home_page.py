from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField

from foundation_cms.base.models.abstract_home_page import AbstractHomePage
from foundation_cms.blocks import (
    NarrowTextImageBlock,
    ProductReviewCarouselBlock,
    TwoColumnContainerBlock,
)
from foundation_cms.mixins.hero_image import HeroImageMixin


class NothingPersonalHomePage(AbstractHomePage, HeroImageMixin):
    max_count = 1

    nothing_personal_block_options = [
        ("two_column_container_block", TwoColumnContainerBlock()),
        ("narrow_text_image_block", NarrowTextImageBlock()),
        ("product_review_carousel_block", ProductReviewCarouselBlock()),
        # NP Text Image Block
        # product review carousel block
        # 50/50 block
    ]
    body = StreamField(
        nothing_personal_block_options,
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["core.HomePage"]
    subpage_types = [
        "nothing_personal.NothingPersonalArticleCollectionPage",
        "nothing_personal.NothingPersonalArticlePage",
        "nothing_personal.NothingPersonalPodcastPage",
        "nothing_personal.NothingPersonalProductReviewPage",
    ]

    content_panels = AbstractHomePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_image"),
                FieldPanel("hero_image_alt_text"),
            ],
            heading="Hero Image",
        ),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Nothing Personal Home Page"

    template = "patterns/pages/nothing_personal/home_page.html"

    def get_context(self, request, virtual_page_name=None):
        context = super().get_context(request)

        if virtual_page_name:
            context["page_type_bem"] = self._to_bem_case(virtual_page_name)

        return context
