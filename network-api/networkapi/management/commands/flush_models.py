from django.core.management.base import BaseCommand

# Models
from networkapi.highlights.models import Highlight
from networkapi.landingpage.models import LandingPage, Signup
from networkapi.milestones.models import Milestone
from networkapi.news.models import News
from networkapi.people.models import (
    Person,
    Affiliation,
    InternetHealthIssue,
)
from networkapi.homepage.models import Homepage


class Command(BaseCommand):
    help = 'Flush the models from the database'

    def handle(self, *args, **options):

        self.stdout.write('Flushing models from the database...')

        self.stdout.write('Dropping Homepage objects..')
        Homepage.objects.all().delete()

        self.stdout.write('Dropping LandingPage objects...')
        LandingPage.objects.all().delete()

        self.stdout.write('Dropping Signup objects...')
        Signup.objects.all().delete()

        self.stdout.write('Dropping Highlight objects...')
        Highlight.objects.all().delete()

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

        self.stdout.write(self.style.SUCCESS('Done!'))
