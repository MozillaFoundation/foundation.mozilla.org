
from django.db import migrations

def map_yes_no_to_cant_determine(apps, schema_editor):
    GeneralProductPage = apps.get_model('wagtailpages', 'GeneralProductPage')

    # Filter all instances where 'ai_is_untrustworthy' is 'Yes' or 'No'
    pages_to_update = GeneralProductPage.objects.filter(ai_is_untrustworthy__in=['Yes', 'No'])
    
    # Iterate over the pages and update them
    for page in pages_to_update:
        print(f"Product '{page.title}' with ID {page.id} has 'ai_is_untrustworthy' set as '{page.ai_is_untrustworthy}'. Updating to 'CD'.")
        page.ai_is_untrustworthy = 'CD'
        page.save()


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0166_homepagehighlights_replace_homepagenewsyoucanuse"),
    ]

    operations = [
        migrations.RunPython(map_yes_no_to_cant_determine),
    ]

