# Generated by Django 4.2.15 on 2024-09-23 19:42

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
from django.db import migrations, models

import foundation_cms.legacy_cms.wagtailpages.validators


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailpages", "0163_remove_focusarea_page"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="hero_intro_body",
            field=models.TextField(
                blank=True,
                default="Mozilla empowers consumers to demand better online privacy, trustworthy AI, and safe online experiences from Big Tech and governments. We work across borders, disciplines, and technologies to uphold principles like privacy, inclusion and decentralization online.",
                max_length=300,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_intro_heading",
            field=models.CharField(
                blank=True,
                default="A healthy internet is one in which privacy, openness, and inclusion are the norms.",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_intro_link",
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
                                        help_text='A path relative to this domain. For example, "/foo/bar" or "?foo=bar".',
                                        label="Relative URL",
                                        max_length=300,
                                        required=False,
                                        validators=[foundation_cms.legacy_cms.wagtailpages.validators.RelativeURLValidator()],
                                    ),
                                ),
                                (
                                    "anchor",
                                    wagtail.blocks.CharBlock(
                                        help_text='An id attribute of an element on the current page. For example, "#section-1"',
                                        label="#",
                                        max_length=300,
                                        required=False,
                                        validators=[foundation_cms.legacy_cms.wagtailpages.validators.AnchorLinkValidator()],
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
