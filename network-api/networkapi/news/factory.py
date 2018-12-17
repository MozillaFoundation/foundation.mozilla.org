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
            publish_after=Faker('future_datetime', end_date='+30d', tzinfo=timezone.utc)
        )
        has_expiry = Trait(
            expires=Faker('future_datetime', end_date='+30d', tzinfo=timezone.utc)
        )
        expired = Trait(
            expires=Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc)
        )
        video = Trait(
            is_video=True
        )

    headline = LazyAttribute(lambda o: o.headline_sentence.rstrip('.'))
    outlet = Faker('company')
    date = Faker('past_date', start_date='-30d')
    link = Faker('url')
    excerpt = Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    author = Faker('name')
    publish_after = Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc)

    # LazyAttribute helper value
    headline_sentence = Faker('sentence', nb_words=4)

    @post_generation
    def set_thumbnail(self, create, extracted, **kwargs):
        self.thumbnail.name = Faker('generic_image').generate({})
