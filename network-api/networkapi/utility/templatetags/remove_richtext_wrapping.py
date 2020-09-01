from django import template
from bs4 import BeautifulSoup
register = template.Library()


@register.filter
def remove_wrapping(content=None):
    """
    Removes the .rich-text wrapper around richtext elements.
    Returns a string of all paragraphs.

    Note: This can be removed in Wagtail 2.11.
    """
    if content:
        soup = BeautifulSoup(str(content), 'html.parser')
        richtext = soup.find('div', attrs={"class": "rich-text"})
        paragraphs = richtext.findAll('p')
        return ' '.join([str(x) for x in paragraphs])

