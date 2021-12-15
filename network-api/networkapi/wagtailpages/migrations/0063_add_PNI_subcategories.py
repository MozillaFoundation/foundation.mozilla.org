from django.db import migrations
from django.template.defaultfilters import slugify

def add_pni_subcategories(apps, schema):
    BuyersGuideProductCategory = apps.get_model("wagtailpages", "BuyersGuideProductCategory")
    healthAndExercise = BuyersGuideProductCategory.objects.get(name="Health & Exercise")

    subcategories = [
        "Exercise Equipment",
        "Smart Scales",
        "Smart Thermometers",
    ]

    for cat in subcategories:
        print(f"creating {cat}")
        subcategory, created = BuyersGuideProductCategory.objects.get_or_create(
            name=cat,
            parent=healthAndExercise,
            locale_id=healthAndExercise.locale_id,
        )
        if created:
            subcategory.slug = slugify(cat)
            subcategory.save()


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0062_auto_20211213_2059'),
    ]

    operations = [
        migrations.RunPython(
            add_pni_subcategories
        ),
    ]
