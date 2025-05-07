from collections import Counter

from django.core.management.base import BaseCommand
from django.db import connection
from wagtail.images.models import Image as LegacyImage

from networkapi.images.models import FoundationCustomImage

BATCH_SIZE = 1000


class Command(BaseCommand):
    help = "Migrate legacy wagtailimages.Image objects to FoundationCustomImage (DB-only, no file access)"

    def handle(self, *args, **options):
        self.stdout.write("Starting image migration...")

        migrated = 0
        skipped = 0
        tagged = 0
        tag_counter = Counter()

        existing_files = set(FoundationCustomImage.objects.values_list("file", flat=True))

        legacy_qs = LegacyImage.objects.select_related("collection").only(
            "id",
            "title",
            "file",
            "width",
            "height",
            "collection",
            "created_at",
            "focal_point_x",
            "focal_point_y",
            "focal_point_width",
            "focal_point_height",
        )

        buffer = []

        for legacy in legacy_qs.iterator(chunk_size=500):
            if legacy.file in existing_files:
                skipped += 1
                continue

            new_img = FoundationCustomImage(
                id=legacy.id,
                title=legacy.title,
                file=legacy.file,
                width=legacy.width,
                height=legacy.height,
                collection=legacy.collection,
                created_at=legacy.created_at,
                focal_point_x=getattr(legacy, "focal_point_x", None),
                focal_point_y=getattr(legacy, "focal_point_y", None),
                focal_point_width=getattr(legacy, "focal_point_width", None),
                focal_point_height=getattr(legacy, "focal_point_height", None),
            )
            new_img._skip_webp = True
            buffer.append(new_img)

            if len(buffer) >= BATCH_SIZE:
                FoundationCustomImage.objects.bulk_create(buffer)
                migrated += len(buffer)
                self.stdout.write(f"Migrated batch — total migrated: {migrated}")
                buffer = []

        if buffer:
            FoundationCustomImage.objects.bulk_create(buffer)
            migrated += len(buffer)
            self.stdout.write(f"Migrated final batch — total migrated: {migrated}")

        # Reset sequence
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT setval(
                    pg_get_serial_sequence('"images_foundationcustomimage"', 'id'),
                    (SELECT MAX(id) FROM "images_foundationcustomimage")
                );
            """
            )
        self.stdout.write("ID sequence reset.")

        # Tag migration
        self.stdout.write("Copying tags...")
        legacy_ids = FoundationCustomImage.objects.values_list("id", flat=True)

        for legacy in LegacyImage.objects.filter(id__in=legacy_ids).iterator():
            if hasattr(legacy, "tags") and legacy.tags.exists():
                try:
                    new_img = FoundationCustomImage.objects.get(id=legacy.id)
                    tag_names = legacy.tags.names()
                    new_img.tags.set(tag_names)
                    tag_counter.update(tag_names)
                    tagged += 1
                    self.stdout.write(f"Tagged {new_img.title} with {len(tag_names)} tag(s).")
                except FoundationCustomImage.DoesNotExist:
                    self.stdout.write(f"Skipped tagging for image ID {legacy.id} — not found.")

        self.stdout.write(self.style.SUCCESS(f"\nTop tags:"))
        for tag, count in tag_counter.most_common(10):
            self.stdout.write(f"   {tag}: {count}")

        self.stdout.write(
            self.style.SUCCESS(f"\nMigration complete! {migrated} migrated, {skipped} skipped, {tagged} tagged.\n")
        )
