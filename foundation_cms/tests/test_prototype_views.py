from django.test import TestCase
from django.urls import reverse


# TODO: Remove with the preview view once the Our Work page type (TP1-4395)
# renders the Meteor hero.
class MeteorHeroPreviewTests(TestCase):
    def test_renders_hero_with_a_real_scroll_target(self):
        response = self.client.get(reverse("meteor_hero_preview"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 class="mzf-c-hero-primary__headline" id="meteor-hero-headline">')
        target_id = response.context["target_id"]
        self.assertContains(response, f'href="#{target_id}"')
        self.assertContains(response, f'id="{target_id}"')

    def test_is_kept_out_of_search_results(self):
        response = self.client.get(reverse("meteor_hero_preview"))

        self.assertContains(response, '<meta name="robots" content="noindex">')


class GalaxyHeroPreviewTests(TestCase):
    def test_renders_accessible_copy_and_real_scroll_target(self):
        response = self.client.get(reverse("galaxy_hero_preview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Mozilla Foundation expands")
        self.assertContains(response, "Because the future should be")
        self.assertContains(response, 'aria-hidden="true"')
        target = response.context["target_id"]
        self.assertContains(response, f'href="#{target}"')
        self.assertContains(response, f'id="{target}"')
        self.assertContains(response, '<meta name="robots" content="noindex">')

    def test_background_choices(self):
        for background in ("Gray", "Orange", "Yellow", "Blue"):
            with self.subTest(background=background):
                response = self.client.get(reverse("galaxy_hero_preview"), {"background": background})
                self.assertContains(response, f'data-background="{background}"')
        response = self.client.get(reverse("galaxy_hero_preview"), {"background": "unknown"})
        self.assertContains(response, 'data-background="Gray"')
