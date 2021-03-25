from datetime import timezone

from factory import (
    DjangoModelFactory,
    Faker,
    Trait,
    LazyAttribute,
)

from networkapi.utility.faker import ImageProvider, generate_fake_data
from networkapi.utility.faker.helpers import reseed
from networkapi.highlights.models import Highlight

Faker.add_provider(ImageProvider)


class HighlightFactory(DjangoModelFactory):
    class Meta:
        model = Highlight
        exclude = (
            'title_sentence',
            'link_label_words',
            'footer_sentence',
        )

    class Params:
        unpublished = Trait(
            publish_after=Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=timezone.utc
            )
        )
        has_expiry = Trait(
            expires=Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=timezone.utc
            )
        )
        expired = Trait(
            expires=Faker(
                'past_datetime',
                start_date='-30d',
                tzinfo=timezone.utc
            )
        )

    title = LazyAttribute(lambda o: o.title_sentence.rstrip('.'))
    description = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    link_label = LazyAttribute(lambda o: ' '.join(o.link_label_words))
    footer = LazyAttribute(lambda o: o.footer_sentence.rstrip('.'))
    link_url = Faker('uri')
    publish_after = Faker(
        'past_datetime',
        start_date='-30d',
        tzinfo=timezone.utc
    )
    expires = None
    order = 0

    # LazyAttribute helper values
    title_sentence = Faker('sentence', nb_words=4)
    link_label_words = Faker('words', nb=3)
    footer_sentence = Faker('sentence', nb_words=5)


def generate(seed):
    reseed(seed)

    print('Generating Highlights')
    generate_fake_data(HighlightFactory, 10)

    reseed(seed)

    for highlight in Highlight.objects.all():
        highlight.image.name = Faker('generic_image').generate({})
        highlight.save()
