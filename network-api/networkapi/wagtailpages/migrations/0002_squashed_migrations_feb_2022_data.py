from django.conf import settings
from django.db import migrations
from django.template.defaultfilters import slugify


def create_default_blog_categories(apps, schema_editor, locale_id):
    BlogPageCategory = apps.get_model("wagtailpages", "BlogPageCategory")

    BlogPageCategory.objects.get_or_create(name='Mozilla Festival', locale_id=locale_id)
    BlogPageCategory.objects.get_or_create(name='Open Leadership & Events', locale_id=locale_id)
    BlogPageCategory.objects.get_or_create(name='Internet Health Report', locale_id=locale_id)
    BlogPageCategory.objects.get_or_create(name='Fellowships & Awards', locale_id=locale_id)
    BlogPageCategory.objects.get_or_create(name='Advocacy', locale_id=locale_id)


def create_default_focus_areas(apps, schema_editor, locale_id):
    FocusArea = apps.get_model("wagtailpages", "FocusArea")

    FocusArea.objects.get_or_create(
        name='Rally Citizens',
        description='Issues like privacy, trustworthy AI, and digital rights impact all of us who use the internet. Mozilla helps translate them and empower meaningful change.',
        locale_id=locale_id,
    )
    FocusArea.objects.get_or_create(
        name='Connect Leaders',
        description='We support activists and thought leaders shaping the future of our online lives.',
        locale_id=locale_id,
    )
    FocusArea.objects.get_or_create(
        name='Shape the Agenda',
        description='We publish open-source research and host global convenings to make ideas like trustworthy AI mainstream.',
        locale_id=locale_id,
    )


def create_default_buyersguide_categories(apps, schema_editor, locale_id):
    BuyersGuideProductCategory = apps.get_model("wagtailpages", "BuyersGuideProductCategory")

    categories = [
        "Toys & Games",
        "Smart Home",
        "Entertainment",
        "Wearables",
        "Health & Exercise",
        "Pets",
        "Valentine's Day",
        "Video Call Apps",
    ]

    for cat in categories:
        category, created = BuyersGuideProductCategory.objects.get_or_create(
            name=cat,
            locale_id=locale_id,
        )
        if created:
            category.slug = slugify(cat)
            category.save()


def add_pni_subcategories(apps, schema, locale_id):
    BuyersGuideProductCategory = apps.get_model("wagtailpages", "BuyersGuideProductCategory")

    healthAndExercise = BuyersGuideProductCategory.objects.get(
        name="Health & Exercise",
        locale_id=locale_id,
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


def bootstrap_data(apps, schema_editor):
    Locale = apps.get_model("wagtailcore", "Locale")
    DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)
    locale_id = DEFAULT_LOCALE.pk

    create_default_blog_categories(apps, schema_editor, locale_id)
    create_default_focus_areas(apps, schema_editor, locale_id)
    create_default_buyersguide_categories(apps, schema_editor, locale_id)
    add_pni_subcategories(apps, schema_editor, locale_id)



class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0001_squashed_migrations_feb_2022'),
    ]

    operations = [
        migrations.RunPython(
            bootstrap_data
        ),
    ]
