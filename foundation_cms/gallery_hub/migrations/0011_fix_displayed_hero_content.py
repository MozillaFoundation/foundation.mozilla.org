from django.db import migrations


def fix(apps, schema_editor):
    """Fix ProjectPage rows with displayed_hero_content set to 'image' but no hero_image."""
    ProjectPage = apps.get_model("gallery_hub", "ProjectPage")
    updated = ProjectPage.objects.filter(displayed_hero_content="image", hero_image__isnull=True).update(
        displayed_hero_content=""
    )
    print(f"\n  gallery_hub.ProjectPage: {updated} rows fixed")


class Migration(migrations.Migration):
    dependencies = [("gallery_hub", "0010_alter_projectpage_displayed_hero_content")]
    operations = [migrations.RunPython(fix, migrations.RunPython.noop)]
