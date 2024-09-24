import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0165_alter_articlepage_body_alter_blogpage_body_and_more"),
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
        migrations.AlterField(
            model_name="homepagehighlights",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="highlights", to="wagtailpages.homepage"
            ),
        ),
    ]
