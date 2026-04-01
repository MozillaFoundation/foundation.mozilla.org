from django.db import migrations


def create_legacy_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name="access/legacy content editor")


def delete_legacy_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="access/legacy content editor").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0173_add_legacy_to_verbose_names"),
    ]

    operations = [
        migrations.RunPython(create_legacy_group, reverse_code=delete_legacy_group),
    ]
