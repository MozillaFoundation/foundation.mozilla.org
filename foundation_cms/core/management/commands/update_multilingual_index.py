from django.core.management.base import BaseCommand
from wagtail.models import Locale, Page
from wagtail.search.index import get_indexed_models

from foundation_cms.search.utils import get_search_backend_for_locale


class Command(BaseCommand):
    help = "Reindex all live pages using the correct search backend per locale."

    def add_arguments(self, parser):
        parser.add_argument(
            "--locale",
            type=str,
            help="Only reindex pages for this locale code (e.g. 'en', 'de').",
        )
        parser.add_argument(
            "--chunk-size",
            type=int,
            default=100,
            dest="chunk_size",
            help="Pages per batch (default: 100).",
        )

    def handle(self, *args, **options):
        locales = Locale.objects.all()

        if options["locale"]:
            locales = locales.filter(language_code=options["locale"])
            if not locales.exists():
                self.stderr.write(self.style.ERROR(f"Locale '{options['locale']}' not found."))
                return

        # Only Page subclasses, the ones that carry locale info
        page_models = [m for m in get_indexed_models() if issubclass(m, Page)]

        for locale in locales:
            self._index_locale(locale, page_models, options["chunk_size"])

    def _index_locale(self, locale, page_models, chunk_size):
        locale_code = locale.language_code
        backend, backend_name = get_search_backend_for_locale(locale_code)

        self.stdout.write(f"\n[{locale_code}] - backend '{backend_name}'")

        total = 0
        for model in page_models:
            qs = model.objects.live().filter(locale=locale).order_by("pk")
            count = qs.count()
            if not count:
                continue

            self.stdout.write(f"  {model.__name__}: {count} pages")

            try:
                for offset in range(0, count, chunk_size):
                    chunk = list(qs[offset : offset + chunk_size])
                    backend.add_bulk(model, chunk)
            except Exception as e:
                self.stderr.write(self.style.WARNING(f"  ⚠ {model.__name__} failed: {e}"))
                continue

            total += count

        self.stdout.write(self.style.SUCCESS(f"  Done: {total} pages indexed for '{locale_code}'."))
