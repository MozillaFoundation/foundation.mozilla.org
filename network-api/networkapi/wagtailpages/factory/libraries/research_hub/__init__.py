from networkapi.utility.faker import helpers as faker_helpers
from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory.libraries.research_hub import (
    author_index as author_index_factory,
)
from networkapi.wagtailpages.factory.libraries.research_hub import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.libraries.research_hub import (
    landing_page as landing_page_factory,
)
from networkapi.wagtailpages.factory.libraries.research_hub import (
    library_page as library_page_factory,
)
from networkapi.wagtailpages.factory.libraries.research_hub import (
    relations as relations_factory,
)
from networkapi.wagtailpages.factory.libraries.research_hub import (
    taxonomies as taxonomies_factory,
)
from networkapi.wagtailpages.pagemodels.profiles import Profile


def create_detail_page_for_visual_regression_tests(seed, research_library_page):
    faker_helpers.reseed(seed)

    percy_author_profile = Profile.objects.get(name="Percy Profile")

    percy_research_detail_page = detail_page_factory.ResearchDetailPageFactory.create(
        parent=research_library_page, title="Fixed Title Research Detail Page"
    )

    relations_factory.ResearchAuthorRelationFactory.create(
        research_detail_page=percy_research_detail_page,
        author_profile=percy_author_profile,
    )


def generate(seed):
    faker_helpers.reseed(seed)
    home_page = faker_helpers.get_homepage()

    print("Generating research hub")

    # Only one landing page can exist
    research_landing_page = wagtailpage_models.ResearchLandingPage.objects.first()
    if not research_landing_page:
        research_landing_page = landing_page_factory.ResearchLandingPageFactory.create(parent=home_page)

    # Only one library page can exist
    research_library_page = wagtailpage_models.ResearchLibraryPage.objects.first()
    if not research_library_page:
        research_library_page = library_page_factory.ResearchLibraryPageFactory.create(parent=research_landing_page)

    # Only one authors index page can exist
    research_authors_index_page = wagtailpage_models.ResearchAuthorsIndexPage.objects.first()
    if not research_authors_index_page:
        research_authors_index_page = author_index_factory.ResearchAuthorsIndexPageFactory.create(
            parent=research_landing_page
        )

    create_detail_page_for_visual_regression_tests(seed, research_library_page)

    for _ in range(4):
        taxonomies_factory.ResearchRegionFactory.create()
        taxonomies_factory.ResearchTopicFactory.create()

    for _ in range(13):
        research_detail_page = detail_page_factory.ResearchDetailPageFactory.create(
            parent=research_library_page,
            research_authors=None,
            related_topics=None,
            related_regions=None,
        )

        for profile in faker_helpers.get_random_objects(source=wagtailpage_models.Profile, max_count=3):
            relations_factory.ResearchAuthorRelationFactory.create(
                research_detail_page=research_detail_page,
                author_profile=profile,
            )

        for region in faker_helpers.get_random_objects(source=wagtailpage_models.ResearchRegion, max_count=2):
            relations_factory.ResearchDetailPageResearchRegionRelationFactory.create(
                research_detail_page=research_detail_page,
                research_region=region,
            )

        for topic in faker_helpers.get_random_objects(source=wagtailpage_models.ResearchTopic, max_count=2):
            relations_factory.ResearchDetailPageResearchTopicRelationFactory.create(
                research_detail_page=research_detail_page,
                research_topic=topic,
            )

    # Populating research landing page with featured research topics
    for topic in faker_helpers.get_random_objects(source=wagtailpage_models.ResearchTopic, max_count=3):
        relations_factory.ResearchLandingPageResearchTopicRelationFactory.create(
            research_landing_page=research_landing_page,
            research_topic=topic,
        )
