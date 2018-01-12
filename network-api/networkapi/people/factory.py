from datetime import timezone

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    SubFactory,
    Trait,
    LazyAttribute,
)

from networkapi.utility.faker_providers import ImageProvider
from networkapi.people.models import InternetHealthIssue, Person, Affiliation

Faker.add_provider(ImageProvider)


class InternetHealthIssueFactory(DjangoModelFactory):
    class Meta:
        model = InternetHealthIssue

    name = Faker('sentence', nb_words=5, variable_nb_words=True)


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person
        exclude = (
            'quote_paragraph',
            'bio_paragraph',
        )

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
    quote = LazyAttribute(lambda o: ' '.join(o.quote_paragraph))
    bio = LazyAttribute(lambda o: ' '.join(o.bio_paragraph))
    twitter_url = Faker('url')
    linkedin_url = Faker('url')
    interview_url = Faker('url')
    publish_after = Faker(
        'past_datetime',
        start_date='-30d',
        tzinfo=timezone.utc,
    )
    featured = False

    # These are excluded from the model and used for lazy attributes
    quote_paragraph = Faker('paragraph', nb_sentences=5)
    bio_paragraph = Faker('paragraph', nb_sentences=5)

    # Methods to run after the model has been generated
    @post_generation
    def set_images(self, create, extracted, **kwargs):
        self.image.name = Faker('people_image').generate({})
        self.partnership_logo.name = Faker('generic_image').generate({})

    @post_generation
    def internet_health_issues(self, create, extracted, **kwargs):
        """
        After model generation, create internet health issues from the
        internet_health_issues kwarg and relate them to this model.

        If the extracted value of the kwarg is an int, that many
        issues will be randomly created. If the extracted value is
        a list of issue names, they'll be created from the list.
        """

        if not create:
            return

        if extracted:
            issue_set = []

            if isinstance(extracted, int):
                for issue in range(extracted):
                    issue_set.append(InternetHealthIssueFactory())
            elif isinstance(extracted, tuple):
                for issue in extracted:
                    issue_set.append(InternetHealthIssueFactory(name=issue))

            self.internet_health_issues.set(issue_set)


class AffiliationFactory(DjangoModelFactory):
    class Meta:
        model = Affiliation

    name = Faker('company')
    person = SubFactory(PersonFactory)
