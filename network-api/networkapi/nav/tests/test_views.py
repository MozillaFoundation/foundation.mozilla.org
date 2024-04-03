from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from wagtail.admin.viewsets import viewsets as wagtail_admin_viewsets
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.models import Locale
from wagtail.test.utils import WagtailTestUtils

from networkapi.nav import factories as nav_factories
from networkapi.nav import models as nav_models


class TestNavMenuSnippetChooser(WagtailTestUtils, TestCase):
    def is_nav_menu_chooser_viewset(self, viewset):
        return viewset.model == nav_models.NavMenu and issubclass(viewset.__class__, ChooserViewSet)

    def get_chooser_viewset(self):
        # Get the last registered ChooserViewSet for the NavMenu model.
        # Note: There can be multiple ChooserViewSets registered for a model.
        wagtail_admin_viewsets.populate()
        model_viewsets = [x for x in wagtail_admin_viewsets.viewsets if self.is_nav_menu_chooser_viewset(x)]
        return model_viewsets[-1]

    def setUp(self):
        # Get the chooser url from the viewsets registry.
        # Would have been easier to get from model.snippet_viewset, but
        # that does not work somehow.
        chooser_viewset = self.get_chooser_viewset()
        print(nav_models.NavMenu.snippet_viewset)
        print(nav_models.NavMenu.snippet_viewset.chooser_viewset.get_url_name("choose"))
        self.chooser_url = reverse(f"{chooser_viewset.name}:choose")

        User = get_user_model()
        self.user = User.objects.create_superuser("admin-user", "admin@example.com", "password")
        self.client.force_login(self.user)

        self.default_locale = Locale.get_default()
        self.fr_locale = Locale.objects.create(language_code="fr")
        self.menus = [
            nav_factories.NavMenuFactory.create(title="Generic"),
            nav_factories.NavMenuFactory.create(title="Foundation"),
            nav_factories.NavMenuFactory.create(title="Mozfest"),
        ]

    def test_menu_chooser_exclude_locale(self):
        translated_menu = self.menus[0].copy_for_translation(self.fr_locale)
        translated_menu.save()
        all_menus = nav_models.NavMenu.objects.all()
        default_menus = nav_models.NavMenu.objects.filter(locale=self.default_locale)
        response = self.client.get(self.chooser_url)
        results = response.context["results"]

        # Chooser does not include every menu, but only the default language ones
        self.assertNotEqual(len(results), all_menus.count())
        self.assertEqual(len(results), default_menus.count())
        self.assertNotIn(translated_menu, results)
        self.assertIn(self.menus[0], results)

        # Menu chooser should not contain locale filter
        self.assertNotContains(response, "id_locale")
