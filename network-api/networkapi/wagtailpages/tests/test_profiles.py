from django import test

from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.factory import profiles as profile_factories
from networkapi.wagtailpages.pagemodels import profiles as profile_models
from networkapi.wagtailpages.pagemodels.blog.blog import BlogAuthors


class ProfileTest(test.TestCase):
    def test_factory(self):
        profile_factories.ProfileFactory()
        self.assertTrue(True)

    def test_filter_blog_authors(self):
        author_profile = profile_factories.ProfileFactory()
        blog_index = blog_factories.BlogIndexPageFactory()
        blog_factories.BlogPageFactory(parent=blog_index, authors=[BlogAuthors(author=author_profile)])
        not_blog_author_profile = profile_factories.ProfileFactory()

        blog_author_profiles = profile_models.Profile.objects.filter_blog_authors()

        self.assertIn(author_profile, blog_author_profiles)
        self.assertNotIn(not_blog_author_profile, blog_author_profiles)
