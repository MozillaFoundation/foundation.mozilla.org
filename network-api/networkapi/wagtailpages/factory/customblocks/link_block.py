import factory
import wagtail_factories

from wagtail import models
from wagtail_link_block.blocks import LinkBlock as WagtailLinkBlock
from wagtail_link_block.blocks import URLValue

from networkapi.wagtailpages.pagemodels import customblocks


class WagtailLinkBlockFactory(wagtail_factories.StructBlockFactory):
    """Factory for WagtailLinkBlock.

    Use traits to create instances based on the type of link needed:
    - page_link: link to a page
    - document_link: link to a file/document
    - external_url_link: link to a custom URL
    - anchor_link: link to an anchor
    - email_link: link to an email
    - phone_link: link to a phone number

    Example:
    ```
    block = WagtailLinkBlockFactory(page_link=True)
    block = WagtailLinkBlockFactory(document_link=True)
    block = WagtailLinkBlockFactory(external_url_link=True)
    block = WagtailLinkBlockFactory(anchor_link=True)
    block = WagtailLinkBlockFactory(email_link=True)
    block = WagtailLinkBlockFactory(phone_link=True)
    ```
    """

    class Meta:
        model = WagtailLinkBlock

    @classmethod
    def _construct_struct_value(cls, block_class, params):
        """Use URLValue to create the StructValue instance."""
        return URLValue(
            block_class(),
            [(name, value) for name, value in params.items()],
        )

    class Params:
        page_link = factory.Trait(
            link_to="page",
            page=factory.Iterator(models.Page.objects.filter(locale_id="1")),
        )
        document_link = factory.Trait(
            link_to="file",
            file=factory.SubFactory(wagtail_factories.DocumentFactory),
        )
        external_url_link = factory.Trait(link_to="custom_url", custom_url=factory.Faker("url"))
        anchor_link = factory.Trait(link_to="anchor", anchor=factory.Faker("uri_path"))
        email_link = factory.Trait(link_to="email", email=factory.Faker("email"))
        phone_link = factory.Trait(link_to="phone", phone=factory.Faker("phone_number"))

    new_window = factory.Faker("boolean")
    # Setup default link as anchor (it won't pass validation without a link type defined though
    # so it's still necessary to use the factory with traits)
    link_to = "anchor"
    # Set all link types to None by default. Only define the needed link type in the factory
    # trait to avoid conflicts
    page = None
    file = None
    custom_url = ""
    anchor = ""
    email = ""
    phone = ""


class LinkBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.LinkBlock

    label = factory.Faker("sentence", nb_words=3)
    link = factory.SubFactory(WagtailLinkBlockFactory)
