# Custom migration to delete existing RedirectingPage instances before removing the model.

from django.db import migrations


def delete_redirecting_pages(apps, schema_editor):
    RedirectingPage = apps.get_model("wagtailpages", "RedirectingPage")
    RedirectingPage.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0102_pni_petition_remove_old_fields"),
    ]

    operations = [
        migrations.RunPython(delete_redirecting_pages, reverse_code=migrations.RunPython.noop),
    ]
