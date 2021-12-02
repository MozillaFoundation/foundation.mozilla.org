from wagtail.core.models.i18n import Locale
from wagtail_localize.models import LocaleSynchronization

from networkapi.utility.faker.helpers import reseed


def generate(seed):
    reseed(seed)

    print("Generating Locale")
    default = Locale.get_default()
    french, _ = Locale.objects.get_or_create(language_code="fr")
    LocaleSynchronization.objects.get_or_create(locale=french, sync_from=default)
