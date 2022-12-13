from datetime import date, datetime, timezone

from django.test import TestCase

from networkapi.wagtailpages.factory.buyersguide import (
    BuyersGuidePageFactory,
    GeneralProductPageFactory,
)
from networkapi.wagtailpages.pagemodels.base import Homepage


class TestPNIAirtableConnections(TestCase):
    """
    This set of tests is used purely to make sure the fieldnames and mappings for PNI products to connect
    to Airtable don't change. No other tests are being performed here, it's simply looking at the import mapping
    and the export field dictionaries.

    If any of these fail, we know something in our code has changed and needs to be reflected in Airtable.
    """

    def setUp(self):
        pni_homepage = BuyersGuidePageFactory.create(
            parent=Homepage.objects.first(),
            title="* Privacy not included",
            slug="privacynotincluded",
            header="Be Smart. Shop Safe.",
        )
        self.general_product_page = GeneralProductPageFactory.create(
            title="General Percy Product",
            first_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            last_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            parent=pni_homepage,
            # product fields
            privacy_ding=True,
            adult_content=True,
            uses_wifi=True,
            uses_bluetooth=True,
            review_date=date(2025, 1, 1),
            company="Percy Corp",
            blurb="This is a general product specifically created for visual regression testing",
            product_url="http://example.com/general-percy",
            worst_case="Visual regression fails",
            # general product fields
            camera_app="Yes",
            camera_device="No",
            microphone_app="NA",
            microphone_device="CD",
            location_app="Yes",
            location_device="No",
            personal_data_collected="Is personal data getting collected?",
            biometric_data_collected="Is biometric data getting collected?",
            social_data_collected="Is social data getting collected?",
            how_can_you_control_your_data="So, how can you control your data?",
            data_control_policy_is_bad=True,
            company_track_record="Needs Improvement",
            track_record_is_bad=True,
            track_record_details="<p> What kind of track record are we talking about? </p>",
            offline_capable="Yes",
            offline_use_description="<p> Although it is unclear how offline capabilities work </p>",
            uses_ai="NA",
            ai_is_transparent="No",
            ai_helptext="The AI is a black box and no one knows how it works",
        )

    def test_product_page_import_mappings(self):
        """
        Ensure import mapping are all what we expect them to be.
        """

        # We can use a GeneralProduct here because it inherits from ProductPage
        mappings = self.general_product_page.map_import_fields()
        self.assertEqual(mappings["Title"], "title")
        self.assertEqual(mappings["Wagtail Page ID"], "pk")
        self.assertEqual(mappings["Slug"], "slug")
        self.assertEqual(mappings["Show privacy ding"], "privacy_ding")
        self.assertEqual(mappings["Has adult content"], "adult_content")
        self.assertEqual(mappings["Uses wifi"], "uses_wifi")
        self.assertEqual(mappings["Uses Bluetooth"], "uses_bluetooth")
        self.assertEqual(mappings["Review date"], "review_date")
        self.assertEqual(mappings["Company"], "company")
        self.assertEqual(mappings["Blurb"], "blurb")
        self.assertEqual(mappings["Product link"], "product_url")
        self.assertEqual(mappings["Worst case"], "worst_case")
        self.assertEqual(mappings["Signup requires email"], "signup_requires_email")
        self.assertEqual(mappings["Signup requires phone number"], "signup_requires_phone")
        self.assertEqual(
            mappings["Signup requires 3rd party account"],
            "signup_requires_third_party_account",
        )
        self.assertEqual(mappings["Signup explanation"], "signup_requirement_explanation")
        self.assertEqual(mappings["How it collects data"], "how_does_it_use_data_collected")
        self.assertEqual(mappings["Data collection privacy ding"], "data_collection_policy_is_bad")
        self.assertEqual(mappings["User friendly privacy policy"], "user_friendly_privacy_policy")
        self.assertEqual(
            mappings["User friendly privacy policy help text"],
            "user_friendly_privacy_policy_helptext",
        )
        self.assertEqual(mappings["Meets MSS"], "meets_minimum_security_standards")
        self.assertEqual(
            mappings["Meets MSS privacy policy ding"],
            "show_ding_for_minimum_security_standards",
        )
        self.assertEqual(mappings["Uses encryption"], "uses_encryption")
        self.assertEqual(mappings["Encryption help text"], "uses_encryption_helptext")
        self.assertEqual(mappings["Has security updates"], "security_updates")
        self.assertEqual(mappings["Security updates help text"], "security_updates_helptext")
        self.assertEqual(mappings["Strong password"], "strong_password")
        self.assertEqual(mappings["Strong password help text"], "strong_password_helptext")
        self.assertEqual(mappings["Manages security vulnerabilities"], "manage_vulnerabilities")
        self.assertEqual(mappings["Manages security help text"], "manage_vulnerabilities_helptext")
        self.assertEqual(mappings["Has privacy policy"], "privacy_policy")
        self.assertEqual(mappings["Privacy policy help text"], "privacy_policy_helptext")

    def test_general_product_page_import_mappings(self):
        """
        Ensure import mapping are all what we expect them to be.
        """
        mappings = self.general_product_page.map_import_fields()
        self.assertEqual(mappings["Has camera device"], "camera_device")
        self.assertEqual(mappings["Has camera app"], "camera_app")
        self.assertEqual(mappings["Has microphone device"], "microphone_device")
        self.assertEqual(mappings["Has microphone app"], "microphone_app")
        self.assertEqual(mappings["Has location device"], "location_device")
        self.assertEqual(mappings["Has location app"], "location_app")
        self.assertEqual(mappings["Personal data collected"], "personal_data_collected")
        self.assertEqual(mappings["Biometric data collected"], "biometric_data_collected")
        self.assertEqual(mappings["Social data collected"], "social_data_collected")
        self.assertEqual(mappings["How you can control your data"], "how_can_you_control_your_data")
        self.assertEqual(mappings["Company track record"], "company_track_record")
        self.assertEqual(mappings["Show company track record privacy ding"], "track_record_is_bad")
        self.assertEqual(mappings["Offline capable"], "offline_capable")
        self.assertEqual(mappings["Offline use"], "offline_use_description")
        self.assertEqual(mappings["Uses AI"], "uses_ai")
        self.assertEqual(mappings["AI help text"], "ai_helptext")
        self.assertEqual(mappings["AI is transparent"], "ai_is_transparent")

    def test_product_page_export_fields(self):
        # We can use a GeneralProduct here because it inherits from ProductPage
        export_fields = self.general_product_page.get_export_fields()
        self.assertIn("Slug", export_fields)
        self.assertIn("Wagtail Page ID", export_fields)
        self.assertIn("Last Updated", export_fields)
        self.assertIn("Status", export_fields)
        self.assertIn("Show privacy ding", export_fields)
        self.assertIn("Has adult content", export_fields)
        self.assertIn("Uses wifi", export_fields)
        self.assertIn("Uses Bluetooth", export_fields)
        self.assertIn("Review date", export_fields)
        self.assertIn("Company", export_fields)
        self.assertIn("Blurb", export_fields)
        self.assertIn("Product link", export_fields)
        self.assertIn("Worst case", export_fields)
        self.assertIn("Signup requires email", export_fields)
        self.assertIn("Signup requires phone number", export_fields)
        self.assertIn("Signup requires 3rd party account", export_fields)
        self.assertIn("Signup explanation", export_fields)
        self.assertIn("How it collects data", export_fields)
        self.assertIn("Data collection privacy ding", export_fields)
        self.assertIn("User friendly privacy policy", export_fields)
        self.assertIn("User friendly privacy policy help text", export_fields)
        self.assertIn("Meets MSS", export_fields)
        self.assertIn("Meets MSS privacy policy ding", export_fields)
        self.assertIn("Uses encryption", export_fields)
        self.assertIn("Encryption help text", export_fields)
        self.assertIn("Has security updates", export_fields)
        self.assertIn("Security updates help text", export_fields)
        self.assertIn("Strong password", export_fields)
        self.assertIn("Strong password help text", export_fields)
        self.assertIn("Manages security vulnerabilities", export_fields)
        self.assertIn("Manages security help text", export_fields)
        self.assertIn("Has privacy policy", export_fields)
        self.assertIn("Privacy policy help text", export_fields)

    def test_general_page_export_fields(self):
        export_fields = self.general_product_page.get_export_fields()
        self.assertIn("Has camera device", export_fields)
        self.assertIn("Has camera app", export_fields)
        self.assertIn("Has microphone device", export_fields)
        self.assertIn("Has microphone app", export_fields)
        self.assertIn("Has location device", export_fields)
        self.assertIn("Has location app", export_fields)
        self.assertIn("Personal data collected", export_fields)
        self.assertIn("Biometric data collected", export_fields)
        self.assertIn("Social data collected", export_fields)
        self.assertIn("How you can control your data", export_fields)
        self.assertIn("Company track record", export_fields)
        self.assertIn("Show company track record privacy ding", export_fields)
        self.assertIn("Offline capable", export_fields)
        self.assertIn("Offline use", export_fields)
        self.assertIn("Uses AI", export_fields)
        self.assertIn("AI is transparent", export_fields)
        self.assertIn("AI help text", export_fields)
