from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.core.models import Locale


class Command(BaseCommand):
    help = 'Look for and create locales if they do not exist. This can be run multiple times if needed.'

    def handle(self, *args, **options):
        for language_code, name in settings.WAGTAIL_CONTENT_LANGUAGES:
            locale, created = Locale.objects.get_or_create(language_code=language_code)
            if created:
                print(f"Create new locale: {name}")
