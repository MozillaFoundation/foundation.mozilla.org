from django.core.management.base import BaseCommand
from rest_framework.renderers import JSONRenderer

from networkapi.people.views import PeopleListView
from networkapi.people.serializers import PersonSerializer

from networkapi.news.views import NewsListView
from networkapi.news.serializers import NewsSerializer

from networkapi.highlights.views import HighlightListView
from networkapi.highlights.serializers import HighlightSerializer

from networkapi.milestones.views import MilestoneListView
from networkapi.milestones.serializers import MilestoneSerializer

renderer = JSONRenderer()


class Command(BaseCommand):
    help = """Dumps people, news, highlights, and milestones to
           json files for the front-end build to consume"""

    def writeToFile(self, filename, querySet, Serializer):
        with open(filename, 'w') as jsonFile:
            jsonFile.write('[')

            iterator = iter(querySet)

            try:
                instance = next(iterator)
                while True:
                    serializedInstance = Serializer(instance)
                    jsonFile.write(
                        renderer.render(
                            serializedInstance.data
                        ).decode('utf-8')
                    )
                    instance = next(iterator)
                    jsonFile.write(',')
            except StopIteration:
                pass

            jsonFile.write(']')

    def handle(self, *args, **options):
        # People
        peopleListView = PeopleListView()
        self.writeToFile(
            '../source/json/temp/people.json',
            peopleListView.get_queryset(),
            PersonSerializer
        )
        self.stdout.write("Wrote /source/json/temp/people.json")

        # news
        newsListView = NewsListView()
        self.writeToFile(
            '../source/json/temp/news.json',
            newsListView.get_queryset(),
            NewsSerializer
        )
        self.stdout.write("Wrote /source/json/temp/news.json")

        # highlights
        highlightListView = HighlightListView()
        self.writeToFile(
            '../source/json/temp/highlights.json',
            highlightListView.get_queryset(),
            HighlightSerializer
        )
        self.stdout.write("Wrote /source/json/temp/highlights.json")

        # milestones
        milestoneListView = MilestoneListView()
        self.writeToFile(
            '../source/json/temp/upcoming.json',
            milestoneListView.get_queryset(),
            MilestoneSerializer
        )
        self.stdout.write("Wrote /source/json/temp/upcoming.json")
