from datetime import timedelta
from random import randrange

from factory import (
    Faker,
    DjangoModelFactory,
    LazyAttribute,
    post_generation
)

from networkapi.utility.faker import ImageProvider
from networkapi.milestones.models import Milestone

Faker.add_provider(ImageProvider)


class MilestoneFactory(DjangoModelFactory):

    class Meta:
        model = Milestone
        exclude = (
            'headline_sentence',
            'link_label_sentence',
            'milestone_length',
        )

    # Model Attributes
    headline = LazyAttribute(lambda o: o.headline_sentence.rstrip('.'))
    description = Faker('paragraph', nb_sentences=4, variable_nb_sentences=True)
    link_label = LazyAttribute(lambda o: o.link_label_sentence.rstrip('.'))
    link_url = Faker('url')
    start_date = Faker('date_time_between', start_date='-30d', end_date='+30d')
    end_date = LazyAttribute(lambda o: o.start_date + timedelta(days=o.milestone_length))

    # LazyAttribute helper values
    headline_sentence = Faker('sentence', nb_words=4)
    link_label_sentence = Faker('sentence', nb_words=4)
    milestone_length = LazyAttribute(lambda o: randrange(30))

    @post_generation
    def photo_name(self, create, extracted, **kwargs):
        self.photo.name = Faker('generic_image').generate({})
