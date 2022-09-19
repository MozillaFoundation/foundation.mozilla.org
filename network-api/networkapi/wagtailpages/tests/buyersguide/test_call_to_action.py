from django.test import TestCase
from wagtail.snippets.views.snippets import get_snippet_edit_handler
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.call_to_action import BuyersGuideCallToAction


class BuyersGuideCallToActionTest(TestCase):

    def setUp(self):
        edit_handler = get_snippet_edit_handler(BuyersGuideCallToAction)
        self.form_class = edit_handler.get_form_class()

    def test_return_target_url_with_external_link(self):
        test_url = "http://test.com"
        cta = BuyersGuideCallToAction.objects.create(
            title="Test CTA",
            link_label="Test Link",
            link_target_url=test_url,
        )
        cta.save()

        target_url = cta.get_target_url()

        self.assertEqual(target_url, test_url)

    def test_return_target_url_with_page_link(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        cta = BuyersGuideCallToAction.objects.create(
            title="Test CTA",
            link_label="Test Link",
            link_target_page=test_page,
        )
        cta.save()

        target_url = cta.get_target_url()

        self.assertEqual(target_url, test_page.url)

    def test_cta_with_no_link_or_label_is_valid(self):
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                }
            )
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))

    def test_cannot_have_label_and_both_external_and_page_link(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_url": "http://test.com",
                    "link_target_page": test_page,
                }
            )
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))
        self.assertIn("link_target_url", form.errors)
        self.assertIn("link_target_page", form.errors)

    def test_label_and_page_link_is_valid(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_page": test_page,
                }
            )
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))

    def test_label_without_page_link_is_invalid(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        form = self.form_class(
            data=({"title": "Test CTA", "link_target_page": test_page}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("link_label", form.errors)

    def test_label_and_external_link_is_valid(self):
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_url": "http://test.com",
                }
            )
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))

    def test_label_without_external_link_is_invalid(self):
        form = self.form_class(
            data=({"title": "Test CTA", "link_target_url": "http://test.com"}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
        self.assertIn("link_label", form.errors)

    def test_cta_link_cannot_have_both_external_and_page_link(self):
        test_page = buyersguide_factories.BuyersGuidePageFactory()
        form = self.form_class(
            data=(
                {
                    "title": "Test CTA",
                    "link_label": "Test Link",
                    "link_target_url": "http://test.com",
                    "link_target_page": test_page,
                }
            )
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))
        self.assertIn("link_target_url", form.errors)
        self.assertIn("link_target_page", form.errors)

    def test_cta_link_must_have_external_or_page_link(self):
        form = self.form_class(
            data=({"title": "Test CTA", "link_label": "Test Link"}),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))
        self.assertIn("link_target_url", form.errors)
        self.assertIn("link_target_page", form.errors)
