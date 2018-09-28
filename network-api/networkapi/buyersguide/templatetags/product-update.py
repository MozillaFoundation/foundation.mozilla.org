from django import template

register = template.Library()


@register.inclusion_tag('tags/product-update.html')
def productUpdate(source, title, author, snippet):
    return {
        'source': source,
        'title': title,
        'author': author,
        'snippet': snippet,
    }
