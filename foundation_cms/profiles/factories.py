import random

import factory
import wagtail_factories
from wagtail import models as wagtail_models

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.utils.helpers import get_faker, reseed
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory
from foundation_cms.profiles.models import (
    ExpertDirectoryPage,
    ExpertHubFeaturedExpert,
    ExpertHubFeaturedTopic,
    ExpertHubPage,
    ExpertProfilePage,
)


def generate(seed):
    reseed(seed)
    fake = get_faker()

    site = wagtail_models.Site.objects.filter(is_default_site=True).first()
    root = site.root_page if site else wagtail_models.Page.get_first_root_node()
    default_locale = wagtail_models.Locale.get_default()

    topics = list(Topic.objects.all())

    # Create Expert Hub page
    print("Creating Expert Hub Page...")
    hub = ExpertHubPage.objects.filter(slug="mozilla-expert-hub", locale=default_locale).first()
    if not hub:
        hub = ExpertHubPage(
            title="Mozilla Expert Hub",
            slug="mozilla-expert-hub",
            locale=default_locale,
            seo_title="Mozilla Expert Hub",
            search_description="Explore Mozilla's network of experts.",
        )
        root.add_child(instance=hub)
        hub.save_revision().publish()
        print("  Expert Hub Page created.")
    else:
        print("  Expert Hub Page already exists.")

    # Create Expert Directory page under hub
    print("Creating Expert Directory Page...")
    directory = ExpertDirectoryPage.objects.filter(slug="directory", locale=default_locale).first()
    if not directory:
        directory = ExpertDirectoryPage(
            title="Expert Directory",
            slug="directory",
            locale=default_locale,
            seo_title="Expert Directory",
            search_description="Browse and filter all Mozilla experts.",
        )
        hub.add_child(instance=directory)
        directory.save_revision().publish()
        print("  Expert Directory Page created.")
    else:
        print("  Expert Directory Page already exists.")

    # Create Expert Profile pages
    print("Creating Expert Profile Pages...")
    expert_pages = []
    country_codes = ["US", "DE", "BR", "KE", "JP", "GB", "FR", "IN", "MX", "CA", "AU", "NL"]
    for i in range(15):
        slug = f"expert-{i + 1}"
        existing = ExpertProfilePage.objects.filter(slug=slug, locale=default_locale).first()
        if existing:
            expert_pages.append(existing)
            continue

        name = fake.name()
        expert = ExpertProfilePage(
            title=name,
            slug=slug,
            locale=default_locale,
            image=ImageFactory(),
            role=fake.job(),
            bio=fake.paragraph(nb_sentences=3),
            location=country_codes[i % len(country_codes)],
            affiliation=fake.company(),
            seo_title=name,
            search_description=fake.sentence(nb_words=10).rstrip("."),
        )
        hub.add_child(instance=expert)

<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
from foundation_cms.profiles.models import ExpertProfilePage
=======
        if topics:
            assigned_topics = random.sample(topics, min(random.randint(1, 3), len(topics)))
            expert.topics.add(*assigned_topics)
>>>>>>> main

        expert.save_revision().publish()
        print(f"  + Expert: {name}")
        expert_pages.append(expert)

<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
=======
    print(f"  {len(expert_pages)} Expert Profile Pages ready.")

    # Link featured experts to hub
    print("Linking featured experts to Expert Hub Page...")
    if not hub.featured_experts.exists():
        for i, expert in enumerate(expert_pages[:6]):
            ExpertHubFeaturedExpert.objects.create(hub_page=hub, expert=expert, sort_order=i)
        hub.save_revision().publish()
        print(f"  {min(6, len(expert_pages))} featured experts linked.")
    else:
        print("  Featured experts already linked.")

    # Link featured topics to directory
    print("Linking featured topics to Expert Directory Page...")
    if not directory.featured_topics.exists():
        for i, topic in enumerate(topics[:5]):
            ExpertHubFeaturedTopic.objects.create(hub_page=directory, topic=topic, sort_order=i)
        directory.save_revision().publish()
        print(f"  {min(5, len(topics))} featured topics linked.")
    else:
        print("  Featured topics already linked.")

    print("Expert Hub setup complete.")
    return hub


class ExpertHubPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ExpertHubPage

    title = "Expert Hub"
    slug = factory.Faker("slug")
    seo_title = factory.Faker("sentence", nb_words=3)
    search_description = factory.Faker("sentence", nb_words=10)


class ExpertDirectoryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ExpertDirectoryPage

    title = "Expert Directory"
    slug = factory.Faker("slug")
    seo_title = factory.Faker("sentence", nb_words=3)
    search_description = factory.Faker("sentence", nb_words=10)


>>>>>>> main
class ExpertProfilePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ExpertProfilePage

<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
    role = factory.Faker("job")
    bio = factory.Faker("paragraph")
    location = factory.Iterator(["US", "DE", "BR", "KE", "JP"])
    image = factory.SubFactory(wagtail_factories.ImageFactory)
    seo_title = factory.Faker("sentence")
    search_description = factory.Faker("paragraph")
=======
    title = factory.Faker("name")
    slug = factory.Faker("slug")
    image = factory.SubFactory(wagtail_factories.ImageFactory)
    role = factory.Faker("job")
    bio = factory.Faker("paragraph", nb_sentences=3)
    location = "US"
    affiliation = factory.Faker("company")
    seo_title = factory.Faker("sentence", nb_words=3)
    search_description = factory.Faker("sentence", nb_words=10)
>>>>>>> main
