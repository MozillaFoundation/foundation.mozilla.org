import json

from random import randint, choice, random
from django.conf import settings
from faker import Faker
from faker.providers import BaseProvider
from wagtail.images.models import Image
from networkapi.wagtailpages.models import BlogPage


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


def generate_content_field():
    image_id = choice(Image.objects.all()).id

    paragraphs = (
        f'<h2>{fake.sentence()}</h2>',
        f'<p>{fake.text(max_nb_chars=200)} <b>This sentence is in bold text.</b> {fake.text(max_nb_chars=200)} ',
        f'<a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a></p>',
        f'<embed alt="An image" embedtype="image" format="right" id="{image_id}"/>',
        f'<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>',
        f'<embed alt="An image" embedtype="image" format="left" id="{image_id}"/>',
        f'<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>',
        f'<embed alt="An image" embedtype="image" format="fullwidth" id="{image_id}"/>',
        f'<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>',
        f'<p><a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a></p>',
    )

    return generate_field('content', ''.join(paragraphs))


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


def generate_double_image_field():
    image_1 = choice(Image.objects.all()).id
    image_1_caption = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    image_2 = choice(Image.objects.all()).id

    return generate_field('double_image', {
        'image_1': image_1,
        'image_1_caption': image_1_caption,
        'image_2': image_2,
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
        'url': 'https://www.youtube.com/embed/83fk3RT8318',
        'caption': caption,
        'captionURL': captionURL,
        'video_width': 'full_width'
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


def generate_callout_field():
    value = fake.sentence(nb_words=10)
    return generate_field('callout', value)


def generate_full_width_image_field():
    image = choice(Image.objects.all()).id
    caption = fake.sentence(nb_words=10)

    return generate_field('full_width_image', {
        'image': image,
        'caption': caption,
    })


def generate_dear_internet_intro_text_field():
    text = f'<p>{fake.paragraph(nb_sentences=3, variable_nb_sentences=True)}</p>'

    return generate_field('intro_text', text)


def generate_image_grid_field():
    imgs = []

    for n in range(4):
        imgs.append({
                'image': choice(Image.objects.all()).id,
                'caption': fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
            }
        )

    return generate_field('image_grid', {
        'grid_items': imgs
    })


def generate_card_grid_field():
    cards = []

    for n in range(6):
        cards.append({
                'image': choice(Image.objects.all()).id,
                'title': fake.paragraph(nb_sentences=1, variable_nb_sentences=False),
                'body': fake.paragraph(nb_sentences=10, variable_nb_sentences=True),
                'link_label': ' '.join(fake.words(nb=3)),
                'link_url': fake.url(schemes=['https'])
            }
        )

    return generate_field('card_grid', {
        'cards': cards
    })


def generate_pulse_listing_field():
    return generate_field('pulse_listing', {
        'only_featured_entries': True,
        'help': 'all',
        'issues': 'all',
        'size': 6,
        'search_terms': '',
        'newest_first': True,
        'direct_link': False
    })


def generate_profile_listing_field():
    return generate_field('profile_listing', {
        'max_number_of_results': 6
    })


def generate_recent_blog_entries_field():
    return generate_field('recent_blog_entries', {})


def generate_blog_set_field():
    return generate_field('blog_set', {
        'title': ' Test Blog Set',
        'blog_pages': [blog.id for blog in BlogPage.objects.all()[:5]]
    })


def generate_airtable_field():
    return generate_field('airtable', {
        'url': 'https://airtable.com/embed/shrWlw8ElgBb17nrM?backgroundColor=blue'
    })


def generate_typeform_field():
    return generate_field('typeform', {
        'embed_id': 'ZdwBxz8E',
        'button_text': 'Test'
    })


def generate_dear_internet_letter_field():
    author_name = fake.name()
    author_description = ''.join(
        (
            '<p>',
            f'<a href="{fake.url(schemes=["https"])}" target="_blank">{author_name}</a>',
            f' is {" ".join(fake.words(nb=15))}. {fake.sentence()}',
            '</p>',
        )
    )

    letter = f'<p>{fake.paragraph(nb_sentences=10, variable_nb_sentences=True)}</p>'

    attributes = {
        'author_name': author_name,
        'author_description': author_description,
        'letter': letter,
    }

    if random() > 0.5:
        attributes['author_photo'] = choice(Image.objects.all()).id

    if random() > 0.5:
        attributes['image'] = choice(Image.objects.all()).id

    if random() > 0.5:
        attributes['video_url'] = fake.url(schemes=["https"])

    return generate_field('letter', attributes)


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
            'double_image': generate_double_image_field,
            'video': generate_video_field,
            'linkbutton': generate_linkbutton_field,
            'text': generate_text_field,
            'regret_story': generate_regret_story_field,
            'content': generate_content_field,
            'callout': generate_callout_field,
            'full_width_image': generate_full_width_image_field,
            'intro_text': generate_dear_internet_intro_text_field,
            'letter': generate_dear_internet_letter_field,
            'card_grid': generate_card_grid_field,
            'image_grid': generate_image_grid_field,
            'pulse_listing': generate_pulse_listing_field,
            'profile_listing': generate_profile_listing_field,
            'recent_blog_entries': generate_recent_blog_entries_field,
            'blog_set': generate_blog_set_field,
            'airtable': generate_airtable_field,
            'typeform': generate_typeform_field
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
