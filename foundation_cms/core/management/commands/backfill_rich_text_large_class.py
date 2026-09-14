from django.apps import apps
from django.core.management.base import BaseCommand
from wagtail.fields import RichTextField, StreamField
from wagtail.models import RevisionMixin

# Order matters: the combined-class variants must be replaced before the
# single-class ones, otherwise a combined match leaves a stray "rich-text-large"
# plus a leftover single legacy class behind.
REPLACEMENTS = [
    ("tw-body-large body-text-large", "rich-text-large"),
    ("body-text-large tw-body-large", "rich-text-large"),
    ("tw-body-large", "rich-text-large"),
    ("body-text-large", "rich-text-large"),
]


def replace_legacy_classes(text):
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def rewrite_stream_data(data):
    if isinstance(data, str):
        return replace_legacy_classes(data)
    if isinstance(data, list):
        return [rewrite_stream_data(item) for item in data]
    if isinstance(data, dict):
        return {key: rewrite_stream_data(value) for key, value in data.items()}
    return data


def fix_latest_revision(obj, field_names, dry_run):
    """Apply the same replacements to the latest revision's stored content.

    Without this, publishing a pending draft revision would overwrite the
    live fields we just fixed with the old, unrevised revision content.
    """
    if not isinstance(obj, RevisionMixin):
        return False

    revision = obj.get_latest_revision()
    if revision is None:
        return False

    content = revision.content
    changed = False

    for field_name in field_names:
        if field_name not in content or not content[field_name]:
            continue
        new_value = rewrite_stream_data(content[field_name])
        if new_value != content[field_name]:
            content[field_name] = new_value
            changed = True

    if changed and not dry_run:
        revision.content = content
        revision.save(update_fields=["content"])

    return changed


class Command(BaseCommand):
    help = (
        "Backfill legacy rich text 'large' class names (tw-body-large, body-text-large) "
        "to rich-text-large across every RichTextField and StreamField in the project. "
        "See TP1-3685."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would change without saving anything.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        total_objects = 0
        total_fields = 0

        for model in apps.get_models():
            richtext_fields = [f.name for f in model._meta.get_fields() if isinstance(f, RichTextField)]
            streamfield_fields = [f.name for f in model._meta.get_fields() if isinstance(f, StreamField)]

            if not richtext_fields and not streamfield_fields:
                continue

            # Collect pks up front, as a finished query, instead of streaming rows with
            # .iterator() while we write to the same table from inside the loop.
            pks = list(model._default_manager.all().values_list("pk", flat=True))

            for pk in pks:
                obj = model._default_manager.get(pk=pk)
                changed_fields = []

                for field_name in richtext_fields:
                    value = getattr(obj, field_name)
                    if not value:
                        continue
                    new_value = replace_legacy_classes(value)
                    if new_value != value:
                        setattr(obj, field_name, new_value)
                        changed_fields.append(field_name)

                for field_name in streamfield_fields:
                    stream = getattr(obj, field_name)
                    raw_data = stream.raw_data
                    new_raw_data = rewrite_stream_data(raw_data)
                    if new_raw_data != raw_data:
                        setattr(obj, field_name, new_raw_data)
                        changed_fields.append(field_name)

                revision_changed = fix_latest_revision(obj, richtext_fields + streamfield_fields, dry_run)

                if not changed_fields and not revision_changed:
                    continue

                total_objects += 1
                total_fields += len(changed_fields)
                verb = "Would update" if dry_run else "Updating"
                detail = ", ".join(changed_fields) or "(latest revision only)"
                self.stdout.write(f"{verb} {model._meta.label} pk={obj.pk}: {detail}")

                if not dry_run and changed_fields:
                    obj.save(update_fields=changed_fields)

        summary = f"{'Would update' if dry_run else 'Updated'} {total_fields} field(s) across {total_objects} object(s)."
        self.stdout.write(self.style.SUCCESS(summary))
