import factory
import wagtail_factories
from wagtail import models as wagtail_models

from networkapi.nav import blocks as nav_blocks


class NavItemFactory(wagtail_factories.StructBlockFactory):
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

    @classmethod
    def _construct_struct_value(cls, block_class, params):
        """Use NavLinkValue to create the StructValue instance."""
        return nav_blocks.NavItemValue(
            block_class(),
            [(name, value) for name, value in params.items()],
        )

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


class NavButtonFactory(wagtail_factories.StructBlockFactory):
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

    @classmethod
    def _construct_struct_value(cls, block_class, params):
        """Use NavLinkValue to create the StructValue instance."""
        return nav_blocks.NavItemValue(
            block_class(),
            [(name, value) for name, value in params.items()],
        )

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

