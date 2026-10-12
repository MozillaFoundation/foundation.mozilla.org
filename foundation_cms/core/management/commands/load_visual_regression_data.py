from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Site

from foundation_cms.core.factories.visual_regression import generate
from foundation_cms.core.models import HomePage


class Command(BaseCommand):
    help = "Create two visual regression General Pages under the existing default redesign homepage."

    def handle(self, *args, **options):
        site = Site.objects.filter(is_default_site=True).first()
        if not site or not isinstance(site.root_page.specific, HomePage):
            raise CommandError("The default site must already have a redesign HomePage. Run load_redesign_data first.")
        for page in generate(parent=site.root_page.specific):
            self.stdout.write(
                self.style.SUCCESS(f"Visual fixture ready: {page.slug} (id={page.pk}, live={page.live})")
            )
