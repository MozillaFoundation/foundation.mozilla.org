from django.db import migrations
from django.conf import settings
from django.template.defaultfilters import slugify

def add_pni_subcategories(apps, schema):
    Locale = apps.get_model("wagtailcore", "Locale")
    DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)

    BuyersGuideProductCategory = apps.get_model("wagtailpages", "BuyersGuideProductCategory")
    healthAndExercise = BuyersGuideProductCategory.objects.get(
        name="Health & Exercise",
        locale=DEFAULT_LOCALE
    )

    subcategories = [
        "Exercise Equipment",
        "Smart Scales",
        "Smart Thermometers",
    ]

    for cat in subcategories:
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
        ('wagtailpages', '0063_pulsefilter_pulsefilteroption'),
    ]

    operations = [
        migrations.RunPython(
            add_pni_subcategories
        ),
    ]
