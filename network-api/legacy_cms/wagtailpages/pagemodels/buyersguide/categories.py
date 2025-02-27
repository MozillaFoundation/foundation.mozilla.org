import typing
from functools import cached_property

from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import F, OuterRef
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.models import Orderable, TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from legacy_cms.utility import orderables
from legacy_cms.wagtailpages.pagemodels.buyersguide.forms import (
    BuyersGuideProductCategoryForm,
)
from legacy_cms.wagtailpages.utils import CharCountWidget

if typing.TYPE_CHECKING:
    from legacy_cms.wagtailpages.models import BuyersGuideArticlePage


class BuyersGuideProductCategoryQuerySet(models.QuerySet):
    def with_usage_annotation(self):
        # Avoid circular import:
        ProductPage = apps.get_model("wagtailpages", "ProductPage")
        return self.annotate(
            _is_being_used=models.Exists(
                ProductPage.objects.filter(
                    live=True, product_categories__category__translation_key=OuterRef("translation_key")
                )
            )
        )


class BuyersGuideProductCategory(
    index.Indexed,
    TranslatableMixin,
    # models.Model
    ClusterableModel,
):
    """
    A simple category class for use with Buyers Guide products,
    registered as snippet so that we can moderate them if and
    when necessary.
    """

    name = models.CharField(max_length=100)

    description = models.TextField(
        max_length=300,
        help_text="Description of the product category. Max. 300 characters.",
        blank=True,
    )

    parent = models.ForeignKey(
        "wagtailpages.BuyersGuideProductCategory",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Leave this blank for a top-level category, or pick another category to nest this under",
    )

    featured = models.BooleanField(
        default=False,
        help_text="Featured category will appear first on Buyer's Guide site nav",
    )

    hidden = models.BooleanField(
        default=False,
        help_text="Hidden categories will not appear in the Buyer's Guide site nav at all",
    )

    slug = models.SlugField(
        blank=True,
        help_text="A URL-friendly version of the category name. This is an auto-generated field.",
        max_length=100,
    )

    share_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Share Image",
        help_text="Optional image that will apear when category page is shared.",
    )

    show_cta = models.BooleanField(
        default=False,
        help_text="Do we want the Buyers Guide featured CTA to be displayed on this category's page?",
    )

    objects = BuyersGuideProductCategoryQuerySet.as_manager()

    panels = [
        FieldPanel(
            "name",
            widget=CharCountWidget(attrs={"class": "max-length-warning", "data-max-length": 50}),
        ),
        FieldPanel("description"),
        FieldPanel("parent"),
        FieldPanel("featured"),
        FieldPanel("hidden"),
        FieldPanel("share_image"),
        FieldPanel("show_cta"),
        InlinePanel(
            "related_article_relations",
            heading="Related articles",
            label="Article",
            max_num=6,
        ),
    ]

    translatable_fields = [
        TranslatableField("name"),
        TranslatableField("description"),
        TranslatableField("related_article_relations"),
        SynchronizedField("slug"),
        SynchronizedField("share_image"),
        SynchronizedField("parent"),
    ]

    search_fields = [
        index.SearchField("name", boost=10),
        index.AutocompleteField("name", boost=10),
        index.FilterField("locale_id"),
        index.FilterField("featured"),
        index.FilterField("hidden"),
    ]

    @cached_property
    def is_being_used(self):
        try:
            # Try to get pre-filtered/pre-fetched annotated value
            return self._is_being_used
        except AttributeError:
            # It failed, let's query it ourselves
            ProductPage = apps.get_model("wagtailpages", "ProductPage")  # Avoid circular import
            return ProductPage.objects.filter(
                live=True, product_categories__category__translation_key=self.translation_key
            ).exists()

    def get_parent(self):
        return self.parent

    def get_children(self):
        return BuyersGuideProductCategory.objects.filter(parent=self)

    def get_related_articles(self) -> list["BuyersGuideArticlePage"]:
        return orderables.get_related_items(
            self.related_article_relations.all(),
            "article",
        )

    def get_primary_related_articles(self) -> list["BuyersGuideArticlePage"]:
        return self.get_related_articles()[:3]

    def get_secondary_related_articles(self) -> list["BuyersGuideArticlePage"]:
        return self.get_related_articles()[3:]

    def __str__(self):
        if self.parent is None:
            return f"{self.name}"
        return f"{self.parent.name} > {self.name}"

    base_form_class = BuyersGuideProductCategoryForm

    search_fields = [
        index.SearchField("name"),
        index.AutocompleteField("name"),
        index.FilterField("locale_id"),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Buyers Guide Product Category"
        verbose_name_plural = "Buyers Guide Product Categories"
        ordering = [
            F("parent__name").asc(nulls_first=True),
            "name",
        ]


@receiver(post_save, sender=BuyersGuideProductCategory)
def set_category_slug(sender, instance, created, **kwargs):
    """Post-save hook to create a slug when creating a category.

    Slugfies the name for newly created categories and syncs this with all translations.
    """
    if created:
        if instance.locale.language_code == settings.LANGUAGE_CODE and not instance.slug:
            slug = slugify(instance.name)
            instance.slug = slug
            instance.save(update_fields=["slug"])
            BuyersGuideProductCategory.objects.filter(translation_key=instance.translation_key).exclude(
                locale__language_code=settings.LANGUAGE_CODE
            ).update(slug=slug)
    return instance


class BuyersGuideCategoryNavRelation(Orderable):
    """
    This model is used to relate a BuyersGuideProductCategory to a
    BuyersGuideCategoryNav, so that we can have a many-to-many
    relationship between them.
    """

    nav = ParentalKey(
        "wagtailpages.BuyersGuideCategoryNav",
        related_name="category_relations",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        "wagtailpages.BuyersGuideProductCategory",
        related_name="nav_relations",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("category")]

    class Meta:
        verbose_name = "Category Navigation Relation"
        verbose_name_plural = "Category Navigation Relations"
        ordering = ["sort_order"]
        unique_together = [("nav", "category")]


class BuyersGuideCategoryNav(BaseGenericSetting, ClusterableModel):
    panels = [
        MultiFieldPanel(
            [InlinePanel("category_relations")],
            heading="Categories",
        ),
    ]

    def __str__(self):
        return "*PNI categories navbar"

    class Meta:
        verbose_name = "*PNI categories navbar"
        verbose_name_plural = "*PNI categories navbar"
