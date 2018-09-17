from django import template

register = template.Library()


@register.inclusion_tag('tags/criterion.html')
def criterion(question, answer):
    return {
        'question': question,
        'answer': answer,
    }
