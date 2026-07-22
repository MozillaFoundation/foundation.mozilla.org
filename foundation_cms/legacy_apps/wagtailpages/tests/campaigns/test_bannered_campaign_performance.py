"""
Query-count regression tests for the BanneredCampaignPage menu builder.

These guard the Phase 1 N+1 fix for `wagtail.views.serve` on bannered
campaign pages (ScoutAPM flagged ~283 SQL calls / ~10s, driven by the
mini-site menu being built one query per page).

The optimisation lives in `wagtailpages.utils.get_descendants` /
`get_menu_pages`: children are now fetched with `.specific()` (one query per
tree level instead of one per page) and the walk stops descending once it
reaches a depth the menu templates never render.

`assertNumQueries` is what measures before/after: if the count drifts, the
failure message prints the actual number. To see the pre-optimisation
baseline, `git stash` the changes to `utils.py` and run this test -- it will
fail and report the higher count.
"""

from django.test import RequestFactory
from wagtail.models import Page

from foundation_cms.legacy_apps.wagtailpages.factory import (
    bannered_campaign_page as bannered_factories,
)
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.legacy_apps.wagtailpages.utils import (
    get_menu_pages,
    get_page_tree_information,
)

# Expected query count for `get_menu_pages` over the tree built in setUpTestData
# (1 root + 4 children + 3 grandchildren = 8 menu entries). This is the
# post-optimisation target; update it if the realistic baseline genuinely
# shifts (the assertion error reports the actual count).
EXPECTED_MENU_QUERIES = 21


class BanneredCampaignMenuQueryCountTest(test_base.WagtailpagesTestCase):
    request_factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # A small but representative mini-site tree:
        #   root (depth 0)
        #   ├── child 0 (depth 1)
        #   │   ├── grandchild 0 (depth 2)
        #   │   ├── grandchild 1 (depth 2)
        #   │   └── grandchild 2 (depth 2)
        #   ├── child 1 (depth 1)
        #   ├── child 2 (depth 1)
        #   └── child 3 (depth 1)
        cls.root_page = bannered_factories.BanneredCampaignPageFactory(
            parent=cls.homepage,
            title="Root campaign",
            no_cta=True,
        )
        cls.children = [
            bannered_factories.BanneredCampaignPageFactory(
                parent=cls.root_page,
                title=f"Child campaign {i}",
                no_cta=True,
            )
            for i in range(4)
        ]
        cls.grandchildren = [
            bannered_factories.BanneredCampaignPageFactory(
                parent=cls.children[0],
                title=f"Grandchild campaign {i}",
                no_cta=True,
            )
            for i in range(3)
        ]

    def _fresh_root(self):
        """Return the root as a base Page, mirroring how `context['root']`
        reaches `get_menu_pages` during a real request (it is not guaranteed
        to already be the specific instance)."""
        return Page.objects.get(pk=self.root_page.pk)

    def test_get_menu_pages_query_count(self):
        root = self._fresh_root()

        with self.assertNumQueries(EXPECTED_MENU_QUERIES):
            menu_pages = get_menu_pages(root, authenticated=False)

        # The walk should not scale its query count with the number of pages:
        # adding more siblings must not reintroduce a per-page `.specific`
        # query. (See git-stashed baseline for the pre-fix number.)
        self.assertEqual(len(menu_pages), 8)

    def test_get_menu_pages_content_unchanged(self):
        """The optimisation must produce exactly the same menu data as before."""
        root = self._fresh_root()

        menu_pages = get_menu_pages(root, authenticated=False)

        depths = sorted(entry["depth"] for entry in menu_pages)
        self.assertEqual(depths, [0, 1, 1, 1, 1, 2, 2, 2])

        # Depth 0 is always the "Overview" label.
        overview = next(entry for entry in menu_pages if entry["depth"] == 0)
        self.assertEqual(overview["menu_title"], "Overview")
        self.assertEqual(overview["page"].pk, self.root_page.pk)

        # Non-root entries use the page header as their title.
        child_entry = next(
            entry for entry in menu_pages if entry["page"].pk == self.children[0].pk
        )
        self.assertEqual(child_entry["menu_title"], self.children[0].header)

        # No view restrictions configured, so every entry is unrestricted.
        self.assertTrue(all(entry["restriction"] is None for entry in menu_pages))

    def test_get_page_tree_information_flags(self):
        """`.exists()` refactor must keep the same singleton/uses_menu flags."""
        # Top of a multi-page tree -> not a singleton, and it does use a menu.
        root_context = get_page_tree_information(self._fresh_root(), {})
        self.assertTrue(root_context["is_top_page"])
        self.assertFalse(root_context["singleton_page"])
        self.assertTrue(root_context["uses_menu"])

        # A lone page (top of its own one-page "tree") -> singleton, no menu.
        lone = bannered_factories.BanneredCampaignPageFactory(
            parent=self.homepage,
            title="Lone campaign",
            no_cta=True,
        )
        lone_context = get_page_tree_information(Page.objects.get(pk=lone.pk), {})
        self.assertTrue(lone_context["is_top_page"])
        self.assertTrue(lone_context["singleton_page"])
        self.assertFalse(lone_context["uses_menu"])

    def test_get_context_does_not_compute_unused_related_posts(self):
        """`related_posts` is never rendered by the bannered-campaign template
        chain, so `get_context` must not compute it (it triggered a needless
        tag-matching query against BlogPage on every request)."""
        request = self.request_factory.get(self.root_page.url)
        # Normally set by Wagtail middleware; absent with RequestFactory.
        request.is_preview = False

        context = self.root_page.get_context(request)

        self.assertNotIn("related_posts", context)
        # The context the page actually uses is still present.
        self.assertIn("localized_signup", context)
        self.assertIn("root", context)
