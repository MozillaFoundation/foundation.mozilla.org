from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("wagtailpages", "0161_alter_homepage_ideas_headline_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HomepageNewsYouCanUse",
            new_name="HomepageHighlights",
        ),
        migrations.AddField(
            model_name="homepage",
            name="ideas_title",
            field=models.CharField(default="Ideas", max_length=50),
        ),
        migrations.AddField(
            model_name="homepage",
            name="highlights_title",
            field=models.CharField(default="The Highlights", max_length=50),
        ),
    ]
