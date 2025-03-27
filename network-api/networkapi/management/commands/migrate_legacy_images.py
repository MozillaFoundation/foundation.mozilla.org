from django.core.management.base import BaseCommand
from django.db import connection, transaction
from wagtail.images.models import Image as LegacyImage

from networkapi.images.models import FoundationCustomImage


class Command(BaseCommand):

    help = "Migrate legacy wagtailimages.Image objects to FoundationCustomImage (DB-only, no file access)"

    def handle(self, *args, **options):
        migrated = 0
        skipped = 0

        for legacy in LegacyImage.objects.all():
            # Skip if already exists (by file path)
            if FoundationCustomImage.objects.filter(file=legacy.file).exists():
                self.stdout.write(f"⏩ Skipping duplicate: {legacy.title}")
                skipped += 1
                continue

            # Create the new image (no .save() call to avoid triggering convert_gif_to_webp)
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
            # temporarily skip webp conversion
            new_img._skip_webp = True
            new_img.save()

            # Copy tags if they exist
            if hasattr(legacy, "tags"):
                new_img.tags.set(legacy.tags.names())

            migrated += 1
            self.stdout.write(f"✅ Migrated: {legacy.title}")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT setval(
                    pg_get_serial_sequence('"images_foundationcustomimage"', 'id'),
                    (SELECT MAX(id) FROM "images_foundationcustomimage")
                );
                """
            )
        self.stdout.write(self.style.SUCCESS("🔧 ID sequence reset for FoundationCustomImage."))

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Migration complete! {migrated} migrated, {skipped} skipped.\n"))
