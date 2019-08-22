from django import template

register = template.Library()


@register.inclusion_tag('wagtailpages/blocks/tr_key_value_block.html', takes_context=True)
def gettext(context, key):
    page = context['page']

    if 'value' in context:
        del context['value']

    for textfield in page.specific.textfields:
        value = textfield.value
        if value['key'] == key:
            context['value'] = value

    if 'value' not in context:
        context['value'] = {
            'key': key,
            'textblock': f'ERROR: no text found for key "{key}"!',
        }

    return context
