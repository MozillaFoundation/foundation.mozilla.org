import wagtail_factories
from factory import Faker, LazyAttribute, SubFactory
from wagtail.rich_text import RichText

from networkapi.donate.pagemodels.customblocks.notice_block import NoticeBlock

description_faker = Faker("paragraphs", nb=2)


class NoticeBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = NoticeBlock
        exclude = ("description_text",)

    image = SubFactory(wagtail_factories.ImageChooserBlockFactory)
    image_alt_text = Faker("sentence", nb_words=4)
    text = LazyAttribute(lambda o: RichText("".join([f"<p>{p}</p>" for p in o.description_text])))

    # Lazy Values
    description_text = description_faker
