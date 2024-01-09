import factory
import wagtail_factories

from networkapi.wagtailcustomization.factories.snippets import (
    SnippetChooserBlockFactory,
)
from networkapi.wagtailpages.models import BlogSignup, Signup
from networkapi.wagtailpages.pagemodels import customblocks


class SignupChooserBlockFactory(SnippetChooserBlockFactory):
    snippet = factory.SubFactory("networkapi.wagtailpages.factory.signup.SignupFactory")

    class Meta:
        model = Signup


class NewsletterSignupBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.NewsletterSignupBlock

    signup = factory.SubFactory(SignupChooserBlockFactory)


class BlogSignupChooserBlockFactory(SnippetChooserBlockFactory):
    snippet = factory.SubFactory("networkapi.wagtailpages.factory.signup.BlogSignupFactory")

    class Meta:
        model = BlogSignup


class BlogNewsletterSignupBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.BlogNewsletterSignupBlock

    signup = factory.SubFactory(BlogSignupChooserBlockFactory)
