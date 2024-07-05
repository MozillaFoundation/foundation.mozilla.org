import json
from random import choice, randint, random

from django.conf import settings
from faker import Faker
from faker.providers import BaseProvider
from wagtail.images.models import Image

from networkapi.wagtailpages.models import BlogPage, BlogPageTopic

seed = randint(0, 5000000)
if settings.RANDOM_SEED is not None:
    seed = settings.RANDOM_SEED

fake = Faker()
fake.random.seed(seed)


def generate_field(field_type, value):
    return {
        "type": field_type,
        "value": value,
        "id": fake.uuid4(),
    }


def generate_paragraph_field():
    paragraphs = (
        f"<h3>{fake.sentence()}</h3>",
        f"<p>{fake.text(max_nb_chars=200)} <b>This sentence is in bold text.</b> {fake.text(max_nb_chars=200)} ",
        f'<a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a> ',
        f"{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>",
        f"<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>",
        "<ul>",
        "".join([f"<li>{fake.word()}</li>" for i in range(10)]),
        "</ul><br />",
        f'<p><a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a></p>',
    )

    return generate_field("paragraph", "".join(paragraphs))


def generate_content_field():
    image_id = choice(Image.objects.all()).id

    paragraphs = (
        f"<h2>{fake.sentence()}</h2>",
        f"<p>{fake.text(max_nb_chars=200)} <b>This sentence is in bold text.</b> {fake.text(max_nb_chars=200)} ",
        f'<a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a></p>',
        f'<embed alt="An image" embedtype="image" format="right" id="{image_id}"/>',
        f"<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>",
        f'<embed alt="An image" embedtype="image" format="left" id="{image_id}"/>',
        f"<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>",
        f'<embed alt="An image" embedtype="image" format="fullwidth" id="{image_id}"/>',
        f"<p>{fake.paragraph(nb_sentences=20, variable_nb_sentences=True)}</p>",
        f'<p><a href="{fake.url(schemes=["https"])}">This is a link to a fake url!</a></p>',
    )

    return generate_field("content", "".join(paragraphs))


def generate_header_field():
    value = " ".join(fake.words())

    return generate_field("header", value)


# generates a image field of type "ImageBlock"
def generate_basic_image_field():
    image_id = choice(Image.objects.all()).id
    alt_text = " ".join(fake.words(nb=5))

    return generate_field(
        "image",
        {
            "image": image_id,
            "altText": alt_text,
        },
    )


# generates a image field of type "AnnotatedImageBlock"
def generate_image_field():
    image_id = choice(Image.objects.all()).id
    alt_text = " ".join(fake.words(nb=5))
    caption = " ".join(fake.words(nb=5))
    caption_external_url = [
        {
            "link_to": "external_url",
            "external_url": fake.url(schemes=["https"]),
            "new_window": True,
        }
    ]

    return generate_field(
        "image",
        {"image": image_id, "altText": alt_text, "caption": caption, "caption_url": caption_external_url},
    )


def generate_image_text_field():
    image_id = choice(Image.objects.all()).id
    image_text = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    url = [
        {
            "link_to": "external_url",
            "external_url": fake.url(schemes=["https"]),
            "new_window": True,
        }
    ]
    alt_text = " ".join(fake.words(nb=5))
    top_divider = fake.boolean()
    bottom_divider = top_divider

    return generate_field(
        "image_text",
        {
            "image": image_id,
            "text": image_text,
            "url": url,
            "altText": alt_text,
            "top_divider": top_divider,
            "bottom_divider": bottom_divider,
        },
    )


def generate_image_text_mini_field():
    image_id = choice(Image.objects.all()).id
    image_text = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    alt_text = " ".join(fake.words(nb=5))

    return generate_field(
        "image_text_mini",
        {
            "image": image_id,
            "text": image_text,
            "altText": alt_text,
        },
    )


def generate_double_image_field():
    image_1 = choice(Image.objects.all()).id
    image_1_caption = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    image_2 = choice(Image.objects.all()).id

    return generate_field(
        "double_image",
        {
            "image_1": image_1,
            "image_1_caption": image_1_caption,
            "image_2": image_2,
        },
    )


def generate_spacer_field():
    size = randint(1, 5)

    return generate_field("spacer", {"size": size})


def generate_common_quote_field(dark=False):
    """
    Generate common quote fields used by both generate_quote_field and generate_dark_quote_field.

    Args:
        dark (bool): Whether to generate fields for a dark quote.
        Defaults to False for a single quote.
    """
    quote = f"<p>{fake.sentence()}</p>"
    attribution = fake.name()
    attribution_info = f'<p>{fake.sentence()} <a href="{fake.url(schemes=["https"])}">{fake.sentence()}</a></p>'

    field_name = "dark_quote" if dark else "single_quote"

    return generate_field(
        field_name,
        {
            "quote": quote,
            "attribution": attribution,
            "attribution_info": attribution_info,
        },
    )


def generate_quote_field():
    return generate_common_quote_field()


def generate_dark_quote_field():
    return generate_common_quote_field(dark=True)


def generate_video_field():
    caption = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    captionURL = fake.url(schemes=["https"])

    return generate_field(
        "video",
        {
            # Fake embed url will lead to timeout error for Percy.
            # Solution: either we provide a valid embed url or use an empty string.
            # See details: https://github.com/mozilla/foundation.mozilla.org/issues/3833#issuecomment-562240677
            "url": "https://www.youtube.com/embed/83fk3RT8318",
            "caption": caption,
            "captionURL": captionURL,
            "video_width": "full_width",
        },
    )


def generate_linkbutton_field():
    label = " ".join(fake.words(nb=3))
    url = fake.url(schemes=["https"])
    styling = choice(["btn-primary", "btn-secondary"])

    return generate_field(
        "linkbutton",
        {
            "label": label,
            "styling": styling,
            "link_to": "external_url",
            "external_url": url,
            "relative_url": "",
            "page": None,
            "file": None,
            "anchor": "",
            "email": "",
            "phone": "",
        },
    )


def generate_text_field():
    value = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    return generate_field("text", value)


def generate_regret_story_field():
    headline = " ".join(fake.words(nb=10))
    image_id = choice(Image.objects.all()).id
    image_text = fake.paragraph(nb_sentences=1, variable_nb_sentences=False)
    story = fake.paragraph(nb_sentences=5, variable_nb_sentences=True)

    return generate_field(
        "regret_story",
        {
            "headline": headline,
            "image": image_id,
            "imageAltText": image_text,
            "story": story,
        },
    )


def generate_callout_field():
    value = f"<p>{fake.sentence(nb_words=10)}</p>"

    return generate_field("callout", value)


def generate_full_width_image_field():
    image = choice(Image.objects.all()).id
    caption = fake.sentence(nb_words=10)

    return generate_field(
        "full_width_image",
        {
            "image": image,
            "caption": caption,
        },
    )


def generate_dear_internet_intro_text_field():
    text = f"<p>{fake.paragraph(nb_sentences=3, variable_nb_sentences=True)}</p>"

    return generate_field("intro_text", text)


def generate_image_grid_field():
    imgs = []

    for n in range(4):
        imgs.append(
            {
                "image": choice(Image.objects.all()).id,
                "caption": fake.paragraph(nb_sentences=1, variable_nb_sentences=False),
            }
        )

    return generate_field("image_grid", {"grid_items": imgs})


def generate_card_grid_field():
    cards = []

    for n in range(6):
        cards.append(
            {
                "image": choice(Image.objects.all()).id,
                "title": fake.paragraph(nb_sentences=1, variable_nb_sentences=False),
                "body": fake.paragraph(nb_sentences=10, variable_nb_sentences=True),
                "link_label": " ".join(fake.words(nb=3)),
                "link_url": fake.url(schemes=["https"]),
            }
        )

    return generate_field("card_grid", {"cards": cards})


def generate_stats_block_field():
    statistics = []

    for n in range(4):
        statistics.append(
            {
                "title": str(fake.pyint()),
                "description": " ".join(fake.words(nb=8)),
            }
        )

    return generate_field("statistics", {"statistics": statistics})


def generate_pulse_listing_field():
    return generate_field(
        "pulse_listing",
        {
            "only_featured_entries": True,
            "help": "all",
            "issues": "all",
            "size": 6,
            "search_terms": "",
            "newest_first": True,
            "direct_link": False,
        },
    )


def generate_profile_listing_field():
    return generate_field("profile_listing", {"max_number_of_results": 6})


def generate_recent_blog_entries_field():
    return generate_field("recent_blog_entries", {})


def generate_blog_set_field():
    return generate_field(
        "blog_set",
        {
            "title": " Test Blog Set",
            "blog_pages": [blog.id for blog in BlogPage.objects.all()[:5]],
        },
    )


def generate_airtable_field():
    return generate_field(
        "airtable",
        {"url": "https://airtable.com/embed/shrWlw8ElgBb17nrM?backgroundColor=blue"},
    )


def generate_typeform_field():
    return generate_field("typeform", {"embed_id": "ZdwBxz8E", "button_text": "Test"})


def generate_datawrapper_field():
    return generate_field("datawrapper", "https://datawrapper.dwcdn.net/0rmUn/3/")


def generate_dear_internet_letter_field():
    author_name = fake.name()
    author_description = "".join(
        (
            "<p>",
            f'<a href="{fake.url(schemes=["https"])}" target="_blank">{author_name}</a>',
            f' is {" ".join(fake.words(nb=15))}. {fake.sentence()}',
            "</p>",
        )
    )

    letter = f"<p>{fake.paragraph(nb_sentences=10, variable_nb_sentences=True)}</p>"

    attributes = {
        "author_name": author_name,
        "author_description": author_description,
        "letter": letter,
    }

    if random() > 0.5:
        attributes["author_photo"] = choice(Image.objects.all()).id

    if random() > 0.5:
        attributes["image"] = choice(Image.objects.all()).id

    if random() > 0.5:
        attributes["video_url"] = fake.url(schemes=["https"])

    return generate_field("letter", attributes)


def generate_banner_carousel_field():
    return generate_field(
        "slide",
        {
            "image": choice(Image.objects.all()).id,
            "heading": fake.sentence(nb_words=4, variable_nb_words=True),
            "description": fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
        },
    )


def generate_banner_video_field():
    return generate_field(
        "external_video",
        {
            "video_url": "https://www.youtube.com/embed/3FIVXBawyQw",
            "thumbnail": choice(Image.objects.all()).id,
        },
    )


def generate_current_events_slider_field():
    title = fake.sentence(nb_words=4, variable_nb_words=True)
    current_events = [
        generate_current_event_field(),
        generate_current_event_field(),
        generate_current_event_field(),
    ]

    return generate_field(
        "current_events_slider",
        {
            "title": title,
            "current_events": current_events,
        },
    )


def generate_current_event_field():
    title = fake.sentence(nb_words=4, variable_nb_words=True)
    subheading_link = [generate_labelled_external_link_field()]

    image = choice(Image.objects.all()).id
    body = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)

    buttons = [
        generate_labelled_external_link_field(),
        generate_labelled_external_link_field(),
    ]

    return generate_field(
        "current_event",
        {
            "title": title,
            "subheading_link": subheading_link,
            "image": image,
            "body": body,
            "buttons": buttons,
        },
    )


def generate_labelled_external_link_field():
    return generate_field(
        "external",
        {"label": fake.sentence(nb_words=3), "link": fake.url(schemes=["https"])},
    )


def generate_blog_index_callout_box_field():
    title = fake.sentence(nb_words=10, variable_nb_words=True)
    related_topics = [choice(BlogPageTopic.objects.all()).id]
    body = fake.paragraph(nb_sentences=6, variable_nb_sentences=False)
    show_icon = True
    link_button = [
        {
            "label": "Learn More",
            "link_to": "external_url",
            "external_url": fake.url(schemes=["https"]),
            "new_window": True,
        }
    ]

    return generate_field(
        "callout_box",
        {
            "title": title,
            "related_topics": related_topics,
            "show_icon": show_icon,
            "body": body,
            "link_button": link_button,
        },
    )


def generate_blog_newsletter_signup_field():
    from networkapi.wagtailpages.factory.customblocks.newsletter_signup_block import (
        BlogNewsletterSignupBlockFactory,
    )
    from networkapi.wagtailpages.pagemodels.customblocks.newsletter_signup_block import (
        BlogNewsletterSignupBlock,
    )

    block = BlogNewsletterSignupBlockFactory.create()
    return generate_field("newsletter_signup", BlogNewsletterSignupBlock().get_api_representation(block))


def generate_listing_block_field():
    heading = fake.sentence(nb_words=10, variable_nb_words=True)
    cards = []

    for n in range(2):
        cards.append(
            {
                "image": choice(Image.objects.all()).id,
                "alt_text": " ".join(fake.words(nb=5)),
                "title": fake.paragraph(nb_sentences=1, variable_nb_sentences=False),
                "highlighted_metadata": " ".join(fake.words(nb=2)),
                "metadata": " ".join(fake.words(nb=3)),
                "body": fake.paragraph(nb_sentences=10, variable_nb_sentences=True),
                "link": [
                    {
                        "link_to": "external_url",
                        "external_url": fake.url(schemes=["https"]),
                        "new_window": True,
                    }
                ],
            }
        )

    return generate_field("listing", {"cards": cards, "heading": heading})


def generate_carousel_text_block_field():
    heading = fake.sentence(nb_words=10, variable_nb_words=True)
    text = fake.paragraph(nb_sentences=10, variable_nb_sentences=True)
    link_url = fake.url(schemes=["https"])
    link_label = fake.sentence(nb_words=5, variable_nb_words=True)
    carousel_images = []

    for n in range(4):
        carousel_images.append(
            {
                "image": choice(Image.objects.all()).id,
                "altText": " ".join(fake.words(nb=5)),
            }
        )

    data = {
        "heading": heading,
        "text": text,
        "link_url": link_url,
        "link_label": link_label,
        "carousel_images": carousel_images,
    }

    return generate_field("carousel_and_text", data)


def generate_cta_field():
    heading = fake.sentence(nb_words=3, variable_nb_words=True)
    text = fake.paragraph(nb_sentences=2, variable_nb_sentences=True)
    link = fake.url(schemes=["https"])
    label = fake.sentence(nb_words=2, variable_nb_words=True)
    dark_background = True

    cta = {
        "heading": heading,
        "text": text,
        "label": label,
        "dark_background": dark_background,
        "link_to": "external_url",
        "external_url": link,
        "page": None,
        "file": None,
        "anchor": "",
        "email": "",
        "phone": "",
    }

    return generate_field("cta", cta)


def generate_tickets_block_field():
    heading = fake.sentence(nb_words=10, variable_nb_words=True)
    tickets = []
    from networkapi.mozfest.factory import TicketSnippetFactory

    for n in range(3):
        ticket_snippet = TicketSnippetFactory.create()
        tickets.append(ticket_snippet.id)

    return generate_field("tickets", {"heading": heading, "tickets": tickets})


def generate_session_slider_item():
    title = fake.sentence(nb_words=4, variable_nb_words=True)
    author_subheading = fake.sentence(nb_words=3, variable_nb_words=True)

    image = choice(Image.objects.all()).id
    body = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
    return generate_field(
        "session_item",
        {
            "title": title,
            "author_subheading": author_subheading,
            "image": image,
            "body": body,
            "link": [generate_labelled_external_link_field()],
        },
    )


def generate_session_slider_field():
    title = fake.sentence(nb_words=3, variable_nb_words=True)
    button = [generate_labelled_external_link_field()]
    session_items = [
        generate_session_slider_item(),
        generate_session_slider_item(),
        generate_session_slider_item(),
        generate_session_slider_item(),
        generate_session_slider_item(),
    ]

    return generate_field("session_slider", {"title": title, "session_items": session_items, "button": button})


def generate_profiles_field():
    profiles = []
    from networkapi.wagtailpages.factory.profiles import ProfileFactory

    for n in range(9):
        profile_snippet = ProfileFactory.create()
        profiles.append({"profile": profile_snippet.id})

    return generate_field("profiles", {"profiles": profiles})


def generate_newsletter_signup_with_background_field():
    from networkapi.mozfest.factory import NewsletterSignupWithBackgroundSnippetFactory

    newsletter_snippet = NewsletterSignupWithBackgroundSnippetFactory.create()

    return generate_field("newsletter_signup", {"snippet": newsletter_snippet.id})


def generate_mixed_content_field():
    cards = []
    link_url = fake.url(schemes=["https"])
    link_text = fake.sentence(nb_words=2, variable_nb_words=True)

    for n in range(4):
        cards.append(
            {
                "image": choice(Image.objects.all()).id,
                "alt_text": " ".join(fake.words(nb=5)),
                "title": fake.paragraph(nb_sentences=1, variable_nb_sentences=False),
                "highlighted_metadata": " ".join(fake.words(nb=2)),
                "metadata": " ".join(fake.words(nb=3)),
                "body": fake.paragraph(nb_sentences=10, variable_nb_sentences=True),
                "link": [
                    {
                        "link_to": "external_url",
                        "external_url": fake.url(schemes=["https"]),
                        "new_window": True,
                    }
                ],
            }
        )

    video = {
        "url": "https://www.youtube.com/embed/83fk3RT8318",
        "caption": fake.sentence(nb_words=2, variable_nb_words=True),
        "thumbnail": choice(Image.objects.all()).id,
        "title": fake.sentence(nb_words=4, variable_nb_words=True),
        "text": fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
    }

    return generate_field(
        "mixed_content", {"cards": cards, "video": video, "link_url": link_url, "link_text": link_text}
    )


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
            "header": generate_header_field,
            "paragraph": generate_paragraph_field,
            "image": generate_image_field,
            "spacer": generate_spacer_field,
            "quote": generate_quote_field,
            "basic_image": generate_basic_image_field,
            "image_text": generate_image_text_field,
            "image_text_mini": generate_image_text_mini_field,
            "double_image": generate_double_image_field,
            "video": generate_video_field,
            "linkbutton": generate_linkbutton_field,
            "text": generate_text_field,
            "regret_story": generate_regret_story_field,
            "content": generate_content_field,
            "callout": generate_callout_field,
            "full_width_image": generate_full_width_image_field,
            "intro_text": generate_dear_internet_intro_text_field,
            "letter": generate_dear_internet_letter_field,
            "card_grid": generate_card_grid_field,
            "image_grid": generate_image_grid_field,
            "pulse_listing": generate_pulse_listing_field,
            "profile_listing": generate_profile_listing_field,
            "recent_blog_entries": generate_recent_blog_entries_field,
            "blog_set": generate_blog_set_field,
            "airtable": generate_airtable_field,
            "typeform": generate_typeform_field,
            "datawrapper": generate_datawrapper_field,
            "banner_carousel": generate_banner_carousel_field,
            "banner_video": generate_banner_video_field,
            "current_events_slider": generate_current_events_slider_field,
            "callout_box": generate_blog_index_callout_box_field,
            "blog_newsletter_signup": generate_blog_newsletter_signup_field,
            "statistics": generate_stats_block_field,
            "listing": generate_listing_block_field,
            "carousel_and_text": generate_carousel_text_block_field,
            "tickets": generate_tickets_block_field,
            "dark_quote": generate_dark_quote_field,
            "cta": generate_cta_field,
            "session_slider": generate_session_slider_field,
            "profiles": generate_profiles_field,
            "newsletter_signup": generate_newsletter_signup_with_background_field,
            "mixed_content": generate_mixed_content_field,
        }

        streamfield_data = []

        # Default to a header and paragraph
        if not fields:
            fields = ["header", "paragraph"]

        for field in fields:
            if field in valid_fields:
                streamfield_data.append(valid_fields[field]())
            else:
                raise Exception(f"unknown field: {field}")

        return json.dumps(streamfield_data)
