from django.db import migrations
from django.utils.text import slugify


def set_default_slug(apps, schema_editor):
    ResearchRegion = apps.get_model("wagtailpages", "ResearchRegion")
    ResearchTopic = apps.get_model("wagtailpages", "ResearchTopic")

    for region in ResearchRegion.objects.all():
        slug = slugify(region.name)
        unique_slug = slug
        counter = 1

        while ResearchRegion.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1

        region.slug = unique_slug
        region.save()

    for topic in ResearchTopic.objects.all():
        slug = slugify(topic.name)
        unique_slug = slug
        counter = 1

        while ResearchTopic.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1

        topic.slug = unique_slug
        topic.save()


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        ("wagtailpages", "0083_add_slug_to_base_taxonomy"),
    ]

    operations = [
        migrations.RunPython(set_default_slug, reverse_code=migrations.RunPython.noop),
    ]
