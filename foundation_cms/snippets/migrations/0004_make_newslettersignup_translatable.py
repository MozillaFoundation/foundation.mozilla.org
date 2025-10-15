# snippets/migrations/00xx_newslettersignup_make_translatable.py
import uuid

import django.db.models.deletion
from django.db import migrations, models
from wagtail.models import Locale


def backfill_newslettersignup_locale_and_key(apps, schema_editor):
    NewsletterSignup = apps.get_model("snippets", "NewsletterSignup")

    default_locale = Locale.get_default()

    # Assign a new unique translation key to every existing newsletter signup, and set the Locale to the default locale. (English)
    # This avoids the error "DETAIL: Key (translation_key, locale_id)=(<UUID>, 1) is duplicated.",
    # that occurs if we try to set this through django's migrations helper.
    for obj in NewsletterSignup.objects.all().only("id", "translation_key", "locale_id").iterator():
        changed_fields = []
        obj.translation_key = uuid.uuid4()
        changed_fields.append("translation_key")

        if obj.locale_id is None:
            obj.locale = default_locale
            changed_fields.append("locale")

        if changed_fields:
            obj.save(update_fields=changed_fields)


class Migration(migrations.Migration):

    dependencies = [
        ("snippets", "0003_newsletter_add_cta_description_and_rename_cta_text"),
    ]

    operations = [
        # 1) Add translation fields fields as NULLABLE first
        migrations.AddField(
            model_name="newslettersignup",
            name="translation_key",
            field=models.UUIDField(editable=False, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="newslettersignup",
            name="locale",
            field=models.ForeignKey(
                to="wagtailcore.locale",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                null=True,
            ),
        ),
        # 2) Backfill existing newslettersignups with unique translation keys + default locale
        migrations.RunPython(backfill_newslettersignup_locale_and_key, migrations.RunPython.noop),
        # 3) Enforce translation fields as NOT NULL
        migrations.AlterField(
            model_name="newslettersignup",
            name="translation_key",
            field=models.UUIDField(editable=False, db_index=True, null=False),
        ),
        migrations.AlterField(
            model_name="newslettersignup",
            name="locale",
            field=models.ForeignKey(
                to="wagtailcore.locale",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                null=False,
            ),
        ),
        # 4) Add the uniqueness constraint required by TranslatableMixin
        migrations.AlterUniqueTogether(
            name="newslettersignup",
            unique_together={("translation_key", "locale")},
        ),
    ]
