from django.utils.translation import gettext

from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


class TestProductPage(BuyersGuideTestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = self.create_superuser(username="admin", password="password")
        self.login(self.admin_user)

    def test_votes(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)

        evaluation = product_page.evaluation

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
        evaluation.refresh_from_db()
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
        evaluation.refresh_from_db()
        self.assertEqual(evaluation.total_votes, 3)
        self.assertEqual(evaluation.total_creepiness, 6)
        self.assertEqual(evaluation.average_creepiness, 2)

        self.translate_page(product_page, self.fr_locale)

        # Make sure properties are correct
        fr_evaluation = fr_product_page.evaluation
        self.assertEqual(fr_evaluation, evaluation)
        self.assertIn(vote_1, fr_evaluation.votes.all())
        self.assertIn(vote_2, fr_evaluation.votes.all())
        self.assertIn(vote_3, fr_evaluation.votes.all())
        self.assertEqual(fr_evaluation.total_votes, 3)
        self.assertEqual(fr_evaluation.total_creepiness, 6)
        self.assertEqual(fr_evaluation.average_creepiness, 2)

    def test_creepiness_per_bin(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        evaluation = product_page.evaluation

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
        evaluation.refresh_from_db()
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

    def test_creepiness_per_bin_limits(self):
        product_page = buyersguide_factories.ProductPageFactory(parent=self.bg)
        evaluation = product_page.evaluation

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
        evaluation.refresh_from_db()
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
