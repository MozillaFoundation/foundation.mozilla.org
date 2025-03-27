# Generated by Django 4.2.20 on 2025-03-26 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
        ("nav", "0008_alter_navmenu_locale_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="navmenufeaturedblogtopicrelationship",
            name="icon",
            field=models.ForeignKey(
                help_text="Please use SVG format",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Icon",
            ),
        ),
    ]
