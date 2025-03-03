from django.test import SimpleTestCase
from wagtail.admin.panels.base import get_form_for_model

from foundation_cms.legacy_cms.nav.forms import NavMenuForm
from foundation_cms.legacy_cms.nav.models import NavMenu


class NavMenuFormTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        cls.form = get_form_for_model(
            NavMenu,
            form_class=NavMenuForm,
            fields=["title", "dropdowns", "enable_blog_dropdown", "blog_button_label"],
            formsets=["featured_blog_topics"],
        )
        cls.extra_form_data = {
            "title": "foo+bar",
            "dropdowns-count": "1",
            "dropdowns-0-deleted": "",
            "dropdowns-0-order": "0",
            "dropdowns-0-type": "dropdown",
            "dropdowns-0-id": "a1123c22-eedb-4e02-85e8-96ec46333ef4",
            "dropdowns-0-value-title": "My+title",
            "dropdowns-0-value-button-label": "Learn+more",
            "dropdowns-0-value-button-link_to": "external_url",
            "dropdowns-0-value-button-external_url": "https://mozilla.org",
            "dropdowns-0-value-overview-count": "0",
            "dropdowns-0-value-columns-count": "1",
            "dropdowns-0-value-columns-0-deleted": "",
            "dropdowns-0-value-columns-0-order": "0",
            "dropdowns-0-value-columns-0-type": "",
            "dropdowns-0-value-columns-0-id": "50aaed85-df06-49ab-83b6-cc8c19bff7ac",
            "dropdowns-0-value-columns-0-value-title": "Column+title",
            "dropdowns-0-value-columns-0-value-nav_items-count": "1",
            "dropdowns-0-value-columns-0-value-nav_items-0-deleted": "",
            "dropdowns-0-value-columns-0-value-nav_items-0-order": "0",
            "dropdowns-0-value-columns-0-value-nav_items-0-type": "",
            "dropdowns-0-value-columns-0-value-nav_items-0-id": "",
            "dropdowns-0-value-columns-0-value-nav_items-0-value-label": "First+nav+item",
            "dropdowns-0-value-columns-0-value-nav_items-0-value-description": "",
            "dropdowns-0-value-columns-0-value-nav_items-0-value-link_to": "external_url",
            "dropdowns-0-value-columns-0-value-nav_items-0-value-external_url": "https://mozilla.org",
            "dropdowns-0-value-columns-0-value-button-count": "0",
            "dropdowns-0-value-featured_column-count": "0",
            "featured_blog_topics-TOTAL_FORMS": "0",
            "featured_blog_topics-INITIAL_FORMS": "0",
            "featured_blog_topics-MIN_NUM_FORMS": "0",
            "featured_blog_topics-MAX_NUM_FORMS": "4",
            "blog_button_label": "",
        }

    def test_form_is_valid_without_enabling_blog_dropdown(self):
        form_data = {
            "enable_blog_dropdown": False,
            "blog_button_label": "",
            "featured_blog_topics-TOTAL_FORMS": 0,
        }
        form = self.form(data={**self.extra_form_data, **form_data})
        form.is_valid()
        self.assertEqual(form.errors, {})

    def test_invalid_form_with_enabled_blog_dropdown_and_empty_featured_blog_topics(self):
        form_data = {
            "enable_blog_dropdown": True,
            "blog_button_label": "See all blog posts",
            "featured_blog_topics-TOTAL_FORMS": 0,
        }
        form = self.form(data={**self.extra_form_data, **form_data})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "__all__": ["You must add at least one featured blog topic if the blog dropdown is enabled"],
                "enable_blog_dropdown": [
                    "You must add at least one featured blog topic if the blog dropdown is enabled"
                ],
            },
        )

    def test_blog_enabled_form_is_not_valid_without_a_label(self):
        form_data = {
            "enable_blog_dropdown": True,
            "blog_button_label": "",
            "featured_blog_topics-TOTAL_FORMS": "1",
            "featured_blog_topics-INITIAL_FORMS": "0",
            "featured_blog_topics-MIN_NUM_FORMS": "0",
            "featured_blog_topics-MAX_NUM_FORMS": "4",
            "featured_blog_topics-0-topic": "5",
            "featured_blog_topics-0-icon": "9978",
            "featured_blog_topics-0-id": "",
            "featured_blog_topics-0-ORDER": "1",
            "featured_blog_topics-0-DELETE": "",
        }
        form = self.form(data={**self.extra_form_data, **form_data})
        form.is_valid()
        self.assertEqual(
            form.errors,
            {"blog_button_label": ["You must provide a label for the blog button if the blog dropdown is enabled"]},
        )

    def test_blog_enabled_form_is_valid_with_a_label_and_at_least_one_featured_topic(self):
        form_data = {
            "enable_blog_dropdown": True,
            "blog_button_label": "See all blog posts",
            "featured_blog_topics-TOTAL_FORMS": "1",
            "featured_blog_topics-INITIAL_FORMS": "0",
            "featured_blog_topics-MIN_NUM_FORMS": "0",
            "featured_blog_topics-MAX_NUM_FORMS": "4",
            "featured_blog_topics-0-topic": "5",
            "featured_blog_topics-0-icon": "9978",
            "featured_blog_topics-0-id": "",
            "featured_blog_topics-0-ORDER": "1",
            "featured_blog_topics-0-DELETE": "",
        }
        form = self.form(data={**self.extra_form_data, **form_data})
        form.is_valid()
        self.assertEqual(form.errors, {})
