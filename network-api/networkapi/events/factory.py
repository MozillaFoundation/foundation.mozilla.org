from factory import Faker
from factory.django import DjangoModelFactory

from networkapi.events.models import TitoEvent


class TitoEventFactory(DjangoModelFactory):
    class Meta:
        model = TitoEvent

    title = Faker("sentence", nb_words=3)
    event_id = Faker("lexify", text="???????/???????")
    security_token = Faker("numerify", text="###########")
    newsletter_question_id = Faker("numerify", text="###########")
