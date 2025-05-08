import factory
from factory import Faker, LazyAttribute
from wagtail.rich_text import RichText

from networkapi.donate.snippets.help_page_notice import HelpPageNotice
from networkapi.wagtailpages.factory.image_factory import ImageFactory

notice_text_contents = Faker("paragraph", nb_sentences=3, variable_nb_sentences=False)


class HelpPageNoticeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HelpPageNotice
        exclude = ("notice_text",)

    name = Faker("sentence", nb_words=3)
    text = LazyAttribute(lambda o: RichText(f"<p>{o.notice_text}</p>"))
    notice_image = factory.SubFactory(ImageFactory)
    notice_image_alt_text = Faker("sentence", nb_words=4)

    # Lazy Values
    notice_text = notice_text_contents
