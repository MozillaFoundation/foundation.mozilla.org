from datetime import timezone

from slugify import slugify
from factory import (
    DjangoModelFactory,
    LazyAttribute,
    Faker,
    Trait,
)

from networkapi.landingpage.models import LandingPage, Signup

sentence_kwargs = {'nb_words': 3, 'variable_nb_words': False}
past_datetime_kwargs = {'start_date': '-30d', 'tzinfo': timezone.utc}


class SignupFactory(DjangoModelFactory):
    class Meta:
        model = Signup
        exclude = (
            'title_text',
            'header_text',
            'newsletter_text',
        )

    title = LazyAttribute(lambda o: o.title_text.rstrip('.'))
    header = LazyAttribute(lambda o: o.header_text.rstrip('.'))
    newsletter = LazyAttribute(lambda o: o.newsletter_text.rstrip('.'))
    description = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)

    title_text = Faker('sentence', **sentence_kwargs)
    header_text = Faker('sentence', **sentence_kwargs)
    newsletter_text = Faker('sentence', **sentence_kwargs)


class LandingPageFactory(DjangoModelFactory):
    class Meta:
        model = LandingPage
        exclude = (
            'title_text',
            'header_text',
        )

    class Params:
        has_expired = Trait(
            expiry_date=Faker('past_datetime', **past_datetime_kwargs)
        )

    header = LazyAttribute(lambda o: o.header_text.rstrip('.'))
    content = Faker('paragraph', nb_sentences=15, variable_nb_sentences=True)
    signup = None

    title = LazyAttribute(lambda o: o.title_text.rstrip('.'))
    slug = LazyAttribute(lambda o: slugify(o.title_text))
    publish_date = Faker('past_datetime', **past_datetime_kwargs)

    title_text = Faker('sentence', **sentence_kwargs)
    header_text = Faker('sentence', **sentence_kwargs)
