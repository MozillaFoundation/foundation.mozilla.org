from http import HTTPStatus
from urllib.parse import urlsplit

from django.test import override_settings
from django.urls import reverse
from wagtail.models import PageViewRestriction

from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class PasswordRequiredPageTests(test_base.WagtailpagesTestCase):
    password = "test-password"

    def setUp(self):
        super().setUp()
        self.restriction = PageViewRestriction.objects.create(
            page=self.homepage,
            restriction_type=PageViewRestriction.PASSWORD,
            password=self.password,
        )
        self.page_url = urlsplit(self.homepage.url).path
        self.action_url = reverse(
            "wagtailcore_authenticate_with_password",
            args=[self.restriction.pk, self.homepage.pk],
        )

    def test_password_gate_uses_current_branding(self):
        response = self.client.get(self.page_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "wagtailcore/password_required.html")
        self.assertContains(response, "password_required.compiled.css")
        self.assertContains(response, "primary-nav-wordmark-symbol.svg")
        self.assertContains(response, "password-required__submit")
        self.assertContains(response, "btn-primary__roller")
        self.assertContains(response, "data-csrf-form")
        self.assertContains(response, "data-csrf-field")
        self.assertNotContains(response, "legacy_apps/_js/csrf-global.compiled.js")

    def test_incorrect_password_renders_error(self):
        response = self.client.post(
            self.action_url,
            {"password": "incorrect", "return_url": self.page_url},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "wagtailcore/password_required.html")
        self.assertContains(response, "The password you have entered is not correct")
        self.assertContains(response, 'aria-invalid="true"')

    def test_correct_password_unlocks_page(self):
        response = self.client.post(
            self.action_url,
            {"password": self.password, "return_url": self.page_url},
        )

        self.assertRedirects(response, self.page_url, fetch_redirect_response=False)
        self.assertIn(
            self.restriction.pk,
            self.client.session[self.restriction.passed_view_restrictions_session_key],
        )
