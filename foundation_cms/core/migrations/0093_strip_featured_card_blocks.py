import json

from django.db import migrations

BLOCK_TYPE_TO_REMOVE = "featured_card_block"

AFFECTED_PAGE_MODELS = [
    ("core", "GeneralPage"),
    ("core", "HomePage"),
    ("campaigns", "CampaignPage"),
    ("gallery_hub", "GalleryPage"),
    ("gallery_hub", "ProjectPage"),
    ("nothing_personal", "NothingPersonalArticleCollectionPage"),
    ("nothing_personal", "NothingPersonalArticlePage"),
    ("nothing_personal", "NothingPersonalHomePage"),
    ("nothing_personal", "NothingPersonalPodcastPage"),
    ("nothing_personal", "NothingPersonalProductCollectionPage"),
    ("nothing_personal", "NothingPersonalProductReviewPage"),
    ("profiles", "ExpertDirectoryPage"),
    ("profiles", "ExpertHubPage"),
    ("profiles", "ExpertProfilePage"),
]


def _as_list(value):
    if isinstance(value, list):
        return value, False

    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            return None, False
        return (value, True) if isinstance(value, list) else (None, False)

    raw_data = getattr(value, "raw_data", None)
    if raw_data is not None:
        return list(raw_data), False

    return None, False


def _remove_featured_cards(value):
    stream, was_string = _as_list(value)
    if stream is None:
        return value, 0

    cleaned = [
        block for block in stream if not (isinstance(block, dict) and block.get("type") == BLOCK_TYPE_TO_REMOVE)
    ]
    removed = len(stream) - len(cleaned)

    if was_string and removed:
        return json.dumps(cleaned), removed
    return cleaned, removed


def strip_featured_card_blocks(apps, schema_editor):
    for app_label, model_name in AFFECTED_PAGE_MODELS:
        Model = apps.get_model(app_label, model_name)

        for page in Model.objects.all().iterator():
            cleaned, removed = _remove_featured_cards(page.body)
            if removed:
                page.body = cleaned
                page.save(update_fields=["body"])

    Revision = apps.get_model("wagtailcore", "Revision")
    ContentType = apps.get_model("contenttypes", "ContentType")

    content_type_ids = ContentType.objects.filter(
        app_label__in={app for app, _ in AFFECTED_PAGE_MODELS},
        model__in={name.lower() for _, name in AFFECTED_PAGE_MODELS},
    ).values_list("id", flat=True)

    for revision in Revision.objects.filter(content_type_id__in=content_type_ids).iterator():
        content = revision.content
        content_was_string = isinstance(content, str)

        if content_was_string:
            try:
                content = json.loads(content)
            except (TypeError, ValueError):
                continue

        if not isinstance(content, dict) or "body" not in content:
            continue

        cleaned, removed = _remove_featured_cards(content["body"])
        if not removed:
            continue

        content["body"] = cleaned
        revision.content = json.dumps(content) if content_was_string else content
        revision.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0092_alter_generalpage_body_alter_homepage_body"),
        ("campaigns", "0028_alter_campaignpage_body"),
        ("gallery_hub", "0013_alter_projectpage_body"),
        ("nothing_personal", "0063_alter_nothingpersonalarticlecollectionpage_body_and_more"),
        ("profiles", "0016_alter_expertdirectorypage_body_and_more"),
        ("contenttypes", "0001_initial"),
        ("wagtailcore", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            strip_featured_card_blocks,
            migrations.RunPython.noop,
        ),
    ]
