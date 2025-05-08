from collections import Counter

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from wagtail.images.models import Image as LegacyImage
from networkapi.images.models import FoundationCustomImage

BATCH_SIZE = 1000


class Command(BaseCommand):
    help = "Migrate legacy wagtailimages.Image objects to FoundationCustomImage (with tags + timestamp fix)"

    def handle(self, *args, **options):
        self.stdout.write("Starting full image migration...")

        migrated = 0
        skipped = 0
        tagged = 0
        updated_ts = 0
        missing_ts = 0
        tag_counter = Counter()
        timestamp_updates = []

        # Step 1: Build lookup for legacy timestamps
        legacy_timestamps = dict(
            LegacyImage.objects.values_list("id", "created_at")
        )

        # Step 2: Migrate images
        existing_files = set(FoundationCustomImage.objects.values_list("file", flat=True))
        legacy_qs = LegacyImage.objects.select_related("collection").only(
            "id", "title", "file", "width", "height",
            "collection", "created_at",
            "focal_point_x", "focal_point_y", "focal_point_width", "focal_point_height",
        )

        buffer = []

        for legacy in legacy_qs.iterator(chunk_size=500):
            if legacy.file in existing_files:
                skipped += 1
                continue

            created_at = legacy_timestamps.get(legacy.id)
            if not created_at:
                missing_ts += 1

            img = FoundationCustomImage(
                id=legacy.id,
                title=legacy.title,
                file=legacy.file,
                width=legacy.width,
                height=legacy.height,
                collection=legacy.collection,
                created_at=created_at,
                focal_point_x=getattr(legacy, "focal_point_x", None),
                focal_point_y=getattr(legacy, "focal_point_y", None),
                focal_point_width=getattr(legacy, "focal_point_width", None),
                focal_point_height=getattr(legacy, "focal_point_height", None),
            )
            img._skip_webp = True
            buffer.append(img)

            if len(buffer) >= BATCH_SIZE:
                FoundationCustomImage.objects.bulk_create(buffer)
                migrated += len(buffer)
                self.stdout.write(f"Migrated batch — total migrated: {migrated}")
                buffer = []

        if buffer:
            FoundationCustomImage.objects.bulk_create(buffer)
            migrated += len(buffer)
            self.stdout.write(f"Final batch migrated — total migrated: {migrated}")

        # Step 3: Reset ID sequence
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

        # Step 4: Tag migration
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

        self.stdout.write(self.style.SUCCESS("\nTop tags:"))
        for tag, count in tag_counter.most_common(10):
            self.stdout.write(f"   {tag}: {count}")

        # Step 5: Timestamp repair (recheck in case bulk_create didn't persist it)
        self.stdout.write("Backfilling timestamps if needed...")

        for img in FoundationCustomImage.objects.only("id", "created_at").iterator(chunk_size=500):
            if not img.created_at:
                ts = legacy_timestamps.get(img.id)
                if ts:
                    img.created_at = ts
                    timestamp_updates.append(img)
                    updated_ts += 1

            if len(timestamp_updates) >= BATCH_SIZE:
                self._bulk_update_timestamps(timestamp_updates)
                self.stdout.write(f"Timestamp batch update — total updated: {updated_ts}")
                timestamp_updates = []

        if timestamp_updates:
            self._bulk_update_timestamps(timestamp_updates)
            self.stdout.write(f"Final timestamp batch updated: {len(timestamp_updates)}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! {migrated} migrated, {skipped} skipped, {tagged} tagged, {updated_ts} timestamps updated, {missing_ts} missing timestamps."
        ))

    def _bulk_update_timestamps(self, objs):
        with transaction.atomic():
            FoundationCustomImage.objects.bulk_update(objs, ["created_at"])
