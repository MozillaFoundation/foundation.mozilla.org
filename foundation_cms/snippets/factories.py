import factory
from factory.django import DjangoModelFactory
from wagtail.models import Locale

from foundation_cms.base.factories import ImageFactory
from foundation_cms.snippets.models import IllustratedNewsletterSignup, NewsletterSignup
from foundation_cms.snippets.models.newsletter_signup import FooterNewsletterSignup


class NewsletterSignupFactory(DjangoModelFactory):
    class Meta:
        model = NewsletterSignup

    name = factory.Faker("sentence", nb_words=3)
    cta_header = factory.Faker("sentence", nb_words=6)
    cta_description = factory.Faker("sentence", nb_words=10)
    button_text = "Sign Up"
    newsletter = "mozilla-foundation"
    layout = "expand_on_focus"
    locale = factory.LazyFunction(Locale.get_default)


class IllustratedNewsletterSignupFactory(DjangoModelFactory):
    class Meta:
        model = IllustratedNewsletterSignup

    name = factory.Faker("sentence", nb_words=3)
    heading = factory.Faker("sentence", nb_words=6)
    illustration = factory.SubFactory(ImageFactory)
    newsletter = "mozilla-foundation"
    locale = factory.LazyFunction(Locale.get_default)


def ensure_homepage_newsletters(site):
    """
    Ensure the homepage newsletters exist for the given site.
    Helper function used by the homepage factory to ensure the expected
    newsletters are available, and that the footer newsletter is
    assigned in the site settings.
    """
    locale = Locale.get_default()

    main_newsletter, _ = NewsletterSignup.objects.get_or_create(
        name="Main Newsletter",
        locale=locale,
        defaults={
            "cta_header": "The internet we deserve starts with you",
            "cta_description": "Join the movement now",
            "button_text": "Sign Up",
            "newsletter": "mozilla-foundation",
            "layout": "expand_on_focus",
        },
    )

    footer_newsletter, _ = NewsletterSignup.objects.get_or_create(
        name="Footer Newsletter",
        locale=locale,
        defaults={
            "cta_header": "Stay updated with our newsletter",
            "cta_description": "",
            "button_text": "Sign Up",
            "newsletter": "mozilla-foundation",
            "layout": "expand_on_focus",
        },
    )

    settings_obj = FooterNewsletterSignup.for_site(site)
    if settings_obj.newsletter_signup_id != footer_newsletter.id:
        settings_obj.newsletter_signup = footer_newsletter
        settings_obj.save()

    return {
        "main": main_newsletter,
        "footer": footer_newsletter,
    }
