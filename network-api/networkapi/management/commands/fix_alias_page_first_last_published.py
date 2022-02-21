from django.core.management.base import BaseCommand
from django.db.models import Q
from wagtail.core.models import Page


class Command(BaseCommand):

    def handle(self, **options):
        aliases_without_first_last_published = (
            Page.objects
            .filter(alias_of__isnull=False)
            .filter(Q(alias_of__first_published_at__isnull=False) | Q(alias_of__last_published_at__isnull=False))
            .select_related('alias_of')
        )
        found = aliases_without_first_last_published.count()
        if not found:
            return self.stdout.write(self.style.WARNING("Found no alias pages to update"))

        self.stdout.write(f"Found {found} alias page(s) to update")
        for alias in aliases_without_first_last_published:
            alias.first_published_at = alias.alias_of.first_published_at
            alias.last_published_at = alias.alias_of.last_published_at
            alias.save()
            self.stdout.write(f'Updated "{alias.title}" ({alias.pk})')

        self.stdout.write(self.style.SUCCESS("Done!"))
