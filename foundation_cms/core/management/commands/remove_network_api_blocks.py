"""
Django management command: remove_network_api_blocks
=====================================================
Removes network API-dependent blocks (profile_listing, profile_by_id,
profile_directory, pulse_listing) from all Wagtail pages across all locales, then republishes.

Usage:
    # Dry run (default) — shows what would be changed, no DB writes:
    python manage.py remove_network_api_blocks

    # Commit — removes blocks and republishes each affected page:
    python manage.py remove_network_api_blocks --commit

Place this file at:
    <your_app>/management/commands/remove_network_api_blocks.py
"""

import json

from django.apps import apps
from django.core.management.base import BaseCommand
from wagtail.models import Page

# ── Block types that reference the network/Pulse API ────────────────────────
BLOCK_TYPES_TO_REMOVE = {
    "profile_listing",
    "profile_by_id",
    "profile_directory",
    "pulse_listing",
    "tabbed_profile_directory",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def remove_blocks_from_stream(stream_data, block_types):
    """
    Recursively walk a StreamField list and remove any block whose 'type'
    is in block_types.  Returns (new_stream, count_removed).

    Handles:
      - Top-level stream blocks
      - Blocks nested inside other StreamBlocks (value is a list)
      - Blocks nested inside StructBlocks (value is a dict)
    """
    if not isinstance(stream_data, list):
        return stream_data, 0

    new_stream = []
    removed = 0

    for block in stream_data:
        if not isinstance(block, dict):
            new_stream.append(block)
            continue

        if block.get("type") in block_types:
            removed += 1
            continue  # drop this block entirely

        # Recurse into nested StreamBlocks (value is a list)
        value = block.get("value")
        if isinstance(value, list):
            new_value, child_removed = remove_blocks_from_stream(value, block_types)
            removed += child_removed
            block = {**block, "value": new_value}

        # Recurse into StructBlocks (value is a dict whose values may be streams)
        elif isinstance(value, dict):
            new_value = {}
            for key, sub_value in value.items():
                if isinstance(sub_value, list):
                    cleaned, child_removed = remove_blocks_from_stream(sub_value, block_types)
                    new_value[key] = cleaned
                    removed += child_removed
                else:
                    new_value[key] = sub_value
            block = {**block, "value": new_value}
            
        new_stream.append(block)

    return new_stream, removed


def get_stream_data(field_value):
    """
    Safely extract raw Python list from a Wagtail StreamValue (or a JSON string).
    Returns None if the field doesn't look like a StreamField.
    """
    # Already a list (stream_data attribute or raw JSON decode)
    if isinstance(field_value, list):
        return field_value

    # StreamValue exposes .stream_data (public API)
    if hasattr(field_value, "stream_data"):
        return field_value.stream_data

    # StreamValue may store raw data in _raw_data when stream_data is unavailable
    if hasattr(field_value, "_raw_data"):
        raw = field_value._raw_data
        if isinstance(raw, list):
            return raw

    # Fallback: try JSON decode — but never call str() on StreamValue objects,
    # as that triggers HTML rendering which requires a full request context.
    if not hasattr(field_value, "stream_block"):
        try:
            parsed = json.loads(str(field_value))
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass

    return None


def set_stream_data(page, field_name, new_data):
    """
    Write new_data (a Python list) back into the StreamField on the page instance.
    Wagtail accepts a JSON string assignment to a StreamField attribute.
    """
    setattr(page, field_name, json.dumps(new_data))


def get_streamfield_names(model):
    """Return names of StreamField fields on a model."""
    from wagtail.fields import StreamField
    return [
        field.name
        for field in model._meta.get_fields()
        if isinstance(field, StreamField)
    ]


# ── Command ───────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = (
        "Remove network API blocks (profile_listing, profile_by_id, "
        "profile_directory, pulse_listing) from all Wagtail pages across all locales and republish."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            action="store_true",
            default=False,
            help="Apply changes and republish pages. Omit for a dry run (default).",
        )
        parser.add_argument(
            "--locale",
            type=str,
            default=None,
            help="Restrict to a single locale code, e.g. --locale fr (default: all locales).",
        )

    def handle(self, *args, **options):
        commit = options["commit"]
        locale_filter = options.get("locale")

        if not commit:
            self.stdout.write(self.style.WARNING(
                "\n⚠️  DRY RUN — no changes will be written to the database.\n"
                "    Re-run with --commit to apply.\n"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                "\n🚨 COMMIT MODE — blocks will be removed and pages republished.\n"
            ))

        self.stdout.write(
            f"Targeting block types: {', '.join(sorted(BLOCK_TYPES_TO_REMOVE))}\n"
        )
        if locale_filter:
            self.stdout.write(f"Locale filter: {locale_filter}\n")
        self.stdout.write("─" * 70 + "\n")

        # Collect every concrete Page subclass that has at least one StreamField
        page_models = [
            model for model in apps.get_models()
            if issubclass(model, Page)
            and model is not Page
            and not model._meta.abstract
            and get_streamfield_names(model)
        ]

        if not page_models:
            self.stdout.write(self.style.WARNING("No page models with StreamFields found."))
            return

        total_pages_affected = 0
        total_blocks_removed = 0
        locales_seen = set()
        seen_ids = set()

        for model in page_models:
            stream_field_names = get_streamfield_names(model)
            qs = model.objects.filter(alias_of__isnull=True).select_related("locale")

            if locale_filter:
                qs = qs.filter(locale__language_code=locale_filter)

            for page in qs.iterator():
                if page.pk in seen_ids:
                    continue
                seen_ids.add(page.pk)

                page_blocks_removed = 0
                modified_fields = {}

                for field_name in stream_field_names:
                    field_value = getattr(page, field_name, None)
                    if field_value is None:
                        continue

                    stream_data = get_stream_data(field_value)
                    if stream_data is None:
                        continue

                    new_stream, removed = remove_blocks_from_stream(
                        stream_data, BLOCK_TYPES_TO_REMOVE
                    )

                    if removed:
                        page_blocks_removed += removed
                        modified_fields[field_name] = new_stream

                if not page_blocks_removed:
                    continue

                # Determine locale label
                locale_label = "en"
                if hasattr(page, "locale") and page.locale:
                    locale_label = page.locale.language_code
                locales_seen.add(locale_label)

                total_pages_affected += 1
                total_blocks_removed += page_blocks_removed

                live_str = "live" if page.live else "draft"
                self.stdout.write(
                    f"  [{locale_label:5}] [{live_str:5}]  "
                    f"ID={page.pk:<6}  "
                    f"blocks removed={page_blocks_removed}  "
                    f"\"{page.title}\""
                )
                for field_name, removed_count in {
                    k: sum(1 for b in get_stream_data(getattr(page, k)) or []
                           if b.get("type") in BLOCK_TYPES_TO_REMOVE)
                    for k in modified_fields
                }.items():
                    self.stdout.write(f"           └─ field '{field_name}'")

                if commit:
                    # Use page.specific so save_revision() is called on the
                    # correct subclass instance, not a generic parent type.
                    specific = page.specific
                    for field_name, new_data in modified_fields.items():
                        set_stream_data(specific, field_name, new_data)

                    try:
                        revision = specific.save_revision(log_action="wagtail.publish")
                        if specific.live:
                            revision.publish()
                            self.stdout.write(
                                self.style.SUCCESS(f"           ✓ republished")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"           ~ saved as draft (page was not live)")
                            )
                    except Exception as exc:
                        self.stdout.write(
                            self.style.ERROR(f"           ✗ ERROR saving page {page.pk}: {exc}")
                        )

        self.stdout.write("\n" + "─" * 70)
        self.stdout.write(
            f"Summary: {total_pages_affected} page(s) affected across "
            f"{len(locales_seen)} locale(s) — "
            f"{total_blocks_removed} block(s) {'removed' if commit else 'would be removed'}."
        )
        if locales_seen:
            self.stdout.write(f"Locales: {', '.join(sorted(locales_seen))}")

        if not commit and total_pages_affected:
            self.stdout.write(self.style.WARNING(
                "\nRun with --commit to apply these changes.\n"
            ))
