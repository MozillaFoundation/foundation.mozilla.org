import factory
import factory.fuzzy
import wagtail_factories

from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.utility.faker import helpers as faker_helpers



class ResearchLandingPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchLandingPage

    title = "Research"


class ResearchLibraryPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchLibraryPage

    title = "Library"


class ResearchAuthorsIndexPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchAuthorsIndexPage

    title = "Authors"


class ResearchDetailPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailPage

    title = factory.Faker('sentence', nb_words=8, variable_nb_words=True)


class ResearchRegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchRegion

    name = factory.Faker('country')


class ResearchTopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchTopic

    name = factory.Faker('catch_phrase')
    description = factory.Faker('paragraph')


class ResearchAuthorRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchAuthorRelation

    research_detail_page = factory.fuzzy.FuzzyChoice(
        wagtailpage_models.ResearchDetailPage.objects.all(),
    )
    author_profile = factory.fuzzy.FuzzyChoice(
        wagtailpage_models.Profile.objects.all(),
    )


def generate(seed):
    faker_helpers.reseed(seed)
    home_page = faker_helpers.get_homepage()

    print("Generating research hub")

    # Only one landing page can exist
    research_landing_page = wagtailpage_models.ResearchLandingPage.objects.first()
    if not research_landing_page:
        research_landing_page = ResearchLandingPageFactory.create(parent=home_page)

    # Only one library page can exist
    research_library_page = wagtailpage_models.ResearchLibraryPage.objects.first()
    if not research_library_page:
        research_library_page = ResearchLibraryPageFactory.create(parent=research_landing_page)

    # Only one authors index page can exist
    research_authors_index_page = wagtailpage_models.ResearchAuthorsIndexPage.objects.first()
    if not research_authors_index_page:
        research_authors_index_page = ResearchAuthorsIndexPageFactory.create(parent=research_landing_page)

    for _ in range(4):
        ResearchRegionFactory.create()
        ResearchTopicFactory.create()

    for _ in range(6):
        research_detail_page = ResearchDetailPageFactory.create(parent=research_library_page)

        for profile in profiles_factory.get_random_profiles(max_count=3):
            ResearchAuthorRelationFactory.create(
                research_detail_page=research_detail_page,
                author_profile=profile,
            )


