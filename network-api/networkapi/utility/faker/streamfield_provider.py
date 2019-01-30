import json

from random import randint
from django.conf import settings
from faker import Faker
from faker.providers import BaseProvider
from wagtail.images.models import Image

seed = randint(0, 5000000)
if settings.RANDOM_SEED is not None:
    seed = settings.RANDOM_SEED

fake = Faker()
fake.random.seed(seed)


def generate_field(field_type, value):
    return {
        'type': field_type,
        'value': value,
        'id': fake.uuid4(),
    }


def generate_paragraph_field():
    paragraphs = (
        f'<h3>{fake.sentence()}</h3>',
        f'<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>',
        f'<ul>',
        ''.join([f'<li>{fake.word()}</li>' for i in range(10)]),
        f'</ul><br />',
        f'<a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a>'
    )

    return generate_field('paragraph', ''.join(paragraphs))


def generate_header_field():
    value = ' '.join(fake.words())

    return generate_field('header', value)


def generate_image_field():
    images = Image.objects.all()
    image_idx = fake.unix_time() % images.count()
    image_id = images[image_idx].id

    alt_text = ' '.join(fake.words(nb=5))
    caption = ' '.join(fake.words(nb=5))
    caption_url = fake.url(schemes=['https'])

    return generate_field('image', {
        'image': image_id,
        'altText': alt_text,
        'caption': caption,
        'captionURL': caption_url,
    })


def generate_image_text2_field():
    images = Image.objects.all()
    image_idx = fake.unix_time() % images.count()
    image_id = images[image_idx].id

    image_text = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    url = fake.url(schemes=['https'])
    alt_text = ' '.join(fake.words(nb=5))
    small = fake.boolean()

    return generate_field('image_text2', {
        'image': image_id,
        'text': image_text,
        'url': url,
        'altText': alt_text,
        'small': small,
    })


def generate_spacer_field():
    size =  1 + (fake.unix_time() % 5)

    return generate_field('spacer', {
        'size': size
    })


def generate_quote_field():
    quote = fake.sentence()
    attribution = fake.name()

    return generate_field('quote', {
        'quotes': [{
            'quote': quote,
            'attribution': attribution
        }]
    })


class StreamfieldProvider(BaseProvider):
    """
    A custom Faker Provider for relative image urls, for use with factory_boy

    >>> from factory import Faker
    >>> from networkapi.utility.faker import StreamfieldProvider
    >>> fake = Faker()
    >>> Faker.add_provider(StreamfieldProvider)
    """

    def streamfield(self, fields=None):
        """
        Generate a streamfield string containing the fields optionally defined in fields.
        Defaults to ['header', 'paragraph']
        """

        valid_fields = {
            'header': generate_header_field,
            'paragraph': generate_paragraph_field,
            'image': generate_image_field,
            'spacer': generate_spacer_field,
            'image_text2': generate_image_text2_field,
            'quote': generate_quote_field
        }

        streamfield_data = []

        # Default to a header and paragraph
        if not fields:
            fields = ['header', 'paragraph']

        for field in fields:
            if field in valid_fields:
                streamfield_data.append(valid_fields[field]())
            else:
                raise Exception(f'unknown field: {field}')

        return json.dumps(streamfield_data)
