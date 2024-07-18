# Generated by Django 4.2.14 on 2024-07-18 06:16

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
from django.db import migrations

import networkapi.wagtailpages.validators


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0148_update_imagegridblock_with_linkblock"),
    ]

    operations = [
        migrations.AddField(
            model_name="dearinternetpage",
            name="cta_button",
            field=wagtail.fields.StreamField(
                [
                    (
                        "link",
                        wagtail.blocks.StructBlock(
                            [
                                ("label", wagtail.blocks.CharBlock()),
                                (
                                    "link_to",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("page", "Page"),
                                            ("external_url", "External URL"),
                                            ("relative_url", "Relative URL"),
                                            ("email", "Email"),
                                            ("anchor", "Anchor"),
                                            ("file", "File"),
                                            ("phone", "Phone"),
                                        ],
                                        label="Link to",
                                    ),
                                ),
                                ("page", wagtail.blocks.PageChooserBlock(label="Page", required=False)),
                                (
                                    "external_url",
                                    wagtail.blocks.URLBlock(
                                        help_text="Enter a full URL including http:// or https://",
                                        label="External URL",
                                        max_length=300,
                                        required=False,
                                    ),
                                ),
                                (
                                    "relative_url",
                                    wagtail.blocks.CharBlock(
                                        help_text='A path relative to this domain. For example, "/foo/bar"',
                                        label="Relative URL",
                                        max_length=300,
                                        required=False,
                                        validators=[networkapi.wagtailpages.validators.RelativeURLValidator()],
                                    ),
                                ),
                                (
                                    "anchor",
                                    wagtail.blocks.CharBlock(
                                        help_text='An id attribute of an element on the current page. For example, "#section-1"',
                                        label="#",
                                        max_length=300,
                                        required=False,
                                        validators=[networkapi.wagtailpages.validators.AnchorLinkValidator()],
                                    ),
                                ),
                                ("email", wagtail.blocks.EmailBlock(required=False)),
                                ("file", wagtail.documents.blocks.DocumentChooserBlock(label="File", required=False)),
                                ("phone", wagtail.blocks.CharBlock(label="Phone", max_length=30, required=False)),
                                (
                                    "new_window",
                                    wagtail.blocks.BooleanBlock(label="Open in new window", required=False),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]
