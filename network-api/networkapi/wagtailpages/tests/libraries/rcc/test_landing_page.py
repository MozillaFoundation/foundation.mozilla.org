from networkapi.wagtailpages.tests.libraries.rcc import base


class RCCLandingPageTestCase(base.RCCHubTestCase):
    def test_page_loads(self):
        """
        Ensure that the page loads
        """
        response = self.client.get(self.landing_page.url)
        self.assertEqual(response.status_code, 200)

    def test_get_latest_rcc_pages_returns_three_latest_pages_by_publication_date(self):
        """
        Ensure that the latest RCC pages are returned
        """
        detail_page_1 = self.create_rcc_detail_page(days_ago=4)
        detail_page_2 = self.create_rcc_detail_page(days_ago=3)
        detail_page_3 = self.create_rcc_detail_page(days_ago=2)
        detail_page_4 = self.create_rcc_detail_page(days_ago=1)

        latest_rcc_pages = self.landing_page.get_latest_rcc_pages()

        self.assertEqual(len(latest_rcc_pages), 3)
        self.assertIn(detail_page_4, latest_rcc_pages)
        self.assertIn(detail_page_3, latest_rcc_pages)
        self.assertIn(detail_page_2, latest_rcc_pages)
        self.assertNotIn(detail_page_1, latest_rcc_pages)

    def test_get_latest_rcc_pages_does_not_return_private_page(self):
        """
        Ensure that the latest RCC pages don't contain private pages.
        """
        detail_page_public = self.create_rcc_detail_page()
        detail_page_private = self.create_rcc_detail_page()
        self.make_page_private(detail_page_private)

        latest_rcc_pages = self.landing_page.get_latest_rcc_pages()

        self.assertEqual(len(latest_rcc_pages), 1)
        self.assertIn(detail_page_public, latest_rcc_pages)
        self.assertNotIn(detail_page_private, latest_rcc_pages)

    def test_get_latest_rcc_pages_returns_detail_pages_of_same_locale(self):
        """
        Ensure that the latest RCC pages are returned in the same locale as the landing page.
        """
        # Create a detail page in the default locale
        self.create_rcc_detail_page()
        # Sync the tree to ensure that the detail page is created in the fr locale
        self.synchronize_tree()
        fr_landing_page = self.landing_page.get_translation(locale=self.fr_locale)

        latest_rcc_pages = fr_landing_page.get_latest_rcc_pages()

        self.assertEqual(len(latest_rcc_pages), 1)
        self.assertEqual(latest_rcc_pages[0].locale, self.fr_locale)
        self.assertEqual(latest_rcc_pages[0].locale, fr_landing_page.locale)

    def test_get_library_page_returns_library_page(self):
        """
        Ensure that the library page is returned.
        """
        library_page = self.landing_page.get_library_page()
        self.assertEqual(library_page, self.library_page)

    def test_get_library_page_returns_library_page_of_same_locale(self):
        """
        Ensure that the library page is returned in the same locale as the landing page.
        """
        fr_landing_page = self.landing_page.get_translation(locale=self.fr_locale)

        fr_library_page = fr_landing_page.get_library_page()

        self.assertEqual(fr_library_page.locale, self.fr_locale)
        self.assertEqual(fr_library_page.locale, fr_landing_page.locale)
