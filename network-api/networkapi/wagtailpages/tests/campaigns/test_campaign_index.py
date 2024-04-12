from networkapi.wagtailpages.factory import campaign_page as campaign_factories
from networkapi.wagtailpages.tests import base as test_base


class CampaignIndexTestCase(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        super().setUpTestData()

    def test_get_featured_pages_initial_order(self):
        """Verify that featured pages are retrieved in the correct initial order."""
        # Setting up a campaign index page and three campaign pages
        campaign_index_page = campaign_factories.CampaignIndexPageFactory(parent=self.homepage)
        campaign_page_1 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)
        campaign_page_2 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)
        campaign_page_3 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)

        # Creating relationships with defined sort orders
        campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_2,
            sort_order=0,
        )
        campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_1,
            sort_order=1,
        )
        campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_3,
            sort_order=2,
        )

        # Fetching the featured pages in their defined order
        featured_pages = list(campaign_index_page.get_entries())

        # Validating both the order and the correct retrieval of pages
        self.assertEqual(len(featured_pages), 3)
        self.assertListEqual(
            featured_pages,
            [campaign_page_2, campaign_page_1, campaign_page_3],
        )

    def test_delete_featured_page(self):
        """Check correct handling when a featured page is deleted."""
        # Initial setup of index and campaign pages
        campaign_index_page = campaign_factories.CampaignIndexPageFactory(parent=self.homepage)
        campaign_page_1 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)
        campaign_page_2 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)
        campaign_page_3 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)

        # Establishing featured relationships
        relation_to_delete = campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_2,
            sort_order=0,
        )
        campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_1,
            sort_order=1,
        )
        campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_3,
            sort_order=2,
        )

        # Deleting one featured page and its relation
        relation_to_delete.delete()

        # Re-fetching the featured pages post deletion
        featured_pages = list(campaign_index_page.get_entries())

        # Ensuring the list is updated correctly after deletion
        self.assertEqual(len(featured_pages), 2)
        self.assertListEqual(
            featured_pages,
            [campaign_page_1, campaign_page_3],
        )

    def test_reorder_featured_pages(self):
        """Ensure that pages reflect changes in order after reordering."""
        # Setup of campaign pages and their initial order
        campaign_index_page = campaign_factories.CampaignIndexPageFactory(parent=self.homepage)
        campaign_page_1 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)
        campaign_page_2 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)
        campaign_page_3 = campaign_factories.CampaignPageFactory(parent=campaign_index_page)

        # Creating initial relationships
        relation1 = campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_1,
        )
        relation2 = campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_2,
        )
        relation3 = campaign_factories.CampaignIndexFeaturedCampaignPageRelationFactory(
            index_page=campaign_index_page,
            featured_page=campaign_page_3,
        )

        featured_pages = list(campaign_index_page.get_entries())

        # Ensuring the list is updated correctly after deletion
        self.assertEqual(len(featured_pages), 3)
        self.assertListEqual(
            featured_pages,
            [campaign_page_1, campaign_page_2, campaign_page_3],
        )

        campaign_index_page.featured_campaign_pages = [relation3, relation2, relation1]

        featured_pages = list(campaign_index_page.get_entries())

        # Ensuring the list is updated correctly after deletion
        self.assertEqual(len(featured_pages), 3)
        self.assertListEqual(
            featured_pages,
            [campaign_page_3, campaign_page_2, campaign_page_1],
        )
