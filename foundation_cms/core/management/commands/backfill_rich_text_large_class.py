import re

from django.apps import apps
from django.core.management.base import BaseCommand
from wagtail.fields import RichTextField, StreamField
from wagtail.models import RevisionMixin

CHUNK_SIZE = 500

LEGACY_CLASSES = {"tw-body-large", "body-text-large"}
NEW_CLASS = "rich-text-large"

# Anchored to class attributes so the legacy names are left alone in body copy. The
# optional backslash covers StreamField values stored as JSON strings in revision
# content, where the surrounding quotes arrive escaped.
CLASS_ATTR_RE = re.compile(r"""(class=)(\\?["'])(.*?)\2""")


def _rewrite_class_attr(match):
    prefix, quote, class_list = match.groups()
    tokens = class_list.split()
    if not any(token in LEGACY_CLASSES for token in tokens):
        return match.group(0)

    rewritten = []
    for token in tokens:
        token = NEW_CLASS if token in LEGACY_CLASSES else token
        if token not in rewritten:
            rewritten.append(token)
    return f"{prefix}{quote}{' '.join(rewritten)}{quote}"


def replace_legacy_classes(text):
    return CLASS_ATTR_RE.sub(_rewrite_class_attr, text)


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

            queryset = model._default_manager.all()
            if issubclass(model, RevisionMixin):
                # get_latest_revision() just reads this FK, so join it instead of
                # querying once per object.
                queryset = queryset.select_related("latest_revision")

            # Collect pks up front, as a finished query, instead of streaming rows with
            # .iterator() while we write to the same table from inside the loop.
            pks = list(model._default_manager.all().values_list("pk", flat=True))

            for start in range(0, len(pks), CHUNK_SIZE):
                chunk = pks[start : start + CHUNK_SIZE]

                for obj in queryset.filter(pk__in=chunk):
                    updates = {}

                    for field_name in richtext_fields:
                        value = getattr(obj, field_name)
                        if not value:
                            continue
                        new_value = replace_legacy_classes(value)
                        if new_value != value:
                            updates[field_name] = new_value

                    for field_name in streamfield_fields:
                        # raw_data is a RawDataView, not a list, so materialize it before
                        # rewriting or nothing matches and nothing compares unequal.
                        raw_data = list(getattr(obj, field_name).raw_data)
                        new_raw_data = rewrite_stream_data(raw_data)
                        if new_raw_data != raw_data:
                            updates[field_name] = new_raw_data

                    revision_changed = fix_latest_revision(obj, richtext_fields + streamfield_fields, dry_run)

                    if not updates and not revision_changed:
                        continue

                    total_objects += 1
                    total_fields += len(updates)
                    verb = "Would update" if dry_run else "Updating"
                    detail = ", ".join(updates) or "(latest revision only)"
                    self.stdout.write(f"{verb} {model._meta.label} pk={obj.pk}: {detail}")

                    if not dry_run and updates:
                        # Writes the column directly: Page.save() would run full_clean() and
                        # abort the run on any page that no longer validates, and assigning a
                        # StreamField drops blocks whose type is gone from the code.
                        model._default_manager.filter(pk=obj.pk).update(**updates)

        summary = (
            f"{'Would update' if dry_run else 'Updated'} {total_fields} field(s) across {total_objects} object(s)."
        )
        self.stdout.write(self.style.SUCCESS(summary))
