# Generated by Django 2.2.11 on 2020-04-15 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0040_auto_20200415_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='softwareproduct',
            name='signup_with_contact_info',
        ),
        migrations.RemoveField(
            model_name='softwareproduct',
            name='signup_with_contact_info_helptext',
        ),
        migrations.AddField(
            model_name='softwareproduct',
            name='signup_methods_helptext',
            field=models.TextField(blank=True, help_text='Describe the kind of contact information requirements for signing up for this product', max_length=5000),
        ),
        migrations.AddField(
            model_name='softwareproduct',
            name='signup_with_email',
            field=models.BooleanField(help_text='Email required to sign up?', null=True),
        ),
        migrations.AddField(
            model_name='softwareproduct',
            name='signup_with_phone',
            field=models.BooleanField(help_text='Phone number required to sign up?', null=True),
        ),
        migrations.AddField(
            model_name='softwareproduct',
            name='signup_with_third_party',
            field=models.BooleanField(help_text='Third Party account required to sign up?', null=True),
        ),
    ]
