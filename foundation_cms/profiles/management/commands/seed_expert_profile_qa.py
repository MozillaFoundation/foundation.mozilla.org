import uuid

from django.core.management.base import BaseCommand, CommandError

from foundation_cms.base.utils.helpers import to_streamfield_value
from foundation_cms.gallery_hub.models import ProjectPage
from foundation_cms.nothing_personal.models import NothingPersonalArticlePage
from foundation_cms.profiles.models import ExpertHubPage, ExpertProfilePage

QA_SLUG = "expert-profile-figma-qa"
QA_TITLE = "Expert Profile Figma QA"
QA_IMAGELESS_ARTICLE_SLUG = "expert-profile-figma-qa-image-fallback"
QA_NAMESPACE = uuid.UUID("dd312649-b18b-4fb0-8b62-709934abce84")
QA_BIO = (
    "<p>Alex Rivera works with communities to make technology more trustworthy, inclusive, and accountable. "
    "Their work brings together researchers, artists, organizers, and builders who want digital systems to "
    "serve people rather than extract from them. Alex has led international collaborations on responsible AI, "
    "public-interest technology, and the future of open source.</p>"
    "<p>Across these projects, Alex focuses on turning complex technical questions into practical choices that "
    "communities can understand and influence. They regularly advise civic organizations, teach workshops, and "
    "publish accessible research about platform power and data governance. This intentionally long local-only "
    "biography exercises the six-hundred-character collapsed state, the accessible Show more and Show less "
    "controls, responsive headshot wrapping, and the full-content fallback when JavaScript is unavailable.</p>"
)


def _id(label):
    return str(uuid.uuid5(QA_NAMESPACE, label))


def _ensure_imageless_article(source_article):
    page = NothingPersonalArticlePage.objects.filter(
        slug=QA_IMAGELESS_ARTICLE_SLUG,
        locale=source_article.locale,
    ).first()
    created = page is None
    if created:
        page = NothingPersonalArticlePage(
            title="Article without a listing image",
            slug=QA_IMAGELESS_ARTICLE_SLUG,
            locale=source_article.locale,
        )

    field_values = {
        "title": "Article without a listing image",
        "theme": "nothing_personal",
        "displayed_hero_content": "",
        "hero_image": None,
        "hero_image_alt_text": "",
        "lede_text": "A deterministic local-only article that exercises the neutral image fallback.",
        "search_image": None,
        "seo_title": "Article without a listing image",
        "search_description": "A deterministic local-only article that exercises the neutral image fallback.",
    }
    changed = created or any(getattr(page, name) != value for name, value in field_values.items())
    for field_name, value in field_values.items():
        setattr(page, field_name, value)

    if created:
        source_article.get_parent().specific.add_child(instance=page)

    if changed or not page.live:
        page.save_revision().publish()

    return page


def _body(projects, articles):
    project_items = [
        {
            "type": "cms_project",
            "value": projects[0].pk,
            "id": _id("project-cms-1"),
        },
        {
            "type": "manual_project",
            "value": {
                "title": "Community Technology Fellowship",
                "description": "A manually entered collaboration demonstrating the text-first project card.",
                "url": "https://example.com/projects/community-technology",
                "link_label": "Read the project story",
            },
            "id": _id("project-manual"),
        },
    ]
    if len(projects) > 1:
        project_items.append(
            {
                "type": "cms_project",
                "value": projects[1].pk,
                "id": _id("project-cms-2"),
            }
        )

    article_items = [
        {
            "type": "cms_article",
            "value": articles[0].pk,
            "id": _id("article-cms-1"),
        },
        {
            "type": "manual_article",
            "value": {
                "title": "Building public-interest technology together",
                "description": "A manual article entry with its source derived from the example URL.",
                "url": "https://example.org/insights/public-interest-technology",
            },
            "id": _id("article-manual"),
        },
    ]
    if len(articles) > 1:
        article_items.append(
            {
                "type": "cms_article",
                "value": articles[1].pk,
                "id": _id("article-cms-2"),
            }
        )

    return [
        {
            "type": "quote",
            "value": {
                "quote": "Technology should expand the choices communities can make together.",
                "attribution": "Alex Rivera",
            },
            "id": _id("quote"),
        },
        {
            "type": "projects_section",
            "value": {"source": "curated", "items": project_items},
            "id": _id("projects"),
        },
        {
            "type": "articles_section",
            "value": {"items": article_items},
            "id": _id("articles"),
        },
        {
            "type": "link_section",
            "value": {
                "heading": "Awards & Recognition",
                "rows": [
                    {
                        "type": "link",
                        "value": {
                            "title": "Open Technology Leadership Award",
                            "description": "Recognition for community-centered technology work.",
                            "url": "https://example.com/awards/open-technology",
                        },
                        "id": _id("award-linked"),
                    },
                    {
                        "type": "link",
                        "value": {
                            "title": "Community Research Fellowship",
                            "description": "A URL-less row demonstrating non-linked content.",
                            "url": "",
                        },
                        "id": _id("award-unlinked"),
                    },
                ],
            },
            "id": _id("awards"),
        },
        {
            "type": "link_section",
            "value": {
                "heading": "Featured Talks",
                "rows": [
                    {
                        "type": "link",
                        "value": {
                            "title": "Designing technology with communities",
                            "description": "A representative external talk link.",
                            "url": "https://example.net/talks/designing-with-communities",
                        },
                        "id": _id("talk"),
                    }
                ],
            },
            "id": _id("talks"),
        },
    ]


class Command(BaseCommand):
    help = "Create or update the deterministic local-only Expert Profile Figma QA page."

    def handle(self, *args, **options):
        hub = ExpertHubPage.objects.live().order_by("pk").first()
        source_profile = ExpertProfilePage.objects.exclude(image=None).order_by("pk").first()
        projects = list(ProjectPage.objects.live().public().order_by("pk")[:2])
        articles = list(NothingPersonalArticlePage.objects.live().public().order_by("pk")[:2])

        if not hub or not source_profile or not projects or not articles:
            raise CommandError(
                "Seed the standard redesign data first; an Expert Hub, profile image, "
                "project, and article are required."
            )

        articles = [articles[0], _ensure_imageless_article(articles[0])]

        page = ExpertProfilePage.objects.filter(slug=QA_SLUG, locale=hub.locale).first()
        created = page is None
        if created:
            page = ExpertProfilePage(title=QA_TITLE, slug=QA_SLUG, locale=hub.locale)

        field_values = {
            "title": QA_TITLE,
            "role": "Public-interest technology researcher",
            "location": "US",
            "affiliation": "Mozilla Foundation QA",
            "bio": QA_BIO,
            "image": source_profile.image,
            "blurb": "Local-only profile page for complete TP1-4209 visual and editor QA.",
            "linkedin_url": "https://www.linkedin.com/in/example-profile",
            "bluesky_url": "https://bsky.app/profile/example.org",
            "facebook_url": "https://www.facebook.com/example.profile",
            "instagram_url": "https://www.instagram.com/example.profile/",
            "tiktok_url": "https://www.tiktok.com/@example.profile",
            "seo_title": QA_TITLE,
            "search_description": "Local-only Expert Profile Page QA fixture.",
        }
        desired_body = _body(projects, articles)
        changed = created
        for field_name, value in field_values.items():
            current_value = getattr(page, field_name)
            if field_name == "image":
                current_value = current_value.pk if current_value else None
                value = value.pk
            elif field_name == "location":
                current_value = str(current_value)
            if current_value != value:
                changed = True
                break
        changed = changed or list(page.body.raw_data) != desired_body

        if not changed:
            self.stdout.write(self.style.SUCCESS(f"Unchanged {page.url}"))
            return

        for field_name, value in field_values.items():
            setattr(page, field_name, value)
        page.body = to_streamfield_value(desired_body, stream_block=page.body.stream_block)

        if created:
            hub.add_child(instance=page)

        page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} {page.url}"))
