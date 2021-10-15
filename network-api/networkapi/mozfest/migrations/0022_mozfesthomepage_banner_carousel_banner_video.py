# Generated by Django 3.1.11 on 2021-10-15 11:12

from django.db import migrations
import networkapi.wagtailpages.pagemodels.customblocks.video_block
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('mozfest', '0021_add_spaces_cards'),
    ]

    operations = [
        migrations.AddField(
            model_name='mozfesthomepage',
            name='banner_carousel',
            field=wagtail.core.fields.StreamField([('slide', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('heading', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.CharBlock(required=False))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mozfesthomepage',
            name='banner_video',
            field=wagtail.core.fields.StreamField([('CMS_video', networkapi.wagtailpages.pagemodels.customblocks.video_block.WagtailVideoChooserBlock()), ('external_video', wagtail.core.blocks.StructBlock([('video_url', wagtail.core.blocks.URLBlock(help_text='For YouTube: go to your YouTube video and click “Share,” then “Embed,” and then copy and paste the provided URL only. For example: https://www.youtube.com/embed/3FIVXBawyQw For Vimeo: follow similar steps to grab the embed URL. For example: https://player.vimeo.com/video/9004979')), ('thumbnail', wagtail.images.blocks.ImageChooserBlock(help_text='The image to show before the video is played.'))]))], blank=True, help_text='The video to play when users click "watch video"', null=True),
        ),
    ]
