import factory
import wagtail_factories
from wagtail import models as wagtail_models

from networkapi.wagtailpages.pagemodels.customblocks.link_block import (
    LinkBlock,
    LinkValue,
)


class LinkBlockFactory(wagtail_factories.StructBlockFactory):
    """Factory for LinkBlock.

    Use traits to create instances based on the type of link needed:
    - page_link: link to a page
    - document_link: link to a file/document
    - external_url_link: link to a custom external URL
    - relative_url_link: link to a relative URL
    - anchor_link: link to an anchor
    - email_link: link to an email
    - phone_link: link to a phone number

    Example:
    ```
    block = LinkBlockFactory(page_link=True)
    block = LinkBlockFactory(document_link=True)
    block = LinkBlockFactory(external_url_link=True)
    block = LinkBlockFactory(relative_url_link=True)
    block = LinkBlockFactory(anchor_link=True)
    block = LinkBlockFactory(email_link=True)
    block = LinkBlockFactory(phone_link=True)
    ```
    """

    class Meta:
        model = LinkBlock

    @classmethod
    def _construct_struct_value(cls, block_class, params):
        """Use BaseLinkValue to create the StructValue instance."""
        return LinkValue(
            block_class(),
            [(name, value) for name, value in params.items()],
        )

    class Params:
        page_link = factory.Trait(
            link_to="page",
            page=factory.Iterator(wagtail_models.Page.objects.filter(locale_id="1")),
        )
        document_link = factory.Trait(
            link_to="file",
            file=factory.SubFactory(wagtail_factories.DocumentFactory),
        )
        external_url_link = factory.Trait(link_to="external_url", external_url=factory.Faker("url"))
        relative_url_link = factory.Trait(link_to="relative_url", relative_url=f'/{factory.Faker("uri_path")}')
        anchor_link = factory.Trait(link_to="anchor", anchor=f'#{factory.Faker("slug")}')
        email_link = factory.Trait(link_to="email", email=factory.Faker("email"))
        phone_link = factory.Trait(link_to="phone", phone=factory.Faker("phone_number"))

    label = factory.Faker("sentence", nb_words=3)
    new_window = factory.Faker("boolean")

    # Setup default link as anchor (it won't pass validation without a link type defined though
    # so it's still necessary to use the factory with traits)
    link_to = "external_url"
    # Set all link types to None by default. Only define the needed link type in the factory
    # trait to avoid conflicts
    page = None
    file = None
    external_url = ""
    relative_url = ""
    anchor = ""
    email = ""
    phone = ""
