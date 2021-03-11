# Generated by Django 2.2.17 on 2021-03-03 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0044_buyersguideproductcategory'),
    ]

    operations = [
        # Remove BuyersGuideProductCategory.category
        migrations.RemoveField(
            model_name='productpagecategory',
            name='category',
        ),
        # Rename BuyersGuideProductCategory.category_new = BuyersGuideProductCategory.category
        migrations.RenameField(
            model_name='productpagecategory',
            old_name='category_new',
            new_name='category',
        ),
    ]
