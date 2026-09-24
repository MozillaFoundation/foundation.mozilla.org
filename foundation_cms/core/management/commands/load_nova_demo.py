from django.core.management.base import BaseCommand

from foundation_cms.core.factories.nova_demo import generate


class Command(BaseCommand):
    help = "Create missing Nova theme demo pages beneath the default site root, preserving existing content."

    def handle(self, *args, **options):
        for page in generate():
            self.stdout.write(f"{page.pk}: {page.url} (theme: {page.get_theme()})")
