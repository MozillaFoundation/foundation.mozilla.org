from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.profiles.factories import (
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
)


class ExpertProfilePageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.hub = ExpertHubPageFactory()
        self.page = ExpertProfilePageFactory(parent=self.hub)

    def test_str_representation(self):
        self.assertEqual(str(self.page), self.page.title)

    def test_required_fields_populated(self):
        self.assertTrue(self.page.role)
        self.assertTrue(self.page.bio)
        self.assertTrue(self.page.location)
        self.assertIsNotNone(self.page.image)

    def test_is_leaf_page(self):
        self.assertEqual(self.page.subpage_types, [])
