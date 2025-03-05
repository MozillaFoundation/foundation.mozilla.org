from datetime import date, datetime, timezone

from django.test import TestCase

from foundation_cms.legacy_apps.wagtailpages.factory.buyersguide import (
    BuyersGuidePageFactory,
    GeneralProductPageFactory,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.base import Homepage


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
