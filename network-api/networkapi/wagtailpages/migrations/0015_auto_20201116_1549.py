# Generated by Django 2.2.16 on 2020-11-16 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0014_product_page_orderables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primarypage',
            name='intro',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350),
        ),
        migrations.AlterField(
            model_name='primarypage',
            name='intro_de',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='primarypage',
            name='intro_en',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='primarypage',
            name='intro_es',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='primarypage',
            name='intro_fr',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='primarypage',
            name='intro_fy_NL',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='primarypage',
            name='intro_nl',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='primarypage',
            name='intro_pl',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='primarypage',
            name='intro_pt',
            field=models.CharField(blank=True, help_text='Intro paragraph to show in hero cutout box', max_length=350, null=True),
        ),
    ]
