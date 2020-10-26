# Generated by Django 2.2.16 on 2020-10-26 20:15

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import networkapi.buyersguide.fields
import wagtailmetadata.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0052_pagelogentry'),
        ('wagtailpages', '0012_add_article_page_hero_remove_summary_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('privacy_ding', models.BooleanField(default=False, help_text='Tick this box if privacy is not included for this product')),
                ('adult_content', models.BooleanField(default=False, help_text='When checked, product thumbnail will appear blurred as well as have an 18+ badge on it')),
                ('uses_wifi', models.BooleanField(default=False, help_text='Does this product rely on WiFi connectivity?')),
                ('uses_bluetooth', models.BooleanField(default=False, help_text='Does this product rely on Bluetooth connectivity?')),
                ('review_date', models.DateField(help_text='Review date of this product')),
                ('company', models.CharField(blank=True, help_text='Name of Company', max_length=100)),
                ('company_en', models.CharField(blank=True, help_text='Name of Company', max_length=100, null=True)),
                ('company_de', models.CharField(blank=True, help_text='Name of Company', max_length=100, null=True)),
                ('company_pt', models.CharField(blank=True, help_text='Name of Company', max_length=100, null=True)),
                ('company_es', models.CharField(blank=True, help_text='Name of Company', max_length=100, null=True)),
                ('company_fr', models.CharField(blank=True, help_text='Name of Company', max_length=100, null=True)),
                ('company_fy_NL', models.CharField(blank=True, help_text='Name of Company', max_length=100, null=True)),
                ('company_nl', models.CharField(blank=True, help_text='Name of Company', max_length=100, null=True)),
                ('company_pl', models.CharField(blank=True, help_text='Name of Company', max_length=100, null=True)),
                ('blurb', models.TextField(blank=True, help_text='Description of the product', max_length=5000)),
                ('blurb_en', models.TextField(blank=True, help_text='Description of the product', max_length=5000, null=True)),
                ('blurb_de', models.TextField(blank=True, help_text='Description of the product', max_length=5000, null=True)),
                ('blurb_pt', models.TextField(blank=True, help_text='Description of the product', max_length=5000, null=True)),
                ('blurb_es', models.TextField(blank=True, help_text='Description of the product', max_length=5000, null=True)),
                ('blurb_fr', models.TextField(blank=True, help_text='Description of the product', max_length=5000, null=True)),
                ('blurb_fy_NL', models.TextField(blank=True, help_text='Description of the product', max_length=5000, null=True)),
                ('blurb_nl', models.TextField(blank=True, help_text='Description of the product', max_length=5000, null=True)),
                ('blurb_pl', models.TextField(blank=True, help_text='Description of the product', max_length=5000, null=True)),
                ('url', models.URLField(blank=True, help_text='Link to this product page', max_length=2048)),
                ('price', models.CharField(blank=True, help_text='Price', max_length=100)),
                ('price_en', models.CharField(blank=True, help_text='Price', max_length=100, null=True)),
                ('price_de', models.CharField(blank=True, help_text='Price', max_length=100, null=True)),
                ('price_pt', models.CharField(blank=True, help_text='Price', max_length=100, null=True)),
                ('price_es', models.CharField(blank=True, help_text='Price', max_length=100, null=True)),
                ('price_fr', models.CharField(blank=True, help_text='Price', max_length=100, null=True)),
                ('price_fy_NL', models.CharField(blank=True, help_text='Price', max_length=100, null=True)),
                ('price_nl', models.CharField(blank=True, help_text='Price', max_length=100, null=True)),
                ('price_pl', models.CharField(blank=True, help_text='Price', max_length=100, null=True)),
                ('cloudinary_image', cloudinary.models.CloudinaryField(blank=True, help_text='Image representing this product - hosted on Cloudinary', max_length=255, verbose_name='image')),
                ('worst_case', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000)),
                ('worst_case_en', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000, null=True)),
                ('worst_case_de', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000, null=True)),
                ('worst_case_pt', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000, null=True)),
                ('worst_case_es', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000, null=True)),
                ('worst_case_fr', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000, null=True)),
                ('worst_case_fy_NL', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000, null=True)),
                ('worst_case_nl', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000, null=True)),
                ('worst_case_pl', models.CharField(blank=True, help_text="What's the worst thing that could happen by using this product?", max_length=5000, null=True)),
                ('signup_requires_email', networkapi.buyersguide.fields.ExtendedYesNoField(help_text='Does this product requires providing an email address in order to sign up?')),
                ('signup_requires_phone', networkapi.buyersguide.fields.ExtendedYesNoField(help_text='Does this product requires providing a phone number in order to sign up?')),
                ('signup_requires_third_party_account', networkapi.buyersguide.fields.ExtendedYesNoField(help_text='Does this product require a third party account in order to sign up?')),
                ('signup_requirement_explanation', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000)),
                ('signup_requirement_explanation_en', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000, null=True)),
                ('signup_requirement_explanation_de', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000, null=True)),
                ('signup_requirement_explanation_pt', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000, null=True)),
                ('signup_requirement_explanation_es', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000, null=True)),
                ('signup_requirement_explanation_fr', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000, null=True)),
                ('signup_requirement_explanation_fy_NL', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000, null=True)),
                ('signup_requirement_explanation_nl', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000, null=True)),
                ('signup_requirement_explanation_pl', models.TextField(blank=True, help_text='Describe the particulars around sign-up requirements here.', max_length=5000, null=True)),
                ('how_does_it_use_data_collected', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000)),
                ('how_does_it_use_data_collected_en', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000, null=True)),
                ('how_does_it_use_data_collected_de', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000, null=True)),
                ('how_does_it_use_data_collected_pt', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000, null=True)),
                ('how_does_it_use_data_collected_es', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000, null=True)),
                ('how_does_it_use_data_collected_fr', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000, null=True)),
                ('how_does_it_use_data_collected_fy_NL', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000, null=True)),
                ('how_does_it_use_data_collected_nl', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000, null=True)),
                ('how_does_it_use_data_collected_pl', models.TextField(blank=True, help_text='How does this product use the data collected?', max_length=5000, null=True)),
                ('data_collection_policy_is_bad', models.BooleanField(default=False, verbose_name='Privacy ding')),
                ('user_friendly_privacy_policy', networkapi.buyersguide.fields.ExtendedYesNoField(help_text='Does this product have a user-friendly privacy policy?')),
                ('show_ding_for_minimum_security_standards', models.BooleanField(default=False, verbose_name='Privacy ding')),
                ('meets_minimum_security_standards', models.BooleanField(help_text='Does this product meet our minimum security standards?', null=True)),
                ('uses_encryption', networkapi.buyersguide.fields.ExtendedYesNoField(help_text='Does the product use encryption?')),
                ('uses_encryption_helptext', models.TextField(blank=True, max_length=5000)),
                ('security_updates', networkapi.buyersguide.fields.ExtendedYesNoField(help_text='Security updates?')),
                ('security_updates_helptext', models.TextField(blank=True, max_length=5000)),
                ('security_updates_helptext_en', models.TextField(blank=True, max_length=5000, null=True)),
                ('security_updates_helptext_de', models.TextField(blank=True, max_length=5000, null=True)),
                ('security_updates_helptext_pt', models.TextField(blank=True, max_length=5000, null=True)),
                ('security_updates_helptext_es', models.TextField(blank=True, max_length=5000, null=True)),
                ('security_updates_helptext_fr', models.TextField(blank=True, max_length=5000, null=True)),
                ('security_updates_helptext_fy_NL', models.TextField(blank=True, max_length=5000, null=True)),
                ('security_updates_helptext_nl', models.TextField(blank=True, max_length=5000, null=True)),
                ('security_updates_helptext_pl', models.TextField(blank=True, max_length=5000, null=True)),
                ('strong_password', networkapi.buyersguide.fields.ExtendedYesNoField()),
                ('strong_password_helptext', models.TextField(blank=True, max_length=5000)),
                ('strong_password_helptext_en', models.TextField(blank=True, max_length=5000, null=True)),
                ('strong_password_helptext_de', models.TextField(blank=True, max_length=5000, null=True)),
                ('strong_password_helptext_pt', models.TextField(blank=True, max_length=5000, null=True)),
                ('strong_password_helptext_es', models.TextField(blank=True, max_length=5000, null=True)),
                ('strong_password_helptext_fr', models.TextField(blank=True, max_length=5000, null=True)),
                ('strong_password_helptext_fy_NL', models.TextField(blank=True, max_length=5000, null=True)),
                ('strong_password_helptext_nl', models.TextField(blank=True, max_length=5000, null=True)),
                ('strong_password_helptext_pl', models.TextField(blank=True, max_length=5000, null=True)),
                ('manage_vulnerabilities', networkapi.buyersguide.fields.ExtendedYesNoField(help_text='Manages security vulnerabilities?')),
                ('manage_vulnerabilities_helptext', models.TextField(blank=True, max_length=5000)),
                ('manage_vulnerabilities_helptext_en', models.TextField(blank=True, max_length=5000, null=True)),
                ('manage_vulnerabilities_helptext_de', models.TextField(blank=True, max_length=5000, null=True)),
                ('manage_vulnerabilities_helptext_pt', models.TextField(blank=True, max_length=5000, null=True)),
                ('manage_vulnerabilities_helptext_es', models.TextField(blank=True, max_length=5000, null=True)),
                ('manage_vulnerabilities_helptext_fr', models.TextField(blank=True, max_length=5000, null=True)),
                ('manage_vulnerabilities_helptext_fy_NL', models.TextField(blank=True, max_length=5000, null=True)),
                ('manage_vulnerabilities_helptext_nl', models.TextField(blank=True, max_length=5000, null=True)),
                ('manage_vulnerabilities_helptext_pl', models.TextField(blank=True, max_length=5000, null=True)),
                ('privacy_policy', networkapi.buyersguide.fields.ExtendedYesNoField(help_text='Does this product have a privacy policy?')),
                ('privacy_policy_helptext', models.TextField(blank=True, max_length=5000)),
                ('privacy_policy_helptext_en', models.TextField(blank=True, max_length=5000, null=True)),
                ('privacy_policy_helptext_de', models.TextField(blank=True, max_length=5000, null=True)),
                ('privacy_policy_helptext_pt', models.TextField(blank=True, max_length=5000, null=True)),
                ('privacy_policy_helptext_es', models.TextField(blank=True, max_length=5000, null=True)),
                ('privacy_policy_helptext_fr', models.TextField(blank=True, max_length=5000, null=True)),
                ('privacy_policy_helptext_fy_NL', models.TextField(blank=True, max_length=5000, null=True)),
                ('privacy_policy_helptext_nl', models.TextField(blank=True, max_length=5000, null=True)),
                ('privacy_policy_helptext_pl', models.TextField(blank=True, max_length=5000, null=True)),
                ('phone_number', models.CharField(blank=True, help_text='Phone Number', max_length=100)),
                ('phone_number_en', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('phone_number_de', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('phone_number_pt', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('phone_number_es', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('phone_number_fr', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('phone_number_fy_NL', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('phone_number_nl', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('phone_number_pl', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('live_chat', models.CharField(blank=True, help_text='Live Chat', max_length=100)),
                ('live_chat_en', models.CharField(blank=True, help_text='Live Chat', max_length=100, null=True)),
                ('live_chat_de', models.CharField(blank=True, help_text='Live Chat', max_length=100, null=True)),
                ('live_chat_pt', models.CharField(blank=True, help_text='Live Chat', max_length=100, null=True)),
                ('live_chat_es', models.CharField(blank=True, help_text='Live Chat', max_length=100, null=True)),
                ('live_chat_fr', models.CharField(blank=True, help_text='Live Chat', max_length=100, null=True)),
                ('live_chat_fy_NL', models.CharField(blank=True, help_text='Live Chat', max_length=100, null=True)),
                ('live_chat_nl', models.CharField(blank=True, help_text='Live Chat', max_length=100, null=True)),
                ('live_chat_pl', models.CharField(blank=True, help_text='Live Chat', max_length=100, null=True)),
                ('email', models.CharField(blank=True, help_text='Email', max_length=100)),
                ('email_en', models.CharField(blank=True, help_text='Email', max_length=100, null=True)),
                ('email_de', models.CharField(blank=True, help_text='Email', max_length=100, null=True)),
                ('email_pt', models.CharField(blank=True, help_text='Email', max_length=100, null=True)),
                ('email_es', models.CharField(blank=True, help_text='Email', max_length=100, null=True)),
                ('email_fr', models.CharField(blank=True, help_text='Email', max_length=100, null=True)),
                ('email_fy_NL', models.CharField(blank=True, help_text='Email', max_length=100, null=True)),
                ('email_nl', models.CharField(blank=True, help_text='Email', max_length=100, null=True)),
                ('email_pl', models.CharField(blank=True, help_text='Email', max_length=100, null=True)),
                ('twitter', models.CharField(blank=True, help_text='Twitter username', max_length=100)),
                ('image', models.ForeignKey(blank=True, help_text='Image representing this product', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Search image')),
            ],
            options={
                'verbose_name': 'Product Page',
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='GeneralProductPage',
            fields=[
                ('productpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailpages.ProductPage')),
            ],
            options={
                'verbose_name': 'General Product Page',
            },
            bases=('wagtailpages.productpage',),
        ),
        migrations.CreateModel(
            name='SoftwareProductPage',
            fields=[
                ('productpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailpages.ProductPage')),
            ],
            options={
                'verbose_name': 'Software Product Page',
            },
            bases=('wagtailpages.productpage',),
        ),
    ]
