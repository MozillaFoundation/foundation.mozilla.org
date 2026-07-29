from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.navigation import factories as nav_factories
from foundation_cms.navigation import models as nav_models


class DefaultNavigationTests(test_base.WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        nav_models.NavigationMenu.objects.all().delete()
        settings = nav_models.SiteNavigationMenu.for_site(self.site)
        settings.active_navigation_menu = None
        settings.save(update_fields=["active_navigation_menu"])

    def test_generate_creates_and_activates_expected_menu(self):
        menu = nav_factories.generate(self.site)

        settings = nav_models.SiteNavigationMenu.for_site(self.site)
        self.assertEqual(settings.active_navigation_menu, menu)
        self.assertEqual(menu.title, "Main Navigation")
        self.assertEqual(menu.locale, self.default_locale)

        dropdowns = list(menu.dropdowns)
        self.assertEqual(
            [(item.value.header_value["label"], item.value.header_value.url) for item in dropdowns],
            [
                ("Meet Mozilla", "/meet-mozilla/"),
                ("What We Do", "/what-we-do/"),
                ("Join Us", "/join-us/"),
                ("Nothing Personal", "/nothing-personal/"),
            ],
        )
        self.assertEqual([len(item.value.dropdown_items) for item in dropdowns], [0, 3, 0, 0])
        self.assertEqual(
            [(item["label"], item.url) for item in dropdowns[1].value.dropdown_items],
            [
                ("Imagine", "/what-we-do/imagine/"),
                ("Co-create", "/what-we-do/co-create/"),
                ("Mobilize", "/what-we-do/mobilize/"),
            ],
        )
        for dropdown in dropdowns:
            self.assertEqual(dropdown.value.header_value.get_link_to(), "relative_url")
            for item in dropdown.value.dropdown_items:
                self.assertEqual(item.get_link_to(), "relative_url")

    def test_generate_is_idempotent(self):
        first_menu = nav_factories.generate(self.site)
        second_menu = nav_factories.generate(self.site)

        self.assertEqual(second_menu, first_menu)
        self.assertEqual(nav_models.NavigationMenu.objects.count(), 1)

    def test_generate_preserves_existing_active_menu(self):
        active_menu = nav_factories.NavigationMenuFactory(title="Editor-managed Navigation")
        original_dropdowns = nav_models.NavigationMenu.objects.values_list("dropdowns", flat=True).get(
            pk=active_menu.pk
        )
        settings = nav_models.SiteNavigationMenu.for_site(self.site)
        settings.active_navigation_menu = active_menu
        settings.save(update_fields=["active_navigation_menu"])

        generated_menu = nav_factories.generate(self.site)

        self.assertEqual(generated_menu, active_menu)
        self.assertEqual(
            nav_models.NavigationMenu.objects.values_list("dropdowns", flat=True).get(pk=active_menu.pk),
            original_dropdowns,
        )
        self.assertEqual(nav_models.NavigationMenu.objects.count(), 1)

    def test_generate_reuses_existing_inactive_main_navigation_without_modifying_it(self):
        existing_menu = nav_factories.NavigationMenuFactory(title="Main Navigation")
        original_dropdowns = nav_models.NavigationMenu.objects.values_list("dropdowns", flat=True).get(
            pk=existing_menu.pk
        )

        generated_menu = nav_factories.generate(self.site)

        self.assertEqual(generated_menu, existing_menu)
        self.assertEqual(
            nav_models.NavigationMenu.objects.values_list("dropdowns", flat=True).get(pk=existing_menu.pk),
            original_dropdowns,
        )
        self.assertEqual(nav_models.NavigationMenu.objects.count(), 1)
