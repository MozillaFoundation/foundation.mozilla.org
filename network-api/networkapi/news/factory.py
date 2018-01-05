import factory

from networkapi.news.models import News


class NewsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = News

    headline = factory.Faker('sentence')
    outlet = factory.Faker('sentence', nb_words=4)
    date = factory.Faker('past_date')
    link = factory.Faker('url')
