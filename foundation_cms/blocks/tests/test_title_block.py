from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from wagtail.models import Locale, Page
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.blocks.title_block import TitleBlock
from foundation_cms.core.models import GeneralPage


class TestTitleBlockAnchorId(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fr_locale, _ = Locale.objects.get_or_create(language_code="fr")
        cls.page = Page.get_first_root_node().add_child(
            instance=GeneralPage(
                title="Festival",
                slug="festival",
                seo_title="Festival",
                search_description="Festival page.",
                body=[("title_block", {"title": "Before the festival", "style": "shape"})],
            )
        )

    def render_heading_ids(self, page):
        html = render_to_string("patterns/components/_streamfield.html", {"streamfield": page.body, "page": page})
        return [heading["id"] for heading in BeautifulSoup(html, "html.parser").select("h2.title-block__title")]

    def translate(self):
        return self.page.copy_for_translation(self.fr_locale, copy_parents=True)

    def test_default_locale_page_uses_its_own_title(self):
        self.assertEqual(self.render_heading_ids(self.page), ["before-the-festival"])

    def test_translated_title_keeps_the_english_anchor(self):
        """Links copied from the English page point at the English slug, so the translated heading must match it."""
        translation = self.translate()
        translation.body[0].value["title"] = "Avant le festival"
        translation.save()

        self.assertEqual(self.render_heading_ids(translation), ["before-the-festival"])

    def test_title_missing_from_english_page_uses_its_own_title(self):
        translation = self.translate()
        translation.body = [("title_block", {"title": "Seulement en français", "style": "shape"})]
        translation.save()

        self.assertEqual(self.render_heading_ids(translation), ["seulement-en-francais"])

    def test_renders_outside_a_page(self):
        block = TitleBlock()
        html = block.render(block.to_python({"title": "Before the festival", "style": "shape"}))

        self.assertIn('id="before-the-festival"', html)
