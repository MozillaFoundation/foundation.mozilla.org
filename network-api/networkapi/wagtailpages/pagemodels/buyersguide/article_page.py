import typing

from django.db import models
from modelcluster import fields as cluster_fields
from wagtail import blocks, fields, images
from wagtail import models as wagtail_models
from wagtail.admin import panels as panels
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.utility import orderables
from networkapi.wagtailpages.pagemodels import customblocks
from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.buyersguide.forms import (
    BuyersGuideArticlePageForm,
)

if typing.TYPE_CHECKING:
    from networkapi.wagtailpages.models import BuyersGuideContentCategory, Profile


class BuyersGuideArticlePage(BasePage):
    parent_page_types = ["wagtailpages.BuyersGuideEditorialContentIndexPage"]
    subpage_types: list = []
    template = "pages/buyersguide/article_page.html"
    # Custom base form for additional validation
    base_form_class = BuyersGuideArticlePageForm

    hero_image = models.ForeignKey(
        images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Image for the hero section of the page.",
    )
    body = fields.StreamField(
        block_types=(
            ("accordion", customblocks.AccordionBlock()),
            (
                "paragraph",
                blocks.RichTextBlock(
                    features=customblocks.full_content_rich_text_options,
                    template="wagtailpages/blocks/rich_text_block.html",
                ),
            ),
            ("card_grid", customblocks.CardGridBlock()),
            ("image_grid", customblocks.ImageGridBlock()),
            ("iframe", customblocks.iFrameBlock()),
            ("image", customblocks.AnnotatedImageBlock()),
            ("audio", customblocks.AudioBlock()),
            ("image_text", customblocks.ImageTextBlock()),
            ("image_text_mini", customblocks.ImageTextMini()),
            ("video", customblocks.VideoBlock()),
            ("linkbutton", customblocks.LinkButtonBlock()),
            ("looping_video", customblocks.LoopingVideoBlock()),
            ("pulse_listing", customblocks.PulseProjectList()),
            ("single_quote", customblocks.SingleQuoteBlock()),
            ("slider", customblocks.FoundationSliderBlock()),
            ("spacer", customblocks.BootstrapSpacerBlock()),
            ("airtable", customblocks.AirTableBlock()),
            ("datawrapper", customblocks.DatawrapperBlock()),
            ("typeform", customblocks.TypeformBlock()),
        ),
        block_counts={"typeform": {"max_num": 1}},
        null=True,
        blank=False,
        use_json_field=True,
    )

    content_panels = wagtail_models.Page.content_panels + [
        panels.FieldPanel("hero_image"),
        panels.InlinePanel("author_profile_relations", heading="Authors", label="Author"),
        panels.InlinePanel(
            "content_category_relations",
            heading="Content categories",
            label="Content category",
            max_num=2,
        ),
        panels.FieldPanel("body"),
        panels.InlinePanel(
            "related_article_relations",
            heading="What to read next (related articles)",
            label="Article",
            max_num=3,
        ),
    ]

    settings_panels = [
        panels.PublishingPanel(),
        panels.FieldPanel("first_published_at"),
    ]

    translatable_fields = [
        # Content tab fields
        TranslatableField("title"),
        TranslatableField("body"),
        SynchronizedField("hero_image"),
        SynchronizedField("content_category_relations"),
        SynchronizedField("related_article_relations"),
        SynchronizedField("author_profile_relations"),
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
    ]

    def get_author_profiles(self) -> list["Profile"]:
        author_profiles = orderables.get_related_items(
            self.author_profile_relations.all(),
            "author_profile",
        )
        # The relations are synchronized from the default locale on non-default
        # locales. But, then working with a page of a non-default locale we are of
        # course interested in the related articles in that same locale.
        #
        # FIXME: This version is bad, because it uses 1+n queries to generate the list
        #        of author profiles in the correct locale. We should create something
        #        more elegant to retrieve the author profiles of the correct locale
        #        directly from the database.
        return [ap.localized for ap in author_profiles]

    def get_content_categories(self) -> list["BuyersGuideContentCategory"]:
        content_categories = orderables.get_related_items(
            self.content_category_relations.all(),
            "content_category",
        )
        # The relations are synchronized from the default locale on non-default
        # locales. But, then working with a page of a non-default locale we are of
        # course interested in the related articles in that same locale.
        #
        # FIXME: This version is bad, because it uses 1+n queries to generate the list
        #        content categories in the correct locale. We should create something
        #        more elegant to retrieve the content categories of the correct locale
        #        directly from the database.
        return [cc.localized for cc in content_categories]

    def get_related_articles(self) -> list["BuyersGuideArticlePage"]:
        related_articles = orderables.get_related_items(
            self.related_article_relations.all(),
            "article",
        )
        # The relations are synchronized from the default locale on non-default
        # locales. But, then working with a page of a non-default locale we are of
        # course interested in the related articles in that same locale.
        #
        # FIXME: This version is bad, because it uses 1+n queries to generate the list
        #        related articles in the correct locale. We should create something
        #        more elegant to retrieve the related articles of the correct locale
        #        directly from the database.
        return [a.localized for a in related_articles]


class BuyersGuideArticlePageAuthorProfileRelation(
    wagtail_models.TranslatableMixin,
    wagtail_models.Orderable,
):
    """Through model for relation from article page to author profile."""

    page = cluster_fields.ParentalKey(
        "wagtailpages.BuyersGuideArticlePage",
        related_name="author_profile_relations",
    )
    author_profile = models.ForeignKey(
        "wagtailpages.Profile",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [panels.FieldPanel("author_profile")]

    def __str__(self):
        return f"{self.page.title} -> {self.author_profile.name}"

    class Meta(wagtail_models.TranslatableMixin.Meta, wagtail_models.Orderable.Meta):
        pass


class BuyersGuideArticlePageContentCategoryRelation(
    wagtail_models.TranslatableMixin,
    wagtail_models.Orderable,
):
    """Through model for relation from article page to content category."""

    page = cluster_fields.ParentalKey(
        "wagtailpages.BuyersGuideArticlePage",
        related_name="content_category_relations",
    )
    content_category = models.ForeignKey(
        "wagtailpages.BuyersGuideContentCategory",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [panels.FieldPanel("content_category")]

    def __str__(self):
        return f"{self.page.title} -> {self.content_category.title}"

    class Meta(wagtail_models.TranslatableMixin.Meta, wagtail_models.Orderable.Meta):
        pass


class BuyersGuideArticlePageRelatedArticleRelation(
    wagtail_models.Orderable,
):
    page = cluster_fields.ParentalKey(
        "wagtailpages.BuyersGuideArticlePage",
        related_name="related_article_relations",
    )
    article = models.ForeignKey(
        "wagtailpages.BuyersGuideArticlePage",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [panels.FieldPanel("article")]

    def __str__(self):
        return f"{self.page.title} -> {self.article.title}"

    class Meta(wagtail_models.Orderable.Meta):
        pass
