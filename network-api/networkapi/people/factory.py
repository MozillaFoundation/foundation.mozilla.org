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
    image = factory.LazyAttribute(
        lambda o: '{}{}.png'.format(o.url, o.image_filename)
    )
    partnership_logo = factory.LazyAttribute(
        lambda o: '{}{}.png'.format(o.url, o.partnership_logo_filename)
    )
    twitter_url = factory.Faker('url')
    linkedin_url = factory.Faker('url')
    interview_url = factory.Faker('url')
    publish_after = factory.Faker('past_datetime', start_date='-30d', tzinfo=utc)
    featured = False

    @factory.post_generation
    def internet_health_issues(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for issue in extracted:
                self.internet_health_issues.add(issue)

    # These are excluded from the Django model, but are used in the lazy generators
    url = factory.Faker('url')
    image_filename = factory.Faker('word')
    partnership_logo_filename = factory.Faker('word')

    class Meta:
        model = Person
        exclude =(
            'url',
            'image_filename',
            'partnership_logo_filename',
        )

    class Params:
        is_featured = factory.Trait(
            featured = True
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


class AffiliationFactory(DjangoModelFactory):
    name = factory.Faker('company')
    person = factory.SubFactory(PersonFactory)

    class Meta:
        model = Affiliation
