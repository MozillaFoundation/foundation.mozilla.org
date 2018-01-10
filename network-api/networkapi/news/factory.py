from datetime import timezone

from factory import DjangoModelFactory, Faker, Trait

from networkapi.news.models import News


class NewsFactory(DjangoModelFactory):

    class Meta:
        model = News

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

    headline = Faker('sentence', nb_words=4)
    outlet = Faker('sentence', nb_words=3)
    date = Faker('past_date', start_date='-30d')
    link = Faker('url')
    excerpt = Faker('paragraphs', nb=2)
    author = Faker('name')
    publish_after = Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc)
    thumbnail = Faker('image_url')
