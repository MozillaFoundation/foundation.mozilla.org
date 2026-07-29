from django.utils import translation
from wagtail.models import Locale, Site
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.base.utils.helpers import to_streamfield_value
from foundation_cms.core.factories import generate_homepage
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
)


class TopicListingPageTestCase(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_locale = Locale.get_default()
        cls.fr_locale, _ = Locale.objects.get_or_create(language_code="fr")

        cls.home_page = generate_homepage(slug="redesign-home")
        cls.site = Site.objects.get(is_default_site=True)
        cls.site.root_page = cls.home_page
        cls.site.save()

        cls.topic = Topic.objects.create(
            name="Privacy",
            slug="privacy",
            description="Privacy topic for listing tests.",
        )

        cls.np_home = NothingPersonalHomePage(
            title="Nothing Personal",
            slug="nothing-personal",
            seo_title="Nothing Personal",
            search_description="Nothing Personal articles.",
            theme="nothing_personal",
            locale=cls.default_locale,
        )
        cls.home_page.add_child(instance=cls.np_home)
        cls.np_home.save_revision().publish()

        model_instance = NothingPersonalArticlePage()
        cls.en_article = NothingPersonalArticlePage(
            title="Ultrahuman Ring Privacy Review",
            slug="ultrahuman-ring-privacy-review",
            seo_title="Ultrahuman Ring Privacy Review",
            theme="nothing_personal",
            locale=cls.default_locale,
            lede_text="English lede for topic listing test.",
            search_description="English search description.",
            displayed_hero_content=NothingPersonalArticlePage.HERO_CONTENT_VIDEO,
            hero_video_url=(
                "https://player.vimeo.com/progressive_redirect/playback/123456789/" "rendition/1080p/file.mp4"
            ),
            hero_image_alt_text="Test hero alt text",
        )
        cls.en_article.body = to_streamfield_value(
            [{"type": "rich_text", "value": "<p>English article body.</p>"}],
            stream_block=model_instance.body.stream_block,
        )
        cls.np_home.add_child(instance=cls.en_article)
        cls.en_article.topics.add(cls.topic)
        cls.en_article.save_revision().publish()

        cls.home_page.copy_for_translation(cls.fr_locale)
        cls.np_home.copy_for_translation(cls.fr_locale)
        cls.fr_article = cls.en_article.copy_for_translation(cls.fr_locale)
        cls.fr_article.title = "Analyse de confidentialité Ultrahuman Ring"
        cls.fr_article.seo_title = "Analyse de confidentialité Ultrahuman Ring"
        cls.fr_article.save_revision().publish()

    def test_french_topic_listing_links_to_french_articles(self):
        with translation.override(self.fr_locale.language_code):
            response = self.client.get("/fr/topics/privacy/")

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.fr_article.url)
            self.assertNotContains(response, self.en_article.url)

    def test_english_topic_listing_links_to_english_articles(self):
        with translation.override(self.default_locale.language_code):
            response = self.client.get("/en/topics/privacy/")

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.en_article.url)
