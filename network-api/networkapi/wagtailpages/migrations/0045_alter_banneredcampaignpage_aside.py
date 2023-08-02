# Generated by Django 3.2.13 on 2022-10-05 09:31

import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailpages", "0044_banneredcampaignpage_aside"),
    ]

    operations = [
        migrations.AlterField(
            model_name="banneredcampaignpage",
            name="aside",
            field=wagtail.fields.StreamField(
                [
                    (
                        "aside",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Heading for the card.",
                                        required=False,
                                    ),
                                ),
                                (
                                    "body",
                                    wagtail.blocks.TextBlock(
                                        help_text="Body text of the card.",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "linkbutton",
                        wagtail.blocks.StructBlock(
                            [
                                ("label", wagtail.blocks.CharBlock()),
                                ("URL", wagtail.blocks.CharBlock()),
                                (
                                    "styling",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("btn-primary", "Primary button"),
                                            ("btn-secondary", "Secondary button"),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "spacer",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "size",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("1", "quarter spacing"),
                                            ("2", "half spacing"),
                                            ("3", "single spacing"),
                                            ("4", "one and a half spacing"),
                                            ("5", "triple spacing"),
                                        ]
                                    ),
                                )
                            ]
                        ),
                    ),
                ],
                blank=True,
            ),
        ),
    ]
