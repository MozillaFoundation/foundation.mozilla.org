from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from networkapi.homepage.models import HomepageNews, HomepageHighlights


register = template.Library()


# This template tag allows us to customize the label for each choice field
# for People, News, and Highlights. It also allows us to add special case
# labels for certain fields.
# Most of this code is copied from
# django.contrib.admin.helpers.AdminField.label_tag() with some minor tweaks
@register.simple_tag(takes_context=True)
def get_label_for_field(context, field_number):
    admin_field = context['field']
    classes = []
    instance = admin_field.field.form.instance
    label = None

    # Rename the first field for the News section to indicate a video feature
    if isinstance(instance, HomepageNews):
        if field_number is 1:
            label = 'Video Feature'
        # Since we renamed the label for the first field, every subsequent
        # field will now be numbered 1 less than what they originally were
        field_number -= 1
    # Rename the first field for the Highlights section to indicate a project
    # feature
    elif isinstance(instance, HomepageHighlights):
        if field_number is 1:
            label = 'Project Feature'
        field_number -= 1

    # Default label for a field is the initial label followed by the number
    if label is None:
        label = '{} {}'.format(admin_field.field.label, field_number)

    contents = conditional_escape(label)

    if admin_field.field.field.required:
        classes.append('required')
    if not admin_field.is_first:
        classes.append('inline')
    attrs = {'class': ' '.join(classes)} if classes else {}

    return admin_field.field.label_tag(
        contents=mark_safe(contents),
        attrs=attrs,
        label_suffix='',
    )
