from django.test import Client
from wagtail.models import Locale, Page, Site
from wagtail_factories import PageFactory

from foundation_cms.base.utils.helpers import reseed
from foundation_cms.core.factories.general_page_data import build_general_page_body
from foundation_cms.core.models.general_page import GeneralPage


class GeneralPageFactory(PageFactory):
    class Meta:
        model = GeneralPage

    title = "General Page"
    seo_title = "General Page"
    search_description = "A General Page built to exercise body block types that have factories."
    show_hero = False


def generate(parent=None, seed=42, slug="general-page-1"):
    """
    Generate a GeneralPage with the given parent, seed, and slug.
    Returns the created GeneralPage instance.
    """
    reseed(seed)

    if parent is None:
        site = Site.objects.filter(is_default_site=True).first()
        parent = site.root_page if site else Page.get_first_root_node()
        if not parent.pk:
            parent.save()

    locale = Locale.get_default()

    existing = GeneralPage.objects.filter(slug=slug, locale=locale).first()
    if existing:
        print("General Page demo already exists.")
        return existing

    page = GeneralPageFactory.build(
        slug=slug,
        locale=locale,
        body=build_general_page_body(),
    )

    parent.add_child(instance=page)
    page.save_revision().publish()
    _prewarm_image_renditions(page)

    print(f"General Page demo created under {parent}.")
    return page


def _prewarm_image_renditions(page):
    """
    Render the page once, right now, so every image rendition it needs already
    exists in the database. Otherwise the first real request to this page has
    to generate every rendition cold, and if anything else requests the same
    URL around the same time (e.g. Percy's own asset-discovery crawl) they can
    race trying to insert the same not-yet-existing rendition rows.
    """
    try:
        Client().get(page.url, SERVER_NAME="localhost")
    except Exception as e:
        print(f"Warning: failed to pre-warm image renditions for {page}: {e}")
