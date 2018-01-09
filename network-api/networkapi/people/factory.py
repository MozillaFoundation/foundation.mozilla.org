import factory
from factory.django import DjangoModelFactory

from networkapi.utility.utc import UTC
from networkapi.people.models import InternetHealthIssue, Person, Affiliation

utc = UTC()


class InternetHealthIssueFactory(DjangoModelFactory):
    name = factory.Faker('sentence', nb_words=5, variable_nb_words=True)

    class Meta:
        model = InternetHealthIssue


class PersonFactory(DjangoModelFactory):
    name = factory.Faker('name')
    role = factory.Faker('job')
    location = factory.Faker('country')
    quote = factory.Faker('paragraph', nb_sentences=5)
    bio = factory.Faker('paragraph', nb_sentences=5)
    image = factory.Faker('image_url')
    partnership_logo = factory.Faker('image_url')
    twitter_url = factory.Faker('url')
    linkedin_url = factory.Faker('url')
    interview_url = factory.Faker('url')
    publish_after = factory.Faker(
        'past_datetime',
        start_date='-30d',
        tzinfo=utc,
    )
    featured = False

    @factory.post_generation
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

    class Meta:
        model = Person

    class Params:
        is_featured = factory.Trait(
            featured=True
        )
        unpublished = factory.Trait(
            publish_after=factory.Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=utc,
            )
        )
        has_expiry = factory.Trait(
            expires=factory.Faker(
                'future_datetime',
                end_date='+30d',
                tzinfo=utc,
            )
        )
        expired = factory.Trait(
            expires=factory.Faker(
                'past_datetime',
                start_date='-30d',
                tzinfo=utc,
            )
        )


class AffiliationFactory(DjangoModelFactory):
    name = factory.Faker('company')
    person = factory.SubFactory(PersonFactory)

    class Meta:
        model = Affiliation
