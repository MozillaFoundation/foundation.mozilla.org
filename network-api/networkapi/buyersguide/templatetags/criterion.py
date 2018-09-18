from django import template

register = template.Library()


@register.inclusion_tag('tags/criterion.html')
def criterion(id, question, answer):
    return {
        'id': id,
        'question': question,
        'answer': ("No", "Yes")[answer],
        'class': ("no", "yes")[answer],
    }
