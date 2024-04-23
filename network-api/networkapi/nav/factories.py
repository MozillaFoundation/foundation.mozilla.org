import factory
import wagtail_factories
from factory.django import DjangoModelFactory
from wagtail import models as wagtail_models
from wagtail.rich_text import RichText

from networkapi.nav import blocks as nav_blocks
from networkapi.nav import models as nav_models
from networkapi.wagtailcustomization.factories.blocks import ExtendedStructBlockFactory


class NavItemFactory(ExtendedStructBlockFactory):
    """Factory for NavLinkBlock.

    Use traits to create instances based on the type of link needed:
    - page_link: link to a page
    - external_url_link: link to a custom external URL
    - relative_url_link: link to a relative URL

    Example:
    ```
    block = NavLinkBlockFactory(page_link=True)
    block = NavLinkBlockFactory(external_url_link=True)
    block = NavLinkBlockFactory(relative_url_link=True)
    ```
    """

    class Meta:
        model = nav_blocks.NavItem

    class Params:
        page_link = factory.Trait(
            link_to="page",
            page=factory.Iterator(wagtail_models.Page.objects.filter(locale_id="1")),
        )
        external_url_link = factory.Trait(link_to="external_url", external_url=factory.Faker("url"))
        relative_url_link = factory.Trait(link_to="relative_url", relative_url=f'/{factory.Faker("uri_path")}')

    label = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("sentence", nb_words=6)

    # Setup default link as external URL (it won't pass validation without a link type defined though
    # so it's still necessary to use the factory with traits)
    link_to = "external_url"
    # Set all link types to None by default. Only define the needed link type in the factory
    # trait to avoid conflicts
    page = None
    external_url = ""
    relative_url = ""


class NavFeaturedItemFactory(ExtendedStructBlockFactory):
    class Meta:
        model = nav_blocks.NavFeaturedItem

    class Params:
        page_link = factory.Trait(
            link_to="page",
            page=factory.Iterator(wagtail_models.Page.objects.filter(locale_id="1")),
        )
        external_url_link = factory.Trait(link_to="external_url", external_url=factory.Faker("url"))
        relative_url_link = factory.Trait(link_to="relative_url", relative_url=f'/{factory.Faker("uri_path")}')

    label = factory.Faker("sentence", nb_words=3)
    icon = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)

    # Setup default link as external URL (it won't pass validation without a link type defined though
    # so it's still necessary to use the factory with traits)
    link_to = "external_url"
    # Set all link types to None by default. Only define the needed link type in the factory
    # trait to avoid conflicts
    page = None
    external_url = ""
    relative_url = ""


class NavButtonFactory(ExtendedStructBlockFactory):
    """Factory for NavButtonBlock.

    Use traits to create instances based on the type of link needed:
    - page_link: link to a page
    - external_url_link: link to a custom external URL
    - relative_url_link: link to a relative URL

    Example:
    ```
    block = NavButtonBlockFactory(page_link=True)
    block = NavButtonBlockFactory(external_url_link=True)
    block = NavButtonBlockFactory(relative_url_link=True)
    ```
    """

    class Meta:
        model = nav_blocks.NavButton

    class Params:
        page_link = factory.Trait(
            link_to="page",
            page=factory.Iterator(wagtail_models.Page.objects.filter(locale_id="1")),
        )
        external_url_link = factory.Trait(link_to="external_url", external_url=factory.Faker("url"))
        relative_url_link = factory.Trait(link_to="relative_url", relative_url=f'/{factory.Faker("uri_path")}')

    label = factory.Faker("sentence", nb_words=3)

    # Setup default link as external URL (it won't pass validation without a link type defined though
    # so it's still necessary to use the factory with traits)
    link_to = "external_url"
    # Set all link types to None by default. Only define the needed link type in the factory
    # trait to avoid conflicts
    page = None
    external_url = ""
    relative_url = ""


class NavColumnFactory(ExtendedStructBlockFactory):
    class Meta:
        model = nav_blocks.NavColumn

    class Params:
        no_button = factory.Trait(button=[])

    title = factory.Faker("sentence", nb_words=3)
    nav_items = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__external_url_link": True,
            "1__external_url_link": True,
            "2__external_url_link": True,
            "3__external_url_link": True,
        },
    )
    button = wagtail_factories.ListBlockFactory(NavButtonFactory, **{"0__external_url_link": True})


class NavFeaturedColumnFactory(ExtendedStructBlockFactory):
    class Meta:
        model = nav_blocks.NavFeaturedColumn

    title = factory.Faker("sentence", nb_words=3)
    nav_items = wagtail_factories.ListBlockFactory(
        NavFeaturedItemFactory,
        **{
            "0__external_url_link": True,
            "1__external_url_link": True,
            "2__external_url_link": True,
            "3__external_url_link": True,
        },
    )


class NavOverviewFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = nav_blocks.NavOverview

    title = factory.Faker("sentence", nb_words=3)
    description = RichText(str(factory.Faker("sentence", nb_words=6)))


class NavDropdownFactory(ExtendedStructBlockFactory):
    class Meta:
        model = nav_blocks.NavDropdown

    class Params:
        with_overview = factory.Trait(
            overview=wagtail_factories.ListBlockFactory(
                NavOverviewFactory,
                **{
                    "0__title": factory.Faker("sentence", nb_words=3),
                },
            ),
            columns=wagtail_factories.ListBlockFactory(
                NavColumnFactory,
                **{
                    "0__title": factory.Faker("sentence", nb_words=3),
                    "1__title": factory.Faker("sentence", nb_words=3),
                    "2__title": factory.Faker("sentence", nb_words=3),
                },
            ),
            featured_column=[],
        )
        with_featured_column = factory.Trait(
            overview=[],
            columns=wagtail_factories.ListBlockFactory(
                NavColumnFactory,
                **{
                    "0__title": factory.Faker("sentence", nb_words=3),
                    "1__title": factory.Faker("sentence", nb_words=3),
                    "2__title": factory.Faker("sentence", nb_words=3),
                },
            ),
            featured_column=wagtail_factories.ListBlockFactory(
                NavFeaturedColumnFactory,
                **{
                    "0__title": factory.Faker("sentence", nb_words=3),
                },
            ),
        )
        with_overview_and_featured_column = factory.Trait(
            overview=wagtail_factories.ListBlockFactory(
                NavOverviewFactory,
                **{
                    "0__title": factory.Faker("sentence", nb_words=3),
                },
            ),
            columns=wagtail_factories.ListBlockFactory(
                NavColumnFactory,
                **{
                    "0__title": factory.Faker("sentence", nb_words=3),
                    "1__title": factory.Faker("sentence", nb_words=3),
                },
            ),
            featured_column=wagtail_factories.ListBlockFactory(
                NavFeaturedColumnFactory,
                **{
                    "0__title": factory.Faker("sentence", nb_words=3),
                },
            ),
        )
        no_button = factory.Trait(button=[])

    title = factory.Faker("sentence", nb_words=3)
    overview = wagtail_factories.ListBlockFactory(NavOverviewFactory)
    columns = wagtail_factories.ListBlockFactory(
        NavColumnFactory,
        **{
            "0__title": factory.Faker("sentence", nb_words=3),
            "1__title": factory.Faker("sentence", nb_words=3),
            "2__title": factory.Faker("sentence", nb_words=3),
            "3__title": factory.Faker("sentence", nb_words=3),
        },
    )
    featured_column = wagtail_factories.ListBlockFactory(NavFeaturedColumnFactory)
    button = wagtail_factories.ListBlockFactory(NavButtonFactory, **{"0__external_url_link": True})


class NavMenuFactory(DjangoModelFactory):
    class Meta:
        model = nav_models.NavMenu

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
    enable_blog_dropdown = factory.Faker("boolean")
    blog_button_label = factory.Faker("sentence", nb_words=3)
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())


class NavMenuFeaturedBlogTopicRelationshipFactory(DjangoModelFactory):
    class Meta:
        model = nav_models.NavMenuFeaturedBlogTopicRelationship

    icon = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())
    menu = factory.SubFactory("networkapi.nav.factories.NavMenuFactory")
    topic = factory.SubFactory("networkapi.wagtailpages.factory.blog.BlogPageTopicFactory")
