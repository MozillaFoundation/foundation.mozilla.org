# Generated by Django 4.2.15 on 2024-09-11 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("wagtailpages", "0161_alter_homepage_ideas_headline_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="focusarea",
            name="page",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="cause_statement",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="cause_statement_link_page",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="cause_statement_link_text",
        ),
        migrations.RemoveField(
            model_name="homepage",
            name="show_cause_statement",
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_bottom_body",
            field=models.TextField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_bottom_heading",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_bottom_link_page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="hero_bottom_link",
                to="wagtailcore.page",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_bottom_link_text",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
