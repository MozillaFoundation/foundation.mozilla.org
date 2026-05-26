import random

from django.utils.text import slugify
from wagtail import models as wagtail_models
from wagtail.images import get_image_model

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.utils.helpers import get_faker, reseed
from foundation_cms.gallery_hub.models import GalleryPage, ProjectPage
from foundation_cms.gallery_hub.models.gallery_page import FeaturedGalleryProject
from foundation_cms.gallery_hub.models.project_page import (
    ProgramLabel,
    ProjectPageHeroMedia,
)
from foundation_cms.profiles.models import ExpertProfilePage, ExpertProfileSelectedProject

MULTI_HERO_PROJECT_INDEXES = {0, 3, 6}
ADDITIONAL_HERO_MEDIA_COUNT = 3
CURATED_PROJECT_COUNT = 3
CURATED_PROJECT_EXPERT_SLUG = "expert-1"


def ensure_project_hero_gallery_media(project, images, fake, project_index):
    if project_index not in MULTI_HERO_PROJECT_INDEXES or not images:
        return False

    existing_count = project.hero_gallery_media.count()
    if existing_count >= ADDITIONAL_HERO_MEDIA_COUNT:
        return False

    for sort_order in range(existing_count, ADDITIONAL_HERO_MEDIA_COUNT):
        ProjectPageHeroMedia.objects.create(
            page=project,
            locale=project.locale,
            sort_order=sort_order,
            media_type=ProjectPageHeroMedia.MEDIA_TYPE_IMAGE,
            image=random.choice(images),
            alt_text=fake.sentence(nb_words=8).rstrip("."),
            caption=fake.sentence(nb_words=6).rstrip("."),
        )

    return True


def ensure_expert_curated_projects(default_locale, project_pages):
    expert = ExpertProfilePage.objects.filter(
        slug=CURATED_PROJECT_EXPERT_SLUG,
        locale=default_locale,
    ).first()
    if not expert or expert.selected_projects.exists():
        return

    related_projects = [project for project in project_pages if project.expert_id == expert.id]
    filler_projects = [project for project in project_pages if project.expert_id != expert.id]
    curated_projects = (related_projects + filler_projects)[:CURATED_PROJECT_COUNT]

    for sort_order, project in enumerate(curated_projects):
        ExpertProfileSelectedProject.objects.create(
            page=expert,
            project=project,
            sort_order=sort_order,
        )

    expert.save_revision().publish()
    print(f"  {len(curated_projects)} curated projects linked to {expert.title}.")


def generate(seed):
    reseed(seed)
    fake = get_faker()

    site = wagtail_models.Site.objects.filter(is_default_site=True).first()
    root = site.root_page if site else wagtail_models.Page.get_first_root_node()
    default_locale = wagtail_models.Locale.get_default()

    # --- 30 Program Labels ---
    print("Creating Program Labels...")
    labels = []
    for _ in range(30):
        name = fake.sentence(nb_words=2).rstrip(".")
        label, created = ProgramLabel.objects.get_or_create(
            slug=slugify(name),
            defaults={"name": name},
        )
        labels.append(label)
    print(f"  {len(labels)} Program Labels ready.")

    # --- Topics (created earlier in load_redesign_data) ---
    topics = list(Topic.objects.all())

    # --- Images (created earlier in load_redesign_data) ---
    images = list(get_image_model().objects.all())

    # --- Experts (created earlier in load_redesign_data) ---
    experts = list(ExpertProfilePage.objects.live().filter(locale=default_locale))

    # --- 1 Gallery Hub Page (directly under site root) ---
    print("Creating Gallery Hub Page...")
    existing_gallery = GalleryPage.objects.filter(slug="gallery", locale=default_locale).first()
    if existing_gallery:
        gallery_page = existing_gallery
        print("  Gallery Hub Page already exists.")
    else:
        gallery_page = GalleryPage(
            title="Gallery",
            slug="gallery",
            locale=default_locale,
            seo_title="Gallery",
            search_description="Explore Mozilla Foundation gallery projects.",
            lede_text=fake.paragraph(nb_sentences=2),
        )
        root.add_child(instance=gallery_page)
        gallery_page.save_revision().publish()
        print("  Gallery Hub Page created.")

    # --- 20 Project Pages (under gallery hub page) ---
    print("Creating Project Pages...")
    project_pages = []
    for i in range(20):
        slug = f"gallery-project-{i + 1}"
        existing = ProjectPage.objects.filter(slug=slug, locale=default_locale).first()
        if existing:
            if ensure_project_hero_gallery_media(existing, images, fake, i):
                existing.save_revision().publish()
            project_pages.append(existing)
            continue

        title = fake.sentence(nb_words=6).rstrip(".")
        body_html = "".join(f"<p>{fake.paragraph(nb_sentences=4)}</p>" for _ in range(3))
        project = ProjectPage(
            title=title,
            slug=slug,
            locale=default_locale,
            program_year=2018 + (i % 8),
            lede_text=fake.paragraph(nb_sentences=2),
            seo_title=title,
            search_description=fake.sentence(nb_words=10).rstrip("."),
            hero_image=random.choice(images) if images else None,
            hero_image_alt_text=fake.sentence(nb_words=8).rstrip("."),
            expert=experts[i % len(experts)] if experts else None,
            project_link=fake.url(),
            body=[{"type": "rich_text", "value": body_html}],
        )
        gallery_page.add_child(instance=project)

        # Tags must be added after add_child so the page has a PK.
        assigned_labels = random.sample(labels, random.randint(1, 2))
        project.program_label.add(*assigned_labels)

        assigned_topics = random.sample(topics, random.randint(1, 2))
        project.topics.add(*assigned_topics)

        ensure_project_hero_gallery_media(project, images, fake, i)
        project.save_revision().publish()
        project_pages.append(project)

    print(f"  {len(project_pages)} Project Pages ready.")

    print("Linking curated projects to an Expert Profile Page...")
    ensure_expert_curated_projects(default_locale, project_pages)

    # --- Link all project pages as featured projects on the gallery hub page ---
    print("Linking featured projects to Gallery Hub Page...")
    if not gallery_page.featured_projects.exists():
        for i, project in enumerate(project_pages):
            FeaturedGalleryProject.objects.create(
                gallery_page=gallery_page,
                project=project,
                sort_order=i,
            )
        gallery_page.save_revision().publish()
        print(f"  {len(project_pages)} featured projects linked.")
    else:
        print("  Featured projects already linked.")

    print("Gallery Hub setup complete.")
    return gallery_page
