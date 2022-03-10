import factory
import wagtail_factories

from networkapi.wagtailpages.models import (
    ResearchLandingPage,
    ResearchLibraryPage,
    ResearchDetailPage,
    ResearchAuthorsIndexPage,
)

from networkapi.utility.faker import helpers as faker_helpers


class ResearchLandingPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ResearchLandingPage

    title = "Research"


class ResearchLibraryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ResearchLibraryPage

    title = "Library"


class ResearchAuthorsIndexPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ResearchAuthorsIndexPage

    title = "Authors"


class ResearchDetailPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = ResearchDetailPage

    title = factory.Faker('sentence', nb_words=8, variable_nb_words=True)


def generate(seed):
    faker_helpers.reseed(seed)
    home_page = faker_helpers.get_homepage()

    print("Generating research hub")

    # Only one landing page can exist
    research_landing_page = ResearchLandingPage.objects.first()
    if not research_landing_page:
        research_landing_page = ResearchLandingPageFactory.create(parent=home_page)

    # Only one library page can exist
    research_library_page = ResearchLibraryPage.objects.first()
    if not research_library_page:
        research_library_page = ResearchLibraryPageFactory.create(parent=research_landing_page)

    # Only one authors index page can exist
    research_authors_index_page = ResearchAuthorsIndexPage.objects.first()
    if not research_authors_index_page:
        research_authors_index_page = ResearchAuthorsIndexPageFactory.create(parent=research_landing_page)

    for i in range(6):
        ResearchDetailPageFactory.create(parent=research_library_page)
