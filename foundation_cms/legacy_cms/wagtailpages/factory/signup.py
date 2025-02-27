from legacy_cms.wagtailpages.models import BlogSignup, Signup

from .abstract import CTAFactory


class SignupFactory(CTAFactory):
    class Meta:
        model = Signup


class BlogSignupFactory(CTAFactory):
    class Meta:
        model = BlogSignup
