from unittest.mock import MagicMock, patch

from django.urls import reverse
from django.utils.translation import gettext
from faker import Faker
from wagtail import hooks

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.pagemodels.buyersguide.homepage import BuyersGuidePage
from networkapi.wagtailpages.pagemodels.buyersguide.products import (
    ProductPage,
    ProductPageEvaluation,
    reset_product_page_votes,
)
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


class TestProductPageEvaluation(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = self.create_superuser(username="admin", password="password")
        self.login(self.admin_user)

    def test_votes(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)

        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=product_page.evaluation.pk)
        )

        # There should be no votes initially.
        self.assertCountEqual(list(evaluation.votes.all()), [])
        self.assertEqual(evaluation.total_votes, 0)
        self.assertEqual(evaluation.total_creepiness, 0)
        self.assertEqual(evaluation.average_creepiness, 0)

        # Create some votes
        vote_1 = buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=1)
        vote_2 = buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=2)
        vote_3 = buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=3)

        # Make sure properties are correct
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=product_page.evaluation.pk)
        )
        self.assertIn(vote_1, evaluation.votes.all())
        self.assertIn(vote_2, evaluation.votes.all())
        self.assertIn(vote_3, evaluation.votes.all())
        self.assertEqual(evaluation.total_votes, 3)
        self.assertEqual(evaluation.total_creepiness, 6)
        self.assertEqual(evaluation.average_creepiness, 2)

    def test_votes_with_translated_page(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        # Copy page for translation
        self.homepage.copy_for_translation(self.fr_locale)
        self.bg.copy_for_translation(self.fr_locale)

        self.translate_page(product_page, self.fr_locale)
        fr_product_page = product_page.get_translation(self.fr_locale)

        # Create some votes
        evaluation = product_page.evaluation
        vote_1 = buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=1)
        vote_2 = buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=2)
        vote_3 = buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=3)

        product_page.save_revision().publish()

        # Make sure properties are correct
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=product_page.evaluation.pk)
        )
        self.assertEqual(evaluation.total_votes, 3)
        self.assertEqual(evaluation.total_creepiness, 6)
        self.assertEqual(evaluation.average_creepiness, 2)

        self.translate_page(product_page, self.fr_locale)

        # Make sure properties are correct
        fr_evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=fr_product_page.evaluation.pk)
        )
        self.assertEqual(fr_evaluation, evaluation)
        self.assertIn(vote_1, fr_evaluation.votes.all())
        self.assertIn(vote_2, fr_evaluation.votes.all())
        self.assertIn(vote_3, fr_evaluation.votes.all())
        self.assertEqual(fr_evaluation.total_votes, 3)
        self.assertEqual(fr_evaluation.total_creepiness, 6)
        self.assertEqual(fr_evaluation.average_creepiness, 2)

    def test_creepiness_per_bin(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=product_page.evaluation.pk)
        )

        # There should be no votes initially.
        self.assertDictEqual(
            evaluation.labelled_creepiness_per_bin,
            {
                "Not creepy": {"count": 0, "label": gettext("Not creepy")},
                "A little creepy": {"count": 0, "label": gettext("A little creepy")},
                "Somewhat creepy": {"count": 0, "label": gettext("Somewhat creepy")},
                "Very creepy": {"count": 0, "label": gettext("Very creepy")},
                "Super creepy": {"count": 0, "label": gettext("Super creepy")},
            },
        )

        # Create some votes
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=10)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=30)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=50)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=70)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=90)

        # Make sure properties are correct
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=product_page.evaluation.pk)
        )
        self.assertDictEqual(
            evaluation.labelled_creepiness_per_bin,
            {
                "Not creepy": {"count": 1, "label": gettext("Not creepy")},
                "A little creepy": {"count": 1, "label": gettext("A little creepy")},
                "Somewhat creepy": {"count": 1, "label": gettext("Somewhat creepy")},
                "Very creepy": {"count": 1, "label": gettext("Very creepy")},
                "Super creepy": {"count": 1, "label": gettext("Super creepy")},
            },
        )
        self.assertEqual(evaluation.average_creepiness, 50)
        self.assertEqual(evaluation.total_creepiness, 250)
        self.assertEqual(evaluation.total_votes, 5)
        self.assertDictEqual(
            evaluation.average_bin, {"label": "Somewhat creepy", "localized": gettext("Somewhat creepy")}
        )

    def test_creepiness_per_bin_limits(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=product_page.evaluation.pk)
        )

        # Create some votes
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=0)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=19)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=20)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=39)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=40)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=59)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=60)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=79)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=80)
        buyersguide_factories.ProductVoteFactory(evaluation=evaluation, value=99)

        # Make sure properties are correct
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=product_page.evaluation.pk)
        )
        self.assertDictEqual(
            evaluation.labelled_creepiness_per_bin,
            {
                "Not creepy": {"count": 2, "label": gettext("Not creepy")},
                "A little creepy": {"count": 2, "label": gettext("A little creepy")},
                "Somewhat creepy": {"count": 2, "label": gettext("Somewhat creepy")},
                "Very creepy": {"count": 2, "label": gettext("Very creepy")},
                "Super creepy": {"count": 2, "label": gettext("Super creepy")},
            },
        )
        self.assertEqual(evaluation.average_creepiness, 49.5)
        self.assertEqual(evaluation.total_creepiness, 495)
        self.assertEqual(evaluation.total_votes, 10)
        self.assertDictEqual(
            evaluation.average_bin, {"label": "Somewhat creepy", "localized": gettext("Somewhat creepy")}
        )


class TestProductPageEvaluationAverageBin(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = self.create_superuser(username="admin", password="password")
        self.login(self.admin_user)
        self.product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        self.fake = Faker()
        Faker.seed(0)

    def test_avg_bin_with_no_votes(self):
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.product_page.evaluation.pk)
        )

        self.assertEqual(evaluation.total_votes, 0)
        self.assertDictEqual(evaluation.average_bin, {"label": "No votes", "localized": gettext("No votes")})

    def test_avg_bin_with_avg_vote_equal_0(self):
        buyersguide_factories.ProductVoteFactory(evaluation=self.product_page.evaluation, value=0)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.product_page.evaluation.pk)
        )

        self.assertEqual(evaluation.average_creepiness, 0)
        self.assertDictEqual(evaluation.average_bin, {"label": "Not creepy", "localized": gettext("Not creepy")})

    def test_avg_bin_with_avg_vote_between_1_and_20(self):
        vote_value = self.fake.random_int(min=1, max=19)
        buyersguide_factories.ProductVoteFactory(evaluation=self.product_page.evaluation, value=vote_value)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.product_page.evaluation.pk)
        )

        self.assertEqual(evaluation.average_creepiness, vote_value)
        self.assertDictEqual(evaluation.average_bin, {"label": "Not creepy", "localized": gettext("Not creepy")})

    def test_avg_bin_with_avg_vote_between_20_and_40(self):
        vote_value = self.fake.random_int(min=20, max=39)
        buyersguide_factories.ProductVoteFactory(evaluation=self.product_page.evaluation, value=vote_value)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.product_page.evaluation.pk)
        )

        self.assertEqual(evaluation.average_creepiness, vote_value)
        self.assertDictEqual(
            evaluation.average_bin, {"label": "A little creepy", "localized": gettext("A little creepy")}
        )

    def test_avg_bin_with_avg_vote_between_40_and_60(self):
        vote_value = self.fake.random_int(min=40, max=59)
        buyersguide_factories.ProductVoteFactory(evaluation=self.product_page.evaluation, value=vote_value)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.product_page.evaluation.pk)
        )

        self.assertEqual(evaluation.average_creepiness, vote_value)
        self.assertDictEqual(
            evaluation.average_bin, {"label": "Somewhat creepy", "localized": gettext("Somewhat creepy")}
        )

    def test_avg_bin_with_avg_vote_between_60_and_80(self):
        vote_value = self.fake.random_int(min=60, max=79)
        buyersguide_factories.ProductVoteFactory(evaluation=self.product_page.evaluation, value=vote_value)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.product_page.evaluation.pk)
        )

        self.assertEqual(evaluation.average_creepiness, vote_value)
        self.assertDictEqual(evaluation.average_bin, {"label": "Very creepy", "localized": gettext("Very creepy")})

    def test_avg_bin_with_avg_vote_between_80_and_99(self):
        vote_value = self.fake.random_int(min=80, max=99)
        buyersguide_factories.ProductVoteFactory(evaluation=self.product_page.evaluation, value=vote_value)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.product_page.evaluation.pk)
        )

        self.assertEqual(evaluation.average_creepiness, vote_value)
        self.assertDictEqual(evaluation.average_bin, {"label": "Super creepy", "localized": gettext("Super creepy")})

    def test_avg_bin_with_avg_vote_equal_100(self):
        buyersguide_factories.ProductVoteFactory(evaluation=self.product_page.evaluation, value=100)
        evaluation = (
            ProductPageEvaluation.objects.with_total_votes()
            .with_total_creepiness()
            .with_average_creepiness()
            .get(pk=self.product_page.evaluation.pk)
        )

        self.assertEqual(evaluation.average_creepiness, 100)
        self.assertDictEqual(evaluation.average_bin, {"label": "Super creepy", "localized": gettext("Super creepy")})


class TestProductPageEvaluationPrefetching(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = self.create_superuser(username="admin", password="password")
        self.login(self.admin_user)
        self.product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        self.evaluation = self.product_page.evaluation
        self.vote_1 = buyersguide_factories.ProductVoteFactory(evaluation=self.evaluation, value=1)
        self.vote_2 = buyersguide_factories.ProductVoteFactory(evaluation=self.evaluation, value=2)
        self.vote_3 = buyersguide_factories.ProductVoteFactory(evaluation=self.evaluation, value=3)

    def test_votes(self):
        query_number = 1
        with self.assertNumQueries(query_number):
            evaluation = ProductPageEvaluation.objects.with_total_votes().get(pk=self.evaluation.pk)
            self.assertEqual(evaluation.total_votes, 3)

    def test_empty_votes(self):
        self.evaluation.votes.all().delete()
        query_number = 1
        with self.assertNumQueries(query_number):
            evaluation = ProductPageEvaluation.objects.with_total_votes().get(pk=self.evaluation.pk)
            self.assertEqual(evaluation.total_votes, 0)

    def test_total_creepiness(self):
        query_number = 1
        with self.assertNumQueries(query_number):
            evaluation = ProductPageEvaluation.objects.with_total_creepiness().get(pk=self.evaluation.pk)
            self.assertEqual(evaluation.total_creepiness, 6)

    def test_cant_get_total_creepiness_without_prefetching(self):
        evaluation = self.evaluation
        with self.assertRaises(AttributeError):
            evaluation.total_creepiness

    def test_total_creepiness_with_no_votes(self):
        self.evaluation.votes.all().delete()
        query_number = 1
        with self.assertNumQueries(query_number):
            evaluation = ProductPageEvaluation.objects.with_total_creepiness().get(pk=self.evaluation.pk)
            self.assertEqual(evaluation.total_creepiness, 0)

    def test_average_creepiness(self):
        query_number = 1
        with self.assertNumQueries(query_number):
            evaluation = ProductPageEvaluation.objects.with_average_creepiness().get(pk=self.evaluation.pk)
            self.assertEqual(evaluation.average_creepiness, 2)

    def test_cant_get_average_creepiness_without_prefetching(self):
        evaluation = self.evaluation
        with self.assertRaises(AttributeError):
            evaluation.average_creepiness

    def test_average_creepiness_with_no_votes(self):
        self.evaluation.votes.all().delete()
        query_number = 1
        with self.assertNumQueries(query_number):
            evaluation = ProductPageEvaluation.objects.with_average_creepiness().get(pk=self.evaluation.pk)
            self.assertEqual(evaluation.average_creepiness, 0)

    def test_bin_data(self):
        query_number = 1
        with self.assertNumQueries(query_number):
            evaluation = ProductPageEvaluation.objects.with_bin_data().get(pk=self.evaluation.pk)
            self.assertDictEqual(
                evaluation.labelled_creepiness_per_bin,
                {
                    "Not creepy": {"count": 3, "label": gettext("Not creepy")},
                    "A little creepy": {"count": 0, "label": gettext("A little creepy")},
                    "Somewhat creepy": {"count": 0, "label": gettext("Somewhat creepy")},
                    "Very creepy": {"count": 0, "label": gettext("Very creepy")},
                    "Super creepy": {"count": 0, "label": gettext("Super creepy")},
                },
            )


class CreateEvaluationPostSaveSignalTests(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.login()

    def test_that_created_product_page_in_default_language_has_evaluation(self):
        product_page = buyersguide_factories.ProductPageFactory.build(locale=self.default_locale, evaluation=None)
        self.bg.add_child(instance=product_page)
        self.assertIsNotNone(product_page.evaluation)
        self.assertIsInstance(product_page.evaluation, ProductPageEvaluation)

    def test_that_created_product_page_in_translated_language_syncs_evaluation(self):
        product_page = buyersguide_factories.ProductPageFactory.build(locale=self.default_locale, evaluation=None)
        self.bg.add_child(instance=product_page)

        self.translate_page(product_page, self.fr_locale)
        fr_product_page = product_page.get_translation(self.fr_locale)

        self.assertIsNotNone(fr_product_page.evaluation)
        self.assertIsInstance(fr_product_page.evaluation, ProductPageEvaluation)
        self.assertEqual(fr_product_page.evaluation, product_page.evaluation)

    def test_that_updated_page_is_not_changed(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        evaluation = product_page.evaluation
        self.assertIsNotNone(evaluation)
        self.assertIsInstance(evaluation, ProductPageEvaluation)

        product_page.title = "New title"
        product_page.save()

        self.assertEqual(product_page.evaluation, evaluation)

    def test_that_latest_revision_includes_evaluation(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        evaluation = product_page.evaluation
        self.assertIsNotNone(evaluation)
        self.assertIsInstance(evaluation, ProductPageEvaluation)

        product_page.title = "New title"
        product_page.save_revision().publish()

        self.assertEqual(product_page.evaluation, evaluation)
        # Verify that the latest revision includes the evaluation
        latest_revision_evaluation = product_page.get_latest_revision_as_object().evaluation
        self.assertIsNotNone(evaluation)
        self.assertEqual(latest_revision_evaluation, evaluation)
        # The evaluation on the product page was not changed
        product_page.refresh_from_db()
        self.assertEqual(product_page.evaluation, evaluation)


# This is a bit weird, but somewhere along the copy page action
# the GeneralProductPage.specific_class is being resolved
# to ProductPage, which is not allowed as a child of BuyersGuidePage.
# Thus, we need to mock the subpage_types and allowed_subpage_models to allow for
# ProductPage to be added as a child of BuyersGuidePage. If we don't, the
# copy page action will fail with a Permission Error since we can't add a
# ProductPage as a child of BuyersGuidePage.
MOCK_BG_SUBPAGE_TYPES = BuyersGuidePage.subpage_types + ["wagtailpages.ProductPage"]
MOCK_BG_ALLOWED_SUBPAGE_MODELS = BuyersGuidePage.allowed_subpage_models() + [ProductPage]


class AfterCopyProductPageHookTests(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.login()

    @hooks.register_temporarily("after_copy_page", reset_product_page_votes)
    @patch.multiple(
        BuyersGuidePage,
        subpage_types=MagicMock(return_value=MOCK_BG_SUBPAGE_TYPES),
        allowed_subpage_models=MagicMock(return_value=MOCK_BG_ALLOWED_SUBPAGE_MODELS),
    )
    def test_that_copied_page_gets_evaluation(self):
        product_page = buyersguide_factories.GeneralProductPageFactory(
            parent=self.bg, title="My Product", slug="my-product"
        )
        self.assertIsNotNone(product_page.evaluation)
        self.assertIsInstance(product_page.evaluation, ProductPageEvaluation)

        # Add some votes to product page
        buyersguide_factories.ProductVoteFactory.create_batch(10, evaluation=product_page.evaluation)
        self.assertTrue(product_page.creepiness > 0)

        post_data = {
            "new_title": "My Product 2",
            "new_slug": "my-product-2",
            "new_parent_page": str(self.bg.pk),
        }

        # Copy page
        self.client.post(reverse("wagtailadmin_pages:copy", args=(self.product_page.id,)), post_data)
        product_page_copy = self.bg.get_children().get(slug="my-product-2").specific

        self.assertIsNotNone(product_page_copy.evaluation)
        self.assertIsInstance(product_page_copy.evaluation, ProductPageEvaluation)
        self.assertNotEqual(product_page_copy.evaluation, product_page.evaluation)
        self.assertEqual(product_page_copy.creepiness, 0)
