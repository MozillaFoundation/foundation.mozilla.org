from factory import DjangoModelFactory, Faker, post_generation, SubFactory, Trait

from datetime import timezone

from networkapi.people.models import InternetHealthIssue, Person, Affiliation


class InternetHealthIssueFactory(DjangoModelFactory):
    name = Faker('sentence', nb_words=5, variable_nb_words=True)

    class Meta:
        model = InternetHealthIssue


class PersonFactory(DjangoModelFactory):
    name = Faker('name')
    role = Faker('job')
    location = Faker('country')
    quote = Faker('paragraph', nb_sentences=5)
    bio = Faker('paragraph', nb_sentences=5)
    image = Faker('image_url')
    partnership_logo = Faker('image_url')
    twitter_url = Faker('url')
    linkedin_url = Faker('url')
    interview_url = Faker('url')
    publish_after = Faker(
        'past_datetime',
        start_date='-30d',
        tzinfo=timezone.utc,
    )
    featured = False

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


class AffiliationFactory(DjangoModelFactory):
    name = Faker('company')
    person = SubFactory(PersonFactory)

    class Meta:
        model = Affiliation
