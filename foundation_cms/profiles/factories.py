import random

import factory
import wagtail_factories
from wagtail import models as wagtail_models

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.utils.helpers import get_faker, reseed, to_streamfield_value
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
)
from foundation_cms.profiles.models import (
    ExpertDirectoryPage,
    ExpertExternalLink,
    ExpertHubFeaturedExpert,
    ExpertHubFeaturedTopic,
    ExpertHubPage,
    ExpertProfilePage,
    ExpertProfileSelectedArticle,
)

CURATED_ARTICLE_COUNT = 5
CURATED_ARTICLE_EXPERT_SLUG = "expert-1"
CURATED_ARTICLE_DESCRIPTIONS = [
    "A short seeded description for the compact article row.",
    (
        "The Internet has always been a place where you can find your people. "
        "It's a lifeline for collaboration among far flung collaborators."
    ),
    (
        "The Internet has always been a place where you can find your people. "
        "It's a lifeline for collaboration among far flung individuals with "
        "specific interests, backgrounds, or tastes. "
        "This longer seeded description gives the expert profile article list "
        "enough copy to exercise clamped text."
    ),
]
PROFILE_INTRO_EXPERT_SLUG = "expert-1"
PROFILE_INTRO_BIO = (
    "<p>Priya is a feminist tech and media maker, and the co-founder and CEO of a feminist AI-social "
    "entrepreneurship, Mumkin App LLP. Priya is a winner of the national film award of India, conferred by the "
    "President of India, a recipient of the German Chancellor Fellowship for Young Leaders (AvH Stiftung, "
    "Germany), "
    "and the co-founder of an international non-profit, Sahiyo.</p>"
    "<p>Priya is collaborating with SOPPECOM to build a platform to share stories of women farmers, mainstreaming "
    "their struggles. Priya's individual research project explores the impact of digital public infrastructures "
    "(DPIs) on the health and livelihood of rural health workers and daily wage labourers. Her project further "
    "explores the onset of data mining for emergent AI-based technologies and its impact on India's rural "
    "population.</p>"
)
PROFILE_INTRO_QUOTE = "Involved elephant club later best ditching points place status hits."
PROFILE_INTRO_QUOTE_ATTRIBUTION = "Quote by Firstname Lastname"
EXTERNAL_LINK_EXPERT_SLUG = "expert-1"
EXTERNAL_LINKS = [
    {
        "title": (
            "Network Neutrality in Brazil: the recently enacted Presidential " "Decree consolidates meaningful rules"
        ),
        "description": (
            "Amidst an economic and political turmoil, Brazil gave a "
            "significant step towards protection of "
            "network neutrality - the principle that keeps the Internet an open platform."
        ),
        "url": "https://foundation.mozilla.org/",
    },
    {
        "title": "Portfolio",
        "description": "Description of link and stuff",
        "url": "https://foundation.mozilla.org/en/",
    },
    {
        "title": (
            "Network Neutrality in Brazil: the recently enacted Presidential " "Decree consolidates meaningful rules"
        ),
        "description": (
            "Amidst an economic and political turmoil, Brazil gave a "
            "significant step towards protection of "
            "network neutrality - the principle that keeps the Internet an open platform."
        ),
        "url": "https://foundation.mozilla.org/en/blog/",
    },
    {
        "title": (
            "Network Neutrality in Brazil: the recently enacted Presidential " "Decree consolidates meaningful rules"
        ),
        "description": (
            "Amidst an economic and political turmoil, Brazil gave a "
            "significant step towards protection of "
            "network neutrality - the principle that keeps the Internet an open platform."
        ),
        "url": "https://foundation.mozilla.org/en/research/",
    },
]


def ensure_nothing_personal_home(root, default_locale):
    existing = NothingPersonalHomePage.objects.filter(slug="nothing-personal", locale=default_locale).first()
    if existing:
        if not existing.live:
            existing.save_revision().publish()
        return existing

    home = NothingPersonalHomePage(
        title="Nothing Personal",
        slug="nothing-personal",
        theme="nothing_personal",
        locale=default_locale,
        seo_title="Nothing Personal",
        search_description="Nothing Personal articles and reviews.",
    )
    root.add_child(instance=home)
    home.save_revision().publish()
    return home


def ensure_expert_curated_articles(root, default_locale, topics, expert_pages, fake):
    expert = next((page for page in expert_pages if page.slug == CURATED_ARTICLE_EXPERT_SLUG), None)
    if not expert or expert.selected_articles.exists():
        return

    np_home = ensure_nothing_personal_home(root, default_locale)
    model_instance = NothingPersonalArticlePage()
    articles = []

    for i in range(CURATED_ARTICLE_COUNT):
        slug = f"expert-profile-article-{i + 1}"
        article = NothingPersonalArticlePage.objects.filter(slug=slug, locale=default_locale).first()

        if not article:
            title = fake.sentence(nb_words=5).rstrip(".")
            lede_text = CURATED_ARTICLE_DESCRIPTIONS[i % len(CURATED_ARTICLE_DESCRIPTIONS)]
            body_html = f"<p>{fake.paragraph(nb_sentences=4)}</p>"
            article = NothingPersonalArticlePage(
                title=title,
                slug=slug,
                theme="nothing_personal",
                locale=default_locale,
                displayed_hero_content=NothingPersonalArticlePage.HERO_CONTENT_IMAGE,
                hero_image=ImageFactory(),
                hero_image_alt_text=fake.sentence(nb_words=8).rstrip("."),
                lede_text=lede_text,
                search_image=ImageFactory(),
                seo_title=title,
                search_description=lede_text,
            )
            article.body = to_streamfield_value(
                [{"type": "rich_text", "value": body_html}],
                stream_block=model_instance.body.stream_block,
            )
            np_home.add_child(instance=article)

            if topics:
                article.topics.add(*random.sample(topics, min(random.randint(1, 3), len(topics))))

            article.save_revision().publish()

        articles.append(article)

    for sort_order, article in enumerate(articles):
        ExpertProfileSelectedArticle.objects.create(
            page=expert,
            article=article,
            sort_order=sort_order,
        )

    expert.save_revision().publish()
    print(f"  {len(articles)} curated articles linked to {expert.title}.")


def ensure_expert_external_links(default_locale):
    expert = ExpertProfilePage.objects.filter(
        slug=EXTERNAL_LINK_EXPERT_SLUG,
        locale=default_locale,
    ).first()
    if not expert or expert.external_links.exists():
        return

    for sort_order, link in enumerate(EXTERNAL_LINKS):
        ExpertExternalLink.objects.create(
            page=expert,
            sort_order=sort_order,
            **link,
        )

    expert.save_revision().publish()
    print(f"  {len(EXTERNAL_LINKS)} external links added to {expert.title}.")


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
            title="Explore All Experts",
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
    for i in range(20):
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
            bio=PROFILE_INTRO_BIO if slug == PROFILE_INTRO_EXPERT_SLUG else fake.paragraph(nb_sentences=3),
            location=country_codes[i % len(country_codes)],
            affiliation=fake.company(),
            blurb=fake.sentence(nb_words=12)[:115],
            quote=PROFILE_INTRO_QUOTE if slug == PROFILE_INTRO_EXPERT_SLUG else "",
            quote_attribution=PROFILE_INTRO_QUOTE_ATTRIBUTION if slug == PROFILE_INTRO_EXPERT_SLUG else "",
            seo_title=name,
            search_description=fake.sentence(nb_words=10).rstrip("."),
        )
        hub.add_child(instance=expert)

        if topics:
            assigned_topics = random.sample(topics, min(random.randint(1, 3), len(topics)))
            expert.topics.add(*assigned_topics)

        expert.save_revision().publish()
        print(f"  + Expert: {name}")
        expert_pages.append(expert)

    print(f"  {len(expert_pages)} Expert Profile Pages ready.")

    print("Linking curated articles to an Expert Profile Page...")
    ensure_expert_curated_articles(root, default_locale, topics, expert_pages, fake)

    print("Adding external links to an Expert Profile Page...")
    ensure_expert_external_links(default_locale)

    # Link featured experts to hub
    print("Linking featured experts to Expert Hub Page...")
    if not hub.featured_experts.exists():
        for i, expert in enumerate(expert_pages[:13]):
            ExpertHubFeaturedExpert.objects.create(hub_page=hub, expert=expert, sort_order=i)
        hub.save_revision().publish()
        print(f"  {min(13, len(expert_pages))} featured experts linked.")
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
    blurb = factory.LazyAttribute(lambda _: get_faker().sentence(nb_words=12)[:115])
    quote = factory.Faker("sentence", nb_words=8)
    quote_attribution = factory.Faker("name")
    seo_title = factory.Faker("sentence", nb_words=3)
    search_description = factory.Faker("sentence", nb_words=10)
