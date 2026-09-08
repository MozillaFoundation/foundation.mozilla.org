from wagtail import models as wagtail_models
from wagtail.models import Locale, Page

from foundation_cms.base.utils.helpers import get_faker, reseed
from foundation_cms.nothing_personal import models as np_models
from foundation_cms.nothing_personal.models.home_page import NothingPersonalFeaturedItem


def _simple_rich_body(fake, paragraphs=2):
    """Generate a simple rich text body with the specified number of paragraphs."""
    return [
        {"type": "rich_text", "value": "".join(f"<p>{fake.paragraph(nb_sentences=3)}</p>" for _ in range(paragraphs))}
    ]


def generate(seed=42, parent=None, slug="nothing-personal"):
    """
    Generate a Nothing Personal homepage with articles and a podcast.
    """
    reseed(seed)
    fake = get_faker()

    # Use site's root page if available, else Wagtail root node (same pattern as gallery_hub)
    site = wagtail_models.Site.objects.filter(is_default_site=True).first()
    root = site.root_page if site else Page.get_first_root_node()

    if parent is not None:
        root = parent

    locale = Locale.get_default()

    existing_home = np_models.NothingPersonalHomePage.objects.filter(slug=slug, locale=locale).first()
    if existing_home:
        home = existing_home
        print("Nothing Personal Home Page already exists.")
    else:
        home = np_models.NothingPersonalHomePage(
            title="Nothing Personal",
            slug=slug,
            locale=locale,
            seo_title="Nothing Personal",
            search_description=fake.sentence(nb_words=12),
            tagline=fake.sentence(nb_words=8),
            body=_simple_rich_body(fake, paragraphs=3),
        )
        root.add_child(instance=home)
        home.save_revision().publish()
        print("NothingPersonalHomePage created successfully.")

    # Article collection (child of NP homepage)
    collection_slug = "nothing-personal-articles"
    collection = np_models.NothingPersonalArticleCollectionPage.objects.filter(
        slug=collection_slug, locale=locale
    ).first()
    if not collection:
        collection = np_models.NothingPersonalArticleCollectionPage(
            title="Articles",
            slug=collection_slug,
            locale=locale,
            seo_title="Nothing Personal Articles",
            search_description=fake.sentence(nb_words=10),
            body=_simple_rich_body(fake, paragraphs=2),
        )
        home.add_child(instance=collection)
        collection.save_revision().publish()
        print("NothingPersonalArticleCollectionPage created successfully.")
    else:
        print("Article collection already exists.")

    # Articles (children of NP homepage)
    existing_articles_qs = np_models.NothingPersonalArticlePage.objects.descendant_of(home).filter(locale=locale)
    if existing_articles_qs.exists():
        article_pages = list(existing_articles_qs)
        print(f"{len(article_pages)} NothingPersonalArticlePage already exist - skipping factory article creation.")
    else:
        article_pages = []
        for i in range(3):
            slug_i = f"np-article-{i+1}"
            existing = np_models.NothingPersonalArticlePage.objects.filter(slug=slug_i, locale=locale).first()
            if existing:
                article_pages.append(existing)
                continue

            title = fake.sentence(nb_words=6).rstrip(".")
            article = np_models.NothingPersonalArticlePage(
                title=title,
                slug=slug_i,
                locale=locale,
                seo_title=title,
                search_description=fake.sentence(nb_words=10),
                lede_text=fake.paragraph(nb_sentences=2),
                body=_simple_rich_body(fake, paragraphs=3),
            )
            home.add_child(instance=article)
            article.save_revision().publish()
            article_pages.append(article)
        print(f"{len(article_pages)} NothingPersonalArticlePage created.")

    # Podcast (child of NP homepage)
    podcast_slug = "np-podcast-1"
    podcast = np_models.NothingPersonalPodcastPage.objects.filter(slug=podcast_slug, locale=locale).first()
    if not podcast:
        podcast = np_models.NothingPersonalPodcastPage(
            title="Nothing Personal Podcast",
            slug=podcast_slug,
            locale=locale,
            seo_title="Nothing Personal Podcast",
            search_description=fake.sentence(nb_words=10),
            hero_title=fake.sentence(nb_words=6),
            hero_description=fake.sentence(nb_words=10),
            body=_simple_rich_body(fake, paragraphs=2),
        )
        home.add_child(instance=podcast)
        podcast.save_revision().publish()
        print("NothingPersonalPodcastPage created successfully.")
    else:
        print("Podcast already exists.")

    # Set hero item to the first article if available
    if article_pages:
        home.hero_item = article_pages[0]
        home.save_revision().publish()
        print(f"hero_item set to: {article_pages[0].title}")

    # Keep featured items within the admin limit and avoid duplicating the hero.
    featured_pages = [page for page in article_pages + [podcast] if page != home.hero_item][:3]

    if featured_pages and not home.featured_items.exists():
        for sort_order, page in enumerate(featured_pages):
            NothingPersonalFeaturedItem.objects.create(
                home_page=home,
                page=page,
                sort_order=sort_order,
            )
        home.save_revision().publish()
        print(f"  {home.featured_items.count()} NothingPersonalFeaturedItem linked to home.")

    print("Nothing Personal setup complete.")
    return home
