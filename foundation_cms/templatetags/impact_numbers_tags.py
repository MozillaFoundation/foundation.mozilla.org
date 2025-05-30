import random

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def random_digits(length=10):
    return "".join(random.choices("0123456789", k=length))


@register.filter
def render_animated_number(value):
    """Render HTML digit spans with animation-ready attributes."""
    output = []
    digit_index = 1

    for char in str(value):
        if char.isdigit():
            data_fake = random_digits()
            digit_html = f"""
                <div class="numbers__window is-animated">
                    <div class="numbers__window__digit numbers__window__digit--{digit_index}" data-fake="{data_fake}">{char}</div>
                </div>
            """
            digit_index += 1
        else:
            # Handle non-digit characters like '.' or ','
            digit_html = f"""
                <div class="numbers__window">
                    <div class="numbers__window__digit">{char}</div>
                </div>
            """
        output.append(digit_html.strip())

    return mark_safe("".join(output))
