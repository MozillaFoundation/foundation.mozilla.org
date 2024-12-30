# Generated by Django 4.2.16 on 2024-12-30 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
        ("donate", "0025_alter_donatehelppage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="helppagenotice",
            name="locale",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="wagtailcore.locale",
                verbose_name="locale",
            ),
        ),
    ]
