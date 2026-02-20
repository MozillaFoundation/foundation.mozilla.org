import factory
import wagtail_factories
from factory.django import DjangoModelFactory
from wagtail import models as wagtail_models

from foundation_cms.navigation import blocks as nav_blocks
from foundation_cms.navigation import models as nav_models
from foundation_cms.base.utils.helpers import reseed


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
            external_url=factory.Faker("url"),
        )
        relative_url_link = factory.Trait(
            link_to="relative_url",
            relative_url=f"/{factory.Faker('uri_path')}",
        )

    label = factory.Faker("sentence", nb_words=3)

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



def generate(seed):
    reseed(seed)

    menu, created = nav_models.NavigationMenu.objects.get_or_create(
        title="Main Navigation",
        defaults={
            "dropdowns": wagtail_factories.StreamFieldFactory(
                {"dropdown": factory.SubFactory(NavDropdownFactory)},
                **{
                    "0": "dropdown",
                    "1": "dropdown",
                    "2": "dropdown",
                    "3": "dropdown",
                },
            )(),
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