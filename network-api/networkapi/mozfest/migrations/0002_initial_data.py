from django.db import migrations
from django.conf import settings


def ensure_mozfest_signup(apps, schema_editor, locale_id):
    Signup = apps.get_model('wagtailpages', 'Signup')
    test = Signup.objects.filter(name__iexact='mozfest').first()

    if test is None:
        Signup.objects.create(
            name='Mozfest',
            header='Sign Up for News and Updates',
            description='<p>Receive emails about Mozilla Festival and Mozilla</p>',
            newsletter='mozilla-foundation,mozilla-festival',
            locale_id=locale_id,
        )


def bootstrap_data(apps, schema_editor):
    Locale = apps.get_model("wagtailcore", "Locale")
    DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)
    locale_id = DEFAULT_LOCALE.pk
    ensure_mozfest_signup(apps, schema_editor, locale_id)


class Migration(migrations.Migration):

    dependencies = [
        ('mozfest', '0001_initial_models'),
        ('wagtailpages', '0002_initial_data'),
    ]

    operations = [
        migrations.RunPython(bootstrap_data),
    ]
