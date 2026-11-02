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


# TODO: Remove with the preview view once design review of the Cosmos
# navigation (TP1-4298) is done.
class NavigationPreviewTests(TestCase):
    def test_renders_the_site_header_alone(self):
        response = self.client.get(reverse("navigation_preview"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patterns/components/navigation/primary_nav.html")
        self.assertContains(response, "data-primary-nav")
        self.assertContains(response, '<main><h1 class="show-for-sr">Navigation preview</h1></main>', html=True)
        self.assertTemplateNotUsed(response, "patterns/components/footer.html")
        self.assertTemplateNotUsed(response, "patterns/components/footer/_footer.html")
        self.assertTemplateNotUsed(response, "patterns/components/donate_banner/donate_banner.html")
        self.assertTemplateNotUsed(response, "patterns/components/notice_banner/notice_banner.html")

    def test_is_kept_out_of_search_results(self):
        response = self.client.get(reverse("navigation_preview"))

        self.assertContains(response, '<meta name="robots" content="noindex">')
