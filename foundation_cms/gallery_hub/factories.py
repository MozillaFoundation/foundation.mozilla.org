import random

from django.utils.text import slugify
from wagtail import models as wagtail_models

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.utils.helpers import reseed
from foundation_cms.gallery_hub.models import GalleryPage, ProjectPage
from foundation_cms.gallery_hub.models.gallery_page import FeaturedGalleryProject
from foundation_cms.gallery_hub.models.project_page import ProgramLabel

PROGRAM_LABEL_NAMES = [
    "AI & Democracy",
    "Data Futures Lab",
    "Digital Inclusion",
    "Emerging Technologies",
    "Health Data",
    "Internet Health",
    "Media Literacy",
    "MozFest",
    "Open Source",
    "Privacy Not Included",
    "Responsible AI",
    "Trustworthy AI",
    "Youth & Tech",
    "Digital Rights",
    "Misinformation",
    "Algorithmic Accountability",
    "Surveillance",
    "Encryption",
    "Net Neutrality",
    "Tech Policy",
    "Platform Governance",
    "Cybersecurity",
    "Human-Centered AI",
    "Bias & Fairness",
    "Community",
    "Research & Innovation",
    "Advocacy",
    "Education",
    "Global Programs",
    "Ethics in Tech",
]

TOPIC_NAMES = [
    "Artificial Intelligence",
    "Privacy",
    "Security",
    "Open Web",
    "Democracy",
    "Health",
    "Education",
    "Environment",
    "Human Rights",
    "Media",
]

PROJECT_TITLES = [
    "Protecting Privacy in the Age of AI",
    "Open Source Tools for Digital Rights",
    "Media Literacy Across Borders",
    "Algorithmic Accountability in Hiring",
    "Youth Voices in Tech Policy",
    "Surveillance and Democracy",
    "Community Networks in Rural Areas",
    "Health Data and Informed Consent",
    "Encryption for Activists",
    "Net Neutrality and the Global Web",
    "Bias in Facial Recognition Systems",
    "Platform Moderation and Free Speech",
    "AI Transparency Toolkit",
    "Cybersecurity for Civil Society",
    "Digital Inclusion in the Global South",
    "Human-Centered Design for Accessibility",
    "Misinformation and Election Integrity",
    "Ethics Review Boards in Tech",
    "Data Ownership and Indigenous Rights",
    "Open Standards for a Healthy Internet",
]


def generate(seed):
    reseed(seed)

    site = wagtail_models.Site.objects.filter(is_default_site=True).first()
    root = site.root_page if site else wagtail_models.Page.get_first_root_node()
    default_locale = wagtail_models.Locale.get_default()

    # --- 30 Program Labels ---
    print("Creating Program Labels...")
    labels = []
    for name in PROGRAM_LABEL_NAMES:
        label, created = ProgramLabel.objects.get_or_create(
            slug=slugify(name),
            defaults={"name": name},
        )
        if created:
            print(f"  + Program Label: {name}")
        labels.append(label)
    print(f"  {len(labels)} Program Labels ready.")

    # --- Topics (shared with other pages) ---
    topics = []
    for name in TOPIC_NAMES:
        topic, _ = Topic.objects.get_or_create(
            slug=slugify(name),
            defaults={"name": name},
        )
        topics.append(topic)

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
        )
        root.add_child(instance=gallery_page)
        gallery_page.save_revision().publish()
        print("  Gallery Hub Page created.")

    # --- 20 Project Pages (under gallery hub page) ---
    print("Creating Project Pages...")
    project_pages = []
    for i, title in enumerate(PROJECT_TITLES):
        slug = f"gallery-project-{i + 1}"
        existing = ProjectPage.objects.filter(slug=slug, locale=default_locale).first()
        if existing:
            project_pages.append(existing)
            continue

        project = ProjectPage(
            title=title,
            slug=slug,
            locale=default_locale,
            program_year=2018 + (i % 8),
            lede_text=f"An exploration of {title.lower()}.",
            seo_title=title,
            search_description=f"An exploration of {title.lower()}.",
        )
        gallery_page.add_child(instance=project)

        # Tags must be added after add_child so the page has a PK.
        assigned_labels = random.sample(labels, random.randint(1, 2))
        project.program_label.add(*assigned_labels)

        assigned_topics = random.sample(topics, random.randint(1, 2))
        project.topics.add(*assigned_topics)

        project.save_revision().publish()
        print(f"  + Project Page: {title}")
        project_pages.append(project)

    print(f"  {len(project_pages)} Project Pages ready.")

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
