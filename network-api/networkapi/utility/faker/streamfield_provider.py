import json

from random import randint, choice
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
        f'<p>{fake.text(max_nb_chars=200)} <b>This sentence is in bold text.</b> {fake.text(max_nb_chars=200)} ',
        f'<a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a> ',
        f'{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>',
        f'<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>',
        '<ul>',
        ''.join([f'<li>{fake.word()}</li>' for i in range(10)]),
        '</ul><br />',
        f'<p><a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a></p>',
    )

    return generate_field('paragraph', ''.join(paragraphs))


def generate_header_field():
    value = ' '.join(fake.words())

    return generate_field('header', value)


# generates a image field of type "ImageBlock"
def generate_basic_image_field():
    image_id = choice(Image.objects.all()).id
    alt_text = ' '.join(fake.words(nb=5))

    return generate_field('image', {
        'image': image_id,
        'altText': alt_text,
    })


# generates a image field of type "AnnotatedImageBlock"
def generate_image_field():
    image_id = choice(Image.objects.all()).id
    alt_text = ' '.join(fake.words(nb=5))
    caption = ' '.join(fake.words(nb=5))
    caption_url = fake.url(schemes=['https'])

    return generate_field('image', {
        'image': image_id,
        'altText': alt_text,
        'caption': caption,
        'captionURL': caption_url,
    })


def generate_image_text_field():
    image_id = choice(Image.objects.all()).id
    image_text = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    url = fake.url(schemes=['https'])
    alt_text = ' '.join(fake.words(nb=5))
    top_divider = fake.boolean()
    bottom_divider = top_divider

    return generate_field('image_text', {
        'image': image_id,
        'text': image_text,
        'url': url,
        'altText': alt_text,
        'top_divider': top_divider,
        'bottom_divider': bottom_divider,
    })


def generate_image_text_mini_field():
    image_id = choice(Image.objects.all()).id
    image_text = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    alt_text = ' '.join(fake.words(nb=5))

    return generate_field('image_text_mini', {
        'image': image_id,
        'text': image_text,
        'altText': alt_text,
    })


def generate_spacer_field():
    size = randint(1, 5)

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


def generate_video_field():
    caption = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    captionURL = fake.url(schemes=['https'])

    return generate_field('video', {
        # Fake embed url will lead to timeout error for Percy.
        # Solution: either we provide a valid embed url or use an empty string.
        # See details: https://github.com/mozilla/foundation.mozilla.org/issues/3833#issuecomment-562240677
        'url': '',
        'caption': caption,
        'captionURL': captionURL,
    })


def generate_linkbutton_field():
    label = ' '.join(fake.words(nb=3))
    url = fake.url(schemes=['https'])
    styling = choice(['btn-primary', 'btn-secondary'])

    return generate_field('linkbutton', {
        'label': label,
        'URL': url,
        'styling': styling,
    })


def generate_text_field():
    value = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)

    return generate_field('text', value)


def generate_regret_story_field():
    headline = ' '.join(fake.words(nb=10))
    image_id = choice(Image.objects.all()).id
    image_text = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    story = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)

    return generate_field('regret_story', {
        'headline': headline,
        'image': image_id,
        'imageAltText': image_text,
        'story': story,
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
            'quote': generate_quote_field,
            'basic_image': generate_basic_image_field,
            'image_text': generate_image_text_field,
            'image_text_mini': generate_image_text_mini_field,
            'video': generate_video_field,
            'linkbutton': generate_linkbutton_field,
            'text': generate_text_field,
            'regret_story': generate_regret_story_field,
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
