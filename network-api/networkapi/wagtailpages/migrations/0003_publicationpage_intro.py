# Generated by Django 2.2.17 on 2021-03-31 16:54

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0002_remove_productpage_cloudinary_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationpage',
            name='intro_notes',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
