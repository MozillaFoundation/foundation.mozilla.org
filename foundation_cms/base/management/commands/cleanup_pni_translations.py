from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail_localize.models import (
    OverridableSegment,
    RelatedObjectSegment,
    SegmentOverride,
    StringSegment,
    StringTranslation,
    TemplateSegment,
    TranslatableObject,
    Translation,
    TranslationSource,
)
from wagtail_localize_git.models import Resource

# The buyersguide/PNI models dropped by wagtailpages migration 0178. DeleteModel emits raw DDL,
# so wagtail-localize's post_delete cleanup never ran and its tables still hold this content.
PNI_MODELS = [
    "buyersguidearticlepage",
    "buyersguidearticlepageauthorprofilerelation",
    "buyersguidearticlepagecontentcategoryrelation",
    "buyersguidearticlepagerelatedarticlerelation",
    "buyersguidecalltoaction",
    "buyersguidecampaignpage",
    "buyersguidecampaignpagedonationmodalrelation",
    "buyersguidecategorynav",
    "buyersguidecategorynavrelation",
    "buyersguidecontentcategory",
    "buyersguideeditorialcontentindexpage",
    "buyersguideeditorialcontentindexpagearticlepagerelation",
    "buyersguidepage",
    "buyersguidepagefeaturedarticlerelation",
    "buyersguidepagefeaturedupdaterelation",
    "buyersguidepageherosupportingpagerelation",
    "buyersguideproductcategory",
    "buyersguideproductcategoryarticlepagerelation",
    "buyersguideproductpagearticlepagerelation",
    "consumercreepometerpage",
    "excludedcategories",
    "generalproductpage",
    "productpage",
    "productpagecategory",
    "productpageevaluation",
    "productpageprivacypolicylink",
    "productpagevotes",
    "productupdates",
    "productvote",
    "relatedproducts",
    "softwareproductpage",
    "update",
]


class Command(BaseCommand):
    help = "Remove the orphaned PNI/buyersguide translation data left behind in wagtail-localize."

    def add_arguments(self, parser):
        parser.add_argument(
            "--execute",
            action="store_true",
            help="Commit the changes. Without it the command reports what it would do and rolls back.",
        )
        parser.add_argument(
            "--disable-only",
            action="store_true",
            help="Only mark the translations disabled, which is all the Pontoon sync reads. Leaves the rows in place.",
        )

    def handle(self, *args, **options):
        execute = options["execute"]
        disable_only = options["disable_only"]

        content_types = ContentType.objects.filter(app_label="wagtailpages", model__in=PNI_MODELS)

        still_installed = [ct for ct in content_types if ct.model_class() is not None]
        if still_installed:
            raise CommandError(
                "Refusing to run: these content types still resolve to installed models, so their "
                f"content is live: {', '.join(str(ct) for ct in still_installed)}"
            )

        keys = set(
            TranslationSource.objects.filter(specific_content_type__in=content_types).values_list(
                "object_id", flat=True
            )
        )
        if not keys:
            self.stdout.write(self.style.SUCCESS("Nothing to do: no PNI translation data found."))
            return

        translations = Translation.objects.filter(source__object_id__in=keys)
        self.stdout.write(
            f"Found {len(keys)} PNI objects, {translations.count()} translations "
            f"({translations.filter(enabled=True).count()} still enabled)."
        )

        for path in Resource.objects.filter(object_id__in=keys).values_list("path", flat=True):
            self.stdout.write(f"  {path}")

        with transaction.atomic():
            if disable_only:
                disabled = translations.filter(enabled=True).update(enabled=False)
                self.stdout.write(f"\nDisabled {disabled} translations.")
            else:
                self.stdout.write("\nDeleted rows:")
                for label, queryset in self.deletion_plan(keys):
                    self.stdout.write(f"  {label}: {queryset.delete()[0]}")

            remaining = Translation.objects.filter(enabled=True).count()
            self.stdout.write(f"\n{remaining} enabled translations remain across the rest of the site.")

            if not execute:
                transaction.set_rollback(True)
                self.stdout.write(self.style.WARNING("\nDry run: rolled back. Re-run with --execute to commit."))
                return

        self.stdout.write(self.style.SUCCESS("\nDone. Trigger a Pontoon sync to drop the files from fomo-content."))

    def deletion_plan(self, keys):
        """Ordered to clear the segments before the contexts they PROTECT.

        Deleting the TranslatableObject last cascades to TranslationSource, TranslationContext,
        TranslationLog, Resource and SyncLogResource. String and Template rows are shared with
        other content and are deliberately left alone, matching wagtail-localize's own cleanup.
        """
        return [
            ("StringTranslation", StringTranslation.objects.filter(context__object__translation_key__in=keys)),
            ("SegmentOverride", SegmentOverride.objects.filter(context__object__translation_key__in=keys)),
            ("Translation", Translation.objects.filter(source__object_id__in=keys)),
            ("OverridableSegment", OverridableSegment.objects.filter(context__object_id__in=keys)),
            ("RelatedObjectSegment", RelatedObjectSegment.objects.filter(context__object_id__in=keys)),
            ("StringSegment", StringSegment.objects.filter(context__object_id__in=keys)),
            ("TemplateSegment", TemplateSegment.objects.filter(context__object_id__in=keys)),
            ("TranslatableObject", TranslatableObject.objects.filter(translation_key__in=keys)),
        ]
