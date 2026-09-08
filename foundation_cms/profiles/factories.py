import random
import uuid
from datetime import datetime, timezone

import factory
import wagtail_factories
from wagtail import models as wagtail_models
from wagtail.images import get_image_model

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.utils.helpers import get_faker, reseed, to_streamfield_value
from foundation_cms.blocks.factories import QuoteBlockFactory
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
)
from foundation_cms.nothing_personal.models.home_page import NothingPersonalFeaturedItem
from foundation_cms.profiles import expert_profile_data as profile_data
from foundation_cms.profiles.blocks import (
    ArticlesSectionBlock,
    LinkRowBlock,
    LinkSectionBlock,
    ManualArticleBlock,
    ManualProjectBlock,
    ProjectsSectionBlock,
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
CURATED_ARTICLE_EXPERT_SLUG = profile_data.EXPERT_SLUG
CURATED_ARTICLE_FIRST_PUBLISHED_AT = datetime(2025, 1, 1, tzinfo=timezone.utc)
NOTHING_PERSONAL_FEATURED_ITEM_COUNT = 2
NOTHING_PERSONAL_FEATURED_ITEM_LIMIT = 3
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
PROFILE_INTRO_EXPERT_SLUG = profile_data.EXPERT_SLUG
PROFILE_INTRO_BIO = profile_data.BIO
PROFILE_INTRO_QUOTE = "Technology should expand the choices communities can make together."
PROFILE_INTRO_QUOTE_ATTRIBUTION = "Priya Goswami"
EXTERNAL_LINK_EXPERT_SLUG = profile_data.EXPERT_SLUG
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


class ManualProjectBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ManualProjectBlock

    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=2)
    url = factory.Faker("url")
    link_label = "Learn more"


class ProjectsSectionBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ProjectsSectionBlock

    source = ProjectsSectionBlock.SOURCE_CURATED
    items: list = []


class ManualArticleBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ManualArticleBlock

    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=2)
    url = factory.Faker("url")


class ArticlesSectionBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = ArticlesSectionBlock

    items: list = []


class LinkRowBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = LinkRowBlock

    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=1)
    url = ""


class LinkSectionBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = LinkSectionBlock

    heading = factory.Faker("sentence", nb_words=3)
    rows: list = []


def _body_item(block_type, value, item_id, id_factory):
    return {"type": block_type, "value": value, "id": id_factory(block_type, item_id)}


def build_expert_profile_link_sections(id_factory):
    return [
        _body_item(
            "link_section",
            dict(
                LinkSectionBlockFactory(
                    heading=section["heading"],
                    rows=[
                        _body_item(
                            "link",
                            dict(
                                LinkRowBlockFactory(
                                    title=row["title"],
                                    description=row["description"],
                                    url=row["url"],
                                )
                            ),
                            row["id"],
                            id_factory,
                        )
                        for row in section["rows"]
                    ],
                )
            ),
            section["id"],
            id_factory,
        )
        for section in profile_data.LINK_SECTIONS
    ]


def build_expert_profile_body(projects, articles, id_factory):
    manual_projects = [
        _body_item(
            "manual_project",
            dict(
                ManualProjectBlockFactory(
                    title=project["title"],
                    description=project["description"],
                    url=project["url"],
                    link_label=project["link_label"],
                )
            ),
            project["id"],
            id_factory,
        )
        for project in profile_data.MANUAL_PROJECTS
    ]
    project_items = [
        _body_item("cms_project", projects[0].pk, "project-cms-1", id_factory),
        manual_projects[0],
        _body_item("cms_project", projects[1].pk, "project-cms-2", id_factory),
        *manual_projects[1:],
    ]
    article_items = [
        _body_item("cms_article", articles[0].pk, "article-cms-1", id_factory),
        _body_item("cms_article", articles[1].pk, "article-cms-2", id_factory),
        *[
            _body_item(
                "manual_article",
                dict(
                    ManualArticleBlockFactory(
                        title=article["title"],
                        description=article["description"],
                        url=article["url"],
                    )
                ),
                article["id"],
                id_factory,
            )
            for article in profile_data.MANUAL_ARTICLES
        ],
    ]

    return [
        _body_item(
            "quote",
            dict(
                QuoteBlockFactory(
                    quote="Technology should expand the choices communities can make together.",
                    attribution="Priya Goswami",
                )
            ),
            None,
            id_factory,
        ),
        _body_item(
            "projects_section",
            dict(ProjectsSectionBlockFactory(source="curated", items=project_items)),
            None,
            id_factory,
        ),
        _body_item(
            "articles_section",
            dict(ArticlesSectionBlockFactory(items=article_items)),
            None,
            id_factory,
        ),
        *build_expert_profile_link_sections(id_factory),
    ]


SEED_BODY_NAMESPACE = uuid.UUID("a3ffb092-3e58-462e-97ed-72ddc8f68d65")


def _seed_body_id(page, block_type, item_id=None):
    identity = f"profiles.seed:{page.pk}:{block_type}"
    if item_id is not None:
        identity = f"{identity}:{item_id}"
    return str(uuid.uuid5(SEED_BODY_NAMESPACE, identity))


def _ensure_seeded_body_block(page, block, unique_by_type=False):
    body = list(page.body.raw_data)
    if any(
        existing.get("id") == block["id"] or (unique_by_type and existing.get("type") == block["type"])
        for existing in body
    ):
        return False

    body.append(block)
    page.body = to_streamfield_value(body, stream_block=page.body.stream_block)
    page.save_revision().publish()
    return True


def ensure_expert_intro_quote(expert):
    if expert.slug != PROFILE_INTRO_EXPERT_SLUG:
        return

    _ensure_seeded_body_block(
        expert,
        {
            "type": "quote",
            "value": {
                "quote": PROFILE_INTRO_QUOTE,
                "attribution": PROFILE_INTRO_QUOTE_ATTRIBUTION,
            },
            "id": _seed_body_id(expert, "quote"),
        },
        unique_by_type=True,
    )


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
    if not expert:
        return

    np_home = ensure_nothing_personal_home(root, default_locale)
    model_instance = NothingPersonalArticlePage()
    articles = []

    for i in range(CURATED_ARTICLE_COUNT):
        slug = f"expert-profile-article-{i + 1}"
        article = NothingPersonalArticlePage.objects.filter(slug=slug, locale=default_locale).first()
        is_imageless = i == CURATED_ARTICLE_COUNT - 1

        if not article:
            title = fake.sentence(nb_words=5).rstrip(".")
            lede_text = CURATED_ARTICLE_DESCRIPTIONS[i % len(CURATED_ARTICLE_DESCRIPTIONS)]
            body_html = f"<p>{fake.paragraph(nb_sentences=4)}</p>"
            article = NothingPersonalArticlePage(
                title=title,
                slug=slug,
                theme="nothing_personal",
                locale=default_locale,
                first_published_at=CURATED_ARTICLE_FIRST_PUBLISHED_AT,
                displayed_hero_content=("" if is_imageless else NothingPersonalArticlePage.HERO_CONTENT_IMAGE),
                hero_image=None if is_imageless else ImageFactory(),
                hero_image_alt_text="" if is_imageless else fake.sentence(nb_words=8).rstrip("."),
                lede_text=lede_text,
                search_image=None if is_imageless else ImageFactory(),
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

        elif is_imageless and (
            article.displayed_hero_content
            or article.hero_image_id
            or article.hero_image_alt_text
            or article.search_image_id
        ):
            article.displayed_hero_content = ""
            article.hero_image = None
            article.hero_image_alt_text = ""
            article.search_image = None
            article.save_revision().publish()

        articles.append(article)

    selected_articles = list(expert.selected_articles.order_by("sort_order", "pk"))
    selected_article_ids = {selection.article_id for selection in selected_articles if selection.article_id}
    next_selected_sort_order = (
        max(
            (selection.sort_order if selection.sort_order is not None else -1 for selection in selected_articles),
            default=-1,
        )
        + 1
    )
    expert_changed = False

    for article in articles:
        if article.pk in selected_article_ids:
            continue

        ExpertProfileSelectedArticle.objects.create(
            page=expert,
            article=article,
            sort_order=next_selected_sort_order,
        )
        selected_article_ids.add(article.pk)
        next_selected_sort_order += 1
        expert_changed = True

    if expert_changed:
        expert.save_revision().publish()
        print(f"  {len(articles)} curated articles linked to {expert.title}.")

    _ensure_seeded_body_block(
        expert,
        {
            "type": "articles_section",
            "value": {
                "items": [
                    {
                        "type": "cms_article",
                        "value": article.pk,
                        "id": _seed_body_id(expert, "article", article.pk),
                    }
                    for article in articles
                ]
            },
            "id": _seed_body_id(expert, "articles_section"),
        },
        unique_by_type=True,
    )

    featured_items = list(np_home.featured_items.order_by("sort_order", "pk"))
    featured_page_ids = {item.page_id for item in featured_items if item.page_id}
    home_changed = False
    if not np_home.hero_item_id:
        hero_item = next((article for article in articles if article.pk not in featured_page_ids), None)
        if hero_item:
            np_home.hero_item = hero_item
            home_changed = True

    hero_item_id = np_home.hero_item_id
    useful_featured_page_ids = {page_id for page_id in featured_page_ids if page_id != hero_item_id}
    empty_featured_items = [item for item in featured_items if not item.page_id]
    next_featured_sort_order = (
        max(
            (item.sort_order if item.sort_order is not None else -1 for item in featured_items),
            default=-1,
        )
        + 1
    )

    for article in articles:
        if len(useful_featured_page_ids) >= NOTHING_PERSONAL_FEATURED_ITEM_COUNT:
            break
        if article.pk == hero_item_id or article.pk in featured_page_ids:
            continue

        if empty_featured_items:
            featured_item = empty_featured_items.pop(0)
            featured_item.page = article
            featured_item.save(update_fields=["page"])
        elif len(featured_items) < NOTHING_PERSONAL_FEATURED_ITEM_LIMIT:
            featured_item = NothingPersonalFeaturedItem.objects.create(
                home_page=np_home,
                page=article,
                sort_order=next_featured_sort_order,
            )
            featured_items.append(featured_item)
            next_featured_sort_order += 1
        else:
            break

        featured_page_ids.add(article.pk)
        useful_featured_page_ids.add(article.pk)
        home_changed = True

    if home_changed:
        np_home.save_revision().publish()


def ensure_expert_external_links(default_locale):
    expert = ExpertProfilePage.objects.filter(
        slug=EXTERNAL_LINK_EXPERT_SLUG,
        locale=default_locale,
    ).first()
    if not expert:
        return

    if not expert.external_links.exists():
        for sort_order, link in enumerate(EXTERNAL_LINKS):
            ExpertExternalLink.objects.create(
                page=expert,
                sort_order=sort_order,
                **link,
            )

        expert.save_revision().publish()
        print(f"  {len(EXTERNAL_LINKS)} external links added to {expert.title}.")

    for block in build_expert_profile_link_sections(
        lambda block_type, item_id=None: _seed_body_id(expert, block_type, item_id)
    ):
        _ensure_seeded_body_block(expert, block)


def ensure_expert_profile_composition(default_locale, projects):
    """Keep the representative seeded profile complete and deterministic."""
    expert = ExpertProfilePage.objects.filter(
        slug=profile_data.EXPERT_SLUG,
        locale=default_locale,
    ).first()
    articles = list(
        NothingPersonalArticlePage.objects.live()
        .public()
        .filter(locale=default_locale, slug__startswith="expert-profile-article-")
        .order_by("slug")
    )
    profile_image = get_image_model().objects.filter(title=profile_data.PROFILE_IMAGE_TITLE).order_by("pk").first()

    if not expert or len(projects) < 2 or len(articles) < 2 or not profile_image:
        raise RuntimeError("Generate the standard profile, Gallery projects, articles, and images first.")

    selected_articles = [articles[0], articles[-1]]
    desired_body_payload = build_expert_profile_body(
        projects[:2],
        selected_articles,
        lambda block_type, item_id=None: _seed_body_id(expert, block_type, item_id),
    )
    desired_body = expert.body.stream_block.clean(expert.body.stream_block.to_python(desired_body_payload))
    desired_body_prep = expert.body.stream_block.get_prep_value(desired_body)
    field_values = {**profile_data.PROFILE_FIELDS, "image": profile_image}

    changed = expert.body.stream_block.get_prep_value(expert.body) != desired_body_prep
    for field_name, value in field_values.items():
        current_value = getattr(expert, field_name)
        if field_name == "image":
            current_value = current_value.pk if current_value else None
            value = value.pk
        elif field_name == "location":
            current_value = str(current_value)
        if current_value != value:
            changed = True
            break

    if not changed:
        return expert

    for field_name, value in field_values.items():
        setattr(expert, field_name, value)
    expert.body = desired_body
    expert.save_revision().publish()
    return expert


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

    for expert in expert_pages:
        ensure_expert_intro_quote(expert)

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
