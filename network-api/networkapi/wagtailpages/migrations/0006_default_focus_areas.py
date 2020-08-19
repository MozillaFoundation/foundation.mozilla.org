from django.db import migrations, models


def create_default_focus_areas(apps, schema_editor):
    FocusArea = apps.get_model("wagtailpages", "FocusArea")
    FocusArea.objects.get_or_create(
        name='Empower Action',
        description='Issues like privacy, trustworthy AI, and digital rights impact all of us. Mozilla helps empower meaningful',
    )
    FocusArea.objects.get_or_create(
        name='Connect Leaders',
        description='We support activists and thought leaders shaping the future of our online lives.',
    )
    FocusArea.objects.get_or_create(
        name='Investigate & Research',
        description='We publish open source research and host global convenings to make ideas like trustworthy AI mainstream.',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0005_homepage_refresh'),
    ]

    operations = [
        migrations.RunPython(create_default_focus_areas),
    ]


