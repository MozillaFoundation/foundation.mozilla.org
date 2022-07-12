# Generated by Django 3.2.13 on 2022-07-12 22:17

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtailmedia.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0037_auto_20220706_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogindexpage',
            name='callout_box',
            field=wagtail.core.fields.StreamField([('callout', wagtail.core.blocks.StructBlock([('topics', wagtail.core.blocks.MultipleChoiceBlock(choices=[('All', 'All'), ('Advocacy', 'Advocacy'), ('Common Voice', 'Common Voice'), ('Fellowships & Awards', 'Fellowships & Awards'), ('Insights', 'Insights'), ('Moz News Beat', 'Moz News Beat'), ('Mozilla Explains', 'Mozilla Explains'), ('Mozilla Festival', 'Mozilla Festival'), ('Open Leadership & Events', 'Open Leadership & Events')], help_text='', label='Related Topics', max_num=2)), ('show_icon', wagtail.core.blocks.BooleanBlock(help_text='Check this if you would like to render the headphone icon.', required=False)), ('title', wagtail.core.blocks.CharBlock(help_text='Heading for the Callout block')), ('body', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link'], label='Body text for the callout block')), ('audio', wagtailmedia.blocks.AudioChooserBlock()), ('cta_button_text', wagtail.core.blocks.CharBlock(help_text='Label text for the cta button')), ('cta_button_url', wagtail.core.blocks.CharBlock())]))], blank=True),
        ),
    ]
