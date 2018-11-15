from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clear the cache - used post deploy'

    def handle(self, *args, **options):
        print("Clearing cache")
        cache.clear()
        print("Done!")
