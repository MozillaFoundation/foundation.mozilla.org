from datetime import timezone

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    SubFactory,
    Trait,
)

from networkapi.utility.faker import ImageProvider, get_random_items
from networkapi.people.models import InternetHealthIssue, Person, Affiliation

Faker.add_provider(ImageProvider)


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    class Params:
        is_featured = Trait(
            featured=True
        )
        unpublished = Trait(
            publish_after=Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=timezone.utc,
            )
        )
        has_expiry = Trait(
            expires=Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=timezone.utc,
            )
        )
        expired = Trait(
            expires=Faker(
                'past_datetime',
                start_date='-30d',
                tzinfo=timezone.utc,
            )
        )

    name = Faker('name')
    role = Faker('job')
    location = Faker('country')
    quote = Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    bio = Faker('paragraph', nb_sentences=2, variable_nb_sentences=True)
    twitter_url = Faker('url')
    linkedin_url = Faker('url')
    interview_url = Faker('url')
    publish_after = Faker(
        'past_datetime',
        start_date='-30d',
        tzinfo=timezone.utc,
    )
    featured = False

    # Methods to run after the model has been generated
    @post_generation
    def set_images(self, create, extracted, **kwargs):
        self.image.name = Faker('people_image').generate({})
        self.partnership_logo.name = Faker('generic_image').generate({})

    @post_generation
    def internet_health_issues(self, create, extracted, **kwargs):
        """
        After model generation, Relate any internet health issues from the
        internet_health_issues kwarg to the new instance.
        """

        self.internet_health_issues.add(*get_random_items(InternetHealthIssue))


class AffiliationFactory(DjangoModelFactory):
    class Meta:
        model = Affiliation

    name = Faker('company')
    person = SubFactory(PersonFactory)
