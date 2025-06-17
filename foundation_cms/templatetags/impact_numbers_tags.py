import random

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def random_digits(length=10):
    return "".join(random.choices("0123456789", k=length))


@register.filter
def render_animated_number(value):
    """Render HTML digits with animation-ready attributes."""
    output = []
    digit_index = 1

    for char in str(value):
        if char.isdigit():
            data_fake = random_digits()
            digit_html = f"""
                <div class="impact-stat__digit-window impact-stat__digit-window--animated" aria-hidden="true">
                    <div class="impact-stat__digit impact-stat__digit--{ digit_index } display-text-1"
                         data-fake="{data_fake}">
                        {char}
                    </div>
                </div>
            """
            digit_index += 1
        else:
            # Handle non-digit characters (Ex: #, $, K, M, ',' , '.' )
            digit_html = f"""
                <div class="impact-stat__digit-window" aria-hidden="true">
                    <div class="impact-stat__digit">{char}</div>
                </div>
            """
        output.append(digit_html.strip())

    return mark_safe("".join(output))
