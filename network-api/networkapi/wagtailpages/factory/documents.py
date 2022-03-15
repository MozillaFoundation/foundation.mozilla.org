from factory import Faker, SubFactory, django
from factory.django import DjangoModelFactory
from wagtail.documents import get_document_model
from wagtail.core.models import Collection

# UGLY COPYPASTE FROM latest
# https://github.com/mvantellingen/wagtail-factories/blob/master/src/wagtail_factories/factories.py
from wagtail_factories.factories import MP_NodeFactory


class CollectionFactory(MP_NodeFactory):
    name = Faker('text', max_nb_chars=60)

    class Meta:
        model = Collection


class CollectionMemberFactory(DjangoModelFactory):
    collection = SubFactory(CollectionFactory, parent=None)


class DocumentFactory(CollectionMemberFactory):
    class Meta:
        model = get_document_model()

    title = Faker('text', max_nb_chars=250)
    file = django.FileField(
        filename='test.pdf',
        data=b'''
              %PDF-1.0 1 0 obj<</Pages 2 0 R>>endobj
              2 0 obj<</Kids[3 0 R]/Count 1>>endobj
              3 0 obj<</MediaBox[0 0 3 3]>>endobj
              trailer<</Root 1 0 R>>
              '''
    )
