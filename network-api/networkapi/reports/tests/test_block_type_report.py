from django.contrib.auth import get_user_model
from django.urls import reverse
from factory import Faker
from wagtailinventory.helpers import create_page_inventory, delete_page_inventory

from networkapi.reports.views import BlockTypesReportView
from networkapi.utility.faker import StreamfieldProvider
from networkapi.wagtailpages.factory.campaign_page import CampaignPageFactory
from networkapi.wagtailpages.factory.opportunity import OpportunityPageFactory
from networkapi.wagtailpages.factory.primary_page import PrimaryPageFactory
from networkapi.wagtailpages.tests.base import WagtailpagesTestCase

Faker.add_provider(StreamfieldProvider)


class PatchedPrimaryPageFactory(PrimaryPageFactory):
    body = Faker("streamfield", fields=["paragraph", "image", "airtable"])


class PatchedCampaignPageFactory(CampaignPageFactory):
    body = Faker("streamfield", fields=["paragraph", "image"])


class PatchedOpportunityPageFactory(OpportunityPageFactory):
    body = Faker("streamfield", fields=["paragraph"])


class BlockTypesReportViewTest(WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        self.view = BlockTypesReportView()
        User = get_user_model()
        self.user = User.objects.create_superuser("admin-user", "admin@example.com", "password")
        self.client.force_login(self.user)

    def test_view(self):
        """Tests that the queryset is correct."""
        # Create some pages with custom and standard blocks
        primary_page = PatchedPrimaryPageFactory(parent=self.homepage)
        campaign_page = PatchedCampaignPageFactory(parent=self.homepage)
        opportunity_page = PatchedOpportunityPageFactory(parent=self.homepage)

        # Update `wagtailinventory`'s index
        create_page_inventory(primary_page)
        create_page_inventory(campaign_page)
        create_page_inventory(opportunity_page)

        # Request the view
        response = self.client.get(reverse("block_types_report"))

        # Get the objects:
        object_list = response.context["object_list"]

        # The first, most used, should be the RichTextBlock created on all three pages
        block = object_list[0]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.RichTextBlock")
        self.assertEqual(block["count"], 3)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual(
            [primary_page.content_type, campaign_page.content_type, opportunity_page.content_type],
            block["content_types"],
        )

        # Two pages have crated ImageBlocks
        # Each ImageBlock has a ImageChooserBlock and a CharBlock
        # These should be in alphabetical order since they all have the same count
        block = object_list[1]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.annotated_image_block.AnnotatedImageBlock"
        )
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        block = object_list[2]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.annotated_image_block.RadioSelectBlock"
        )
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        block = object_list[3]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.link_block.LinkWithoutLabelBlock"
        )
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        block = object_list[4]
        self.assertEqual(block["block"], "wagtail.images.blocks.ImageChooserBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # FInally, we have the AirTableBlock, use only in one page
        # This one is made of a URLBlock and a IntegerBlock
        block = object_list[5]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.airtable_block.AirTableBlock"
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type], block["content_types"])

        block = object_list[6]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.IntegerBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type], block["content_types"])

        block = object_list[7]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.URLBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type], block["content_types"])

    def test_page_unpublished(self):
        """Tests that the queryset is updated when a page is unpublished"""
        # Create some pages with custom and standard blocks
        primary_page = PatchedPrimaryPageFactory(parent=self.homepage)
        campaign_page = PatchedCampaignPageFactory(parent=self.homepage)
        opportunity_page = PatchedOpportunityPageFactory(parent=self.homepage)

        # Update `wagtailinventory`'s index
        create_page_inventory(primary_page)
        create_page_inventory(campaign_page)
        create_page_inventory(opportunity_page)

        # Unpublish primary page
        primary_page.unpublish()

        # Request the view
        response = self.client.get(reverse("block_types_report"))

        # Get the objects:
        object_list = response.context["object_list"]

        # The first, most used, should be the RichTextBlock created on the two live pages
        block = object_list[0]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.RichTextBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual(
            [campaign_page.content_type, opportunity_page.content_type],
            block["content_types"],
        )

        # Two pages have crated ImageBlocks
        # Each ImageBlock has a ImageChooserBlock and a CharBlock
        # These should be in alphabetical order since they all have the same count
        block = object_list[1]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.annotated_image_block.AnnotatedImageBlock"
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        block = object_list[2]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.annotated_image_block.RadioSelectBlock"
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        block = object_list[3]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.link_block.LinkWithoutLabelBlock"
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        block = object_list[4]
        self.assertEqual(block["block"], "wagtail.images.blocks.ImageChooserBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

    def test_page_deleted(self):
        """Tests that the queryset is updated when a page is deleted"""
        # Create some pages with custom and standard blocks
        primary_page = PatchedPrimaryPageFactory(parent=self.homepage)
        campaign_page = PatchedCampaignPageFactory(parent=self.homepage)
        opportunity_page = PatchedOpportunityPageFactory(parent=self.homepage)

        # Update `wagtailinventory`'s index
        create_page_inventory(primary_page)
        create_page_inventory(campaign_page)
        create_page_inventory(opportunity_page)

        # Delete primary page
        primary_page.delete()

        # Update the inventory
        delete_page_inventory(primary_page)

        # Request the view
        response = self.client.get(reverse("block_types_report"))

        # Get the objects:
        object_list = response.context["object_list"]

        # The first, most used, should be the RichTextBlock created on the two live pages
        block = object_list[0]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.RichTextBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual(
            [campaign_page.content_type, opportunity_page.content_type],
            block["content_types"],
        )

        # Two pages have crated ImageBlocks
        # Each ImageBlock has a ImageChooserBlock and a LinkWithoutLabelBlock
        # These should be in alphabetical order since they all have the same count
        block = object_list[1]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.annotated_image_block.AnnotatedImageBlock"
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        block = object_list[2]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.annotated_image_block.RadioSelectBlock"
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        block = object_list[3]
        self.assertEqual(
            block["block"], "networkapi.wagtailpages.pagemodels.customblocks.link_block.LinkWithoutLabelBlock"
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        block = object_list[4]
        self.assertEqual(block["block"], "wagtail.images.blocks.ImageChooserBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])
