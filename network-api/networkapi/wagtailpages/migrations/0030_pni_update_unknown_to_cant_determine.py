from django.db import migrations


def update_unknown_to_cantdetermine(apps, schema_editor):
    SoftwareProductPage = apps.get_model("wagtailpages", "SoftwareProductPage")
    GeneralProductPage = apps.get_model("wagtailpages", "GeneralProductPage")

    common_extended_yes_no_fields = [
        'signup_requires_email',
        'signup_requires_phone',
        'signup_requires_third_party_account',
        'user_friendly_privacy_policy',
        'uses_encryption',
        'security_updates',
        'strong_password',
        'manage_vulnerabilities',
        'privacy_policy',
    ]

    software_extended_yes_no_fields = [
        'recording_alert',
    ]

    general_extended_yes_no_fields = [
        'camera_device',
        'camera_app',
        'microphone_device',
        'microphone_app',
        'location_device',
        'location_app',
        'offline_capable',
        'uses_ai',
        'ai_uses_personal_data',
        'ai_is_transparent',
    ]

    # Update SoftwareProductPage
    for p in SoftwareProductPage.objects.all():
        for field in common_extended_yes_no_fields:
            # update 'U' (Unknown) to the new value 'CD' (Can't Determine)
            if getattr(p, field) == 'U':
                setattr(p, field, 'CD')

        for field in software_extended_yes_no_fields:
            # update 'U' (Unknown) to the new value 'CD' (Can't Determine)
            if getattr(p, field) == 'U':
                setattr(p, field, 'CD')
        p.save()

    # Update GeneralProductPage
    for p in GeneralProductPage.objects.all():
        for field in common_extended_yes_no_fields:
            # update 'U' (Unknown) to the new value 'CD' (Can't Determine)
            if getattr(p, field) == 'U':
                setattr(p, field, 'CD')

        for field in general_extended_yes_no_fields:
            # update 'U' (Unknown) to the new value 'CD' (Can't Determine)
            if getattr(p, field) == 'U':
                setattr(p, field, 'CD')
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0029_productpage_airtable_record_id'),
    ]

    operations = [
        migrations.RunPython(update_unknown_to_cantdetermine),
    ]
