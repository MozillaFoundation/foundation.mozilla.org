from bs4 import BeautifulSoup
from django.utils import translation
from wagtail.models import Locale, Site
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.core.factories import generate_homepage


class HomePageMeetMozillaTests(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_locale = Locale.get_default()
        cls.home_page = generate_homepage(slug="redesign-home")
        site = Site.objects.get(is_default_site=True)
        site.root_page = cls.home_page
        site.save()

    def get_homepage(self):
        with translation.override(self.default_locale.language_code):
            response = self.client.get(self.home_page.url)

        self.assertEqual(response.status_code, 200)
        return BeautifulSoup(response.content, "html.parser")

    def test_renders_once_after_the_hero(self):
        soup = self.get_homepage()

        sections = soup.select(".mzf-c-meet-mozilla")
        self.assertEqual(len(sections), 1)
        main = sections[0].find_parent("main")
        self.assertIn("hero-accordion", main.find_previous_sibling().get("class"))
        self.assertIs(main.find(recursive=False), sections[0])

    def test_renders_nothing_when_empty(self):
        self.home_page.meet_mozilla = []
        self.home_page.save_revision().publish()

        soup = self.get_homepage()

        self.assertIsNone(soup.select_one(".mzf-c-meet-mozilla"))
