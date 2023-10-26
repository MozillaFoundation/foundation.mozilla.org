from django.apps import apps
from django.conf import settings
from wagtail.models import Locale

from networkapi.wagtailpages.utils import get_default_locale


def get_categories_for_locale(language_code):
    """
    Start with the English list of categories, and replace any of them
    with their localized counterpart, where possible, so that we don't
    end up with an incomplete category list due to missing locale records.
    """
    BuyersGuideProductCategory = apps.get_model(app_label="wagtailpages", model_name="BuyersGuideProductCategory")
    DEFAULT_LANGUAGE_CODE = settings.LANGUAGE_CODE
    (DEFAULT_LOCALE, DEFAULT_LOCALE_ID) = get_default_locale()

    default_locale_list = BuyersGuideProductCategory.objects.filter(
        hidden=False,
        locale=DEFAULT_LOCALE,
    )

    if language_code == DEFAULT_LANGUAGE_CODE:
        return default_locale_list

    try:
        actual_locale = Locale.objects.get(language_code=language_code)
    except Locale.DoesNotExist:
        actual_locale = Locale.objects.get(language_code=DEFAULT_LANGUAGE_CODE)

    return [
        BuyersGuideProductCategory.objects.filter(
            translation_key=cat.translation_key,
            locale=actual_locale,
        ).first()
        or cat
        for cat in default_locale_list
    ]


def get_buyersguide_featured_cta(page):
    """
    This function takes a page, finds the Buyer's Guide home page in its list
    of ancestors, and then returns the home page's featured CTA if applicable.
    """
    BuyersGuidePage = apps.get_model(app_label="wagtailpages", model_name="BuyersGuidePage")
    buyers_guide_home_page = BuyersGuidePage.objects.ancestor_of(page, inclusive=True).live().first()
    featured_cta = buyers_guide_home_page.call_to_action
    return featured_cta
