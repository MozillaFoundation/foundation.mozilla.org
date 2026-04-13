from wagtail.test.utils import WagtailPageTestCase

<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
from foundation_cms.profiles.factories import ExpertProfilePageFactory
=======
from foundation_cms.profiles.factories import (
    ExpertDirectoryPageFactory,
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
)
>>>>>>> main


class ExpertProfilePageTestCase(WagtailPageTestCase):
    def setUp(self):
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
        self.page = ExpertProfilePageFactory()
=======
        self.hub = ExpertHubPageFactory()
        self.page = ExpertProfilePageFactory(parent=self.hub)
>>>>>>> main

    def test_str_representation(self):
        self.assertEqual(str(self.page), self.page.title)

    def test_required_fields_populated(self):
        self.assertTrue(self.page.role)
        self.assertTrue(self.page.bio)
        self.assertTrue(self.page.location)
        self.assertIsNotNone(self.page.image)

    def test_is_leaf_page(self):
        self.assertEqual(self.page.subpage_types, [])
<<<<<<< TP1-3626-enhanced-3-column-content-grid-container
=======


class ExpertDirectoryPageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.hub = ExpertHubPageFactory()
        self.directory = ExpertDirectoryPageFactory(parent=self.hub)

    def test_parent_is_hub(self):
        self.assertEqual(self.directory.get_parent().specific, self.hub)

    def test_is_leaf_page(self):
        self.assertEqual(self.directory.subpage_types, [])

    def test_get_experts_returns_hub_children(self):
        expert = ExpertProfilePageFactory(parent=self.hub)
        experts = self.directory.get_experts()
        self.assertIn(expert, experts)
>>>>>>> main
