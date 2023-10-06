# Generated by Django 3.2.21 on 2023-10-06 19:23

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0004_remove_donatehelppage_show_notice_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='donatehelppage',
            name='notice',
            field=wagtail.fields.StreamField([('notice', wagtail.blocks.StructBlock([('notice_image', wagtail.images.blocks.ImageChooserBlock()), ('notice_image_altText', wagtail.blocks.CharBlock(help_text='Image description (for screen readers).', required=True)), ('notice_text', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link']))]))], blank=True, help_text='Optional notice that will render at the top of the page.', use_json_field=True),
        ),
    ]
