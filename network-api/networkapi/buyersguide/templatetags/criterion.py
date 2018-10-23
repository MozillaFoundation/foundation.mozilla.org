from django import template

register = template.Library()


@register.inclusion_tag('tags/criterion.html')
def criterion(id, question, answer, helptext=None, indeterminate_copy="Can't determine"):
    cssClassSuffix = "null"

    if answer is None:
        formattedAnswer = indeterminate_copy
    elif isinstance(answer, str):
        if answer is "0":
            cssClassSuffix = "0"
            formattedAnswer = indeterminate_copy
        else:
            cssClassSuffix = answer
            formattedAnswer = ("{answer}".format(answer=answer))
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
