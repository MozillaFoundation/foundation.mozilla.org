from datetime import date, datetime, timezone

from io import StringIO
from os.path import join, abspath, dirname

from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import translation
from django.utils.translation.trans_real import (
    to_language as django_to_language,
    parse_accept_lang_header as django_parse_accept_lang_header
)

# from django.test.utils import override_settings

from unittest.mock import MagicMock
from unittest import skip

from wagtail.core.models import Collection, Site
from wagtail.images.models import Image

from wagtail_factories import SiteFactory

from networkapi.utility.redirects import redirect_to_default_cms_site
from networkapi.utility.middleware import ReferrerMiddleware, XRobotsTagMiddleware
from networkapi.wagtailpages import language_code_to_iso_3166, parse_accept_lang_header, to_language
from networkapi.wagtailpages.factory.buyersguide import (
    BuyersGuidePageFactory,
    GeneralProductPageFactory,
    SoftwareProductPageFactory,
)
from networkapi.wagtailpages.pagemodels.base import Homepage
from networkapi.wagtailpages.utils import create_wagtail_image


class ReferrerMiddlewareTests(TestCase):

    def setUp(self):
        referrer_middleware = ReferrerMiddleware('response')
        self.assertEqual(referrer_middleware.get_response, 'response')

    def test_requestProcessing(self):
        """
        Ensure that the middleware assigns a Referrer-Policy header to the response object
        """

        referrer_middleware = ReferrerMiddleware(MagicMock())
        response = referrer_middleware(MagicMock())
        response.__setitem__.assert_called_with('Referrer-Policy', 'same-origin')


class MissingMigrationsTests(TestCase):

    def test_no_migrations_missing(self):
        """
        Ensure we didn't forget a migration
        """
        output = StringIO()
        call_command('makemigrations', interactive=False, dry_run=True, stdout=output)

        if output.getvalue() != "No changes detected\n":
            raise AssertionError("Missing migrations detected:\n" + output.getvalue())


class DeleteNonStaffTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex'),

    def test_non_staff_is_deleted(self):
        """
        Simple users are deleted
        """

        call_command('delete_non_staff', '--now')

        self.assertEqual(User.objects.count(), 0)


class IsStaffNotDeletedTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex', is_staff=True)

    def test_is_staff_not_deleted(self):
        """
        Users with 'is_staff' flag at True are not deleted
        """

        call_command('delete_non_staff', '--now')

        self.assertEqual(User.objects.count(), 1)


class InGroupNotDeletedTest(TestCase):

    def setUp(self):
        group = Group.objects.create(name='TestGroup')
        group.user_set.create(username='Alex')

    def test_in_group_not_deleted(self):
        """
        Users in a group are not deleted
        """

        call_command('delete_non_staff', '--now')

        self.assertEqual(User.objects.count(), 1)


class MozillaFoundationUsersNotDeletedTest(TestCase):

    def setUp(self):
        User.objects.create(username='Alex', email='alex@mozillafoundation.org')

    def test_mozilla_foundation_users_not_deleted(self):
        """
        Mozilla Foundation Users are not deleted
        """

        call_command('delete_non_staff', '--now')

        self.assertEqual(User.objects.count(), 1)


class RedirectDefaultSiteDecoratorTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        # Change the default site away from localhost
        self.original_default_site = Site.objects.get(is_default_site=True, hostname='localhost')
        self.original_default_site.is_default_site = False
        self.original_default_site.save()
        # Add a default site, and a secondary site.
        self.default_site = SiteFactory(hostname='default-site.com', is_default_site=True)
        self.secondary_site = SiteFactory(hostname="secondary-site.com")

    def test_redirect_decorator(self):
        """
        Test that the decorator redirects.
        """
        decorated_view = redirect_to_default_cms_site(lambda request: None)
        response = decorated_view(self.factory.get('/example/', HTTP_HOST='secondary-site.com'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_decorator_doesnt_redirect(self):
        """
        Test that the redirect is triggered only when needed.
        """
        decorated_view = redirect_to_default_cms_site(lambda request: "untouched response")
        response = decorated_view(self.factory.get('/example/'))
        self.assertEqual(response, "untouched response")

    @skip("TODO: REENABLE: TEMPORARY SKIP TO MAKE PNI-AS-WAGTAIL LAUNCH POSSIBLE")
    # @override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_PNI_homepage_redirect_to_foundation_site(self):
        """
        Test that users gets redirected to PNI on the foundation site when they visit it from a non-default CMS site
        """
        response = self.client.get('/en/privacynotincluded/', HTTP_HOST='secondary-site.com')
        self.assertRedirects(
            response,
            "https://default-site.com/en/privacynotincluded/",
            fetch_redirect_response=False
        )

    def tearDown(self):
        # Re-instante localhost as the default site
        self.original_default_site.is_default_site = True
        self.original_default_site.save()

        # Remove the Site Factories
        self.default_site.delete()
        self.secondary_site.delete()


class WagtailPagesTestCase(TestCase):

    def test_get_language_code_to_iso_3166(self):
        self.assertEqual(language_code_to_iso_3166('en-gb'), 'en-GB')
        self.assertEqual(language_code_to_iso_3166('en-us'), 'en-US')
        self.assertEqual(language_code_to_iso_3166('fr'), 'fr')

    def test_to_language(self):
        self.assertEqual(to_language('en_US'), 'en-US')

    def test_parse_accept_lang_header_returns_iso_3166_language(self):
        self.assertEqual(
            parse_accept_lang_header('en-GB,en;q=0.5'),
            (('en-GB', 1.0), ('en', 0.5)),
        )


class WagtailPagesIntegrationTestCase(TestCase):

    """
    Test that our overrides to Django translation functions work.
    """
    def test_to_language(self):
        self.assertEqual(django_to_language('fy_NL'), 'fy-NL')

    def test_parse_accept_lang_header_returns_iso_3166_language(self):
        self.assertEqual(
            django_parse_accept_lang_header('fy-NL,fy;q=0.5'),
            (('fy-NL', 1.0), ('fy', 0.5)),
        )

    @skip("TODO: REMOVE: NOW DONE BY WAGTAIL")
    def test_reverse_produces_correct_url_prefix(self):
        translation.activate('fy-NL')
        url = reverse('buyersguide-home')
        self.assertTrue(url.startswith('/fy-NL/'))
        translation.deactivate()


class XRobotsTagMiddlewareTest(TestCase):
    def test_returns_response(self):
        xrobotstag_middleware = XRobotsTagMiddleware('response')
        self.assertEqual(xrobotstag_middleware.get_response, 'response')

    def test_sends_x_robots_tag(self):
        """
        Ensure that the middleware assigns an X-Robots-Tag to the response
        """

        xrobotstag_middleware = XRobotsTagMiddleware(MagicMock())
        response = xrobotstag_middleware(MagicMock())
        response.__setitem__.assert_called_with('X-Robots-Tag', 'noindex')


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
            title='* Privacy not included',
            slug='privacynotincluded',
            header='Be Smart. Shop Safe.',
            intro_text=(
                'How creepy is that smart speaker, that fitness tracker'
                ', those wireless headphones? We created this guide to help you shop for safe'
                ', secure connected products.'
            ),
        )
        self.general_product_page = GeneralProductPageFactory.create(
            title='General Percy Product',
            first_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            last_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            parent=pni_homepage,
            # product fields
            privacy_ding=True,
            adult_content=True,
            uses_wifi=True,
            uses_bluetooth=True,
            review_date=date(2025, 1, 1),
            company='Percy Corp',
            blurb='This is a general product specifically created for visual regression testing',
            product_url='http://example.com/general-percy',
            worst_case='Visual regression fails',
            # general product fields
            camera_app='Yes',
            camera_device='No',
            microphone_app='NA',
            microphone_device='CD',
            location_app='Yes',
            location_device='No',
            personal_data_collected='Is personal data getting collected?',
            biometric_data_collected='Is biometric data getting collected?',
            social_data_collected='Is social data getting collected?',
            how_can_you_control_your_data='So, how can you control your data?',
            data_control_policy_is_bad=True,
            company_track_record='Needs Improvement',
            track_record_is_bad=True,
            track_record_details='<p> What kind of track record are we talking about? </p>',
            offline_capable='Yes',
            offline_use_description='<p> Although it is unclear how offline capabilities work </p>',
            uses_ai='NA',
            ai_is_transparent='No',
            ai_helptext='The AI is a black box and no one knows how it works',
        )
        self.software_product_page = SoftwareProductPageFactory.create(
            # page fields
            title='Software Percy Product',
            first_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            last_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            parent=pni_homepage,
            # product fields
            privacy_ding=True,
            adult_content=True,
            uses_wifi=True,
            uses_bluetooth=True,
            review_date=date(2025, 1, 1),
            company='Percy Corp',
            blurb='This is a general product specifically created for visual regression testing',
            product_url='http://example.com/general-percy',
            worst_case='Visual regression fails',
            # software product fields
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
        self.assertEqual(mappings["Signup requires 3rd party account"], "signup_requires_third_party_account")
        self.assertEqual(mappings["Signup explanation"], "signup_requirement_explanation")
        self.assertEqual(mappings["How it collects data"], "how_does_it_use_data_collected")
        self.assertEqual(mappings["Data collection privacy ding"], "data_collection_policy_is_bad")
        self.assertEqual(mappings["User friendly privacy policy"], "user_friendly_privacy_policy")
        self.assertEqual(mappings["User friendly privacy policy help text"], "user_friendly_privacy_policy_helptext")
        self.assertEqual(mappings["Meets MSS"], "meets_minimum_security_standards")
        self.assertEqual(mappings["Meets MSS privacy policy ding"], "show_ding_for_minimum_security_standards")
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

    def test_software_product_page_import_mappings(self):
        """
        Ensure import mapping are all what we expect them to be.
        """
        mappings = self.software_product_page.map_import_fields()
        self.assertEqual(mappings["How it handles recording"], "handles_recordings_how")
        self.assertEqual(mappings["Recording alert"], "recording_alert")
        self.assertEqual(mappings["Recording alert help text"], "recording_alert_helptext")
        self.assertEqual(mappings["Medical privacy compliant"], "medical_privacy_compliant")
        self.assertEqual(mappings["Medical privacy compliant help text"], "medical_privacy_compliant_helptext")
        self.assertEqual(mappings["Host controls"], "host_controls")
        self.assertEqual(mappings["Easy to learn and use"], "easy_to_learn_and_use")
        self.assertEqual(mappings["Easy to learn and use help text"], "easy_to_learn_and_use_helptext")

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

    def test_software_page_export_fields(self):
        export_fields = self.software_product_page.get_export_fields()
        self.assertIn("How it handles recording", export_fields)
        self.assertIn("Recording alert", export_fields)
        self.assertIn("Recording alert help text", export_fields)
        self.assertIn("Medical privacy compliant", export_fields)
        self.assertIn("Medical privacy compliant help text", export_fields)
        self.assertIn("Host controls", export_fields)
        self.assertIn("Easy to learn and use", export_fields)
        self.assertIn("Easy to learn and use help text", export_fields)


class TestCreateWagtailImageUtility(TestCase):

    def setUp(self):
        self.image_path = abspath(join(dirname(__file__), '../media/images/placeholders/products/teddy.jpg'))

    def create_new_image(self):
        """A generic test to ensure the image is created properly."""
        new_image = create_wagtail_image(
            self.image_path,
            image_name='fake teddy.jpg',
            collection_name='pni products'
        )
        # Image was created
        self.assertIsNotNone(new_image)
        # Image has a collection and is in the proper collection
        self.assertIsNotNone(new_image.collection_id)
        self.assertEqual(new_image.collection.name, 'pni products')

    def test_empty_image_name_and_no_collection(self):
        new_image = create_wagtail_image(
            self.image_path,
        )
        self.assertEqual(new_image.title, 'teddy.jpg')
        self.assertEqual(new_image.collection.name, 'Root')

    def test_new_collection(self):
        collection_name = 'brand new collection'
        new_image = create_wagtail_image(
            self.image_path,
            image_name='fake teddy.jpg',
            collection_name=collection_name
        )
        self.assertEqual(new_image.collection.name, collection_name)

    def test_existing_collection(self):
        new_collection_name = 'first collection'

        root_collection = Collection.get_first_root_node()
        new_collection = root_collection.add_child(name=new_collection_name)
        total_images_in_new_collection = Image.objects.filter(collection=new_collection).count()
        self.assertEqual(total_images_in_new_collection, 0)

        new_image = create_wagtail_image(
            self.image_path,
            image_name='fake teddy.jpg',
            collection_name=new_collection_name
        )
        self.assertEqual(new_image.collection.name, new_collection_name)
