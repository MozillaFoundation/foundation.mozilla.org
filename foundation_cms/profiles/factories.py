import random

import factory
import wagtail_factories
from wagtail import models as wagtail_models

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.utils.helpers import get_faker, reseed
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory
from foundation_cms.profiles.models import (
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

    # List of all topics to assign to experts and feature on the hub
    topics = list(Topic.objects.all())

    # Create Expert Hub page if it doesn't exist under site root
    print("Creating Expert Hub Page...")
    existing_hub = ExpertHubPage.objects.filter(slug="mozilla-expert-hub", locale=default_locale).first()
    if existing_hub:
        hub = existing_hub
        print("  Expert Hub Page already exists.")
    else:
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

    # Create Expert Profile pages if they don't exist, and link to hub
    print("Creating Expert Profile Pages...")
    expert_pages = []
    countries = ["US", "DE", "BR", "KE", "JP", "GB", "FR", "IN", "MX", "CA", "AU", "NL"]
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
            location=countries[i % len(countries)],
            affiliation=fake.company(),
            seo_title=name,
            search_description=fake.sentence(nb_words=10).rstrip("."),
        )
        hub.add_child(instance=expert)

        # Topics must be added after add_child so the page has a PK.
        if topics:
            assigned_topics = random.sample(topics, min(random.randint(1, 3), len(topics)))
            expert.topics.add(*assigned_topics)

        expert.save_revision().publish()
        print(f"  + Expert: {name}")
        expert_pages.append(expert)

    print(f"  {len(expert_pages)} Expert Profile Pages ready.")

    # Link featured experts to hub
    print("Linking featured experts to Expert Hub Page...")
    if not hub.featured_experts.exists():
        for i, expert in enumerate(expert_pages[:6]):
            ExpertHubFeaturedExpert.objects.create(
                hub_page=hub,
                expert=expert,
                sort_order=i,
            )
        hub.save_revision().publish()
        print(f"  {min(6, len(expert_pages))} featured experts linked.")
    else:
        print("  Featured experts already linked.")

    # Link featured topics to hub
    print("Linking featured topics to Expert Hub Page...")
    if not hub.featured_topics.exists():
        for i, topic in enumerate(topics[:5]):
            ExpertHubFeaturedTopic.objects.create(
                hub_page=hub,
                topic=topic,
                sort_order=i,
            )
        hub.save_revision().publish()
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


class ExpertProfilePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ExpertProfilePage

    title = factory.Faker("name")
    slug = factory.Faker("slug")
    image = factory.SubFactory(wagtail_factories.ImageFactory)
    role = factory.Faker("job")
    bio = factory.Faker("paragraph", nb_sentences=3)
    location = "US"
    affiliation = factory.Faker("company")
    seo_title = factory.Faker("sentence", nb_words=3)
    search_description = factory.Faker("sentence", nb_words=10)
