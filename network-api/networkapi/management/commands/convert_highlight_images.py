from django.core.management.base import BaseCommand

from networkapi.highlights.models import Highlight
from networkapi.wagtailpages.utils import create_wagtail_image


class Command(BaseCommand):
    help = 'Converst highlight images from a File to a Wagtail Image'

    def handle(self, *args, **options):
        # Loop through every highlight that has an Image
        all_highlights = Highlight.objects.filter(image__isnull=False)
        total_highlights = all_highlights.count()

        for i, highlight in enumerate(all_highlights):
            print(f"Processing {i+1} of {total_highlights}")
            new_image = create_wagtail_image(
                img_src=highlight.image.url,
                collection_name='highlights'
            )
            highlight.image_new = new_image
            highlight.save()
