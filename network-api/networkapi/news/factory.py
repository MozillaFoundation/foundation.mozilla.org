import factory

from networkapi.news.models import News
from networkapi.utility.utc import UTC

utc = UTC()


class NewsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = News

    class Params:
        on_homepage = factory.Trait(
            featured=factory.Faker('pybool')
        )
        unpublished = factory.Trait(
            publish_after=factory.Faker('future_datetime', end_date='+30d', tzinfo=utc)
        )
        has_expiry = factory.Trait(
            expires=factory.Faker('future_datetime', end_date='+30d', tzinfo=utc)
        )
        expired = factory.Trait(
            expires=factory.Faker('past_datetime', start_date='-30d', tzinfo=utc)
        )
        video = factory.Trait(
            is_video=factory.Faker('pybool')
        )

    headline = factory.Faker('sentence', nb_words=4)
    outlet = factory.Faker('sentence', nb_words=3)
    date = factory.Faker('past_date', start_date='-30d')
    link = factory.Faker('url')
    excerpt = factory.Faker('paragraphs', nb=2)
    author = factory.Faker('name')
    thumbnail = factory.Faker('image_url')
