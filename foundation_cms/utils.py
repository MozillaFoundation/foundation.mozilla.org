from django.conf import settings
from django.db import models
from wagtail.models import Locale


def get_default_locale():
    """
    We defer this logic to a function so that we can call it on demand without
    running into "the db is not ready for queries yet" problems.
    """
    DEFAULT_LOCALE = Locale.objects.get(language_code=settings.LANGUAGE_CODE)
    DEFAULT_LOCALE_ID = DEFAULT_LOCALE.id
    return (
        DEFAULT_LOCALE,
        DEFAULT_LOCALE_ID,
    )


def get_related_items(
    queryset: "models.QuerySet", related_item_field: str, order_by: str | None = None
) -> list["models.Model"]:
    """
    Return list of the related items from the queryset.

    For each item in the queryset, the related item stored in `related_item_field` is
    returned.

    """
    # Apply ordering if needed
    if order_by:
        queryset = queryset.order_by(order_by)

    return [getattr(relation, related_item_field) for relation in queryset.select_related(related_item_field)]


def localize_queryset(
    queryset, preserve_order=False, include_draft_translations=False, include_only_translations=False
):
    """
    Return a localized version of this queryset.

    A localized queryset is one where objects are replaced with versions translated
    into the active locale. Where a translation isn't available for an object, the
    original is retained instead.

    By default, the same ordering definition as in the original queryset is applied.
    This means that the translated values are being considered during ordering,
    which can lead to a different order than the original queryset. If you want to
    preserve the same order as the original queryset, you need to pass
    ``preserve_order=True``.

    If a model inherits from
    :py:class:`DraftStateMixin <wagtail.models.DraftStateMixin>`,
    draft translations are not considered as translated instances. If a translation
    is in draft, the original instance is used instead. To override this behavior
    and include draft translations, pass ``include_draft_translations=True``.

    By default, the localized queryset can contain untranslated instances from the
    original queryset if no translation for the instance is available. If this is
    not desired, pass ``include_only_translations=True`` to only include instances
    that are translated into the active locale.

    Note: Because this method uses a complex query to retrieve the items in the
    localized queryset, effects of methods like `annotate`, `select_related` and
    `prefetch_related` will be reapplied to the localized queryset. However, this
    means that the values will be recomputed with the translated values. This can
    lead to unexpected results.

    Extracted from https://github.com/wagtail/wagtail/pull/11274
    """
    # Get all instances that are available in the active locale. We can find these
    # by getting all model instances that have a translation key from the original
    # queryset and that are available in the active locale.
    active_locale = Locale.get_active()
    original_translation_keys = queryset.values_list("translation_key", flat=True)
    translated_instances = queryset.model.objects.filter(
        locale_id=active_locale.pk,
        translation_key__in=original_translation_keys,
    )

    # Don't consider draft translations. If a translation is in draft, we want to
    # use the original instance instead. To do so, we exclude draft translations.
    # This only applies if the model has a `live` field. We allow bypassing this
    # behavior by passing `include_draft_translations=True`.
    from wagtail.models import DraftStateMixin

    if issubclass(queryset.model, DraftStateMixin) and not include_draft_translations:
        translated_instances = translated_instances.exclude(live=False)

    if include_only_translations:
        # If we only want to include translations, we can use the translated
        # instances as the localized queryset.
        localized_queryset = translated_instances
    else:
        # Otherwise, we need to combine the translated instances with the
        # untranslated instance.

        # Get all instances that are not available in the active locale, these are
        # the untranslated instances. We can find these by excluding the translation
        # keys for which translations exist from the original queryset.
        translated_translation_keys = translated_instances.values_list("translation_key", flat=True)
        untranslated_instances = queryset.exclude(
            translation_key__in=translated_translation_keys,
        )

        # Combine the translated and untranslated querysets to get the localized
        # queryset.
        localized_queryset = queryset.model.objects.filter(
            models.Q(pk__in=translated_instances) | models.Q(pk__in=untranslated_instances)
        )

    if annotations := queryset.query.annotations:
        localized_queryset = localized_queryset.annotate(**annotations)

    if not preserve_order:
        # Apply the same `order_by` as in the original queryset. This does not mean
        # that the order of the items is retained. Rather, the same fields are used
        # for ordering. However, the ordering is likely to be different because the
        # translated values are used.
        return localized_queryset.order_by(*queryset.query.order_by)

    else:
        # Keep the same order as in the original queryset. To do so, we annotate the
        # localized queryset with the original order of the translation keys, and
        # then order by that annotation.
        ordering_when_clauses = [
            models.When(translation_key=tk, then=models.Value(index))
            for index, tk in enumerate(original_translation_keys)
        ]
        if ordering_when_clauses:
            localized_annotated_queryset = localized_queryset.annotate(
                original_order=models.Case(*ordering_when_clauses)
            )
            return localized_annotated_queryset.order_by("original_order")
        else:
            return localized_queryset
