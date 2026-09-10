from datetime import timedelta
from http import HTTPStatus

from django.utils import timezone
from wagtail.models import Locale, Page, Site
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.campaigns.models import CampaignPage, Petition
from foundation_cms.campaigns.models.campaign_page import (
    CampaignPageKeepContributingRelation,
)
from foundation_cms.core.models import HomePage


class CampaignPageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.locale = Locale.get_default()
        self.petition = Petition.objects.create(
            name="Test petition",
            campaign_name="Test campaign",
            locale=self.locale,
        )
        self.home_page = self._add_page(
            Page.get_first_root_node(),
            HomePage,
            title="Campaign test home",
            slug="campaign-test-home",
        )

        site = Site.objects.get(is_default_site=True)
        site.root_page = self.home_page
        site.save()

        self.page = self._add_campaign(
            title="Campaign under test",
            slug="campaign-under-test",
        )

    def test_serve_defaults_to_start_state(self):
        response = self.client.get(self.page.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["state"], "start")
        self.assertContains(response, 'data-state="start"')
        self.assertTemplateUsed(
            response,
            "campaigns/components/campaign_page/form_state/01_start.html",
        )

    def test_serve_renders_each_state(self):
        state_templates = {
            "start": "campaigns/components/campaign_page/form_state/01_start.html",
            "signed": "campaigns/components/campaign_page/form_state/02_signed.html",
            "sharing": "campaigns/components/campaign_page/form_state/03_sharing.html",
            "end": "campaigns/components/campaign_page/form_state/04_end.html",
        }

        for state, template in state_templates.items():
            with self.subTest(state=state):
                response = self.client.get(self.page.url, {"state": state})

                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(response.context["state"], state)
                self.assertContains(response, f'data-state="{state}"')
                self.assertTemplateUsed(response, template)

    def test_serve_redirects_post_actions_and_preserves_medium(self):
        action_states = {
            "share": "sharing",
            "skip": "end",
        }

        for action, state in action_states.items():
            with self.subTest(action=action):
                response = self.client.post(
                    f"{self.page.url}?medium=email",
                    {"action": action},
                )

                self.assertRedirects(
                    response,
                    f"{self.page.url}?state={state}&medium=email",
                    fetch_redirect_response=False,
                )

    def test_keep_contributing_uses_exactly_two_selected_pages_in_order(self):
        first_selected = self._add_campaign(
            title="First selected campaign",
            slug="first-selected-campaign",
        )
        second_selected = self._add_campaign(
            title="Second selected campaign",
            slug="second-selected-campaign",
        )
        CampaignPageKeepContributingRelation.objects.create(
            page=self.page,
            keep_contributing_page=first_selected,
            sort_order=1,
            locale=self.locale,
        )
        CampaignPageKeepContributingRelation.objects.create(
            page=self.page,
            keep_contributing_page=second_selected,
            sort_order=0,
            locale=self.locale,
        )

        pages = list(self.page.get_keep_contributing_pages())

        self.assertEqual(pages, [second_selected, first_selected])

    def test_keep_contributing_uses_two_latest_topic_pages_and_excludes_self(self):
        topic = Topic.objects.create(name="Privacy", slug="privacy")
        now = timezone.now()
        latest = self._add_campaign(
            title="Latest topic campaign",
            slug="latest-topic-campaign",
            first_published_at=now,
            topic=topic,
        )
        second_latest = self._add_campaign(
            title="Second latest topic campaign",
            slug="second-latest-topic-campaign",
            first_published_at=now - timedelta(days=1),
            topic=topic,
        )
        self._add_campaign(
            title="Older topic campaign",
            slug="older-topic-campaign",
            first_published_at=now - timedelta(days=2),
            topic=topic,
        )
        self._add_campaign(
            title="Unrelated campaign",
            slug="unrelated-campaign",
            first_published_at=now + timedelta(days=1),
        )
        self.page.keep_contributing_topic = topic
        self.page.topics.add(topic)
        self.page.save_revision().publish()

        pages = self.page.get_keep_contributing_pages()

        self.assertEqual(pages, [latest, second_latest])
        self.assertNotIn(self.page, pages)

    def test_keep_contributing_falls_back_to_two_latest_campaigns_and_excludes_self(self):
        now = timezone.now()
        latest = self._add_campaign(
            title="Latest campaign",
            slug="latest-campaign",
            first_published_at=now,
        )
        second_latest = self._add_campaign(
            title="Second latest campaign",
            slug="second-latest-campaign",
            first_published_at=now - timedelta(days=1),
        )
        self._add_campaign(
            title="Older campaign",
            slug="older-campaign",
            first_published_at=now - timedelta(days=2),
        )

        pages = self.page.get_keep_contributing_pages()

        self.assertEqual(pages, [latest, second_latest])
        self.assertNotIn(self.page, pages)

    def _add_campaign(self, **kwargs):
        return self._add_page(
            self.home_page,
            CampaignPage,
            cta=self.petition,
            **kwargs,
        )

    def _add_page(self, parent, model, topic=None, **kwargs):
        page = model(
            locale=self.locale,
            seo_title=kwargs["title"],
            search_description=f'{kwargs["title"]} description.',
            **kwargs,
        )
        parent.add_child(instance=page)
        if topic:
            page.topics.add(topic)
        page.save_revision().publish()
        page.refresh_from_db()
        return page
