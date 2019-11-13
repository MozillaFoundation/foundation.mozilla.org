from django.conf import settings
from django.utils.html import format_html_join
from django.utils.translation import gettext

from wagtail.core import hooks


@hooks.register('insert_global_admin_js')
def language_toggles():
    """
    On any admin page, try to load the l10n code that aggregates
    fieldsets per locale, then gives it a button that you can
    click to show/hide all those fields.
    """

    js_files = ['js/language_toggles.js']

    lang_codes = []
    for lang in settings.LANGUAGES:
        lang_codes.append("'%s'" % lang[0])

    js_languages = """
    <script>
        wagtailModelTranslations = {{
            languages: [{languages}],
            defaultLanguage: '{language_code}',
            viewEditString: '{view_edit_string}',
        }};
    </script>
    """.format(
        languages=", ".join(lang_codes),
        language_code=settings.LANGUAGE_CODE,
        view_edit_string=gettext('View / edit fields for')
    )

    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    css_files = ['css/language_toggles.css']

    css_includes = format_html_join(
        '\n', '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files)
    )

    return js_languages + js_includes + css_includes
