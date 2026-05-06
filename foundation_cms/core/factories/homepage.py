from pathlib import Path

import factory
from django.core.files.images import ImageFile
from wagtail.images import get_image_model
from wagtail.models import Locale, Page, Site
from wagtail_factories import PageFactory

from foundation_cms.base.utils.helpers import reseed
from foundation_cms.core.factories.homepage_data import (
    build_homepage_body,
    build_homepage_hero_accordion,
)
from foundation_cms.core.models.home_page import HomePage
from foundation_cms.snippets.factories import ensure_homepage_newsletters

IMAGE_DIR = Path(__file__).resolve().parent / "data" / "homepage" / "images"

HOMEPAGE_IMAGE_SPECS = {
    "hero_accordion__1": {"filename": "hero_accordion__1.jpg", "alt_text": "Intro video thumbnail image"},
    "hero_accordion__2": {"filename": "hero_accordion__2.jpg", "alt_text": "Mozilla Festival 2025 visual"},
    "hero_accordion__3": {"filename": "hero_accordion__3.jpg", "alt_text": "Our global community at MozFest"},
    "timely_activations__1": {"filename": "timely_activation_card__1.jpg", "alt_text": "Internet Health"},
    "timely_activations__2": {"filename": "timely_activation_card__2.jpg", "alt_text": "Privacy and Security"},
    "timely_activations__3": {"filename": "timely_activation_card__3.jpg", "alt_text": "Digital Inclusion"},
    "spotlight_card_set__1": {"filename": "spotlight_card__1.jpg", "alt_text": "Faculty"},
    "spotlight_card_set__2": {"filename": "spotlight_card__2.jpg", "alt_text": "Common Voice"},
    "spotlight_card_set__3": {"filename": "spotlight_card__3.jpg", "alt_text": "Festival Wrangler"},
    "pillar_card__1": {"filename": "arrow-up.svg", "alt_text": ""},
    "pillar_card__2": {"filename": "stairs.svg", "alt_text": ""},
    "pillar_card__3": {"filename": "rays.svg", "alt_text": ""},
    "featured_card": {"filename": "featured_card.jpg", "alt_text": ""},
}

Image = get_image_model()


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage

    title = factory.Faker("sentence", nb_words=4)
    seo_title = factory.Faker("sentence", nb_words=3)
    search_description = factory.Faker("sentence", nb_words=12)


def _get_or_create_homepage_image(hp_image):
    """Get or create the image for the given homepage image key."""
    spec = HOMEPAGE_IMAGE_SPECS[hp_image]
    filename = spec["filename"]
    title = spec["alt_text"] or hp_image
    file_path = IMAGE_DIR / filename

    existing = Image.objects.filter(title=title, file=f"original_images/{filename}").first()
    if existing:
        return existing.id

    with open(file_path, "rb") as image_file:
        django_file = ImageFile(image_file, name=filename)
        image = Image.objects.create(title=title, file=django_file)
        return image.id


def _get_homepage_images():
    """Import all homepage images and return a dict of {key: image_id}."""
    return {hp_image: _get_or_create_homepage_image(hp_image) for hp_image in HOMEPAGE_IMAGE_SPECS}


def generate(parent=None, seed=42, slug="redesign-home"):
    """
    Generate a HomePage with the given parent, seed, and slug.
    Returns the created HomePage instance.
    """
    reseed(seed)

    if parent is None:
        parent = Page.get_first_root_node()
        if not parent.pk:
            parent.save()

    site = Site.objects.filter(is_default_site=True).first()
    if site is None:
        site = Site.objects.create(
            hostname="localhost",
            port=8000,
            root_page=parent,
            site_name="Mozilla Foundation",
            is_default_site=True,
        )

    locale = Locale.get_default()

    existing = HomePage.objects.filter(slug=slug, locale=locale).first()
    if existing:
        print("Redesign HomePage already exists.")
        return existing

    images = _get_homepage_images()
    newsletters = ensure_homepage_newsletters(site)

    homepage = HomePageFactory.build(
        title="Redesign Homepage",
        slug=slug,
        seo_title="Mozilla Foundation",
        search_description=(
            "Mozilla is a global non-profit dedicated to putting you in control "
            "of your online experience and shaping the future of the web for the public good."
        ),
        locale=locale,
        hero_accordion=build_homepage_hero_accordion(images),
        body=build_homepage_body(main_newsletter_id=newsletters["main"].id, images=images),
    )

    parent.add_child(instance=homepage)
    homepage.save_revision().publish()

    if site.root_page != homepage:
        site.root_page = homepage
        site.save()

    print(f"Redesign HomePage created under {parent}.")
    return homepage
