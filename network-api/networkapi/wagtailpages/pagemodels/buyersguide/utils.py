from django.apps import apps
from django.core.cache import cache

from networkapi.wagtailpages.utils import localize_queryset


def get_buyersguide_featured_cta(page):
    """
    This function takes a page, finds the Buyer's Guide home page in its list
    of ancestors, and then returns the home page's featured CTA if applicable.
    """
    BuyersGuidePage = apps.get_model(app_label="wagtailpages", model_name="BuyersGuidePage")
    buyers_guide_home_page = BuyersGuidePage.objects.ancestor_of(page, inclusive=True).live().first()
    featured_cta = buyers_guide_home_page.call_to_action
    return featured_cta


def get_product_subset(cutoff_date, authenticated, key, products, language_code="en"):
    """
    filter a queryset based on our current cutoff date,
    as well as based on whether a user is authenticated
    to the system or not (authenticated users get to
    see all products, including draft products)
    """
    products = products.filter(review_date__gte=cutoff_date, locale__language_code=language_code)

    if not authenticated:
        products = products.live()

    products = (
        products.prefetch_related(
            "image__renditions",
            "product_categories__category",
        )
        .with_average_creepiness()
        .order_by("_average_creepiness")
    )

    products = annotate_product_categories_local_names(products, language_code)

    cache.get_or_set(key, products, 24 * 60 * 60)  # Set cache for 24h
    return products


def _localize_category_parent(categories):
    """Localize the parent of each category.

    Go through a BuyersGuideCategory queryset and localize the parent object.

    Args:
        categories (QuerySet): A categories queryset. It is important to have `parent`
            prefetched/pre-selected to avoid N+1 queries.

    Returns:
        QuerySet: The categories queryset where each category has a localized parent.
    """
    BuyersGuideProductCategory = apps.get_model(app_label="wagtailpages", model_name="BuyersGuideProductCategory")

    parents_ids = list({category.parent.pk for category in categories if category.parent})
    parents = BuyersGuideProductCategory.objects.filter(id__in=parents_ids)
    parents = localize_queryset(parents)
    parents_cache = {parent.translation_key: parent for parent in parents}

    for category in categories:
        if category.parent:
            local_parent = parents_cache.get(category.parent.translation_key)
            category.parent = local_parent

    return categories


def localize_categories(categories, preserve_order=True):
    """Localize a category.

    Localizes a category queryset by finding the localized version of the category.
    If the localized version doesn't exist, return the default category.
    It also pre-selects and localizes the parent of the category.

    Args:
        category (BuyersGuideProductCategory): The category to localize.

    Returns:
        BuyersGuideProductCategory: The localized category.
    """
    categories = localize_queryset(categories, preserve_order=preserve_order)
    categories = categories.select_related("parent").with_usage_annotation()
    categories = _localize_category_parent(categories)
    return categories


def annotate_product_categories_local_names(products, active_language_code):
    """Annotate products with localized category names.

    For each product, get the `product_categories`, find the localized version of those
    categories and then return a list of those localized categories names.

    Args:
        products (QuerySet): The products to annotate. The `product_categories__categories`
            property must be prefetched to avoid N+1 queries.
        active_language_code (str): The language code for the current request, e.g. "en".

    Returns:
        QuerySet: The products queryset where each product has a `local_category_names`,
            which is a list of localized category names.
    """
    BuyersGuideProductCategory = apps.get_model(app_label="wagtailpages", model_name="BuyersGuideProductCategory")

    local_categories = BuyersGuideProductCategory.objects.filter(locale__language_code=active_language_code)
    local_categories_cache = {category.translation_key: category for category in local_categories}

    for product in products:
        product_category_relationships = product.product_categories.all()
        default_categories = [relationship.category for relationship in product_category_relationships]
        local_category_names = []
        for category in default_categories:
            if local_category := local_categories_cache.get(category.translation_key):
                # Found a category in the local language, use that
                local_category_names.append(local_category.name)
            else:
                # Fall back to default category
                local_category_names.append(category.name)
        product.local_category_names = local_category_names

    return products
