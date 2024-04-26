# Generated by Django 4.2.11 on 2024-04-26 09:39

import wagtail.blocks
import wagtail.fields
from django.db import migrations

import networkapi.nav.blocks
import networkapi.wagtailpages.validators


class Migration(migrations.Migration):

    dependencies = [
        ("nav", "0005_alter_navmenu_dropdowns"),
    ]

    operations = [
        migrations.AlterField(
            model_name="navmenu",
            name="dropdowns",
            field=wagtail.fields.StreamField(
                [
                    (
                        "dropdown",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="How the dropdown menu will be labelled in the nav bar",
                                        max_length=100,
                                    ),
                                ),
                                (
                                    "overview",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                ("title", wagtail.blocks.CharBlock(max_length=100)),
                                                (
                                                    "description",
                                                    wagtail.blocks.RichTextBlock(
                                                        features=["bold", "italic"], max_length=200
                                                    ),
                                                ),
                                            ],
                                            label="Overview",
                                        ),
                                        default=[],
                                        help_text="If added, the overview will take the place of the first column",
                                        label="Overview",
                                        max_num=1,
                                        min_num=0,
                                    ),
                                ),
                                (
                                    "button",
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
                                                    validators=[
                                                        networkapi.wagtailpages.validators.RelativeURLValidator()
                                                    ],
                                                ),
                                            ),
                                        ],
                                        help_text="Use it to add a CTA to link to the contents of the dropdown menu. If an overview is added, the button will be placed at the overview's column.",
                                        label="Dropdown Button",
                                        required=True,
                                    ),
                                ),
                                (
                                    "columns",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                ("title", wagtail.blocks.CharBlock(max_length=100)),
                                                (
                                                    "nav_items",
                                                    wagtail.blocks.ListBlock(
                                                        networkapi.nav.blocks.NavItem,
                                                        default=[],
                                                        label="Items",
                                                        max_num=4,
                                                        min_num=1,
                                                    ),
                                                ),
                                                (
                                                    "button",
                                                    wagtail.blocks.ListBlock(
                                                        networkapi.nav.blocks.NavButton,
                                                        default=[],
                                                        help_text="Adds a CTA button to the bottom of the nav column.",
                                                        label="Column Button",
                                                        max_num=1,
                                                        min_num=0,
                                                        required=False,
                                                    ),
                                                ),
                                            ],
                                            label="Column",
                                        ),
                                        help_text="Add up to 4 columns of navigation links",
                                        label="Columns",
                                        max_num=4,
                                        min_num=1,
                                    ),
                                ),
                                (
                                    "featured_column",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                ("title", wagtail.blocks.CharBlock(max_length=100)),
                                                (
                                                    "nav_items",
                                                    wagtail.blocks.ListBlock(
                                                        networkapi.nav.blocks.NavFeaturedItem,
                                                        default=[],
                                                        label="Items",
                                                        max_num=4,
                                                        min_num=1,
                                                    ),
                                                ),
                                            ],
                                            label="Featured Column",
                                        ),
                                        default=[],
                                        help_text="A column made of items and icons. If added, it will take the place of the last column",
                                        label="Featured Column",
                                        max_num=1,
                                        min_num=0,
                                    ),
                                ),
                            ],
                            label="Dropdown",
                        ),
                    )
                ],
                help_text="Add up to 5 dropdown menus",
                use_json_field=True,
            ),
        ),
    ]
