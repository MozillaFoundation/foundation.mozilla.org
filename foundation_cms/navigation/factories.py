from copy import deepcopy

import factory
import wagtail_factories
from django.db import transaction
from factory.django import DjangoModelFactory
from faker import Faker as _Faker
from wagtail import models as wagtail_models

from foundation_cms.navigation import blocks as nav_blocks
from foundation_cms.navigation import models as nav_models

_fake = _Faker()


def _relative_link(label, url):
    return {
        "label": label,
        "link_to": "relative_url",
        "page": None,
        "external_url": "",
        "relative_url": url,
    }


DEFAULT_MAIN_NAVIGATION = [
    {
        "type": "dropdown",
        "value": {
            "header": _relative_link("Meet Mozilla", "/meet-mozilla/"),
            "items": [],
        },
    },
    {
        "type": "dropdown",
        "value": {
            "header": _relative_link("What We Do", "/what-we-do/"),
            "items": [
                _relative_link("Imagine", "/what-we-do/imagine/"),
                _relative_link("Co-create", "/what-we-do/co-create/"),
                _relative_link("Mobilize", "/what-we-do/mobilize/"),
            ],
        },
    },
    {
        "type": "dropdown",
        "value": {
            "header": _relative_link("Join Us", "/join-us/"),
            "items": [],
        },
    },
    {
        "type": "dropdown",
        "value": {
            "header": _relative_link("Nothing Personal", "/nothing-personal/"),
            "items": [],
        },
    },
]


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


class NavigationMenuFactory(DjangoModelFactory):
    class Meta:
        model = nav_models.NavigationMenu

    title = factory.Faker("sentence", nb_words=3)
    dropdowns = wagtail_factories.StreamFieldFactory(
        {"dropdown": factory.SubFactory(NavDropdownFactory)},
        **{
            "0": "dropdown",
            "1": "dropdown",
            "2": "dropdown",
            "3": "dropdown",
        },
    )
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())


class HorizontalLinkBlockFactory(DjangoModelFactory):
    class Meta:
        model = nav_models.HorizontalLinkBlock

    title = factory.Faker("sentence", nb_words=3)
    links = wagtail_factories.StreamFieldFactory(
        {"link": factory.SubFactory(NavLinkFactory, relative_url_link=True)},
        **{
            "0": "link",
            "1": "link",
            "2": "link",
        },
    )
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())


def generate(site):
    """Return the site's active menu, creating a deterministic default only when needed."""
    with transaction.atomic():
        site_navigation = nav_models.SiteNavigationMenu.for_site(site)
        site_navigation = nav_models.SiteNavigationMenu.objects.select_for_update().get(pk=site_navigation.pk)

        if site_navigation.active_navigation_menu_id:
            return site_navigation.active_navigation_menu

        default_locale = wagtail_models.Locale.get_default()
        menu = (
            nav_models.NavigationMenu.objects.filter(title="Main Navigation", locale=default_locale)
            .order_by("pk")
            .first()
        )

        if menu is None:
            dropdowns = nav_models.NavigationMenu.dropdowns.field.stream_block.to_python(
                deepcopy(DEFAULT_MAIN_NAVIGATION)
            )
            menu = nav_models.NavigationMenu.objects.create(
                title="Main Navigation",
                dropdowns=dropdowns,
                locale=default_locale,
            )
            print("Generating Main Navigation")
        else:
            print("Main Navigation exists")

        print("Activating Main Navigation")
        site_navigation.active_navigation_menu = menu
        site_navigation.save(update_fields=["active_navigation_menu"])

        return menu
