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
