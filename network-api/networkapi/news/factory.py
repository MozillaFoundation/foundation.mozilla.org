from datetime import timezone

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    Trait,
    LazyAttribute,
)

from networkapi.utility.faker import ImageProvider
from networkapi.news.models import News

from django.conf import settings

RANDOM_SEED = settings.RANDOM_SEED
TESTING = settings.TESTING

Faker.add_provider(ImageProvider)


class NewsFactory(DjangoModelFactory):

    class Meta:
        model = News
        exclude = (
            'headline_sentence',
        )

    class Params:
        is_featured = Trait(
            featured=True
        )
        unpublished = Trait(
            publish_after=Faker('date_time', tzinfo=timezone.utc) if RANDOM_SEED and not TESTING
            else Faker('future_datetime', end_date='+30d', tzinfo=timezone.utc)
        )
        has_expiry = Trait(
            expires=Faker('date_time', tzinfo=timezone.utc) if RANDOM_SEED and not TESTING
            else Faker('future_datetime', end_date='+30d', tzinfo=timezone.utc)
        )
        expired = Trait(
            expires=Faker('date_time', tzinfo=timezone.utc) if RANDOM_SEED and not TESTING
            else Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc)
        )
        video = Trait(
            is_video=True
        )

    headline = LazyAttribute(lambda o: o.headline_sentence.rstrip('.'))
    outlet = Faker('company')
    date = Faker('date') if RANDOM_SEED and not TESTING else Faker('past_date', start_date='-30d')
    link = Faker('url')
    excerpt = Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    author = Faker('name')
    publish_after = (Faker('date_time', tzinfo=timezone.utc) if RANDOM_SEED and not TESTING
                     else Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc))

    # LazyAttribute helper value
    headline_sentence = Faker('sentence', nb_words=4)

    @post_generation
    def set_thumbnail(self, create, extracted, **kwargs):
        self.thumbnail.name = Faker('generic_image').generate({})
