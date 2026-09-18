from wagtail import models as wagtail_models
from wagtail.models import Locale, Page

from foundation_cms.base.utils.helpers import get_faker, reseed
from foundation_cms.nothing_personal import models as np_models
from foundation_cms.nothing_personal.models.home_page import NothingPersonalFeaturedItem
from foundation_cms.nothing_personal.models.product_review_page import ProductMentioned
from foundation_cms.snippets.models import NewsletterSignup


def _simple_rich_body(fake, paragraphs=2):
    """Generate a simple rich text body with the specified number of paragraphs."""
    return [
        {"type": "rich_text", "value": "".join(f"<p>{fake.paragraph(nb_sentences=3)}</p>" for _ in range(paragraphs))}
    ]


def _product_review_sections(fake, newsletter_signup_id):
    """Build minimal, non-empty content for the product review page's StreamFields."""

    def rich(text):
        return f"<p>{text}</p>"

    return {
        "what_you_should_know_section": [
            {
                "type": "content",
                "value": {
                    "trust_default_settings": rich(fake.paragraph(nb_sentences=2)),
                    "what_personal_data_they_have": rich(fake.paragraph(nb_sentences=2)),
                    "track_record": rich(fake.paragraph(nb_sentences=2)),
                    "sells_or_shares_user_data": rich(fake.paragraph(nb_sentences=2)),
                },
            }
        ],
        "newsletter_signup_section": [{"type": "content", "value": {"newsletter_signup": newsletter_signup_id}}],
        "good_and_bad_section": [
            {
                "type": "content",
                "value": {
                    "the_good": rich(fake.paragraph(nb_sentences=2)),
                    "the_bad": rich(fake.paragraph(nb_sentences=2)),
                },
            }
        ],
        "reduce_your_risks_section": [{"type": "content", "value": {"content": rich(fake.paragraph(nb_sentences=2))}}],
        "bottom_line_section": [{"type": "content", "value": {"content": rich(fake.paragraph(nb_sentences=2))}}],
    }


def generate(seed=42, parent=None, slug="nothing-personal"):
    """
    Generate a Nothing Personal homepage with articles and a podcast.
    """
    reseed(seed)
    fake = get_faker()

    if parent is not None:
        root = parent
    else:
        # Use site's root page if available, else Wagtail root node (same pattern as gallery_hub)
        site = wagtail_models.Site.objects.filter(is_default_site=True).first()
        root = site.root_page if site else Page.get_first_root_node()

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
            tagline=f"<p>{fake.sentence(nb_words=8)}</p>",
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

    # Set hero item to the first article if available and not already set
    if article_pages and not home.hero_item_id:
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

    # Product collection (child of NP homepage)
    product_collection_slug = "nothing-personal-products"
    product_collection = np_models.NothingPersonalProductCollectionPage.objects.filter(
        slug=product_collection_slug, locale=locale
    ).first()
    if not product_collection:
        product_collection = np_models.NothingPersonalProductCollectionPage(
            title="Product Reviews",
            slug=product_collection_slug,
            locale=locale,
            seo_title="Nothing Personal Product Reviews",
            search_description=fake.sentence(nb_words=10),
            lede_text=fake.paragraph(nb_sentences=2),
        )
        home.add_child(instance=product_collection)
        product_collection.save_revision().publish()
        print("NothingPersonalProductCollectionPage created successfully.")
    else:
        print("Product collection already exists.")

    # Product reviews (children of NP homepage)
    existing_reviews_qs = np_models.NothingPersonalProductReviewPage.objects.descendant_of(home).filter(locale=locale)
    if existing_reviews_qs.exists():
        product_reviews = list(existing_reviews_qs)
        print(
            f"{len(product_reviews)} NothingPersonalProductReviewPage already exist - "
            "skipping factory product review creation."
        )
    else:
        newsletter_signup, _ = NewsletterSignup.objects.get_or_create(
            name="Nothing Personal Newsletter",
            locale=locale,
        )

        product_reviews = []
        for i in range(2):
            slug_i = f"np-product-review-{i + 1}"
            title = fake.sentence(nb_words=4).rstrip(".")
            review = np_models.NothingPersonalProductReviewPage(
                title=title,
                slug=slug_i,
                locale=locale,
                seo_title=title,
                search_description=fake.sentence(nb_words=10),
                lede_text=fake.paragraph(nb_sentences=2),
                byline=fake.name(),
                who_am_i=f"<p>{fake.paragraph(nb_sentences=2)}</p>",
                scoring=fake.random_element(["Great", "Average", "Needs Improvement", "Bad"]),
                reviewed=fake.date_this_year(),
                updated=fake.date_this_year(),
                hours_tested=str(fake.random_int(min=1, max=40)),
                type_of_testing="Hands-on review",
                **_product_review_sections(fake, newsletter_signup.pk),
            )
            home.add_child(instance=review)
            review.save_revision().publish()
            product_reviews.append(review)
        print(f"{len(product_reviews)} NothingPersonalProductReviewPage created.")

    # Cross-link product reviews via ProductMentioned
    if len(product_reviews) > 1 and not ProductMentioned.objects.filter(page__in=product_reviews).exists():
        for sort_order, review in enumerate(product_reviews):
            mentioned = product_reviews[(sort_order + 1) % len(product_reviews)]
            ProductMentioned.objects.create(page=review, mentioned_product=mentioned, sort_order=sort_order)
        print(f"  Linked {len(product_reviews)} product reviews via ProductMentioned.")

    print("Nothing Personal setup complete.")
    return home
