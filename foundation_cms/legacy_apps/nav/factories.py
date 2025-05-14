import factory
import wagtail_factories
from factory.django import DjangoModelFactory
from wagtail import models as wagtail_models
from wagtail.images.tests import utils as wagtail_images_utils
from wagtail.rich_text import RichText

from foundation_cms.legacy_apps.nav import blocks as nav_blocks
from foundation_cms.legacy_apps.nav import models as nav_models
from foundation_cms.legacy_apps.utility.faker.helpers import get_homepage, reseed
from foundation_cms.legacy_apps.wagtailcustomization.factories.blocks import (
    ExtendedStructBlockFactory,
)
from foundation_cms.legacy_apps.wagtailpages.models import BlogPageTopic


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
    icon = factory.SubFactory(
        wagtail_factories.ImageChooserBlockFactory, image__file=wagtail_images_utils.get_test_image_file_svg()
    )

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
    button = factory.SubFactory(NavButtonFactory, external_url_link=True)


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

    icon = factory.SubFactory(
        wagtail_factories.ImageChooserBlockFactory, image__file=wagtail_images_utils.get_test_image_file_svg()
    )
    locale = factory.LazyFunction(lambda: wagtail_models.Locale.get_default())
    menu = factory.SubFactory("foundation_cms.legacy_apps.nav.factories.NavMenuFactory")
    topic = factory.SubFactory("foundation_cms.legacy_apps.wagtailpages.factory.blog.BlogPageTopicFactory")


# Build "Who We Are" dropdown
def generate_first_dropdown(seed):
    reseed(seed)
    # Create prerequisite data
    # Set dropdown title
    title = "Who We Are"
    # Create a test page for linking purposes only
    page_a1 = wagtail_factories.PageFactory(parent=get_homepage(), title="Test 1st dropdown page")

    # Create Overview section for dropdown
    overview = wagtail_factories.ListBlockFactory(
        NavOverviewFactory,
        **{
            "0__title": "About Us",
            "0__description": RichText(
                (
                    "Mozilla is a global nonprofit dedicated to keeping the Internet"
                    " a public resource that is open and accessible to all."
                )
            ),
        },
    )

    # Build out nav items (columns)
    # Column 1 nav items
    nav_items_0 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__link_to": "page",
            "0__page": page_a1,
            "0__description": "",
            "1__external_url_link": True,
            "1__external_url": "https://mozilla.org/",
            "1__description": "",
        },
    )
    # Column 2 nav items
    nav_items_1 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__external_url_link": True,
            "0__description": "",
            "0__external_url": "https://mozilla.org/",
            "1__external_url_link": True,
            "1__external_url": "https://mozilla.org/",
            "1__description": "",
        },
    )
    # Build out columns
    columns = wagtail_factories.ListBlockFactory(
        NavColumnFactory,
        **{
            "0__title": "Approach",
            "0__nav_items": nav_items_0,
            "0__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
            "1__title": "Legal",
            "1__nav_items": nav_items_1,
            "1__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
        },
    )
    # Build button
    button = factory.SubFactory(
        NavButtonFactory, link_to="relative_url", relative_url="/who-we-are/", label="Learn More"
    )

    # Generate dropdown
    dropdown = NavDropdownFactory(
        title=title,
        overview=overview,
        columns=columns,
        button=button,
    )

    return dropdown


# Build "What We Do" dropdown
def generate_second_dropdown(seed):
    reseed(seed)
    # Create prerequisite data
    # Set dropdown title
    title = "What We Do"

    # Build out nav items (columns)
    # Column 1 nav items
    nav_items_0 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "1__relative_url_link": True,
            "1__relative_url": "/",
            "2__relative_url_link": True,
            "2__relative_url": "/",
        },
    )
    # Column 2 nav items
    nav_items_1 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "0__description": "",
            "1__relative_url_link": True,
            "1__relative_url": "/",
            "2__relative_url_link": True,
            "2__relative_url": "/",
        },
    )
    # Column 3 nav items
    nav_items_2 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "1__relative_url_link": True,
            "1__relative_url": "/",
        },
    )
    # Column 4 nav items
    nav_items_3 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "1__relative_url_link": True,
            "1__relative_url": "/",
        },
    )

    # Build out columns
    columns = wagtail_factories.ListBlockFactory(
        NavColumnFactory,
        **{
            "0__title": "Connect People",
            "0__nav_items": nav_items_0,
            "0__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
            "1__title": "Rally Communities",
            "1__nav_items": nav_items_1,
            "1__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
            "2__title": "Influence Policies",
            "2__nav_items": nav_items_2,
            "2__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
            "3__title": "Research & Analysis",
            "3__nav_items": nav_items_3,
            "3__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
        },
    )

    # Build button
    button = factory.SubFactory(
        NavButtonFactory, link_to="relative_url", relative_url="/", label="Learn more about what we do"
    )

    # Generate dropdown
    dropdown = NavDropdownFactory(
        title=title,
        columns=columns,
        button=button,
    )

    return dropdown


# Build "What You Can Do" dropdown
def generate_third_dropdown(seed):
    reseed(seed)
    # Create prerequisite data
    # Set dropdown title
    title = "What You Can Do"
    # Create a test page for linking purposes only
    page_a2 = wagtail_factories.PageFactory(parent=get_homepage(), title="Test 3rd dropdown page")

    # Create Overview section for dropdown
    overview = wagtail_factories.ListBlockFactory(
        NavOverviewFactory,
        **{
            "0__title": "Get Involved",
            "0__description": RichText(
                (
                    "From donating funds or data, to signing a petition, to applying to become a "
                    "volunteer or fellow there are many ways to get involved with the community."
                )
            ),
        },
    )

    # Build out nav items (columns)
    # Column 1 nav items
    nav_items_0 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "0__description": "",
            "1__relative_url_link": True,
            "1__relative_url": "/",
            "2__relative_url_link": True,
            "2__relative_url": "/",
        },
    )
    # Column 2 nav items
    nav_items_1 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "0__description": "",
            "1__relative_url_link": True,
            "1__relative_url": "/",
            "2__relative_url_link": True,
            "2__relative_url": "/",
        },
    )

    # Build out columns
    columns = wagtail_factories.ListBlockFactory(
        NavColumnFactory,
        **{
            "0__title": "Act",
            "0__nav_items": nav_items_0,
            "0__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
            "1__title": "Learn",
            "1__nav_items": nav_items_1,
            "1__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
        },
    )

    # Build featured nav items
    featured_nav_items = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__label": "Make a Donation",
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "0__description": "",
            "1__label": "Ways to Give",
            "1__relative_url_link": True,
            "1__relative_url": "/",
            "1__description": "",
        },
    )

    # Build featured column
    featured_column = wagtail_factories.ListBlockFactory(
        NavFeaturedColumnFactory,
        **{
            "0__title": "Donate",
            "0__nav_items": featured_nav_items,
        },
    )

    # Build button
    button = factory.SubFactory(NavButtonFactory, link_to="page", page=page_a2, label="Learn More")

    # Generate dropdown
    dropdown = NavDropdownFactory(
        title=title,
        overview=overview,
        columns=columns,
        featured_column=featured_column,
        button=button,
    )

    return dropdown


# Build "What We Fund" dropdown
def generate_fourth_dropdown(seed):
    reseed(seed)
    # Create prerequisite data
    # Set dropdown title
    title = "What We Fund"
    # Create a test page for linking purposes only
    page_a2 = wagtail_factories.PageFactory(parent=get_homepage(), title="Test 4th dropdown page")

    # Create Overview section for dropdown
    overview = wagtail_factories.ListBlockFactory(
        NavOverviewFactory,
        **{
            "0__title": "Apply for Funding",
            "0__description": RichText(
                (
                    "The Mozilla Foundation provides funding and resources to individuals,"
                    " groups, and organizations aligned with creating a more human-centered internet."
                )
            ),
        },
    )

    # Build out nav items (columns)
    # Column 1 nav items
    nav_items_0 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "1__relative_url_link": True,
            "1__relative_url": "/",
        },
    )
    # Column 2 nav items
    nav_items_1 = wagtail_factories.ListBlockFactory(
        NavItemFactory,
        **{
            "0__relative_url_link": True,
            "0__relative_url": "/",
            "1__relative_url_link": True,
            "1__relative_url": "/",
        },
    )

    # Build out columns
    columns = wagtail_factories.ListBlockFactory(
        NavColumnFactory,
        **{
            "0__title": "Opportunities",
            "0__nav_items": nav_items_0,
            "0__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
            "1__title": "Community Impact",
            "1__nav_items": nav_items_1,
            "1__button": wagtail_factories.ListBlockFactory(NavButtonFactory, **{}),
        },
    )

    # Build button
    button = factory.SubFactory(NavButtonFactory, link_to="page", page=page_a2, label="Learn More")

    # Generate dropdown
    dropdown = NavDropdownFactory(
        title=title,
        overview=overview,
        columns=columns,
        button=button,
    )

    return dropdown


# Generate the Nav Menu
def generate(seed):
    reseed(seed)

    try:
        menu = nav_models.NavMenu.objects.get()
        print("Main Navigation exists")
    except nav_models.NavMenu.DoesNotExist:
        print("Generating Main Navigation")

        dropdown_0 = generate_first_dropdown(seed)
        dropdown_1 = generate_second_dropdown(seed)
        dropdown_2 = generate_third_dropdown(seed)
        dropdown_3 = generate_fourth_dropdown(seed)

        # Build menu
        menu = NavMenuFactory(
            dropdowns__0__dropdown=dropdown_0,
            dropdowns__1__dropdown=dropdown_1,
            dropdowns__2__dropdown=dropdown_2,
            dropdowns__3__dropdown=dropdown_3,
            enable_blog_dropdown=True,
            blog_button_label="See all blog posts",
        )

        print("Linking blog topics to New Main Navigation")
        # Get existing topics and create relationships
        topics = BlogPageTopic.objects.all()[:5]
        for topic in topics:
            NavMenuFeaturedBlogTopicRelationshipFactory(menu=menu, topic=topic)

        # Activate menu
        print("Activating New Main Navigation")
        site = wagtail_models.Site.objects.first()
        site_active_nav = nav_models.SiteNavMenu.for_site(site)
        site_active_nav.active_nav_menu = menu
        site_active_nav.save()
