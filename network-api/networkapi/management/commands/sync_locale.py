from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.core.models import Locale
from wagtail_localize.models import LocaleSynchronization


class Command(BaseCommand):
    help = 'Sync pages with original English pages'

    def handle(self, *args, **options):
        print("Select a language code to sync with English. ie: de")

        for language_code, name in settings.WAGTAIL_CONTENT_LANGUAGES:
            if language_code != 'en':
                print(f"{language_code} ({name})")

        language_code = input("Language code: ")

        # Confirm the language code is in the WAGTAIL_CONTENT_LANGUAGES
        language_codes_dict = dict(settings.WAGTAIL_CONTENT_LANGUAGES)
        if language_code not in language_codes_dict:
            print("Invalid language code")
            return

        print("Getting both locales...")
        english_locale, _ = Locale.objects.get_or_create(language_code='en')
        locale, _ = Locale.objects.get_or_create(language_code=language_code)

        print("Getting LocaleSynchronization object")
        sync, created = LocaleSynchronization.objects.get_or_create(
            locale=locale,
            sync_from=english_locale,
        )
        if created:
            print("\tNew LocaleSynchronization object created")

        print(f"Syncing {locale} from {english_locale}")
        sync.sync_trees()
