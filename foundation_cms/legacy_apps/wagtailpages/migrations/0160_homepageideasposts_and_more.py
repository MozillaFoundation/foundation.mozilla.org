import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailpages", "0159_update_bgcta_with_linkblock"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HomepageSpotlightPosts",
            new_name="HomepageIdeasPosts",
        ),
        migrations.RenameField(
            model_name="homepage",
            old_name="spotlight_headline",
            new_name="ideas_headline",
        ),
        migrations.RenameField(
            model_name="homepage",
            old_name="spotlight_image",
            new_name="ideas_image",
        ),
        migrations.AddField(
            model_name="homepageideasposts",
            name="cta",
            field=models.CharField(default="Read more", max_length=50),
        ),
        migrations.AlterField(
            model_name="homepageideasposts",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="ideas_posts", to="wagtailpages.homepage"
            ),
        ),
    ]
