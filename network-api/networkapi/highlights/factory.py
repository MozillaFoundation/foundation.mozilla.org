import factory
from factory.django import DjangoModelFactory

from networkapi.utility.utc import UTC
from networkapi.highlights.models import Highlight

utc = UTC()


class HighlightFactory(DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraphs', nb=2)
    link_label = factory.Faker('words', nb=3)
    link_url = factory.Faker('uri')
    image = factory.Faker('image_url')
    footer = factory.Faker('sentence', nb_words=5)
    publish_after = factory.Faker(
        'past_datetime',
        start_date='-30d',
        tzinfo=utc
    )
    expires = None
    order = 0

    class Meta:
        model = Highlight

    class Params:
        unpublished = factory.Trait(
            publish_after=factory.Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=utc
            )
        )
        has_expiry = factory.Trait(
            expires=factory.Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=utc
            )
        )
        expired = factory.Trait(
            expires=factory.Faker(
                'past_datetime',
                start_date='-30d',
                tzinfo=utc
            )
        )
