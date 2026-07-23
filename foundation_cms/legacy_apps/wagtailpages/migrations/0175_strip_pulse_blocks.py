"""Data migration: strip pulse-API-dependent blocks from page bodies and revisions.

Removes blocks of type profile_listing, profile_by_id, profile_directory,
pulse_listing, and tabbed_profile_directory from every affected page's live
body field as well as from stored Wagtail revisions. Runs inline with the
schema migration that drops PulseFilter/PulseFilterOption.

Why this exists: the next migration removes these block types from the
StreamField definitions. Once the definitions are gone, any leftover JSON
referencing them in the database would break the Wagtail admin editor for
those pages, and revisions containing them would be unsafe to restore. We
clean the data first, then let the schema migration drop the definitions.
"""

import json

from django.db import migrations

# Block types that depend on the (now-defunct) Mozilla Pulse API.
# These strings match the "type" key inside the StreamField JSON for each block.
BLOCK_TYPES_TO_REMOVE = {
    "profile_listing",
    "profile_by_id",
    "profile_directory",
    "pulse_listing",
    "tabbed_profile_directory",
}

# Every concrete page model whose `body` StreamField used to include at least
# one pulse block type. Listed as (app_label, model_name) so we can resolve
# them via apps.get_model() at migration time, which gives us the historical
# model — safe even if the Python class has been removed in this branch.
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
    """Recursively remove pulse blocks from a StreamField JSON list.

    A StreamField is stored as a list of dicts shaped like:
        [{"type": "...", "value": <anything>, "id": "..."}, ...]

    `value` can be:
      - a list  → another StreamBlock, recurse directly
      - a dict  → a StructBlock; its values may themselves contain streams
      - anything else (str, int, etc.) → leaf, leave alone

    Returns (new_stream, removed_count) so callers can detect whether the
    page actually needed saving (avoids no-op writes).
    """
    if not isinstance(stream, list):
        return stream, 0

    new_stream = []
    removed = 0
    for block in stream:
        # Defensive: bad JSON could theoretically contain non-dict entries.
        # Pass them through untouched rather than crashing the migration.
        if not isinstance(block, dict):
            new_stream.append(block)
            continue

        # Drop the block entirely if its type is one we're removing.
        if block.get("type") in BLOCK_TYPES_TO_REMOVE:
            removed += 1
            continue

        # Otherwise, the block stays — but we still need to walk into its
        # value in case a pulse block is nested inside a StreamBlock or
        # StructBlock (e.g. a column block containing a pulse listing).
        value = block.get("value")
        if isinstance(value, list):
            # StreamBlock: value is itself a list of child blocks.
            new_value, child_removed = _strip_blocks(value)
            removed += child_removed
            block = {**block, "value": new_value}
        elif isinstance(value, dict):
            # StructBlock: value is a dict of field_name -> field_value.
            # Any of those fields could be a nested stream (list).
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
    """Normalize a StreamField body to a Python list.

    Depending on Wagtail/Django version and how the field is accessed,
    `body` can come back as either an already-parsed Python list or a
    raw JSON string. We need to handle both, and preserve the original
    shape on the way back out (a string in, a string out) so we don't
    accidentally change the column's storage format.

    Returns (parsed_list_or_None, was_originally_a_string).
    """
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
    # return `page.body` StreamValue as a list.
    raw_data = getattr(value, "raw_data", None)
    if raw_data is not None:
        return list(raw_data), False
    return None, False


def strip_pulse_blocks(apps, schema_editor):
    """Two-phase cleanup: live page bodies first, then stored revisions."""

    # ── Phase 1: clean the live `body` field on every affected page row.
    # This is what readers see and what the Wagtail admin loads when an
    # editor opens the page. If we miss this, the editor will choke on
    # block types it no longer recognizes after migration 0176.
    for app_label, model_name in AFFECTED_PAGE_MODELS:
        try:
            Model = apps.get_model(app_label, model_name)
        except LookupError:
            # Model has been deleted in a later migration that ran first
            # (shouldn't happen given our dependencies, but be safe).
            continue

        for page in Model.objects.all().iterator():
            body = getattr(page, "body", None)
            stream, was_string = _as_list(body)
            if stream is None:
                # body was None, an unparseable string, or some other shape.
                # Nothing to clean.
                continue
            cleaned, removed = _strip_blocks(stream)
            if not removed:
                # No pulse blocks on this page — skip the write entirely.
                continue
            # Round-trip back into the original storage shape (string vs list)
            # so we don't change how the column is serialized.
            page.body = json.dumps(cleaned) if was_string else cleaned
            page.save(update_fields=["body"])

    # ── Phase 2: clean stored Wagtail revisions.
    # Every time an editor saves a draft or publishes, Wagtail snapshots
    # the page into wagtailcore_Revision.content as a JSON dict. If we
    # only cleaned phase 1, reverting to an old revision would re-introduce
    # pulse blocks into the live body and break the editor again.
    Revision = apps.get_model("wagtailcore", "Revision")
    ContentType = apps.get_model("contenttypes", "ContentType")

    # Limit the revision sweep to content types we actually care about.
    # Without this filter we'd iterate every Wagtail revision in the DB
    # (snippets, settings, every other page model), which is wasteful.
    content_type_ids = list(
        ContentType.objects.filter(
            app_label__in={app for app, _ in AFFECTED_PAGE_MODELS},
            model__in={name.lower() for _, name in AFFECTED_PAGE_MODELS},
        ).values_list("id", flat=True)
    )
    if not content_type_ids:
        # None of the affected models have a ContentType row yet —
        # nothing to do (this can happen on a brand-new DB).
        return

    revisions = Revision.objects.filter(content_type_id__in=content_type_ids)
    for revision in revisions.iterator():
        content = revision.content

        # `content` may be a Python dict (recent Wagtail) or a JSON string
        # (older revisions / certain DB drivers). Decode if needed and
        # remember the original shape so we can write it back the same way.
        was_string = False
        if isinstance(content, str):
            try:
                content = json.loads(content)
                was_string = True
            except (ValueError, TypeError):
                continue
        if not isinstance(content, dict) or "body" not in content:
            # Revision doesn't have a body key (e.g. for a non-page model
            # that snuck through, or an oddly-shaped revision). Skip.
            continue

        # The body inside revision content has the same dual list/string
        # shape as the live page.body, so reuse the same normalizer.
        stream, body_was_string = _as_list(content["body"])
        if stream is None:
            continue
        cleaned, removed = _strip_blocks(stream)
        if not removed:
            continue

        # Re-serialize body and the outer content dict back to their
        # original on-disk shape before writing.
        content["body"] = json.dumps(cleaned) if body_was_string else cleaned
        revision.content = json.dumps(content) if was_string else content
        revision.save(update_fields=["content"])


def noop(apps, schema_editor):
    """Reverse migration is intentionally a no-op.

    We can't reconstruct the removed pulse blocks from nothing, and the
    rest of the pulse stack (block classes, templates, JS, API) is being
    deleted in the same PR, so a "real" reverse would dangle anyway.
    Re-applying this migration after a rollback is safe — it just finds
    nothing to strip on the second pass.
    """
    pass


class Migration(migrations.Migration):

    # Depends on wagtailcore + contenttypes because we touch the Revision
    # and ContentType tables directly. The previous wagtailpages migration
    # is included for the usual sequential ordering.
    dependencies = [
        ("wagtailpages", "0174_create_legacy_content_editor_group"),
        ("contenttypes", "0001_initial"),
        ("wagtailcore", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(strip_pulse_blocks, noop),
    ]
