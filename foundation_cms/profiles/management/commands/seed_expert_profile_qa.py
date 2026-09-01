import uuid
from copy import deepcopy

from django.core.management.base import BaseCommand, CommandError
from wagtail.images import get_image_model

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.gallery_hub.models import ProjectPage
from foundation_cms.nothing_personal.models import NothingPersonalArticlePage
from foundation_cms.profiles.models import ExpertHubPage, ExpertProfilePage

QA_SLUG = "expert-profile-figma-qa"
QA_TITLE = "Expert Profile QA"
QA_IMAGELESS_ARTICLE_SLUG = "expert-profile-figma-qa-image-fallback"
QA_NAMESPACE = uuid.UUID("dd312649-b18b-4fb0-8b62-709934abce84")
QA_PROJECTS = [
    {
        "slug": "expert-profile-figma-qa-community-infrastructure",
        "title": "Community Infrastructure Initiative",
        "description": "A collaborative program supporting healthier, safer digital public spaces.",
        "image_title": "Internet Health",
        "image_alt": "Internet Health illustration",
        "topic": "Security",
    },
    {
        "slug": "expert-profile-figma-qa-digital-inclusion",
        "title": "Inclusive Technology Partnerships",
        "description": "Research and community partnerships advancing inclusive access to technology.",
        "image_title": "Digital Inclusion",
        "image_alt": "Digital Inclusion illustration",
        "topic": "Education",
    },
]
QA_MANUAL_PROJECT_IMAGE_TITLE = "Our global community at MozFest"
QA_BIO = (
    "<p>Alex Rivera works with communities to make technology more trustworthy, inclusive, and accountable. "
    "Their work brings together researchers, artists, organizers, and builders who want digital systems to "
    "serve people rather than extract from them. Alex has led international collaborations on responsible AI, "
    '<strong>public-interest technology</strong>, and the future of <a href="https://example.com/open-source">'
    "open source</a>.</p>"
    "<p>Across these projects, Alex focuses on turning complex technical questions into practical choices that "
    "communities can understand and influence. They regularly advise civic organizations, teach workshops, and "
    "publish accessible research about platform power and data governance. This intentionally long local-only "
    "biography exercises the six-hundred-character collapsed state, the accessible Show more and Show less "
    "controls, responsive headshot wrapping, and the full-content fallback when JavaScript is unavailable.</p>"
    "<p>Alex also works alongside local leaders to document how technology changes everyday civic life. These "
    "partnerships produce practical guides, public workshops, and shared research agendas that communities can "
    "adapt to their own priorities while keeping lived experience at the center of technical decisions.</p>"
    "<p>Outside formal projects, Alex mentors emerging practitioners and helps interdisciplinary teams build "
    "lasting relationships across regions. This final paragraph makes the expanded biography continue beneath "
    "the floated headshot while preserving the same rich-text paragraphs, links, and reading order.</p>"
)


def _id(label):
    return str(uuid.uuid5(QA_NAMESPACE, label))


def _validate_stream_payload(block, value, path="body"):
    child_blocks = getattr(block, "child_blocks", {})

    if isinstance(value, list):
        for index, item in enumerate(value):
            if not isinstance(item, dict) or "type" not in item:
                continue
            block_type = item["type"]
            if block_type not in child_blocks:
                raise CommandError(f'Unknown block type "{block_type}" at {path}[{index}].')
            _validate_stream_payload(
                child_blocks[block_type],
                item.get("value"),
                f"{path}[{index}].{block_type}",
            )
    elif isinstance(value, dict):
        for name, child_block in child_blocks.items():
            if name in value:
                _validate_stream_payload(child_block, value[name], f"{path}.{name}")


def _normalize_empty_manual_project_images(payload):
    """Adapt mixed optional ImageBlock values for Wagtail's bulk converter."""
    normalized = deepcopy(payload)
    for section in normalized:
        if section["type"] != "projects_section":
            continue
        for item in section["value"]["items"]:
            if item["type"] == "manual_project" and item["value"].get("image") is None:
                item["value"]["image"] = {
                    "image": None,
                    "alt_text": "",
                    "decorative": False,
                }
    return normalized


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


def _ensure_qa_project(source_project, image, definition):
    page = ProjectPage.objects.filter(
        slug=definition["slug"],
        locale=source_project.locale,
    ).first()
    created = page is None
    if created:
        page = ProjectPage(
            title=definition["title"],
            slug=definition["slug"],
            locale=source_project.locale,
        )

    field_values = {
        "title": definition["title"],
        "program_year": 2026,
        "lede_text": definition["description"],
        "displayed_hero_content": ProjectPage.HERO_CONTENT_IMAGE,
        "hero_image": image,
        "hero_image_alt_text": definition["image_alt"],
        "project_link": "https://example.com/projects/" + definition["slug"],
        "seo_title": definition["title"],
        "search_description": definition["description"],
    }
    changed = created or any(getattr(page, name) != value for name, value in field_values.items())
    for field_name, value in field_values.items():
        setattr(page, field_name, value)

    if created:
        source_project.get_parent().specific.add_child(instance=page)

    topic = Topic.objects.filter(name=definition["topic"]).first()
    if not topic:
        raise CommandError(f'Seed the standard redesign topic "{definition["topic"]}" first.')
    if list(page.topics.values_list("pk", flat=True)) != [topic.pk]:
        page.topics.set([topic])
        changed = True

    if changed or not page.live:
        page.save_revision().publish()

    return page


def _body(projects, articles, manual_project_image):
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
                "description": "A manually entered collaboration demonstrating the optional project image treatment.",
                "image": {
                    "image": manual_project_image.pk,
                    "alt_text": "People gathered at a Mozilla Festival community event",
                    "decorative": False,
                },
                "url": "https://example.com/projects/community-technology",
                "link_label": "Read the project story",
            },
            "id": _id("project-manual-image"),
        },
        {
            "type": "cms_project",
            "value": projects[1].pk,
            "id": _id("project-cms-2"),
        },
        {
            "type": "manual_project",
            "value": {
                "title": "Community Data Stewardship Lab",
                "description": "A text-only manual project with no artificial media space or placeholder.",
                "image": None,
                "url": "https://example.org/projects/community-data-stewardship",
                "link_label": "Explore the project",
            },
            "id": _id("project-manual-text-only-1"),
        },
        {
            "type": "manual_project",
            "value": {
                "title": "Open Source Governance Toolkit",
                "description": "Practical governance resources created with maintainers and community organizers.",
                "image": None,
                "url": "https://example.net/projects/open-source-governance",
                "link_label": "View the toolkit",
            },
            "id": _id("project-manual-text-only-2"),
        },
        {
            "type": "manual_project",
            "value": {
                "title": "Responsible AI Learning Network",
                "description": "A peer-learning program connecting researchers, educators, and civic groups.",
                "image": None,
                "url": "https://example.com/projects/responsible-ai-learning",
                "link_label": "Learn about the network",
            },
            "id": _id("project-manual-text-only-3"),
        },
    ]

    article_items = [
        {
            "type": "cms_article",
            "value": articles[0].pk,
            "id": _id("article-cms-1"),
        },
        {
            "type": "cms_article",
            "value": articles[1].pk,
            "id": _id("article-cms-2"),
        },
        {
            "type": "manual_article",
            "value": {
                "title": "Building public-interest technology together",
                "description": "A manual article entry with its source derived from the example URL.",
                "url": "https://example.org/insights/public-interest-technology",
            },
            "id": _id("article-manual-1"),
        },
        {
            "type": "manual_article",
            "value": {
                "title": "A field guide to accountable platforms",
                "description": "Practical questions for teams evaluating platform governance choices.",
                "url": "https://example.com/publications/accountable-platforms",
            },
            "id": _id("article-manual-2"),
        },
        {
            "type": "manual_article",
            "value": {
                "title": "Community-led approaches to data stewardship",
                "description": "Lessons from collaborative research and community governance programs.",
                "url": "https://example.org/research/community-data-stewardship",
            },
            "id": _id("article-manual-3"),
        },
        {
            "type": "manual_article",
            "value": {
                "title": "Maintaining healthy open-source communities",
                "description": "A concise publication about sustainable participation and shared ownership.",
                "url": "https://example.net/essays/healthy-open-source-communities",
            },
            "id": _id("article-manual-4"),
        },
        {
            "type": "manual_article",
            "value": {
                "title": "Designing public-interest technology programs",
                "description": "A program design note for institutions working with community partners.",
                "url": "https://example.com/notes/public-interest-programs",
            },
            "id": _id("article-manual-5"),
        },
    ]

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
                    {
                        "type": "link",
                        "value": {
                            "title": "Civic Technology Collaboration Prize",
                            "description": "Awarded for sustained cross-sector collaboration.",
                            "url": "https://example.org/awards/civic-collaboration",
                        },
                        "id": _id("award-civic-collaboration"),
                    },
                    {
                        "type": "link",
                        "value": {
                            "title": "Responsible Computing Fellowship",
                            "description": "A fellowship recognizing applied public-interest research.",
                            "url": "",
                        },
                        "id": _id("award-responsible-computing"),
                    },
                    {
                        "type": "link",
                        "value": {
                            "title": "Open Knowledge Community Honor",
                            "description": "Recognition for accessible research and shared learning.",
                            "url": "https://example.net/awards/open-knowledge",
                        },
                        "id": _id("award-open-knowledge"),
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
                    },
                    {
                        "type": "link",
                        "value": {
                            "title": "Building accountable technology ecosystems",
                            "description": "A conference session on governance, research, and community power.",
                            "url": "https://example.org/talks/accountable-ecosystems",
                        },
                        "id": _id("talk-accountable-ecosystems"),
                    },
                    {
                        "type": "link",
                        "value": {
                            "title": "Community research in practice",
                            "description": "An invited workshop recorded as a URL-less speaking engagement.",
                            "url": "",
                        },
                        "id": _id("talk-community-research"),
                    },
                ],
            },
            "id": _id("talks"),
        },
    ]


class Command(BaseCommand):
    help = "Create or update the deterministic local-only Expert Profile QA page."

    def handle(self, *args, **options):
        hub = ExpertHubPage.objects.live().order_by("pk").first()
        source_profile = ExpertProfilePage.objects.exclude(image=None).order_by("pk").first()
        source_project = (
            ProjectPage.objects.live().public().filter(locale=hub.locale).order_by("pk").first() if hub else None
        )
        articles = list(NothingPersonalArticlePage.objects.live().public().order_by("pk")[:2])
        image_model = get_image_model()
        project_images = {
            title: image_model.objects.filter(title=title).order_by("pk").first()
            for title in [
                *(project["image_title"] for project in QA_PROJECTS),
                QA_MANUAL_PROJECT_IMAGE_TITLE,
            ]
        }

        if not hub or not source_profile or not source_project or not articles or not all(project_images.values()):
            raise CommandError(
                "Seed the standard redesign data first; an Expert Hub, profile image, "
                "Gallery project, article, and maintained QA images are required."
            )

        projects = [
            _ensure_qa_project(source_project, project_images[definition["image_title"]], definition)
            for definition in QA_PROJECTS
        ]
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
        desired_body_payload = _body(projects, articles, project_images[QA_MANUAL_PROJECT_IMAGE_TITLE])
        _validate_stream_payload(page.body.stream_block, desired_body_payload)
        conversion_payload = _normalize_empty_manual_project_images(desired_body_payload)
        desired_body = page.body.stream_block.clean(page.body.stream_block.to_python(conversion_payload))
        desired_body_prep = page.body.stream_block.get_prep_value(desired_body)
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
        changed = changed or page.body.stream_block.get_prep_value(page.body) != desired_body_prep

        if not changed:
            self.stdout.write(self.style.SUCCESS(f"Unchanged {page.url}"))
            return

        for field_name, value in field_values.items():
            setattr(page, field_name, value)
        page.body = desired_body

        if created:
            hub.add_child(instance=page)

        page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} {page.url}"))
