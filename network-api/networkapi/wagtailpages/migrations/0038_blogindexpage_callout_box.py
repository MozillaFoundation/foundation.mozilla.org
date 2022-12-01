# Generated by Django 3.2.13 on 2022-07-19 18:53

import wagtail.core.blocks
import wagtail.core.fields
import wagtail.snippets.blocks
import wagtailmedia.blocks
from django.db import migrations

import networkapi.wagtailpages.pagemodels.blog.blog_topic


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0037_auto_20220706_1136"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogindexpage",
            name="callout_box",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "callout_box",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.core.blocks.CharBlock(help_text="Heading for the callout box."),
                                ),
                                (
                                    "related_topics",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.snippets.blocks.SnippetChooserBlock(
                                            networkapi.wagtailpages.pagemodels.blog.blog_topic.BlogPageTopic
                                        ),
                                        help_text="Optional topics to display at the top of the callout box.",
                                        max_num=2,
                                    ),
                                ),
                                (
                                    "show_icon",
                                    wagtail.core.blocks.BooleanBlock(
                                        help_text="Check this if you would like to render the headphone icon.",
                                        required=False,
                                    ),
                                ),
                                (
                                    "body",
                                    wagtail.core.blocks.RichTextBlock(
                                        features=["bold", "italic", "link"],
                                        help_text="Body text for the callout box.",
                                        required=False,
                                    ),
                                ),
                                (
                                    "audio",
                                    wagtailmedia.blocks.AudioChooserBlock(
                                        help_text="Optional audio player that will appear after the body.",
                                        required=False,
                                    ),
                                ),
                                (
                                    "link_button_text",
                                    wagtail.core.blocks.CharBlock(
                                        help_text="Label text for the link button at the bottom of the box.",
                                        required=False,
                                    ),
                                ),
                                (
                                    "link_button_url",
                                    wagtail.core.blocks.CharBlock(
                                        help_text="URL that the button should link out to.",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                help_text="Callout box that appears after the featured posts section",
            ),
        ),
    ]
