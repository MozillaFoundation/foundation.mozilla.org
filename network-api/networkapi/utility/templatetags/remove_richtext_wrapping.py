from django import template
from bs4 import BeautifulSoup
register = template.Library()


@register.filter
def remove_wrapping(content=None):
    """
    Removes the .rich-text wrapper around richtext elements.
    Returns a string of all paragraphs.

    In Wagtail 2.10 the .rich-text class that typically wraps around
    any richtext area from the |richtext template filter is removed.

    We've re-enabled it by installing `wagtail.contrib.legacy.richtext`.

    However, for image captions where we want to support bold, italics
    and links, we still require a richtext field but don't want to inherit
    any other .rich-text styling.

    This filter removes .rich-text from wrapping around the content
    allowing us to style the image captions easier.
    """
    if content:
        soup = BeautifulSoup(str(content), 'html.parser')
        richtext = soup.find('div', attrs={"class": "rich-text"})
        if richtext:
            paragraphs = richtext.findAll('p')
            return ' '.join([str(x) for x in paragraphs])
        return content

