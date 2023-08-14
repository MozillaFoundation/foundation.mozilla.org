# Generated by Django 3.2.20 on 2023-08-03 19:13

from django.db import migrations
from django.db.models import Case, Value, When


def map_old_to_new(apps, schema_editor):
    Petition = apps.get_model("wagtailpages", "Petition")

    # Map value from the old comment_requirements field to the new show_comment_field
    # the current "none" value is mapped to False
    # the current "optional" value and "required" value are mapped to True
    Petition.objects.update(
        show_comment_field=Case(
            When(comment_requirements__isnull=True, then=Value(False)),
            When(comment_requirements__in=["optional", "required"], then=Value(True)),
            default=Value(False),
        )
    )


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0096_add_show_country_field_and_remove_old_fields"),
    ]

    operations = [
        migrations.RunPython(map_old_to_new),
    ]
