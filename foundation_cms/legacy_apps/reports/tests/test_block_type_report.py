from django.contrib.auth import get_user_model
from django.urls import reverse
from factory import Faker
from wagtailinventory.helpers import create_page_inventory, delete_page_inventory

from foundation_cms.legacy_apps.reports.views import BlockTypesReportView
from foundation_cms.legacy_apps.utility.faker import StreamfieldProvider
from foundation_cms.legacy_apps.wagtailpages.factory.campaign_page import (
    CampaignPageFactory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.opportunity import (
    OpportunityPageFactory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.primary_page import (
    PrimaryPageFactory,
)
from foundation_cms.legacy_apps.wagtailpages.tests.base import WagtailpagesTestCase

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

        # Two pages have created AnnotatedImageBlocks
        block = object_list[1]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.annotated_image_block.AnnotatedImageBlock",
        )
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # RadioSelectBlock is used in AnnotatedImageBlock
        block = object_list[2]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.annotated_image_block.RadioSelectBlock",
        )
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # LinkBlockWithoutLabel is used in AnnotatedImageBlock
        block = object_list[3]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.link_block.LinkWithoutLabelBlock",
        )
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # BooleanBlock is used in LinkBlockWithoutLabel
        block = object_list[4]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.BooleanBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # CharBlock is used in LinkBlockWithoutLabel
        block = object_list[5]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.CharBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # ChoiceBlock is used in LinkBlockWithoutLabel
        block = object_list[6]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.ChoiceBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # EmailBlock is used in LinkBlockWithoutLabel
        block = object_list[7]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.EmailBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # PageChooserBlock is used in LinkBlockWithoutLabel
        block = object_list[8]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.PageChooserBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # URLBlock is used in LinkBlockWithoutLabel
        block = object_list[9]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.URLBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # ListBlock is used to wrap LinkBlockWithoutLabel in AnnotatedImageBlock
        block = object_list[10]
        self.assertEqual(block["block"], "wagtail.blocks.list_block.ListBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # DocumentChooserBlock is used in LinkBlockWithoutLabel
        block = object_list[11]
        self.assertEqual(block["block"], "wagtail.documents.blocks.DocumentChooserBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

        # ImageChooserBlock is used in AnnotatedImageBlock
        block = object_list[12]
        self.assertEqual(block["block"], "wagtail.images.blocks.ImageChooserBlock")
        self.assertEqual(block["count"], 2)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([primary_page.content_type, campaign_page.content_type], block["content_types"])

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

        # The remaining blocks should only appear on the campaign page
        # The campaign page is using an AnnotatedImageBlock
        block = object_list[1]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.annotated_image_block.AnnotatedImageBlock",
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # RadioSelectBlock is used in AnnotatedImageBlock
        block = object_list[2]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.annotated_image_block.RadioSelectBlock",
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # LinkBlockWithoutLabel is used in AnnotatedImageBlock
        block = object_list[3]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.link_block.LinkWithoutLabelBlock",
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # BooleanBlock is used in LinkBlockWithoutLabel
        block = object_list[4]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.BooleanBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # CharBlock is used in LinkBlockWithoutLabel
        block = object_list[5]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.CharBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # ChoiceBlock is used in LinkBlockWithoutLabel
        block = object_list[6]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.ChoiceBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # EmailBlock is used in LinkBlockWithoutLabel
        block = object_list[7]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.EmailBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # PageChooserBlock is used in LinkBlockWithoutLabel
        block = object_list[8]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.PageChooserBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # URLBlock is used in LinkBlockWithoutLabel
        block = object_list[9]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.URLBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # ListBlock is used to wrap LinkBlockWithoutLabel in AnnotatedImageBlock
        block = object_list[10]
        self.assertEqual(block["block"], "wagtail.blocks.list_block.ListBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # DocumentChooserBlock is used in LinkBlockWithoutLabel
        block = object_list[11]
        self.assertEqual(block["block"], "wagtail.documents.blocks.DocumentChooserBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # ImageChooserBlock is used in AnnotatedImageBlock
        block = object_list[12]
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

        # The remaining blocks should only appear on the campaign page
        # The campaign page is using an AnnotatedImageBlock
        block = object_list[1]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.annotated_image_block.AnnotatedImageBlock",
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # RadioSelectBlock is used in AnnotatedImageBlock
        block = object_list[2]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.annotated_image_block.RadioSelectBlock",
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # LinkBlockWithoutLabel is used in AnnotatedImageBlock
        block = object_list[3]
        self.assertEqual(
            block["block"],
            "foundation_cms.legacy_apps.wagtailpages.pagemodels.customblocks.link_block.LinkWithoutLabelBlock",
        )
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Custom")
        self.assertTrue(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # BooleanBlock is used in LinkBlockWithoutLabel
        block = object_list[4]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.BooleanBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # CharBlock is used in LinkBlockWithoutLabel
        block = object_list[5]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.CharBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # ChoiceBlock is used in LinkBlockWithoutLabel
        block = object_list[6]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.ChoiceBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # EmailBlock is used in LinkBlockWithoutLabel
        block = object_list[7]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.EmailBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # PageChooserBlock is used in LinkBlockWithoutLabel
        block = object_list[8]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.PageChooserBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # URLBlock is used in LinkBlockWithoutLabel
        block = object_list[9]
        self.assertEqual(block["block"], "wagtail.blocks.field_block.URLBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # ListBlock is used to wrap LinkBlockWithoutLabel in AnnotatedImageBlock
        block = object_list[10]
        self.assertEqual(block["block"], "wagtail.blocks.list_block.ListBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # DocumentChooserBlock is used in LinkBlockWithoutLabel
        block = object_list[11]
        self.assertEqual(block["block"], "wagtail.documents.blocks.DocumentChooserBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])

        # ImageChooserBlock is used in AnnotatedImageBlock
        block = object_list[12]
        self.assertEqual(block["block"], "wagtail.images.blocks.ImageChooserBlock")
        self.assertEqual(block["count"], 1)
        self.assertEqual(block["type_label"], "Core")
        self.assertFalse(block["is_custom_block"])
        self.assertListEqual([campaign_page.content_type], block["content_types"])
