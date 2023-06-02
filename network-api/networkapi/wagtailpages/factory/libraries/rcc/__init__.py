from networkapi.utility.faker import helpers as faker_helpers
from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory.libraries.rcc import (
    author_index as author_index_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    landing_page as landing_page_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    library_page as library_page_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    taxonomies as taxonomies_factory,
)


def generate(seed):
    faker_helpers.reseed(seed)
    home_page = faker_helpers.get_homepage()

    print("Generating rcc playbook")

    # Only one landing page can exist
    rcc_landing_page = wagtailpage_models.RCCLandingPage.objects.first()
    if not rcc_landing_page:
        rcc_landing_page = landing_page_factory.RCCLandingPageFactory.create(parent=home_page)

    # Only one library page can exist
    rcc_library_page = wagtailpage_models.RCCLibraryPage.objects.first()
    if not rcc_library_page:
        rcc_library_page = library_page_factory.RCCLibraryPageFactory.create(parent=rcc_landing_page)

    # Only one authors index page can exist
    rcc_authors_index_page = wagtailpage_models.RCCAuthorsIndexPage.objects.first()
    if not rcc_authors_index_page:
        rcc_authors_index_page = author_index_factory.RCCAuthorsIndexPageFactory.create(parent=rcc_landing_page)

    for _ in range(4):
        taxonomies_factory.RCCContentTypeFactory.create()
        taxonomies_factory.RCCCurricularAreaFactory.create()
        taxonomies_factory.RCCTopicFactory.create()

    for _ in range(13):
        detail_page_factory.RCCDetailPageFactory.create(
            parent=rcc_library_page,
            # rcc_authors=None,
            # related_curricular_areas=None,
            # related_content_types=None,
            # related_topics=None,
        )

        # for profile in faker_helpers.get_random_objects(source=wagtailpage_models.Profile, max_count=3):
        #     relations_factory.RCCAuthorRelationFactory.create(
        #         rcc_detail_page=rcc_detail_page,
        #         author_profile=profile,
        #     )

        # for content_type in faker_helpers.get_random_objects(source=wagtailpage_models.RCCContentType, max_count=2):
        #     relations_factory.RCCDetailPageRCCContentTypeRelationFactory.create(
        #         rcc_detail_page=rcc_detail_page,
        #         content_type=content_type,
        #     )

        # for curricular_area in faker_helpers.get_random_objects(
        #     source=wagtailpage_models.RCCCurricularArea, max_count=2
        # ):
        #     relations_factory.RCCDetailPageRCCCurricularAreaRelationFactory.create(
        #         rcc_detail_page=rcc_detail_page,
        #         curricular_area=curricular_area,
        #     )

        # for topic in faker_helpers.get_random_objects(source=wagtailpage_models.RCCTopic, max_count=2):
        #     relations_factory.RCCDetailPageRCCTopicRelationFactory.create(
        #         rcc_detail_page=rcc_detail_page,
        #         rcc_topic=topic,
        #     )

    # Populating research landing page with featured content types
    # for content_type in faker_helpers.get_random_objects(source=wagtailpage_models.RCCContentType, max_count=3):
    #     relations_factory.RCCLandingPageFeaturedRCCContentTypeRelationFactory.create(
    #         rcc_landing_page=rcc_landing_page,
    #         content_type=content_type,
    #     )
