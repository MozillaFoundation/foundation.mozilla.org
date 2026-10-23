import json

from django.core.exceptions import FieldDoesNotExist
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

        try:
            Model._meta.get_field("body")
        except FieldDoesNotExist:
            continue

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
        ("core", "0093_reskin_quote_block"),
        ("campaigns", "0029_reskin_quote_block"),
        ("gallery_hub", "0014_reskin_quote_block"),
        ("nothing_personal", "0064_reskin_quote_block"),
        ("profiles", "0017_reskin_quote_block"),
        ("contenttypes", "0001_initial"),
        ("wagtailcore", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            strip_featured_card_blocks,
            migrations.RunPython.noop,
        ),
    ]
