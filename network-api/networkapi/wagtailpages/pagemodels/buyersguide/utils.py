from django.apps import apps
from django.conf import settings
from wagtail.core.models import Locale

from networkapi.wagtailpages.utils import get_default_locale


def get_categories_for_locale(language_code):
    """
    Start with the English list of categories, and replace any of them
    with their localized counterpart, where possible, so that we don't
    end up with an incomplete category list due to missing locale records.
    """
    BuyersGuideProductCategory = apps.get_model(app_label='wagtailpages', model_name='BuyersGuideProductCategory')
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
        ).first() or cat for cat in default_locale_list
    ]


def sort_average(products):
    """
    `products` is a QuerySet of ProductPages.
    """
    return sorted(products, key=lambda p: p.creepiness)

def get_featured_cta(self):
    BuyersGuidePage = apps.get_model(app_label='wagtailpages', model_name='BuyersGuidePage')
    pni_home_page = BuyersGuidePage.objects.ancestor_of(self, inclusive=True).live().first()
    featured_cta = pni_home_page.call_to_action
    return featured_cta
