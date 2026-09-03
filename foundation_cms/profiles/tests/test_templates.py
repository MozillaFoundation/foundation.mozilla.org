import re
from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import SimpleTestCase
from wagtail.models import Site
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.base.utils.helpers import to_streamfield_value
from foundation_cms.core.factories import HomePageFactory
from foundation_cms.profiles.factories import (
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
)


class ExpertProfileTemplateTests(WagtailPageTestCase):
    def setUp(self):
        self.root = HomePageFactory()
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            site.root_page = self.root
            site.hostname = "testserver"
            site.port = 80
            site.save(update_fields=["root_page", "hostname", "port"])
        else:
            Site.objects.create(
                hostname="testserver",
                port=80,
                root_page=self.root,
                is_default_site=True,
            )
        self.hub = ExpertHubPageFactory(parent=self.root)
        self.page = ExpertProfilePageFactory(
            parent=self.hub,
            quote="Legacy quote must not render",
            quote_attribution="Legacy attribution",
            linkedin_url="https://www.linkedin.com/in/example",
            bluesky_url="",
            facebook_url="https://www.facebook.com/example",
            instagram_url="",
            tiktok_url="https://www.tiktok.com/@example",
        )
        self.page.body = to_streamfield_value(
            [
                {
                    "type": "quote",
                    "value": {"quote": "Body quote", "attribution": "Body attribution"},
                },
                {
                    "type": "projects_section",
                    "value": {
                        "source": "curated",
                        "items": [
                            {
                                "type": "manual_project",
                                "value": {
                                    "title": "Manual project",
                                    "description": "Manual project description",
                                    "url": "https://example.com/project",
                                    "link_label": "Project details",
                                },
                            }
                        ],
                    },
                },
                {
                    "type": "articles_section",
                    "value": {
                        "items": [
                            {
                                "type": "manual_article",
                                "value": {
                                    "title": "Manual article",
                                    "description": "Manual article description",
                                    "url": "https://www.example.org/article",
                                },
                            }
                        ]
                    },
                },
                {
                    "type": "link_section",
                    "value": {
                        "heading": "Awards & Recognition",
                        "rows": [
                            {
                                "type": "link",
                                "value": {
                                    "title": "Linked award",
                                    "description": "Linked description",
                                    "url": "https://example.net/award",
                                },
                            },
                            {
                                "type": "link",
                                "value": {
                                    "title": "Unlinked award",
                                    "description": "Unlinked description",
                                    "url": "",
                                },
                            },
                        ],
                    },
                },
            ],
            stream_block=self.page.body.stream_block,
        )
        self.page.save_revision().publish()

    def test_renders_body_sections_and_not_legacy_quote(self):
        response = self.client.get(self.page.url)

        self.assertContains(response, "Body quote")
        self.assertContains(response, "Body attribution")
        self.assertContains(response, "Manual project")
        self.assertContains(response, "Manual article")
        self.assertNotContains(response, "expert-profile-article-list__source")
        self.assertContains(response, "Articles & Publications")
        self.assertContains(response, 'class="expert-profile-article-list__manual-link"')
        self.assertContains(response, "Awards &amp; Recognition")
        self.assertNotContains(response, "Legacy quote must not render")

    def test_url_less_link_row_is_not_an_anchor(self):
        response = self.client.get(self.page.url)

        self.assertContains(response, '<div class="expert-profile-link-list__text">')
        self.assertContains(response, '<span class="expert-profile-link-list__content">', count=2)
        self.assertContains(response, '<a class="expert-profile-link-list__link"', count=1)
        self.assertContains(response, "Unlinked award")

    def test_renders_only_populated_accessible_social_links(self):
        response = self.client.get(self.page.url)

        self.assertContains(response, "Where to find me")
        self.assertContains(response, "Visit LinkedIn (opens in a new tab)")
        self.assertContains(response, "Visit Facebook (opens in a new tab)")
        self.assertContains(response, "Visit TikTok (opens in a new tab)")
        self.assertNotContains(response, "Visit Bluesky")
        self.assertNotContains(response, "Visit Instagram")

    def test_bio_has_accessible_progressive_enhancement_controls(self):
        response = self.client.get(self.page.url)
        content = response.content.decode()

        self.assertContains(response, 'data-collapsed-char-limit="600"')
        self.assertContains(response, 'aria-controls="expert-profile-bio"')
        self.assertContains(response, 'aria-expanded="false"')
        self.assertContains(response, 'data-show-more-label="Show more"')
        self.assertContains(
            response,
            "data-expert-profile-bio-toggle-label>Show more</span>",
        )
        self.assertLess(
            content.index('class="expert-profile-intro__image"'),
            content.index('class="expert-profile-intro__bio"'),
        )

    def test_does_not_render_expert_hub_cta(self):
        response = self.client.get(self.page.url)

        self.assertNotContains(response, "expert-profile-cta")
        self.assertNotContains(response, "Want to collab?")


class ExpertProfileSectionTemplateTests(SimpleTestCase):
    def test_manual_project_is_a_natural_text_only_entry(self):
        project = SimpleNamespace(
            title="Manual project without image",
            description="A deliberate text-only project entry.",
            url="https://example.com/project-without-image",
            link_label="Project details",
        )

        rendered = render_to_string(
            "patterns/blocks/themes/default/expert_profile_projects_section_block.html",
            {"rendered_items": [{"type": "manual_project", "value": project}]},
        )

        self.assertIn("Manual project without image", rendered)
        self.assertIn("A deliberate text-only project entry.", rendered)
        self.assertNotIn("<img", rendered)
        self.assertEqual(rendered.count('target="_blank"'), 2)
        self.assertEqual(rendered.count('rel="noopener noreferrer"'), 2)
        self.assertEqual(rendered.count("(opens in a new tab)"), 2)
        self.assertNotIn("project-block", rendered)

    def test_cms_project_uses_profile_card_with_media_topic_and_alt_text(self):
        def get_rendition(_spec):
            return SimpleNamespace(
                url="/media/cms-project-720x489.jpg",
                width=720,
                height=489,
                alt="",
            )

        image = SimpleNamespace(
            file=SimpleNamespace(name="cms-project.jpg"),
            get_rendition=get_rendition,
            title="Community project image",
        )
        topic = SimpleNamespace(
            name="Security",
            get_topic_listing_url="/topics/security/",
        )
        project = SimpleNamespace(
            title="CMS project",
            url="/gallery/cms-project/",
            hero_image=image,
            hero_image_alt_text="People collaborating on community technology",
            lede_text="A CMS project description.",
            topics=SimpleNamespace(all=[topic]),
        )
        project.specific = project

        rendered = render_to_string(
            "patterns/blocks/themes/default/expert_profile_projects_section_block.html",
            {
                "rendered_items": [
                    {
                        "type": "cms_project",
                        "value": SimpleNamespace(project=project),
                    }
                ]
            },
        )

        self.assertIn("expert-profile-project-card--with-media", rendered)
        self.assertIn('alt="People collaborating on community technology"', rendered)
        self.assertIn('class="btn-topic expert-profile-project-card__topic"', rendered)
        self.assertIn(">Security</a>", rendered)
        self.assertIn("A CMS project description.", rendered)
        self.assertNotIn("project-block", rendered)
        self.assertNotIn("program-label", rendered)
        self.assertNotIn("pagination-controls", rendered)

    def test_cms_project_blank_alt_text_falls_back_to_image_title(self):
        def get_rendition(_spec):
            return SimpleNamespace(
                url="/media/cms-project-720x489.jpg",
                width=720,
                height=489,
                alt="",
            )

        image = SimpleNamespace(
            file=SimpleNamespace(name="cms-project.jpg"),
            get_rendition=get_rendition,
            title="Community project image",
        )
        project = SimpleNamespace(
            title="CMS project",
            url="/gallery/cms-project/",
            hero_image=image,
            hero_image_alt_text="",
            lede_text="A CMS project description.",
            topics=SimpleNamespace(all=[]),
        )
        project.specific = project

        rendered = render_to_string(
            "patterns/blocks/themes/default/expert_profile_projects_section_block.html",
            {
                "rendered_items": [
                    {
                        "type": "cms_project",
                        "value": SimpleNamespace(project=project),
                    }
                ]
            },
        )

        self.assertIn('alt="Community project image"', rendered)

    def test_cms_article_renders_its_search_image_with_maintained_alt_text(self):
        def get_rendition(spec):
            width, height = [int(value) for value in re.findall(r"\d+", spec)]
            return SimpleNamespace(
                url=f"/media/article-{width}x{height}.jpg",
                width=width,
                height=height,
                alt="Article search image",
            )

        image = SimpleNamespace(
            file=SimpleNamespace(name="article.jpg"),
            get_rendition=get_rendition,
            title="Article search image",
        )
        article = SimpleNamespace(
            url="/nothing-personal/article/",
            title="CMS article",
            search_description="CMS article description",
            search_image=image,
        )

        rendered = render_to_string(
            "patterns/blocks/themes/default/expert_profile_articles_section_block.html",
            {
                "rendered_items": [{"type": "cms_article", "value": article}],
                "visible_count": 3,
            },
        )

        self.assertIn("Articles & Publications", rendered)
        self.assertIn('class="expert-profile-article-list__cms"', rendered)
        self.assertIn('class="expert-profile-article-list__media-image"', rendered)
        self.assertIn('alt="Article search image"', rendered)
        self.assertIn('sizes="64px"', rendered)
        self.assertIn("64w", rendered)
        self.assertIn("CMS article description", rendered)
        self.assertNotIn("topic-pills", rendered)
        self.assertNotIn("page-card__image-wrapper", rendered)

    def test_cms_article_without_search_image_uses_neutral_fallback(self):
        article = SimpleNamespace(
            url="/nothing-personal/article/",
            title="CMS article",
            search_description="CMS article description",
            search_image=None,
        )

        rendered = render_to_string(
            "patterns/blocks/themes/default/expert_profile_articles_section_block.html",
            {"rendered_items": [{"type": "cms_article", "value": article}]},
        )

        self.assertIn("expert-profile-article-list__media--fallback", rendered)
        self.assertNotIn("<img", rendered)

    def test_manual_article_omits_source_hostname(self):
        article = SimpleNamespace(
            title="Manual article",
            description="Manual article description",
            url="https://www.example.org/article",
        )

        rendered = render_to_string(
            "patterns/blocks/themes/default/expert_profile_articles_section_block.html",
            {"rendered_items": [{"type": "manual_article", "value": article}]},
        )

        self.assertNotIn("expert-profile-article-list__source", rendered)
        self.assertIn("(opens in a new tab)", rendered)
        self.assertNotIn("expert-profile-article-list__media", rendered)
