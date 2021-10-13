# Generated by Django 3.1.11 on 2021-10-12 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('wagtailpages', '0042_productpage_tips_to_protect_yourself'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyersguideproductcategory',
            name='og_image',
        ),
        migrations.AddField(
            model_name='buyersguideproductcategory',
            name='share_image',
            field=models.ForeignKey(blank=True, help_text='Optional image that will apear when category page is shared.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image', verbose_name='Share Image'),
        ),
    ]
