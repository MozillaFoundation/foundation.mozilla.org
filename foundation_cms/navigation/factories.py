import factory
import wagtail_factories
from factory.django import DjangoModelFactory
from faker import Faker as _Faker
from wagtail import models as wagtail_models

from foundation_cms.base.utils.helpers import reseed
from foundation_cms.navigation import blocks as nav_blocks
from foundation_cms.navigation import models as nav_models

_fake = _Faker()

DEFAULT_NAV_DROPDOWNS = (
    (
        ("Meet Mozilla", "/meet-mozilla/"),
        (),
    ),
    (
        ("What We Do", "/what-we-do/"),
        (
            ("Imagine", "/what-we-do/imagine/"),
            ("Co-create", "/what-we-do/co-create/"),
            ("Mobilize", "/what-we-do/mobilize/"),
        ),
    ),
    (
        ("Join Us", "/join-us/"),
        (),
    ),
    (
        ("Nothing Personal", "/nothing-personal/"),
        (),
    ),
)

DEFAULT_SEARCH_TOPIC_LINKS = (
    ("privacy", "privacy"),
    ("personal data", "personal data"),
    ("open source", "open source"),
    ("encryption", "encryption"),
    ("ai", "ai"),
)

DEFAULT_SEARCH_QUICK_LINKS = (
    ("Grantmaking", "/what-we-do/awards/"),
    ("Mozilla Festival", "/festival/"),
    ("Common Voice", "/common-voice/"),
)


class NavLinkFactory(wagtail_factories.StructBlockFactory):
    """
    Factory for NavLink.

    Use traits:
      - page_link
      - external_url_link
      - relative_url_link
    """

    class Meta:
        model = nav_blocks.NavLink

    class Params:
        page_link = factory.Trait(
            link_to="page",
            page=factory.Iterator(wagtail_models.Page.objects.filter(locale_id="1")),
        )
        external_url_link = factory.Trait(
            link_to="external_url",
            external_url=factory.Sequence(lambda n: f"https://example-{n}.com/"),
        )
        relative_url_link = factory.Trait(
            link_to="relative_url",
            relative_url=factory.LazyFunction(lambda: f"/{_fake.uri_path()}"),
        )

    label = factory.Faker("sentence", nb_words=2, variable_nb_words=False)

    # Defaults (use a trait in practice to ensure validity)
    link_to = "external_url"
    page = None
    external_url = ""
    relative_url = ""


class NavDropdownFactory(wagtail_factories.StructBlockFactory):
    """
    Factory for NavDropdown (header link + up to 5 items).
    """

    class Meta:
        model = nav_blocks.NavDropdown

    class Params:
        # Convenience trait: header is a page link
        header_page_link = factory.Trait(
            header=factory.SubFactory(NavLinkFactory, page_link=True),
        )
        # Convenience trait: header is an external link
        header_external_link = factory.Trait(
            header=factory.SubFactory(NavLinkFactory, external_url_link=True),
        )
        # Convenience trait: header is a relative link
        header_relative_link = factory.Trait(
            header=factory.SubFactory(NavLinkFactory, relative_url_link=True),
        )

    header = factory.SubFactory(NavLinkFactory, external_url_link=True)
    items = wagtail_factories.ListBlockFactory(
        NavLinkFactory,
        **{
            "0__external_url_link": True,
            "1__external_url_link": True,
            "2__external_url_link": True,
        },
    )


class SearchTopicLinkFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = nav_blocks.SearchTopicLink

    label = factory.Faker("word")
    query = factory.Faker("word")


def relative_nav_link(label, relative_url):
    return {
        "label": label,
        "link_to": "relative_url",
        "page": None,
        "external_url": "",
        "relative_url": relative_url,
    }


def default_dropdowns():
    payload = [
        {
            "type": "dropdown",
            "value": {
                "header": relative_nav_link(label, relative_url),
                "items": [relative_nav_link(item_label, item_url) for item_label, item_url in items],
            },
        }
        for (label, relative_url), items in DEFAULT_NAV_DROPDOWNS
    ]
    return nav_models.NavigationMenu.dropdowns.field.stream_block.to_python(payload)


def default_search_topic_links():
    payload = [
        {
            "type": "topic",
            "value": {
                "label": label,
                "query": query,
            },
        }
        for label, query in DEFAULT_SEARCH_TOPIC_LINKS
    ]
    return nav_models.NavigationMenu.search_topic_links.field.stream_block.to_python(payload)


def default_search_quick_links():
    payload = [
        {
            "type": "quick_link",
            "value": {
                "label": label,
                "link_to": "relative_url",
                "page": None,
                "external_url": "",
                "relative_url": relative_url,
            },
        }
        for label, relative_url in DEFAULT_SEARCH_QUICK_LINKS
    ]
    return nav_models.NavigationMenu.search_quick_links.field.stream_block.to_python(payload)


class NavigationMenuFactory(DjangoModelFactory):
    class Meta:
        model = nav_models.NavigationMenu

    title = factory.Faker("sentence", nb_words=3)
    dropdowns = factory.LazyFunction(default_dropdowns)
    search_topic_links = factory.LazyFunction(default_search_topic_links)
    search_quick_links = factory.LazyFunction(default_search_quick_links)
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())


def generate(seed):
    reseed(seed)

    menu, created = nav_models.NavigationMenu.objects.get_or_create(
        title="Main Navigation",
        defaults={
            "dropdowns": default_dropdowns(),
            "search_topic_links": default_search_topic_links(),
            "search_quick_links": default_search_quick_links(),
            "locale": wagtail_models.Locale.get_default(),
        },
    )

    if created:
        print("Generating Main Navigation")
    else:
        print("Main Navigation exists")

    # Activate menu
    print("Activating Main Navigation")
    site = wagtail_models.Site.objects.first()
    site_active_nav = nav_models.SiteNavigationMenu.for_site(site)
    site_active_nav.active_navigation_menu = menu
    site_active_nav.save()
