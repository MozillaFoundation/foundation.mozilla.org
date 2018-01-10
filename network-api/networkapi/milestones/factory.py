from datetime import timedelta
from random import randrange

from factory import Faker, DjangoModelFactory, LazyAttribute

from networkapi.milestones.models import Milestone


class MilestoneFactory(DjangoModelFactory):

    class Meta:
        model = Milestone

    headline = Faker('sentence', nb_words=4)
    photo = Faker('image_url')
    start_date = Faker('future_date', end_date='+30d')
    end_date = LazyAttribute(lambda o: o.start_date + timedelta(randrange(30)))
    description = Faker('paragraphs', nb=2)
    link_url = Faker('url')
    link_label = Faker('sentence', nb_words=4)
