# Generated by Django 3.2.18 on 2023-05-31 18:44

import django.db.models.deletion
import wagtail.contrib.routable_page.models
import wagtail.fields
import wagtailmetadata.models
from django.db import migrations, models

import foundation_cms.legacy_cms.wagtailpages.pagemodels.mixin.foundation_navigation


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
        ("wagtailimages", "0024_index_image_file_hash"),
        ("wagtailpages", "0085_set_base_taxonomy_slug_as_non_nullable"),
    ]

    operations = [
        migrations.CreateModel(
            name="RCCLibraryPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "results_count",
                    models.PositiveSmallIntegerField(
                        default=10, help_text="Maximum number of results to be displayed per page."
                    ),
                ),
                (
                    "banner_image",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="wagtailimages.image"
                    ),
                ),
                (
                    "search_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Search image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                foundation_cms.legacy_cms.wagtailpages.pagemodels.mixin.foundation_navigation.FoundationNavigationPageMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="RCCLandingPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("intro", models.CharField(blank=True, max_length=250)),
                (
                    "banner_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image that will render at the top of the page.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "search_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Search image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                foundation_cms.legacy_cms.wagtailpages.pagemodels.mixin.foundation_navigation.FoundationNavigationPageMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="RCCDetailPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "original_publication_date",
                    models.DateField(
                        blank=True, help_text="When was the article (not this page) originally published?", null=True
                    ),
                ),
                (
                    "introduction",
                    models.CharField(
                        blank=True,
                        help_text="Provide a short blurb about the article that will be displayed on listing pages and search results.",
                        max_length=300,
                    ),
                ),
                (
                    "overview",
                    wagtail.fields.RichTextField(
                        blank=True,
                        help_text="Provide an overview about the article. This can be an excerpt from or the executive summary of the original paper.",
                    ),
                ),
                (
                    "collaborators",
                    models.TextField(
                        blank=True, help_text="List all contributors that are not the project leading authors."
                    ),
                ),
                (
                    "cover_image",
                    models.ForeignKey(
                        help_text="Select a cover image for this article. The cover image is displayed on the detail page and all article listings.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "search_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Search image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                foundation_cms.legacy_cms.wagtailpages.pagemodels.mixin.foundation_navigation.FoundationNavigationPageMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="RCCAuthorsIndexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "banner_image",
                    models.ForeignKey(
                        help_text="The image to be used as the banner background image for the author index and all author detail pages.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "search_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Search image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                wagtailmetadata.models.WagtailImageMetadataMixin,
                foundation_cms.legacy_cms.wagtailpages.pagemodels.mixin.foundation_navigation.FoundationNavigationPageMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
    ]
