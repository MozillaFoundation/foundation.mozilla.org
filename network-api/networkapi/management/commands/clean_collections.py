from django.core.management.base import BaseCommand

from wagtail.core.models import Collection
from wagtail.images.models import Image


class Command(BaseCommand):
    help = 'Remove unused Collections with a depth of 1, and move respective images to the root collection'

    def handle(self, *args, **options):
        root = Collection.objects.get(name='Root')

        # Let's confirm root is ID #1, as it should be just to be safe.
        if root.id != 1:
            print("Incorrect root Collection ID. Stopping this script to prevent any mistakes")
            return

        duplicate_root_collections = Collection.objects.filter(depth=1).exclude(name='Root')

        print(f"There are {duplicate_root_collections.count()} duplicate root Collections")
        for collection in duplicate_root_collections:
            # Find images
            print(f"Working with {collection.name}")
            images = Image.objects.filter(collection=collection)

            if images:
                for image in images:
                    print(f"\tMoving {image.title} to the root collection")
                    image.collection = root
                    image.save()

            print(f"\tDeleting {collection.name}")
            collection.delete()
