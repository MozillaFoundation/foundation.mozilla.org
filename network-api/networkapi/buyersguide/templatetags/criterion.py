from django import template

register = template.Library()


@register.inclusion_tag('tags/criterion.html')
def criterion(id, question, answer, helptext=None):
    cssClassSuffix = "null"

    if answer is None:
        formattedAnswer = "Can't determine"
    elif isinstance(answer, str):
        if answer is "0":
            cssClassSuffix = "0"
            formattedAnswer = "Can't Determine"
        else:
            cssClassSuffix = answer
            formattedAnswer = ("Grade {answer}".format(answer=answer))
    else:
        cssClassSuffix = ("false", "true")[answer]
        formattedAnswer = ("No", "Yes")[answer]

    return {
        'id': id,
        'question': question,
        'answer': formattedAnswer,
        'class': cssClassSuffix,
        'helptext': helptext,
    }
