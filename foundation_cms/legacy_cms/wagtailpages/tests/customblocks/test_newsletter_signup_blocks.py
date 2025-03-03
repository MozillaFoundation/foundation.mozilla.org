from django.test import TestCase

from foundation_cms.legacy_cms.wagtailpages.factory import (
    customblocks as customblock_factories,
)
from foundation_cms.legacy_cms.wagtailpages.models import BlogSignup, Signup


class TestNewsletterSignupBlock(TestCase):
    def test_newsletter_signup_block(self):
        Signup.objects.all().delete()
        self.assertEqual(Signup.objects.count(), 0)
        signup_block = customblock_factories.NewsletterSignupBlockFactory()
        self.assertTrue(isinstance(signup_block["signup"], Signup))
        self.assertEqual(Signup.objects.count(), 1)


class TestBlogNewsletterSignupBlock(TestCase):
    def test_blog_newsletter_signup_block(self):
        BlogSignup.objects.all().delete()
        self.assertEqual(BlogSignup.objects.count(), 0)
        signup_block = customblock_factories.BlogNewsletterSignupBlockFactory()
        self.assertTrue(isinstance(signup_block["signup"], BlogSignup))
        self.assertEqual(BlogSignup.objects.count(), 1)
