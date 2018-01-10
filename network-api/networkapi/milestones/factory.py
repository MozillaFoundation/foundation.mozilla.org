from datetime import timedelta
from random import randrange

from factory import Faker, DjangoModelFactory, LazyAttribute

from networkapi.milestones.models import Milestone


class MilestoneFactory(DjangoModelFactory):

    class Meta:
        model = Milestone
        exclude = ('milestone_length',)

    # Model Attributes
    headline = Faker('sentence', nb_words=4)
    photo = Faker('image_url')
    start_date = Faker('future_datetime', end_date='+30d')
    end_date = LazyAttribute(lambda o: o.start_date + timedelta(days=o.milestone_length))
    description = Faker('paragraphs', nb=2)
    link_url = Faker('url')
    link_label = Faker('sentence', nb_words=4)

    # LazyAttribute helper values
    milestone_length = LazyAttribute(lambda o: randrange(30))
