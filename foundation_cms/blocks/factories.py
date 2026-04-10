import factory
import wagtail_factories

from foundation_cms.blocks.link_button_block import LinkButtonBlock


class LinkButtonBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = LinkButtonBlock

    label = factory.Faker("sentence", nb_words=3)
    link_to = "external_url"
    page = None
    external_url = factory.Faker("url")
    relative_url = ""
    anchor = ""
    email = ""
    file = None
    phone = ""
    new_window = False
    style = factory.Faker("random_element", elements=["btn-primary", "btn-secondary"])
    alignment = factory.Faker("random_element", elements=["link-button-block--left", "link-button-block--center"])
