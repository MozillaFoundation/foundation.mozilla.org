from django.db import migrations


def fix(apps, schema_editor):
    """Fix NothingPersonalArticlePage rows with displayed_hero_content set to 'image' but no hero_image."""
    NothingPersonalArticlePage = apps.get_model("nothing_personal", "NothingPersonalArticlePage")
    updated = NothingPersonalArticlePage.objects.filter(
        displayed_hero_content="image", hero_image__isnull=True
    ).update(displayed_hero_content="")
    print(f"\n  nothing_personal.NothingPersonalArticlePage: {updated} rows fixed")


class Migration(migrations.Migration):
    dependencies = [("nothing_personal", "0058_alter_nothingpersonalarticlepage_displayed_hero_content")]
    operations = [migrations.RunPython(fix, migrations.RunPython.noop)]
