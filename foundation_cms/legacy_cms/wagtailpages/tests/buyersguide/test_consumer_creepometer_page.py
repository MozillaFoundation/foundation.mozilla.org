from foundation_cms.legacy_cms.wagtailpages import models as pagemodels
from foundation_cms.legacy_cms.wagtailpages.factory import buyersguide as buyersguide_factories
from foundation_cms.legacy_cms.wagtailpages.tests import base as test_base


class ConsumerCreepometerPageFactoryTests(test_base.WagtailpagesTestCase):
    def test_factory(self):
        buyersguide_factories.ConsumerCreepometerPageFactory()


class ConsumerCreepometerPageTests(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.buyersguide_homepage = buyersguide_factories.BuyersGuidePageFactory(
            parent=cls.homepage,
        )
        cls.content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=cls.buyersguide_homepage,
        )

    def test_parents(self):
        self.assertAllowedParentPageTypes(
            child_model=pagemodels.BuyersGuideArticlePage,
            parent_models={pagemodels.BuyersGuideEditorialContentIndexPage},
        )

    def test_children(self):
        self.assertAllowedSubpageTypes(
            parent_model=pagemodels.ConsumerCreepometerPage,
            child_models={},
        )

    def test_year_choices(self):
        page = buyersguide_factories.ConsumerCreepometerPageFactory(
            parent=self.content_index
        )  # it will use a random year
        choices = page._meta.get_field("year").choices
        self.assertEqual(choices, (("2023", "2023"),))
        self.assertIn((page.year, page.year), choices)

    def test_template(self):
        consumer_creepometer_page = buyersguide_factories.ConsumerCreepometerPageFactory(
            parent=self.content_index,
            year="2023",
        )

        response = self.client.get(consumer_creepometer_page.url)

        self.assertTemplateUsed(
            response=response,
            template_name="buyersguide/pages/consumer_creepometer_page_2023.html",
        )
