from factory import DjangoModelFactory, Faker, post_generation, Trait
from datetime import timezone

from networkapi.utility.faker_providers import ImageProvider
from networkapi.highlights.models import Highlight

Faker.add_provider(ImageProvider)


class HighlightFactory(DjangoModelFactory):
    class Meta:
        model = Highlight

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

    title = Faker('sentence', nb_words=4)
    description = Faker('paragraphs', nb=2)
    link_label = Faker('words', nb=3)
    link_url = Faker('uri')
    footer = Faker('sentence', nb_words=5)
    publish_after = Faker(
        'past_datetime',
        start_date='-30d',
        tzinfo=timezone.utc
    )
    expires = None
    order = 0

    @post_generation
    def image_name(self, create, extracted, **kwargs):
        self.image.name = Faker('generic_image').generate({})
