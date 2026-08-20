from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import SimpleTestCase


class HomePageHeroItemTemplateTests(SimpleTestCase):
    def render_hero(self, orientation, **overrides):
        context = {
            "author": None,
            "displayed_hero_content": "video",
            "hero_video_url": "https://example.com/hero.mp4",
            "hero_image": None,
            "hero_image_alt_text": "Hero artwork",
            "title": "A prominent hero headline",
            "url": "/nothing-personal/hero/",
        }
        context.update(overrides)

        return render_to_string(
            "patterns/components/nothing_personal/home_page/_hero_item.html",
            {"hero_item": SimpleNamespace(**context), "orientation": orientation},
        )

    def test_square_and_landscape_titles_use_centered_eight_column_span(self):
        expected_title_class = 'class="featured-hero-item__text cell small-12 large-8 large-offset-2"'

        for orientation in ("square", "landscape"):
            with self.subTest(orientation=orientation):
                self.assertIn(expected_title_class, self.render_hero(orientation))

    def test_square_and_landscape_media_classes_are_preserved(self):
        expected_media_classes = {
            "square": (
                "featured-hero-item__media featured-hero-item__media--square " "cell small-12 large-6 large-offset-3"
            ),
            "landscape": (
                "featured-hero-item__media featured-hero-item__media--landscape "
                "cell small-12 large-8 large-offset-2"
            ),
        }

        for orientation, classes in expected_media_classes.items():
            with self.subTest(orientation=orientation):
                html = self.render_hero(orientation)
                self.assertIn(f'class="{classes}"', html)
                self.assertIn('href="/nothing-personal/hero/"', html)
                self.assertIn(
                    '<source src="https://example.com/hero.mp4" type="video/mp4">',
                    html,
                )

    def test_webp_image_and_author_are_preserved(self):
        image = SimpleNamespace(
            file=SimpleNamespace(name="hero.webp", url="/media/hero.webp"),
            height=900,
            title="Hero image title",
            width=1600,
        )

        html = self.render_hero(
            "landscape",
            author=SimpleNamespace(name="Hero Author"),
            displayed_hero_content="image",
            hero_image=image,
            hero_video_url="",
        )

        self.assertIn('src="/media/hero.webp"', html)
        self.assertIn('alt="Hero artwork"', html)
        self.assertIn("Hero Author", html)


class ArticlePageHeaderTemplateTests(SimpleTestCase):
    def render_header(self, **overrides):
        context = {
            "author": SimpleNamespace(name="Article Author"),
            "displayed_hero_content": "video",
            "hero_caption": "Hero caption",
            "hero_image": None,
            "hero_image_alt_text": "Article hero artwork",
            "hero_video_url": "https://example.com/article.mp4",
            "title": "A centered article headline",
        }
        context.update(overrides)

        return render_to_string(
            "patterns/components/nothing_personal/_article_page_header.html",
            {"page": SimpleNamespace(**context)},
        )

    def test_meta_and_media_use_confirmed_grid_spans(self):
        html = self.render_header()

        self.assertIn(
            'class="article-header__meta cell small-12 medium-10 medium-offset-1 ' 'large-8 large-offset-2"',
            html,
        )
        self.assertIn('class="article-header__hero cell small-12"', html)

    def test_video_author_and_caption_are_preserved(self):
        html = self.render_header()

        self.assertIn("A centered article headline", html)
        self.assertIn("Article Author", html)
        self.assertIn(
            '<source src="https://example.com/article.mp4" type="video/mp4">',
            html,
        )
        self.assertIn('<p class="article-header__hero-caption">Hero caption</p>', html)

    def test_webp_image_attributes_and_caption_are_preserved(self):
        image = SimpleNamespace(
            file=SimpleNamespace(name="article.webp", url="/media/article.webp"),
            height=900,
            title="Article image title",
            width=1600,
        )

        html = self.render_header(
            displayed_hero_content="image",
            hero_image=image,
            hero_video_url="",
        )

        self.assertIn('src="/media/article.webp"', html)
        self.assertIn('width="1600"', html)
        self.assertIn('height="900"', html)
        self.assertIn('alt="Article hero artwork"', html)
        self.assertIn('loading="lazy"', html)
        self.assertIn('<p class="article-header__hero-caption">Hero caption</p>', html)
