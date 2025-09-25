from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel,InlinePanel, MultiFieldPanel
from wagtail.models import Orderable
from wagtail_localize.fields import SynchronizedField
from foundation_cms.base.models.abstract_base_page import AbstractBasePage


from foundation_cms.utils import get_related_items, localize_queryset


class ProductCollection(Orderable):
    page = ParentalKey(
        "nothing_personal.NothingPersonalProductCollectionPage",
        related_name="products",
        on_delete=models.CASCADE,
    )
    products = models.ForeignKey(
        "nothing_personal.NothingPersonalProductReviewPage",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )
    panels = [FieldPanel("products")]

    class Meta(Orderable.Meta):
        verbose_name = "Product"
        verbose_name_plural = "Products"

class NothingPersonalProductCollectionPage(AbstractBasePage):
    hero_title = models.TextField(blank=True)
    hero_description = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    content_panels = AbstractBasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
            ],
            heading="Hero Section",
            classname="collapsible",
        ),
        FieldPanel("body"),
        InlinePanel("products", label="Products"),
    ]

    parent_page_types = ["nothing_personal.NothingPersonalHomePage"]
    subpage_types: list[str] = []

    translatable_fields = [
        # Content tab fields
        SynchronizedField("hero_description"),
        SynchronizedField("products"),
        SynchronizedField("hero_title"),
    ]

    class Meta:
        verbose_name = "Nothing Personal Product Collection"

    template = "patterns/pages/nothing_personal/product_collection_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["products"] = self.products
        context["anchor_sections"] = self.get_anchor_sections()
        return context

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        context["products"] = self.products
        context["anchor_sections"] = self.get_anchor_sections()
        return context

    def get_anchor_sections(self):
        """Generate anchor sections based on individual page fields"""
        section_configs = [
            (
                "what_you_should_know",
                self.what_you_should_know_section,
                "What You Should Know",
                "what-you-should-know",
            ),
            ("good_and_bad", self.good_and_bad_section, "The Good and The Bad", "good-and-bad"),
            ("reduce_your_risks", self.reduce_your_risks_section, "Reduce Your Risks", "reduce-your-risks"),
            ("bottom_line", self.bottom_line_section, "The Bottom Line", "bottom-line"),
        ]

        sections = []
        for section_key, section_field, title, anchor in section_configs:
            if not section_field:
                continue

            # Skip bottom_line if no products
            if section_key == "bottom_line" and not self.products.exists():
                continue

            sections.append({"title": title, "anchor": anchor})

        return sections

    @cached_property
    def localized_products(self):
        products = NothingPersonalProductCollectionPage.objects.all()
        localized_products = localize_queryset(products, preserve_order=True)

        return localized_products.specific()

    @cached_property
    def preview_products(self):
        """
        Fetches products updates for CMS page previews.
        """ 
        products = get_related_items(
            self.products.all(), "product_collection", order_by="sort_order"
        )

        return products
