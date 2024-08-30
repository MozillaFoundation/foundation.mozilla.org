from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union

from django.apps import apps
from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext
from modelcluster import fields as cluster_fields
from wagtail.admin.panels import (
    FieldPanel,
    HelpPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    TitleFieldPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Orderable, Page, TranslatableMixin
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.utility import orderables
from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.buyersguide import utils as bg_utils
from networkapi.wagtailpages.templatetags.bg_nav_tags import bg_categories_in_subnav
from networkapi.wagtailpages.templatetags.localization import relocalize_url
from networkapi.wagtailpages.utils import (
    get_language_from_request,
    get_locale_from_request,
    localize_queryset,
)

if TYPE_CHECKING:
    from networkapi.wagtailpages.models import (
        BuyersGuideArticlePage,
        BuyersGuideCampaignPage,
        ConsumerCreepometerPage,
        Update,
    )


class BuyersGuidePage(RoutablePageMixin, BasePage):
    """
    Note: We'll likely be converting the "about" pages to Wagtail Pages.
    When that happens, we should remove the RoutablePageMixin and @routes
    """

    template = "pages/buyersguide/home.html"
    subpage_types = [
        "wagtailpages.GeneralProductPage",
        "wagtailpages.BuyersGuideEditorialContentIndexPage",
    ]

    hero_featured_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    hero_supporting_pages_heading = models.CharField(
        max_length=50,
        default=_("Related reading"),
        blank=False,
        null=False,
        help_text=(
            "Heading for the links rendered next to the main featured page. "
            'Common choices are "Related articles", "Popular articles", etc.'
        ),
    )

    featured_advice_article = models.ForeignKey(
        "wagtailpages.BuyersGuideArticlePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    cutoff_date = models.DateField(
        "Product listing cutoff date",
        help_text="Only show products that were reviewed on, or after this date.",
        default=datetime(2020, 10, 29),
    )

    call_to_action = models.ForeignKey(
        "wagtailpages.BuyersGuideCallToAction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = [
        TitleFieldPanel(
            "title"
        ),  # https://docs.wagtail.org/en/stable/releases/5.0.html#changes-to-title-slug-field-synchronisation
        MultiFieldPanel(
            children=[
                HelpPanel(content="<h2>Main Featured Page</h2>"),
                PageChooserPanel(
                    "hero_featured_page",
                    page_type=[
                        "wagtailpages.BuyersGuideArticlePage",
                        "wagtailpages.BuyersGuideCampaignPage",
                        "wagtailpages.ConsumerCreepometerPage",
                    ],
                ),
                HelpPanel(content="<h2>Supporting Featured Pages</h2>"),
                FieldPanel("hero_supporting_pages_heading", heading="Heading"),
                InlinePanel(
                    "hero_supporting_page_relations",
                    heading="Supporting Pages",
                    label="Page",
                ),
            ],
            heading="Hero",
        ),
        PageChooserPanel(
            "featured_advice_article",
            page_type="wagtailpages.BuyersGuideArticlePage",
        ),
        InlinePanel(
            "featured_article_relations",
            heading="Popular articles",
            label="Article",
            max_num=3,
        ),
        InlinePanel(
            "featured_update_relations",
            heading="In the press",
            label="Press update",
            max_num=3,
        ),
        MultiFieldPanel(
            children=[
                FieldPanel("cutoff_date"),
                HelpPanel(content="<h2>Excluded categories</h2>"),
                InlinePanel(
                    "excluded_categories",
                    heading="Excluded categories",
                    label="Category",
                    min_num=0,
                ),
            ],
            heading="Product listing",
        ),
        FieldPanel("call_to_action"),
    ]

    translatable_fields = [
        TranslatableField("title"),
        # Hero featured page should be translatable, but that is causing issues.
        # Using sync field as workaround.
        # See also: https://github.com/wagtail/wagtail-localize/issues/430
        SynchronizedField("hero_featured_page"),
        # Hero supporting page relations should also be translatable, but that is
        # also causing issues. Using sync filed as a workaround.
        # See also: https://github.com/wagtail/wagtail-localize/issues/640
        SynchronizedField("hero_supporting_page_relations"),
        TranslatableField("hero_supporting_pages_heading"),
        # Featured articles should be translatable too. See above explanation for
        # hero supporting articles.
        SynchronizedField("featured_article_relations"),
        # Featured advice article should be translatable. But this faces the same issue
        # as the hero featured article.
        SynchronizedField("featured_advice_article"),
        SynchronizedField("cutoff_date"),
        SynchronizedField("excluded_categories"),
        TranslatableField("call_to_action"),
        # Promote tab fields
        TranslatableField("seo_title"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
    ]

    @route(r"^about/$", name="how-to-use-view")
    def about_page(self, request):
        context = self.get_context(request)
        context["pagetype"] = "about"
        context["pageTitle"] = pgettext(
            "*Privacy Not Included can be localized.",
            "How to use *Privacy Not Included | Mozilla Foundation",
        )
        return render(request, "pages/buyersguide/about/how_to_use.html", context)

    @route(r"^about/why/$", name="about-why-view")
    def about_why_page(self, request):
        context = self.get_context(request)
        context["pagetype"] = "about"
        context["pageTitle"] = pgettext(
            "*Privacy Not Included can be localized.",
            "Why we made *Privacy Not Included | Mozilla Foundation",
        )
        return render(request, "pages/buyersguide/about/why_we_made.html", context)

    @route(r"^about/press/$", name="press-view")
    def about_press_page(self, request):
        context = self.get_context(request)
        context["pagetype"] = "about"
        context["pageTitle"] = (
            pgettext("Noun, media", "Press")
            + " | "
            + pgettext(
                "This can be localized. This is a reference to the “*batteries not included” mention on toys.",
                "*Privacy Not Included | Mozilla Foundation",
            )
        )
        return render(request, "pages/buyersguide/about/press.html", context)

    @route(r"^about/contact/$", name="contact-view")
    def about_contact_page(self, request):
        context = self.get_context(request)
        context["pagetype"] = "about"
        context["pageTitle"] = (
            gettext("Contact us")
            + " | "
            + pgettext(
                "This can be localized. This is a reference to the “*batteries not included” mention on toys.",
                "*Privacy Not Included | Mozilla Foundation",
            )
        )
        return render(request, "pages/buyersguide/about/contact.html", context)

    @route(r"^about/methodology/$", name="methodology-view")
    def about_methodology_page(self, request):
        context = self.get_context(request)
        context["pagetype"] = "about"
        context["pageTitle"] = (
            gettext("Our methodology")
            + " | "
            + pgettext(
                "This can be localized. This is a reference to the “*batteries not included” mention on toys.",
                "*Privacy Not Included | Mozilla Foundation",
            )
        )
        return render(request, "pages/buyersguide/about/methodology.html", context)

    @route(r"^contest/$", name="contest")
    def about_contest(self, request):
        context = self.get_context(request)
        context["pagetype"] = "contest"
        context["pageTitle"] = (
            gettext("Contest terms and conditions")
            + " | "
            + pgettext(
                "This can be localized. This is a reference to the “*batteries not included” mention on toys.",
                "*Privacy Not Included | Mozilla Foundation",
            )
        )
        return render(request, "pages/buyersguide/contest.html", context)

    @route(r"^products/(?P<slug>[-\w\d]+)/$", name="product-view")
    def product_view(self, request, slug):
        # Find product by it's slug and redirect to the product page
        # If no product is found, redirect to the BuyersGuide page
        locale = get_locale_from_request(request)
        ProductPage = apps.get_model(app_label="wagtailpages", model_name="ProductPage")
        product = get_object_or_404(ProductPage, slug=slug, locale=locale)
        url = relocalize_url(product.url, locale.language_code)
        return redirect(url)

    @route(r"^categories/(?P<slug>[\w\W]+)/", name="category-view")
    def categories_page(self, request, slug):
        context = self.get_context(request)
        language_code = get_language_from_request(request)
        slug = slugify(slug)

        # because we may be working with localized content, and the slug
        # will always be our english slug, we need to find the english
        # category first, and then find its corresponding localized version
        BuyersGuideProductCategory = apps.get_model(
            app_label="wagtailpages",
            model_name="BuyersGuideProductCategory",
        )
        try:
            category = BuyersGuideProductCategory.objects.select_related("parent").get(
                slug=slug, locale__language_code=language_code
            )
        except BuyersGuideProductCategory.DoesNotExist:
            category = get_object_or_404(
                BuyersGuideProductCategory, slug=slug, locale__language_code=settings.LANGUAGE_CODE
            )

        if category.parent:
            category.parent = category.parent.localized

        authenticated = request.user.is_authenticated
        exclude_cat_ids = [excats.category.id for excats in self.excluded_categories.all()]

        ProductPage = apps.get_model(app_label="wagtailpages", model_name="ProductPage")
        products = bg_utils.get_product_subset(
            self.cutoff_date,
            authenticated,
            ProductPage.objects.exclude(product_categories__category__id__in=exclude_cat_ids),
            language_code=language_code,
        )

        context["category"] = slug
        context["current_category"] = category
        context["products"] = products
        context["pageTitle"] = f'{category.name} | {gettext("Privacy & Security Guide")}' f" | Mozilla Foundation"

        # Checking if category has custom metadata, if so, update the share image and description.
        if category.share_image:
            setattr(self, "search_image_id", category.share_image_id)
        if category.description:
            setattr(self, "search_description", category.description)

        return render(request, "pages/buyersguide/category_page.html", context)

    def get_sitemap_urls(self, request):
        """
        Add categories and route views to the sitemap for better search indexing.
        """
        sitemap = super().get_sitemap_urls(request)
        last_modified = self.last_published_at or self.latest_revision_created_at
        # Add all the available Buyers Guide categories to the sitemap
        categories = bg_categories_in_subnav()
        for category in categories:
            sitemap.append(
                {
                    "location": self.full_url + self.reverse_subpage("category-view", args=(category.slug,)),
                    "lastmod": last_modified,
                }
            )

        # Add all the available "subpages" (routes) to the sitemap, excluding categories and products.
        # Categories are added above. Products will be their own Wagtail pages and get their own URLs because of that.
        about_page_views = [
            "how-to-use-view",
            "about-why-view",
            "press-view",
            "contact-view",
            "methodology-view",
        ]
        for about_page in about_page_views:
            sitemap.append(
                {
                    "location": self.full_url + self.reverse_subpage(about_page),
                    "lastmod": last_modified,
                }
            )
        return sitemap

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        language_code = get_language_from_request(request)

        authenticated = request.user.is_authenticated
        exclude_cat_ids = [excats.category.id for excats in self.excluded_categories.all()]

        ProductPage = apps.get_model(app_label="wagtailpages", model_name="ProductPage")
        products = bg_utils.get_product_subset(
            self.cutoff_date,
            authenticated,
            ProductPage.objects.exclude(product_categories__category__id__in=exclude_cat_ids),
            language_code=language_code,
        )

        context["current_category"] = None
        context["featured_cta"] = self.call_to_action
        context["products"] = products
        context["web_monetization_pointer"] = settings.WEB_MONETIZATION_POINTER
        return context

    def get_editorial_content_index(self):
        BuyersGuideEditorialContentIndexPage = apps.get_model(
            app_label="wagtailpages",
            model_name="BuyersGuideEditorialContentIndexPage",
        )
        indexes = BuyersGuideEditorialContentIndexPage.objects.descendant_of(self)
        return indexes.first()

    def get_hero_featured_page(
        self,
    ) -> Optional[Union["BuyersGuideArticlePage", "BuyersGuideCampaignPage", "ConsumerCreepometerPage"]]:
        try:
            return self.hero_featured_page.specific.localized
        except AttributeError:
            # If no hero featured page is set (because `None` has no `localized`
            # attribute)
            return None

    def get_hero_supporting_pages(self) -> list[Union["BuyersGuideArticlePage", "BuyersGuideCampaignPage"]]:
        supporting_pages = Page.objects.filter(bg_homepage_supporting_page_relation__page=self).order_by(
            "bg_homepage_supporting_page_relation__sort_order"
        )
        supporting_pages = localize_queryset(supporting_pages, preserve_order=True)
        return supporting_pages.specific()

    def get_featured_articles(self) -> list["BuyersGuideArticlePage"]:
        BuyersGuideArticlePage = apps.get_model(app_label="wagtailpages", model_name="BuyersGuideArticlePage")
        articles_pks = self.featured_article_relations.all().values("article__pk")
        articles = BuyersGuideArticlePage.objects.filter(pk__in=articles_pks)
        return localize_queryset(articles)

    def get_featured_advice_article(self) -> Optional["BuyersGuideArticlePage"]:
        try:
            return self.featured_advice_article.localized
        except AttributeError:
            # If no featured advice article is set (because `None` has no `localized`
            # attribute)
            return None

    def get_featured_updates(self) -> list["Update"]:
        return orderables.get_related_items(
            self.featured_update_relations.all(),
            "update",
        )

    class Meta:
        verbose_name = "Buyers Guide Page"


class BuyersGuidePageHeroSupportingPageRelation(TranslatableMixin, Orderable):
    page = cluster_fields.ParentalKey(
        "wagtailpages.BuyersGuidePage",
        related_name="hero_supporting_page_relations",
    )
    supporting_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="bg_homepage_supporting_page_relation",
    )

    panels = [
        PageChooserPanel(
            "supporting_page",
            page_type=[
                "wagtailpages.BuyersGuideArticlePage",
                "wagtailpages.BuyersGuideCampaignPage",
                "wagtailpages.ConsumerCreepometerPage",
            ],
        )
    ]

    def __str__(self):
        return f"{self.page.title} -> {self.supporting_page.title}"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass


class BuyersGuidePageFeaturedArticleRelation(TranslatableMixin, Orderable):
    page = cluster_fields.ParentalKey(
        "wagtailpages.BuyersGuidePage",
        related_name="featured_article_relations",
    )
    article = models.ForeignKey(
        "wagtailpages.BuyersGuideArticlePage",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [PageChooserPanel("article", page_type="wagtailpages.BuyersGuideArticlePage")]

    def __str__(self):
        return f"{self.page.title} -> {self.article.title}"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass


class BuyersGuidePageFeaturedUpdateRelation(TranslatableMixin, Orderable):
    page = cluster_fields.ParentalKey(
        "wagtailpages.BuyersGuidePage",
        related_name="featured_update_relations",
    )
    update = models.ForeignKey(
        "wagtailpages.Update",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [FieldPanel("update")]

    def __str__(self):
        return f"{self.page.title} -> {self.update.title}"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass


def get_pni_home_page():
    """
    Used in AIRTABLE settings for nesting child pages under a new parent page.
    """
    return BuyersGuidePage.objects.first().id
