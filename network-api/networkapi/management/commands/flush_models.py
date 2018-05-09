from django.core.management.base import BaseCommand

# Models
from wagtail.core.models import Page

from networkapi.milestones.models import Milestone
from networkapi.news.models import News
from networkapi.people.models import (
    Person,
    Affiliation,
    InternetHealthIssue,
)
from networkapi.wagtailpages.models import CTA


class Command(BaseCommand):
    help = 'Flush the models from the database'

    def handle(self, *args, **options):

        self.stdout.write('Flushing models from the database...')

        self.stdout.write('Dropping News objects...')
        News.objects.all().delete()

        self.stdout.write('Dropping Milestone objects...')
        Milestone.objects.all().delete()

        self.stdout.write('Dropping Person objects...')
        Person.objects.all().delete()

        self.stdout.write('Dropping InternetHealthIssue objects...')
        InternetHealthIssue.objects.all().delete()

        self.stdout.write('Dropping Affiliation objects...')
        Affiliation.objects.all().delete()

        self.stdout.write('Dropping Wagtail CTAs...')
        CTA.objects.all().delete()

        self.stdout.write('Dropping all Pages')
        Page.objects.exclude(title='Root').delete()

        self.stdout.write(self.style.SUCCESS('Done!'))
