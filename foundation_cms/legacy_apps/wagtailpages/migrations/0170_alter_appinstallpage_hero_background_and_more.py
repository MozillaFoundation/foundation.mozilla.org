# Generated by Django 4.2.20 on 2025-05-07 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
        ("wagtailpages", "0169_alter_blogpage_body_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appinstallpage",
            name="hero_background",
            field=models.ForeignKey(
                help_text="Background image for the hero section",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="articlepage",
            name="hero_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Publication Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="articlepage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="articlepage",
            name="toc_thumbnail_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Thumbnail image to show on table of content. Use square image of 320×320 pixels or larger.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Table of Content Thumbnail",
            ),
        ),
        migrations.AlterField(
            model_name="blogpage",
            name="hero_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image for the blog page hero section.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="hero_banner_image",
                to="images.foundationcustomimage",
                verbose_name="Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="blogpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="blogpagetopic",
            name="share_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Optional image that will apear when topic page is shared.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
                verbose_name="Share Image",
            ),
        ),
        migrations.AlterField(
            model_name="buyersguidearticlepage",
            name="hero_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image for the hero section of the page.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="buyersguidearticlepage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="buyersguidecalltoaction",
            name="sticker_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Optional image on CTA.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
                verbose_name="Sticker Image",
            ),
        ),
        migrations.AlterField(
            model_name="buyersguidecampaignpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="buyersguideeditorialcontentindexpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="buyersguidepage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="buyersguideproductcategory",
            name="share_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Optional image that will apear when category page is shared.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
                verbose_name="Share Image",
            ),
        ),
        migrations.AlterField(
            model_name="consumercreepometerpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="cta4",
            name="hero",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cta_hero",
                to="images.foundationcustomimage",
                verbose_name="Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="dearinternetpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="focusarea",
            name="interest_icon",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="interest_icon",
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="hero_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="hero_image",
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="ideas_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="ideas_image",
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="partner_background_image",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="images.foundationcustomimage"
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="quote_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="quote_image",
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="homepagetakeactioncards",
            name="image",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="images.foundationcustomimage"
            ),
        ),
        migrations.AlterField(
            model_name="indexpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="initiativesection",
            name="sectionImage",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="section_image",
                to="images.foundationcustomimage",
                verbose_name="Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="initiativespage",
            name="primaryHero",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="primary_hero",
                to="images.foundationcustomimage",
                verbose_name="Primary Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="modularpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="participatepage2",
            name="ctaHero",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="primary_hero_participate",
                to="images.foundationcustomimage",
                verbose_name="Primary Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="participatepage2",
            name="ctaHero2",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="primary_hero_participate2",
                to="images.foundationcustomimage",
                verbose_name="Primary Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="participatepage2",
            name="ctaHero3",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="primary_hero_participate3",
                to="images.foundationcustomimage",
                verbose_name="Primary Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="partnerlogos",
            name="logo",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="images.foundationcustomimage"
            ),
        ),
        migrations.AlterField(
            model_name="primarypage",
            name="banner",
            field=models.ForeignKey(
                blank=True,
                help_text="Choose an image that's bigger than 4032px x 1152px with aspect ratio 3.5:1",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="primary_banner",
                to="images.foundationcustomimage",
                verbose_name="Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="primarypage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="productpage",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="productpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="images.foundationcustomimage"
            ),
        ),
        migrations.AlterField(
            model_name="publicationpage",
            name="hero_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="publication_hero_image",
                to="images.foundationcustomimage",
                verbose_name="Publication Hero Image",
            ),
        ),
        migrations.AlterField(
            model_name="publicationpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="publicationpage",
            name="toc_thumbnail_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Thumbnail image to show on table of content. Use square image of 320×320 pixels or larger.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="toc_thumbnail_image",
                to="images.foundationcustomimage",
                verbose_name="Table of Content Thumbnail",
            ),
        ),
        migrations.AlterField(
            model_name="rccauthorsindexpage",
            name="banner_image",
            field=models.ForeignKey(
                help_text="The image to be used as the banner background image for the author index and all author detail pages.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="rccauthorsindexpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="rccdetailpage",
            name="cover_image",
            field=models.ForeignKey(
                help_text="Select a cover image for this article. The cover image is displayed on the detail page and all article listings.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="rccdetailpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="rcclandingpage",
            name="banner_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will render at the top of the page.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="rcclandingpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="rcclibrarypage",
            name="banner_image",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="images.foundationcustomimage"
            ),
        ),
        migrations.AlterField(
            model_name="rcclibrarypage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="researchauthorsindexpage",
            name="banner_image",
            field=models.ForeignKey(
                help_text="The image to be used as the banner background image for the author index and all author detail pages.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="researchauthorsindexpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="researchdetailpage",
            name="cover_image",
            field=models.ForeignKey(
                help_text="Select a cover image for this article. The cover image is displayed on the detail page and all article listings.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="researchdetailpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="researchlandingpage",
            name="banner_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image that will render at the top of the page.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="researchlandingpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="researchlibrarypage",
            name="banner_image",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="images.foundationcustomimage"
            ),
        ),
        migrations.AlterField(
            model_name="researchlibrarypage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="styleguide",
            name="emoji_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Emoji style image for use in the styleguide.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.foundationcustomimage",
            ),
        ),
        migrations.AlterField(
            model_name="youtuberegrets2021page",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="youtuberegrets2022page",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="youtuberegretspage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
        migrations.AlterField(
            model_name="youtuberegretsreporterpage",
            name="search_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image must be high quality, include our logo mark and have the dimensions 1200 x 628 px. For more design guidelines see here: https://foundation.mozilla.org/en/docs/brand/brand-identity/social-media/#og-images",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.foundationcustomimage",
                verbose_name="Search image",
            ),
        ),
    ]
