from factory.django import DjangoModelFactory
from wagtail_factories import PageFactory
from factory import (
    Faker,
    LazyAttribute
)
from networkapi.utility.faker import StreamfieldProvider

streamfield_fields = ['header', 'paragraph', 'image', 'spacer', 'image_text', 'quote']

sentence_faker: Faker = Faker('sentence', nb_words=3, variable_nb_words=False)
header_faker: Faker = Faker('sentence', nb_words=6, variable_nb_words=True)
description_faker: Faker = Faker('paragraphs', nb=2)
name_and_header = LazyAttribute(lambda o: o.header_text.rstrip('.'))

Faker.add_provider(StreamfieldProvider)


class CTAFactory(DjangoModelFactory):
    class Meta:
        abstract = True
        exclude = (
            'header_text',
            'description_text',
        )

    name = name_and_header
    header = name_and_header
    description = LazyAttribute(lambda o: ''.join([f'<p>{p}</p>' for p in o.description_text]))
    newsletter = Faker('word')

    # Lazy Values
    description_text = description_faker
    header_text = header_faker


class CMSPageFactory(PageFactory):
    class Meta:
        abstract = True
        exclude = (
            'title_text',
            'header_text',
        )

    header = LazyAttribute(lambda o: o.header_text.rstrip('.'))
    title = LazyAttribute(lambda o: o.title_text.rstrip('.'))
    narrowed_page_content = Faker('boolean', chance_of_getting_true=50)
    body = Faker('streamfield', fields=streamfield_fields)

    # Lazy Values
    title_text = sentence_faker
    header_text = header_faker
