# Generated by Django 3.0.14 on 2021-05-17 22:53

from django.db import migrations


def delete_factory_collections(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Collection = apps.get_model('wagtailcore', 'Collection')
    Collection.objects.filter(depth=1).exclude(id=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0007_auto_20210422_2311'),
    ]

    run_before = [
        ('wagtaildocs', '0011_add_choose_permissions'),
    ]

    operations = [
        migrations.RunPython(delete_factory_collections),
    ]
