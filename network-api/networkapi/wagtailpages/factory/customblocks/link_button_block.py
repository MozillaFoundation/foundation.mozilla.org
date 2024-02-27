import factory
import wagtail_factories

from networkapi.wagtailpages.factory.customblocks.link_block import LinkBlockFactory
from networkapi.wagtailpages.pagemodels import customblocks


class LinkButtonBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.LinkButtonBlock

    class Params:
        page_link = factory.Trait(target=factory.SubFactory(LinkBlockFactory, page_link=True))
        document_link = factory.Trait(target=factory.SubFactory(LinkBlockFactory, document_link=True))
        external_url_link = factory.Trait(target=factory.SubFactory(LinkBlockFactory, external_url_link=True))
        anchor_link = factory.Trait(target=factory.SubFactory(LinkBlockFactory, anchor_link=True))
        email_link = factory.Trait(target=factory.SubFactory(LinkBlockFactory, email_link=True))
        phone_link = factory.Trait(target=factory.SubFactory(LinkBlockFactory, phone_link=True))

    # External URL link is the default
    target = factory.SubFactory(LinkBlockFactory, external_url_link=True)
    styling = factory.Faker("random_element", elements=["btn-primary", "btn-secondary"])
