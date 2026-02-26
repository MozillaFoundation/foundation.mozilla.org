import factory
from factory.django import DjangoModelFactory
from wagtail import models as wagtail_models

from foundation_cms.base.utils.helpers import reseed
from foundation_cms.footer import models as footer_models


class FooterInternalLinkFactory(DjangoModelFactory):
    class Meta:
        model = footer_models.FooterInternalLink

    footer = None
    label = factory.Faker("sentence", nb_words=2)
    url = factory.LazyAttribute(lambda _: f"/{factory.Faker('slug').generate()}/")
    sort_order = factory.Sequence(lambda n: n)
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())


class FooterExternalLinkFactory(DjangoModelFactory):
    class Meta:
        model = footer_models.FooterExternalLink

    footer = None
    label = factory.Faker("sentence", nb_words=2)
    url = factory.Faker("url")
    sort_order = factory.Sequence(lambda n: n)
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())


class FooterSocialLinkFactory(DjangoModelFactory):
    class Meta:
        model = footer_models.FooterSocialLink

    footer = None
    platform = factory.Iterator(["bluesky", "instagram", "linkedin", "spotify", "tiktok"])
    url = factory.Faker("url")
    sort_order = factory.Sequence(lambda n: n)
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())


class SiteFooterFactory(DjangoModelFactory):
    class Meta:
        model = footer_models.SiteFooter

    title = factory.Faker("sentence", nb_words=2)
    legal_text = factory.Faker("paragraph")
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())

    @factory.post_generation
    def internal_links(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for link in extracted:
                link.footer = self
                link.save()
        else:
            for i in range(4):
                FooterInternalLinkFactory.create(footer=self, sort_order=i)

    @factory.post_generation
    def external_links(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for link in extracted:
                link.footer = self
                link.save()
        else:
            for i in range(5):
                FooterExternalLinkFactory.create(footer=self, sort_order=i)

    @factory.post_generation
    def social_links(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for link in extracted:
                link.footer = self
                link.save()
        else:
            platforms = ["bluesky", "instagram", "linkedin", "spotify", "tiktok"]
            for i, platform in enumerate(platforms):
                FooterSocialLinkFactory.create(footer=self, platform=platform, sort_order=i)


def generate(seed):
    """
    Generate default footer with real data from current footer.html.
    Called by load_redesign_data management command.
    """
    reseed(seed)

    footer, created = footer_models.SiteFooter.objects.get_or_create(
        title="Main Footer",
        defaults={
            "logo": None,
            "logo_link_url": "/",
            "show_donate_button": True,
            "donate_button_text": "Donate",
            "donate_button_url": "?form=donate-footer",
            "show_language_switcher": True,
            "show_newsletter_signup": True,
            "legal_text": (
                "<p>Mozilla Foundation is a global non-profit and parent of the "
                '<a target="_blank" rel="noopener noreferrer" href="https://www.mozilla.org/">Mozilla Corporation</a>. '
                'Most content available under a <a href="/meet-mozilla/website-licensing/">Creative Commons license</a>.</p>'
            ),
            "locale": wagtail_models.Locale.get_default(),
        },
    )

    if created:
        print("Generating Main Footer")

        # Internal links
        internal_links = [
            ("Licensing", "/meet-mozilla/website-licensing/"),
            ("Annual Reports & Financials", "/meet-mozilla/annual-reports-and-financials/"),
            ("Press Center", "/meet-mozilla/press-center/"),
            ("Grantmaking", "/what-we-do/grantmaking/"),
        ]

        for i, (label, url) in enumerate(internal_links):
            footer_models.FooterInternalLink.objects.create(
                footer=footer, label=label, url=url, sort_order=i, locale=footer.locale
            )

        # External links
        external_links = [
            ("Careers", "https://www.mozilla.org/careers/listings/?team=Mozilla%20Foundation"),
            ("Privacy", "https://www.mozilla.org/privacy/websites/"),
            ("Cookies", "https://www.mozilla.org/privacy/websites/"),
            ("Legal", "https://www.mozilla.org/about/legal/terms/mozilla/"),
            ("Participation guidelines", "https://www.mozilla.org/about/governance/policies/participation/"),
        ]

        for i, (label, url) in enumerate(external_links):
            footer_models.FooterExternalLink.objects.create(
                footer=footer, label=label, url=url, sort_order=i, locale=footer.locale
            )

        # Social links
        social_links = [
            ("bluesky", "https://bsky.app/profile/mozilla.org"),
            ("instagram", "https://www.instagram.com/mozilla/"),
            ("linkedin", "https://www.linkedin.com/company/mozilla-corporation/"),
            ("spotify", "https://open.spotify.com/show/0vT7LJMeVDxyQ2ZamHKu08"),
            ("tiktok", "https://www.tiktok.com/@mozilla"),
        ]

        for i, (platform, url) in enumerate(social_links):
            footer_models.FooterSocialLink.objects.create(
                footer=footer, platform=platform, url=url, sort_order=i, locale=footer.locale
            )
    else:
        print("Main Footer exists")

    # Activate footer
    print("Activating Main Footer")
    site = wagtail_models.Site.objects.first()
    settings_obj = footer_models.SiteFooterSettings.for_site(site)
    settings_obj.active_footer = footer
    settings_obj.save()

    return footer
