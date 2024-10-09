import json
import typing

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import Error, models
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.templatetags.static import static
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy
from modelcluster.fields import ParentalKey
from wagtail import hooks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page, PageManager, PageQuerySet, TranslatableMixin
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.utility import orderables
from networkapi.wagtailpages.fields import ExtendedChoiceField, ExtendedYesNoField
from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.buyersguide.categories import (
    BuyersGuideProductCategory,
)
from networkapi.wagtailpages.pagemodels.buyersguide.utils import (
    get_buyersguide_featured_cta,
    localize_categories,
)
from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)
from networkapi.wagtailpages.utils import insert_panels_after, localize_queryset

if typing.TYPE_CHECKING:
    from networkapi.wagtailpages.models import BuyersGuideArticlePage


TRACK_RECORD_CHOICES = [
    ("Great", "Great"),
    ("Average", "Average"),
    ("Needs Improvement", "Needs Improvement"),
    ("Bad", "Bad"),
]


class BuyersGuideProductCategoryArticlePageRelation(TranslatableMixin, Orderable):
    category = ParentalKey(
        "wagtailpages.BuyersGuideProductCategory",
        related_name="related_article_relations",
    )
    article = models.ForeignKey(
        "wagtailpages.BuyersGuideArticlePage",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [FieldPanel("article")]

    def __str__(self):
        return f"{self.category.name} -> {self.article.title}"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass


class ProductVote(models.Model):
    """Holds a single creepiness vote for a product."""

    value = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(100, message="Creepiness vote must be smaller than 100")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    evaluation = models.ForeignKey("ProductPageEvaluation", on_delete=models.CASCADE, related_name="votes")


class ProductPageEvaluationQuerySet(models.QuerySet):
    def with_total_votes(self):
        return self.annotate(_total_votes=models.Count("votes__id", distinct=True))

    def with_total_creepiness(self):
        return self.annotate(_total_creepiness=Coalesce(models.Sum("votes__value"), 0))

    def with_average_creepiness(self):
        return self.annotate(_average_creepiness=Coalesce(models.Avg("votes__value"), float(0)))

    def with_bin_data(self):
        """Annotate the queryset with the number of votes in each bin.

        There are 5 "bins" for votes: <20%, <40%, <60%, <80%, <100%.
        """
        return self.annotate(
            _bin_0=models.Count("votes__id", distinct=True, filter=Q(votes__value__gte=0, votes__value__lt=20)),
            _bin_1=models.Count("votes__id", distinct=True, filter=Q(votes__value__gte=20, votes__value__lt=40)),
            _bin_2=models.Count("votes__id", distinct=True, filter=Q(votes__value__gte=40, votes__value__lt=60)),
            _bin_3=models.Count("votes__id", distinct=True, filter=Q(votes__value__gte=60, votes__value__lt=80)),
            _bin_4=models.Count("votes__id", distinct=True, filter=Q(votes__value__gte=80, votes__value__lt=100)),
        )


class ProductPageEvaluation(models.Model):
    """Holds creepiness data for a product and performs appropriate calculations.

    The product page is defined in the ProductPage model to make it possible to
    synchronize the field using `wagtail_localize` and avoid having to create
    multiple evaluations for each localized product page.
    """

    BIN_LABELS = {
        "bin_0": {"key": "Not creepy", "label": gettext_lazy("Not creepy")},
        "bin_1": {"key": "A little creepy", "label": gettext_lazy("A little creepy")},
        "bin_2": {"key": "Somewhat creepy", "label": gettext_lazy("Somewhat creepy")},
        "bin_3": {"key": "Very creepy", "label": gettext_lazy("Very creepy")},
        "bin_4": {"key": "Super creepy", "label": gettext_lazy("Super creepy")},
    }

    BIN_SIZE = 20

    objects = ProductPageEvaluationQuerySet.as_manager()

    @property
    def total_votes(self):
        """Total number of votes for this product evaluation.

        To populate the prefetched `_total_votes` annotation, call

        ```
        ProductPageEvaluation.objects.with_total_votes()
        ```

        Returns:
            int: Total number of votes for this product evaluation.
        """
        try:
            return self._total_votes
        except AttributeError:
            return self.votes.count()

    @property
    def total_creepiness(self):
        """Aggregate of vote values for this product evaluation.

        To use this property, make sure to first populate the prefetched `_total_creepiness`
        annotation, i.e.:

        ```
        evaluations = ProductPageEvaluation.objects.with_total_creepiness()
        my_evaluation = evaluations.get(pk=1)
        my_evaluation.total_creepiness
        ```

        Returns:
            int: Sum of creepiness value for all votes for this product evaluation.
        """
        try:
            return self._total_creepiness
        except AttributeError as e:
            raise AttributeError(
                "Can't calculate total creepiness without `_total_creepiness` annotation. "
                "Make sure to annotate the evaluation queryset by calling `.with_total_creepiness()` "
                "method before accessing this property."
            ) from e

    @property
    def average_creepiness(self):
        """Average of vote values for this product evaluation.

        To use this property, make sure to first populate the prefetched `_average_creepiness`
        annotation, i.e.:

        ```
        evaluations = ProductPageEvaluation.objects.with_average_creepiness()
        my_evaluation = evaluations.get(pk=1)
        my_evaluation.average_creepiness
        ```

        Returns:
            int: Average of creepiness value for all votes for this product evaluation.
        """
        try:
            return self._average_creepiness
        except AttributeError as e:
            raise AttributeError(
                "Can't calculate average creepiness without `_average_creepiness` annotation. "
                "Make sure to annotate the evaluation queryset by calling `.with_average_creepiness()` "
                "method before accessing this property."
            ) from e

    @property
    def votes_per_bin(self):
        try:
            return [
                self._bin_0,
                self._bin_1,
                self._bin_2,
                self._bin_3,
                self._bin_4,
            ]
        except AttributeError:
            bin_0 = self.votes.filter(value__gte=0, value__lt=20).count()
            bin_1 = self.votes.filter(value__gte=20, value__lt=40).count()
            bin_2 = self.votes.filter(value__gte=40, value__lt=60).count()
            bin_3 = self.votes.filter(value__gte=60, value__lt=80).count()
            bin_4 = self.votes.filter(value__gte=80, value__lt=100).count()
            return [bin_0, bin_1, bin_2, bin_3, bin_4]

    @property
    def labelled_creepiness_per_bin(self):
        bins = self.votes_per_bin
        creepiness_per_bin = {}
        for i in range(5):
            creepiness_per_bin[self.BIN_LABELS[f"bin_{i}"]["key"]] = {
                "count": bins[i],
                "label": self.BIN_LABELS[f"bin_{i}"]["label"],
            }
        return creepiness_per_bin

    @property
    def average_bin(self):
        """Name of the bin corresponding to the average vote"""
        total_votes = self.total_votes
        # If there's no votes, let the user know (also protects from division by zero errors)
        if total_votes == 0:
            return {
                "label": "No votes",
                "localized": gettext_lazy("No votes"),
            }

        average_vote = self.average_creepiness
        mode_bin = int(average_vote // self.BIN_SIZE)
        if mode_bin == 5:
            # Handle case where average is 100 (which should be in bin 4)
            # Votes should go until 99 to avoid this, but they are allowed to go up to 100
            # due to legacy implementation :facepalm:
            mode_bin = 4
        label = self.BIN_LABELS[f"bin_{mode_bin}"]

        return {
            "label": label["key"],
            "localized": label["label"],
        }


class ProductPageCategory(TranslatableMixin, Orderable):
    product = ParentalKey(
        "wagtailpages.ProductPage",
        related_name="product_categories",
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        "wagtailpages.BuyersGuideProductCategory",
        related_name="product_pages",
        blank=False,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("category"),
    ]

    def __str__(self):
        return f"{self.category.name} -> {self.product.title}"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Product Category"


class RelatedProducts(TranslatableMixin, Orderable):
    page = ParentalKey(
        "wagtailpages.ProductPage",
        related_name="related_product_pages",
        on_delete=models.CASCADE,
    )

    related_product = models.ForeignKey(
        "wagtailpages.ProductPage",
        on_delete=models.SET_NULL,
        null=True,
        related_name="related_product_relationships",
    )

    panels = [FieldPanel("related_product")]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Related Product"


class ProductPagePrivacyPolicyLink(TranslatableMixin, Orderable):
    page = ParentalKey(
        "wagtailpages.ProductPage",
        related_name="privacy_policy_links",
        on_delete=models.CASCADE,
    )

    label = models.CharField(max_length=500, help_text="Label for this link on the product page")

    url = models.URLField(max_length=2048, help_text="Privacy policy URL", blank=True)

    panels = [
        FieldPanel("label"),
        FieldPanel("url"),
    ]

    translatable_fields = [
        TranslatableField("label"),
        SynchronizedField("url"),
    ]

    def __str__(self):
        return f"{self.page.title}: {self.label} ({self.url})"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Privacy Link"


class Update(TranslatableMixin, index.Indexed, models.Model):
    source = models.URLField(
        max_length=2048,
        help_text="Link to source",
    )

    title = models.CharField(
        max_length=256,
    )

    author = models.CharField(
        max_length=256,
        blank=True,
    )

    featured = models.BooleanField(
        default=False, help_text="feature this update at the top of the list?", verbose_name="Featured?"
    )

    snippet = models.TextField(
        max_length=5000,
        blank=True,
    )

    created_date = models.DateField(
        auto_now_add=True,
        verbose_name="Created at",
        help_text="The date this update was created",
    )

    panels = [
        FieldPanel("source"),
        FieldPanel("title"),
        FieldPanel("author"),
        FieldPanel("featured"),
        FieldPanel("snippet"),
    ]

    search_fields = [
        index.SearchField("title"),
        index.AutocompleteField("title"),
        index.FilterField("locale_id"),
        index.FilterField("featured"),
    ]

    translatable_fields = [
        SynchronizedField("source"),
        SynchronizedField("title"),
        SynchronizedField("author"),
        SynchronizedField("snippet"),
    ]

    def __str__(self):
        return self.title

    @property
    def linked_products(self):
        """Title of the product pages linked to this update."""
        # Used on the snippet viewset for this model
        product_updates = self.product_pages.all()
        try:
            titles = []
            for product_update in product_updates:
                if hasattr(product_update, "page"):
                    titles.append(product_update.page.title)
            if not titles:
                return "-"
            return " | ".join(set(titles))
        except AttributeError:
            return "-"

    class Meta(TranslatableMixin.Meta):
        ordering = ["title"]
        verbose_name = "Buyers Guide Product Update"
        verbose_name_plural = "Buyers Guide Product Updates"


class ProductUpdates(TranslatableMixin, Orderable):
    page = ParentalKey(
        "wagtailpages.ProductPage",
        related_name="updates",
        on_delete=models.CASCADE,
    )

    # This is the new update FK to wagtailpages.Update
    update = models.ForeignKey(Update, on_delete=models.SET_NULL, related_name="product_pages", null=True)

    translatable_fields = [
        TranslatableField("update"),
    ]

    panels = [
        FieldPanel("update"),
    ]

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Product Update"


class ProductPageQuerySet(PageQuerySet):
    def with_average_creepiness(self):
        """Annotates the queryset with the average creepiness for each product page."""
        return self.annotate(_average_creepiness=Coalesce(models.Avg("evaluation__votes__value"), float(0)))


ProductPageManager = PageManager.from_queryset(ProductPageQuerySet)


class ProductPage(BasePage):
    """
    ProductPage is the superclass that GeneralProductPages inherits from.

    This used to be shared by the SoftwareProductPage, but that page type
    has been removed. In the past, we needed to connect the two page
    types together. This is why this superclass is abstract.

    """

    template = "pages/buyersguide/product_page.html"
    parent_page_types = ["wagtailpages.BuyersGuidePage"]

    privacy_ding = models.BooleanField(
        verbose_name="*Privacy Not Included ding",
        default=False,
    )
    adult_content = models.BooleanField(
        verbose_name="adult Content",
        default=False,
    )
    uses_wifi = models.BooleanField(
        verbose_name="uses WiFi",
        default=False,
    )
    uses_bluetooth = models.BooleanField(
        verbose_name="uses Bluetooth",
        default=False,
    )
    review_date = models.DateField(
        verbose_name="review Date",
        default=timezone.now,
    )
    company = models.CharField(
        verbose_name="company Name",
        max_length=100,
        blank=True,
    )
    blurb = RichTextField(verbose_name="intro Blurb", features=base_rich_text_options, blank=True)
    product_url = models.URLField(
        verbose_name="product URL",
        max_length=2048,
        blank=True,
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    worst_case = RichTextField(
        max_length=20 * 1000,
        verbose_name="what could happen if something goes wrong?",
        features=base_rich_text_options,
        blank=True,
    )
    tips_to_protect_yourself = RichTextField(features=base_rich_text_options + ["ul"], blank=True)
    mozilla_says = models.BooleanField(
        verbose_name="mozilla Says",
        null=True,
        blank=True,
        help_text="Use 'Yes' for Thumbs Up, 'No' for Thumbs Down, and 'Unknown' for Thumb Sideways",
    )
    time_researched = models.PositiveIntegerField(verbose_name="time spent on research", default=0)

    """
    privacy_policy_links = Orderable, defined in ProductPagePrivacyPolicyLink
    Other "magic" relations that use InlinePanels will follow the same pattern of
    using Wagtail Orderables.
    """

    # What is required to sign up?
    signup_requires_email = ExtendedYesNoField(verbose_name="email")
    signup_requires_phone = ExtendedYesNoField(verbose_name="phone")
    signup_requires_third_party_account = ExtendedYesNoField(verbose_name="third-party account")
    signup_requirement_explanation = models.TextField(
        verbose_name="signup requirement description",
        max_length=5000,
        blank=True,
    )

    # How does it use this data?
    how_does_it_use_data_collected = RichTextField(
        max_length=40 * 1000,
        features=base_rich_text_options,
        help_text="How does this product use the data collected?",
        blank=True,
    )
    data_collection_policy_is_bad = models.BooleanField(default=False, verbose_name="mini-ding for bad data use?")

    # Privacy policy
    user_friendly_privacy_policy = ExtendedYesNoField(
        verbose_name="user-friendly privacy information?",
    )

    user_friendly_privacy_policy_helptext = models.TextField(
        verbose_name="user-friendly privacy description", max_length=5000, blank=True
    )

    # Minimum security standards
    show_ding_for_minimum_security_standards = models.BooleanField(
        default=False,
        verbose_name="mini-ding for doesnt meet Minimum Security Standards",
    )
    meets_minimum_security_standards = models.BooleanField(
        verbose_name="does this product meet our Minimum Security Standards?",
        null=True,
        blank=True,
    )
    uses_encryption = ExtendedYesNoField(
        verbose_name="encryption",
    )
    uses_encryption_helptext = models.TextField(verbose_name="description", max_length=5000, blank=True)
    security_updates = ExtendedYesNoField()
    security_updates_helptext = models.TextField(verbose_name="description", max_length=5000, blank=True)
    strong_password = ExtendedYesNoField()
    strong_password_helptext = models.TextField(verbose_name="description", max_length=5000, blank=True)
    manage_vulnerabilities = ExtendedYesNoField(
        verbose_name="manages security vulnerabilities",
    )
    manage_vulnerabilities_helptext = RichTextField(
        max_length=5000,
        features=base_rich_text_options,
        blank=True,
    )
    privacy_policy = ExtendedYesNoField()
    privacy_policy_helptext = models.TextField(  # REPURPOSED: WILL REQUIRE A 'clear' MIGRATION
        verbose_name="description", max_length=5000, blank=True
    )

    evaluation = models.ForeignKey(
        ProductPageEvaluation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="product_pages",
    )

    objects = ProductPageManager()

    @classmethod
    def map_import_fields(cls):
        mappings = {
            "Title": "title",
            "Wagtail Page ID": "pk",
            "Slug": "slug",
            "Show privacy ding": "privacy_ding",
            "Has adult content": "adult_content",
            "Uses wifi": "uses_wifi",
            "Uses Bluetooth": "uses_bluetooth",
            "Review date": "review_date",
            "Company": "company",
            "Blurb": "blurb",
            "Product link": "product_url",
            "Worst case": "worst_case",
            "Signup requires email": "signup_requires_email",
            "Signup requires phone number": "signup_requires_phone",
            "Signup requires 3rd party account": "signup_requires_third_party_account",
            "Signup explanation": "signup_requirement_explanation",
            "How it collects data": "how_does_it_use_data_collected",
            "Data collection privacy ding": "data_collection_policy_is_bad",
            "User friendly privacy policy": "user_friendly_privacy_policy",
            "User friendly privacy policy help text": "user_friendly_privacy_policy_helptext",
            "Meets MSS": "meets_minimum_security_standards",
            "Meets MSS privacy policy ding": "show_ding_for_minimum_security_standards",
            "Uses encryption": "uses_encryption",
            "Encryption help text": "uses_encryption_helptext",
            "Has security updates": "security_updates",
            "Security updates help text": "security_updates_helptext",
            "Strong password": "strong_password",
            "Strong password help text": "strong_password_helptext",
            "Manages security vulnerabilities": "manage_vulnerabilities",
            "Manages security help text": "manage_vulnerabilities_helptext",
            "Has privacy policy": "privacy_policy",
            "Privacy policy help text": "privacy_policy_helptext",
            "Mozilla Says": "mozilla_says",
            "Time Researched ": "time_researched",
        }
        return mappings

    @property
    def annotated_evaluation(self):
        """Evaluation object annotated with total and average creepiness."""
        if not self.evaluation:
            return None
        return (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.evaluation.pk)
        )

    @property
    def total_vote_count(self):
        return self.annotated_evaluation.total_votes

    @property
    def creepiness(self):
        try:
            # Try an annotation made above the ProductPage level
            return self._average_creepiness
        except AttributeError:
            return self.annotated_evaluation.average_creepiness

    @property
    def average_bin(self):
        return self.annotated_evaluation.average_bin

    @property
    def get_voting_json(self):
        """
        Return a dictionary as a string with the relevant data needed for the frontend:
        """
        votes_per_bin = self.evaluation.votes_per_bin
        data = {
            "creepiness": {
                "vote_breakdown": {k: v for (k, v) in enumerate(votes_per_bin)},
                "average": self.creepiness,
            },
            "total": self.total_vote_count,
        }
        return json.dumps(data)

    # TODO: refactor meta methods out as part of: https://github.com/mozilla/foundation.mozilla.org/issues/7828
    # See package docs for `get_meta_*` methods: https://pypi.org/project/wagtail-metadata/
    def get_meta_title(self):
        return gettext("*Privacy Not Included review:") + f" {self.title}"

    def get_meta_description(self):
        if self.search_description:
            return self.search_description

        soup = BeautifulSoup(self.blurb, "html.parser")
        first_paragraph = soup.find("p")
        if first_paragraph:
            return first_paragraph.text

        return super().get_meta_description()

    def get_meta_image_url(self, request):
        # Heavy-duty exception handling so the page doesn't crash due to a
        # missing sharing image.
        try:
            return (self.search_image or self.image).get_rendition("original").url
        except Exception:
            return static("_images/buyers-guide/evergreen-social.png")

    def get_preview_template(self, request, mode_name):
        return "previews/buyersguide/product_page.html"

    content_panels = Page.content_panels + [
        FieldPanel("company"),
        MultiFieldPanel(
            [
                InlinePanel("product_categories", label="Category"),
            ],
            heading="Product Category",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("privacy_ding"),
                FieldPanel("review_date"),
                FieldPanel("adult_content"),
                FieldPanel("image"),
                FieldPanel("product_url"),
                FieldPanel("time_researched"),
                FieldPanel("mozilla_says"),
                FieldPanel("uses_wifi"),
                FieldPanel("uses_bluetooth"),
                FieldPanel("blurb"),
                FieldPanel("worst_case"),
                FieldPanel("tips_to_protect_yourself"),
            ],
            heading="General Product Details",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("signup_requires_email"),
                FieldPanel("signup_requires_phone"),
                FieldPanel("signup_requires_third_party_account"),
                FieldPanel("signup_requirement_explanation"),
            ],
            heading="What can be used to sign up?",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "privacy_policy_links",
                    label="link",
                    min_num=1,
                    max_num=25,
                ),
            ],
            heading="Privacy policy links",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("meets_minimum_security_standards"),
                FieldPanel("show_ding_for_minimum_security_standards"),
                FieldPanel("uses_encryption"),
                FieldPanel("uses_encryption_helptext"),
                FieldPanel("strong_password"),
                FieldPanel("strong_password_helptext"),
                FieldPanel("security_updates"),
                FieldPanel("security_updates_helptext"),
                FieldPanel("manage_vulnerabilities"),
                FieldPanel("manage_vulnerabilities_helptext"),
                FieldPanel("privacy_policy"),
                FieldPanel("privacy_policy_helptext"),
            ],
            heading="Security",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [InlinePanel("updates", label="Update")],
            heading="News Links",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [InlinePanel("related_product_pages", label="Product")],
            heading="Related Products",
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "related_article_relations",
                    heading="Related articles",
                    label="Article",
                    max_num=5,
                ),
            ],
            heading="Related Articles",
        ),
    ]

    translatable_fields = [
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
        # Content tab fields
        TranslatableField("title"),
        SynchronizedField("privacy_ding"),
        SynchronizedField("adult_content"),
        SynchronizedField("uses_wifi"),
        SynchronizedField("uses_bluetooth"),
        SynchronizedField("review_date"),
        SynchronizedField("company"),
        TranslatableField("blurb"),
        SynchronizedField("product_url"),
        SynchronizedField("image"),
        TranslatableField("worst_case"),
        SynchronizedField("product_categories"),
        SynchronizedField("signup_requires_email"),
        SynchronizedField("signup_requires_phone"),
        SynchronizedField("signup_requires_third_party_account"),
        TranslatableField("signup_requirement_explanation"),
        SynchronizedField("signup_requires_third_party_account"),
        TranslatableField("how_does_it_use_data_collected"),
        SynchronizedField("data_collection_policy_is_bad"),
        SynchronizedField("user_friendly_privacy_policy"),
        TranslatableField("user_friendly_privacy_policy_helptext"),
        SynchronizedField("privacy_policy_links"),
        SynchronizedField("show_ding_for_minimum_security_standards"),
        SynchronizedField("meets_minimum_security_standards"),
        SynchronizedField("uses_encryption"),
        TranslatableField("uses_encryption_helptext"),
        SynchronizedField("security_updates"),
        TranslatableField("security_updates_helptext"),
        SynchronizedField("strong_password"),
        TranslatableField("strong_password_helptext"),
        SynchronizedField("manage_vulnerabilities"),
        TranslatableField("manage_vulnerabilities_helptext"),
        SynchronizedField("privacy_policy"),
        TranslatableField("privacy_policy_helptext"),
        # non-translatable fields:
        SynchronizedField("mozilla_says"),
        SynchronizedField("related_product_pages"),
        SynchronizedField("related_article_relations"),
        SynchronizedField("time_researched"),
        SynchronizedField("updates"),
        TranslatableField("tips_to_protect_yourself"),
        SynchronizedField("evaluation"),
    ]

    @property
    def product_type(self):
        return "unknown"

    @property
    def localized_related_products(self):
        related_products = ProductPage.objects.filter(related_product_relationships__page=self).order_by(
            "related_product_relationships__sort_order"
        )
        related_products = localize_queryset(related_products, preserve_order=True)
        return related_products.specific()

    @property
    def preview_related_products(self) -> list:
        """
        Fetches related product updates for CMS page previews.
        """
        related_products = orderables.get_related_items(
            self.related_product_pages.all(), "related_product", order_by="sort_order"
        )

        return related_products

    @property
    def local_categories(self):
        categories = BuyersGuideProductCategory.objects.filter(product_pages__product=self)
        return localize_categories(categories)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["product"] = self
        context["featured_cta"] = self.get_featured_cta()
        context["mediaUrl"] = settings.MEDIA_URL
        context["use_commento"] = settings.USE_COMMENTO
        context["pageTitle"] = f"{self.title} | " + gettext("Privacy & security guide") + " | Mozilla Foundation"
        return context

    def get_related_articles(self) -> models.QuerySet["BuyersGuideArticlePage"]:
        articles = orderables.get_related_items(
            self.related_article_relations.all(),
            "article",
        )
        # FIXME: This implementation does return the localized version of each article.
        #        But, it is inefficient. It would be better to pull all articles
        #        for the correct locale at once. This would require the above returns
        #        a queryset of the articles (rather than a list) and that we have an
        #        efficient way of pulling all items for a given locale.
        #        See: https://github.com/MozillaFoundation/foundation.mozilla.org/issues/9509
        return [a.localized for a in articles]

    def get_primary_related_articles(self) -> models.QuerySet["BuyersGuideArticlePage"]:
        return self.get_related_articles()[:3]

    def get_secondary_related_articles(
        self,
    ) -> models.QuerySet["BuyersGuideArticlePage"]:
        return self.get_related_articles()[3:]

    def get_featured_cta(self):
        if ProductPageCategory.objects.filter(product=self, category__show_cta=True).exists():
            return get_buyersguide_featured_cta(self)
        else:
            return None

    def serve(self, request, *args, **kwargs):
        # In Wagtail we use the serve() method to detect POST submissions.
        # Alternatively, this could be a routable view.
        # For more on this, see the docs here:
        # https://docs.wagtail.io/en/stable/reference/pages/model_recipes.html#overriding-the-serve-method
        if request.body and request.method == "POST":
            # If the request is POST. Parse the body.
            data = json.loads(request.body)
            # If the POST body has a productID and value, it's someone voting on the product
            if data.get("value"):
                # Product ID and Value can both be zero. It's impossible to get a Page with ID of zero.
                try:
                    value = int(data["value"])
                except ValueError:
                    return HttpResponseNotAllowed("Product ID or value is invalid")

                if value < 0 or value > 100:
                    return HttpResponseNotAllowed("Cannot save vote")

                try:
                    product = self

                    # 404 if the product exists but isn't live and the user isn't logged in.
                    if (not product.live and not request.user.is_authenticated) or not product:
                        return HttpResponseNotFound("Product does not exist")

                    # Save the new vote
                    ProductVote.objects.create(value=value, evaluation=product.evaluation)

                    return HttpResponse("Vote recorded", content_type="text/plain")
                except ProductPage.DoesNotExist:
                    return HttpResponseNotFound("Missing page")
                except ValidationError as ex:
                    return HttpResponseNotAllowed(f"Payload validation failed: {ex}")
                except Error as ex:
                    print(f"Internal Server Error (500) for ProductPage: {ex.message} ({type(ex)})")
                    return HttpResponseServerError()

        return super().serve(request, *args, **kwargs)

    def with_content_json(self, content):
        """
        Adds the evaluation object to ``content`` to make sure that it is preserved
        through revisions.
        """
        obj = super().with_content_json(content)
        obj.evaluation = self.evaluation
        return obj

    class Meta:
        verbose_name = "Product Page"


class BuyersGuideProductPageArticlePageRelation(TranslatableMixin, Orderable):
    product = ParentalKey(
        "wagtailpages.ProductPage",
        related_name="related_article_relations",
    )
    article = models.ForeignKey(
        "wagtailpages.BuyersGuideArticlePage",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    panels = [FieldPanel("article")]

    def __str__(self):
        return f"{self.product.name} -> {self.article.title}"

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        pass


class GeneralProductPage(ProductPage):
    template = "pages/buyersguide/product_page.html"

    camera_device = ExtendedYesNoField(
        verbose_name="camera: Device",
    )

    camera_app = ExtendedYesNoField(
        verbose_name="camera: App",
    )

    microphone_device = ExtendedYesNoField(
        verbose_name="microphone: Device",
    )

    microphone_app = ExtendedYesNoField(
        verbose_name="microphone: App",
    )

    location_device = ExtendedYesNoField(
        verbose_name="tracks location: Device",
    )

    location_app = ExtendedYesNoField(
        verbose_name="tracks location: App",
    )

    # What data does it collect?

    personal_data_collected = models.TextField(
        verbose_name="personal",
        max_length=5000,
        blank=True,
    )

    biometric_data_collected = models.TextField(
        verbose_name="body Related",
        max_length=5000,
        blank=True,
    )

    social_data_collected = models.TextField(
        verbose_name="social",
        max_length=5000,
        blank=True,
    )

    # How can you control your data

    how_can_you_control_your_data = RichTextField(
        max_length=20 * 1000,
        features=base_rich_text_options,
        help_text="How does this product let you control your data?",
        blank=True,
    )

    data_control_policy_is_bad = models.BooleanField(default=False, verbose_name="mini-ding for bad data control?")

    # Company track record

    company_track_record = models.CharField(
        verbose_name="company's known track record?",
        choices=TRACK_RECORD_CHOICES,
        default="Average",
        max_length=20,
    )

    track_record_is_bad = models.BooleanField(default=False, verbose_name="mini-ding for bad track record")

    track_record_details = RichTextField(
        max_length=5000,
        features=base_rich_text_options,
        help_text="Describe the track record of this company here.",
        blank=True,
    )

    # Child Safety Blurb

    child_safety_blurb = RichTextField(
        max_length=10000,
        features=base_rich_text_options,
        help_text="Child safety information, if applicable.",
        blank=True,
    )

    # Offline use

    offline_capable = ExtendedYesNoField(
        verbose_name="can this product be used offline?",
    )

    offline_use_description = RichTextField(
        max_length=5000,
        features=base_rich_text_options,
        help_text="Describe how this product can be used offline.",
        blank=True,
    )

    # Artificial Intelligence

    uses_ai = ExtendedYesNoField(
        verbose_name="does the product use AI?",
    )
    ai_helptext = RichTextField(
        max_length=5000,
        features=base_rich_text_options,
        help_text="Helpful text around AI to show on the product page",
        blank=True,
    )
    ai_is_untrustworthy = ExtendedChoiceField(
        verbose_name="How trustworthy is the AI?",
    )
    ai_is_untrustworthy_helptext = models.TextField(
        verbose_name="How trustworthy is the AI explanation",
        max_length=5000,
        blank=True,
    )
    ai_is_untrustworthy_ding = models.BooleanField(
        verbose_name="mini-ding for bad AI",
        default=False,
    )
    ai_what_can_it_do = RichTextField(
        verbose_name="what kind of decisions does the AI make about you or for you?",
        blank=True,
    )
    ai_is_transparent = ExtendedChoiceField(
        verbose_name="How transparent is the company about how the AI works?",
    )
    ai_is_transparent_helptext = models.TextField(
        verbose_name="AI Transparency Explanation",
        max_length=5000,
        blank=True,
    )
    ai_can_user_control = ExtendedChoiceField(
        verbose_name="How much control do users have over the data the AI collects?",
    )
    ai_can_user_control_helptext = models.TextField(
        verbose_name="AI Control Explanation",
        max_length=5000,
        blank=True,
    )

    @classmethod
    def map_import_fields(cls):
        generic_product_import_fields = super().map_import_fields()
        general_product_mappings = {
            "Has camera device": "camera_device",
            "Has camera app": "camera_app",
            "Has microphone device": "microphone_device",
            "Has microphone app": "microphone_app",
            "Has location device": "location_device",
            "Has location app": "location_app",
            "Personal data collected": "personal_data_collected",
            "Biometric data collected": "biometric_data_collected",
            "Social data collected": "social_data_collected",
            "How you can control your data": "how_can_you_control_your_data",
            "Company track record": "company_track_record",
            "Show company track record privacy ding": "track_record_is_bad",
            "Child safety blurb": "child_safety_blurb",
            "Offline capable": "offline_capable",
            "Offline use": "offline_use_description",
            "Uses AI": "uses_ai",
            "AI help text": "ai_helptext",
            "AI is transparent": "ai_is_transparent",
            "AI is transparent help text": "ai_is_transparent_helptext",
            "AI is untrustworthy": "ai_is_untrustworthy",
            "AI is untrustworthy help text": "ai_is_untrustworthy_helptext",
            "AI is untrustworthy ding": "ai_is_untrustworthy_ding",
            "AI What can it do": "ai_what_can_it_do",
            "AI can user control": "ai_can_user_control",
            "AI can user control help text": "ai_can_user_control_helptext",
        }
        # Return the merged fields
        return {**generic_product_import_fields, **general_product_mappings}

    # administrative panels
    content_panels = ProductPage.content_panels.copy()
    content_panels = insert_panels_after(
        content_panels,
        "General Product Details",
        [
            MultiFieldPanel(
                [
                    FieldPanel("camera_device"),
                    FieldPanel("camera_app"),
                    FieldPanel("microphone_device"),
                    FieldPanel("microphone_app"),
                    FieldPanel("location_device"),
                    FieldPanel("location_app"),
                ],
                heading="Can it snoop on me?",
                classname="collapsible",
            ),
        ],
    )

    content_panels = insert_panels_after(
        content_panels,
        "What can be used to sign up?",
        [
            MultiFieldPanel(
                [
                    FieldPanel("personal_data_collected"),
                    FieldPanel("biometric_data_collected"),
                    FieldPanel("social_data_collected"),
                    FieldPanel("how_does_it_use_data_collected"),
                    FieldPanel("data_collection_policy_is_bad"),
                    FieldPanel("how_can_you_control_your_data"),
                    FieldPanel("data_control_policy_is_bad"),
                    FieldPanel("company_track_record"),
                    FieldPanel("track_record_details"),
                    FieldPanel("track_record_is_bad"),
                    FieldPanel("child_safety_blurb"),
                    FieldPanel("offline_capable"),
                    FieldPanel("offline_use_description"),
                    FieldPanel("user_friendly_privacy_policy"),
                    FieldPanel("user_friendly_privacy_policy_helptext"),
                ],
                heading="What data does the company collect?",
                classname="collapsible",
            ),
        ],
    )

    content_panels = insert_panels_after(
        content_panels,
        "Security",
        [
            MultiFieldPanel(
                [
                    FieldPanel("uses_ai"),
                    FieldPanel("ai_helptext"),
                    FieldPanel("ai_is_untrustworthy"),
                    FieldPanel("ai_is_untrustworthy_helptext"),
                    FieldPanel("ai_is_transparent"),
                    FieldPanel("ai_is_transparent_helptext"),
                    FieldPanel("ai_can_user_control"),
                    FieldPanel("ai_can_user_control_helptext"),
                ],
                heading="Artificial Intelligence",
                classname="collapsible",
            ),
        ],
    )

    translatable_fields = ProductPage.translatable_fields + [
        TranslatableField("personal_data_collected"),
        TranslatableField("biometric_data_collected"),
        TranslatableField("social_data_collected"),
        TranslatableField("how_can_you_control_your_data"),
        SynchronizedField("data_control_policy_is_bad"),
        SynchronizedField("company_track_record"),
        SynchronizedField("track_record_is_bad"),
        TranslatableField("track_record_details"),
        TranslatableField("child_safety_blurb"),
        SynchronizedField("offline_capable"),
        TranslatableField("offline_use_description"),
        SynchronizedField("uses_ai"),
        SynchronizedField("ai_is_transparent"),
        TranslatableField("ai_is_transparent_helptext"),
        TranslatableField("ai_helptext"),
        SynchronizedField("ai_is_untrustworthy"),
        TranslatableField("ai_is_untrustworthy_helptext"),
        SynchronizedField("ai_is_untrustworthy_ding"),
        TranslatableField("ai_what_can_it_do"),
        SynchronizedField("ai_can_user_control"),
        TranslatableField("ai_can_user_control_helptext"),
    ]

    @property
    def product_type(self):
        return "general"

    class Meta:
        verbose_name = "General Product Page"


@receiver(post_save, sender=GeneralProductPage)
@receiver(post_save, sender=ProductPage)
def create_evaluation(sender, instance, created, **kwargs):
    """Post-save hook to create a ProductPageEvaluation for a ProductPage.

    Creates an evaluation for newly created products and syncs this with all translations.
    """
    if created:
        if instance.locale.language_code == settings.LANGUAGE_CODE and not instance.evaluation:
            evaluation = ProductPageEvaluation.objects.create()
            instance.evaluation = evaluation
            instance.save(update_fields=["evaluation"])
            ProductPage.objects.filter(translation_key=instance.translation_key).update(evaluation=evaluation)
    return instance


@hooks.register("after_copy_page")
def reset_product_page_votes(request, page, new_page):
    """Resets the votes on copied product pages.

    When copying a ProductPage (or GeneralProductPage), the votes are copied as well since
    the evaluation object is copied over. This hook resets the evaluation object on the
    product page and its translations so that the votes are also reset.
    """
    if new_page.specific_class == ProductPage or new_page.specific_class == GeneralProductPage:
        evaluation = ProductPageEvaluation.objects.create()
        new_page.evaluation = evaluation
        new_page.save(update_fields=["evaluation"])
        new_products = ProductPage.objects.filter(translation_key=new_page.translation_key)
        new_products.update(evaluation=evaluation)


class ExcludedCategories(TranslatableMixin, Orderable):
    """
    This allows us to filter categories from showing up on the PNI site
    """

    page = ParentalKey("wagtailpages.BuyersGuidePage", related_name="excluded_categories")
    category = models.ForeignKey(
        BuyersGuideProductCategory,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("category"),
    ]

    def __str__(self):
        return self.category.name

    class Meta(TranslatableMixin.Meta, Orderable.Meta):
        verbose_name = "Excluded Category"
