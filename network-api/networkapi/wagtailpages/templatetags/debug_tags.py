from django.template import Library
from django.conf import settings
register = Library()

if settings.DEBUG:
    print('→ Running in DEBUG mode: enabling debug template tag "inspect_object" in tag collection "debug_tags".\n')

    @register.simple_tag
    def inspect_object(instance, prefix_label=""):
        output = str(dir(instance)).replace(', ', ',\n')
        prefix_label = str(prefix_label)
        return f'<pre>{prefix_label} {output}</pre>'
