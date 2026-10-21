import json
import re
import uuid

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


def rewrite_json_text(text):
    """Rewrite a JSON document held in a text column.

    content_json nests JSON inside JSON, so the HTML arrives double-escaped and the
    class regex, which tolerates a single backslash, will not match the raw text.
    """
    data = json.loads(text)
    new_data = rewrite_stream_data(data)
    return text if new_data == data else json.dumps(new_data)


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

    def _fix_translation_memory(self, dry_run):
        """Rewrite wagtail-localize's rich text templates and source snapshots.

        Both are plain TextFields, so the RichTextField/StreamField scan never reaches
        them, and a stale template reintroduces the legacy class when a translation is
        republished.
        """
        try:
            Template = apps.get_model("wagtail_localize", "Template")
            TemplateSegment = apps.get_model("wagtail_localize", "TemplateSegment")
            TranslationSource = apps.get_model("wagtail_localize", "TranslationSource")
        except LookupError:
            return 0

        changed = 0
        template_pks = list(Template.objects.values_list("pk", flat=True))

        for start in range(0, len(template_pks), CHUNK_SIZE):
            for template in Template.objects.filter(pk__in=template_pks[start : start + CHUNK_SIZE]):
                new_template = replace_legacy_classes(template.template)
                if new_template == template.template:
                    continue

                # uuid is a content hash under a unique constraint, so it has to move with
                # the template. If a row already holds the rewritten content, repoint the
                # segments at it and drop this duplicate instead of colliding.
                namespace = uuid.uuid5(Template.BASE_UUID_NAMESPACE, template.template_format)
                new_uuid = uuid.uuid5(namespace, new_template)
                existing = Template.objects.filter(uuid=new_uuid).exclude(pk=template.pk).first()

                changed += 1
                if existing:
                    verb = "Would merge" if dry_run else "Merging"
                    self.stdout.write(f"{verb} wagtail_localize.Template pk={template.pk} into pk={existing.pk}")
                    if not dry_run:
                        TemplateSegment.objects.filter(template=template).update(template=existing)
                        template.delete()
                else:
                    verb = "Would update" if dry_run else "Updating"
                    self.stdout.write(f"{verb} wagtail_localize.Template pk={template.pk}")
                    if not dry_run:
                        Template.objects.filter(pk=template.pk).update(template=new_template, uuid=new_uuid)

        source_pks = list(TranslationSource.objects.values_list("pk", flat=True))

        for start in range(0, len(source_pks), CHUNK_SIZE):
            for source in TranslationSource.objects.filter(pk__in=source_pks[start : start + CHUNK_SIZE]):
                new_json = rewrite_json_text(source.content_json)
                if new_json == source.content_json:
                    continue

                changed += 1
                verb = "Would update" if dry_run else "Updating"
                self.stdout.write(f"{verb} wagtail_localize.TranslationSource pk={source.pk}")
                if not dry_run:
                    TranslationSource.objects.filter(pk=source.pk).update(content_json=new_json)

        return changed

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        total_objects = 0
        total_fields = 0

        for model in apps.get_models():
            # Only fields stored in this model's own table. A field declared on a concrete
            # ancestor is handled when that ancestor is iterated, whose queryset already
            # returns every descendant row, so skipping it here drops duplicate visits
            # without losing coverage.
            fields = [
                f
                for f in model._meta.get_fields()
                if isinstance(f, (RichTextField, StreamField)) and f.model._meta.db_table == model._meta.db_table
            ]
            richtext_fields = [f.name for f in fields if isinstance(f, RichTextField)]
            streamfield_fields = [f.name for f in fields if isinstance(f, StreamField)]

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

        translation_memory_changed = self._fix_translation_memory(dry_run)

        summary = (
            f"{'Would update' if dry_run else 'Updated'} {total_fields} field(s) across {total_objects} object(s)."
        )
        self.stdout.write(self.style.SUCCESS(summary))
        if translation_memory_changed:
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Would update' if dry_run else 'Updated'} {translation_memory_changed} "
                    "wagtail-localize translation memory row(s)."
                )
            )
