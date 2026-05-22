"""Data migration: strip pulse-API-dependent blocks from page bodies and revisions.

Removes blocks of type profile_listing, profile_by_id, profile_directory,
pulse_listing, and tabbed_profile_directory from every affected page's live
body field as well as from stored Wagtail revisions. Runs inline with the
schema migration that drops PulseFilter/PulseFilterOption.
"""

import json

from django.db import migrations

BLOCK_TYPES_TO_REMOVE = {
    "profile_listing",
    "profile_by_id",
    "profile_directory",
    "pulse_listing",
    "tabbed_profile_directory",
}

AFFECTED_PAGE_MODELS = [
    ("wagtailpages", "BlogPage"),
    ("wagtailpages", "BuyersGuideArticlePage"),
    ("wagtailpages", "BuyersGuideCampaignPage"),
    ("wagtailpages", "ModularPage"),
    ("wagtailpages", "PrimaryPage"),
    ("mozfest", "MozfestPrimaryPage"),
    ("donate", "DonateHelpPage"),
]


def _strip_blocks(stream):
    if not isinstance(stream, list):
        return stream, 0
    new_stream = []
    removed = 0
    for block in stream:
        if not isinstance(block, dict):
            new_stream.append(block)
            continue
        if block.get("type") in BLOCK_TYPES_TO_REMOVE:
            removed += 1
            continue
        value = block.get("value")
        if isinstance(value, list):
            new_value, child_removed = _strip_blocks(value)
            removed += child_removed
            block = {**block, "value": new_value}
        elif isinstance(value, dict):
            new_value = {}
            for key, sub_value in value.items():
                if isinstance(sub_value, list):
                    cleaned, child_removed = _strip_blocks(sub_value)
                    new_value[key] = cleaned
                    removed += child_removed
                else:
                    new_value[key] = sub_value
            block = {**block, "value": new_value}
        new_stream.append(block)
    return new_stream, removed


def _as_list(value):
    if isinstance(value, list):
        return value, False
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError):
            return None, False
        if isinstance(parsed, list):
            return parsed, True
    return None, False


def strip_pulse_blocks(apps, schema_editor):
    for app_label, model_name in AFFECTED_PAGE_MODELS:
        try:
            Model = apps.get_model(app_label, model_name)
        except LookupError:
            continue

        for page in Model.objects.all().iterator():
            body = getattr(page, "body", None)
            stream, was_string = _as_list(body)
            if stream is None:
                continue
            cleaned, removed = _strip_blocks(stream)
            if not removed:
                continue
            page.body = json.dumps(cleaned) if was_string else cleaned
            page.save(update_fields=["body"])

    Revision = apps.get_model("wagtailcore", "Revision")
    ContentType = apps.get_model("contenttypes", "ContentType")

    content_type_ids = list(
        ContentType.objects.filter(
            app_label__in={app for app, _ in AFFECTED_PAGE_MODELS},
            model__in={name.lower() for _, name in AFFECTED_PAGE_MODELS},
        ).values_list("id", flat=True)
    )
    if not content_type_ids:
        return

    revisions = Revision.objects.filter(content_type_id__in=content_type_ids)
    for revision in revisions.iterator():
        content = revision.content
        was_string = False
        if isinstance(content, str):
            try:
                content = json.loads(content)
                was_string = True
            except (ValueError, TypeError):
                continue
        if not isinstance(content, dict) or "body" not in content:
            continue
        stream, body_was_string = _as_list(content["body"])
        if stream is None:
            continue
        cleaned, removed = _strip_blocks(stream)
        if not removed:
            continue
        content["body"] = json.dumps(cleaned) if body_was_string else cleaned
        revision.content = json.dumps(content) if was_string else content
        revision.save(update_fields=["content"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0174_create_legacy_content_editor_group"),
        ("contenttypes", "0001_initial"),
        ("wagtailcore", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(strip_pulse_blocks, noop),
    ]
