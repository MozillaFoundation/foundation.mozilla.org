from django.db import migrations


def fix(apps, schema_editor):
    """Fix GeneralPage rows with displayed_hero_content set to 'image' but no hero_image."""
    GeneralPage = apps.get_model("core", "GeneralPage")
    updated = GeneralPage.objects.filter(displayed_hero_content="image", hero_image__isnull=True).update(
        displayed_hero_content=""
    )
    print(f"\n  core.GeneralPage: {updated} rows fixed")


class Migration(migrations.Migration):
    dependencies = [("core", "0084_add_catalan_locale")]
    operations = [migrations.RunPython(fix, migrations.RunPython.noop)]
