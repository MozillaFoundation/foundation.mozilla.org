import datetime

from django.utils import timezone
from wagtail import models as wagtail_models


def days_ago(n: int):
    return timezone.now().date() - datetime.timedelta(days=n)


def make_page_private(page):
    wagtail_models.PageViewRestriction.objects.create(
        page=page,
        restriction_type=wagtail_models.PageViewRestriction.PASSWORD,
        password="test",
    )


def translate_detail_page(detail_page, locale):
    # Requires previous tree synchronization
    trans_detail_page = detail_page.get_translation(locale)

    for rcc_author_trans in trans_detail_page.rcc_authors.all():
        # The through model is already for the new locale after the tree sync,
        # but the related model is not.
        author_profile_orig = rcc_author_trans.author_profile
        author_profile_trans = author_profile_orig.copy_for_translation(locale)
        author_profile_trans.save()
        rcc_author_trans.author_profile = author_profile_trans
        rcc_author_trans.save()

    for related_content_type_trans in trans_detail_page.related_content_types.all():
        content_type_orig = related_content_type_trans.content_type
        content_type_trans = content_type_orig.copy_for_translation(locale)
        content_type_trans.save()
        related_content_type_trans.content_type = content_type_trans
        related_content_type_trans.save()

    for related_curricular_area_trans in trans_detail_page.related_curricular_areas.all():
        curricular_area_orig = related_curricular_area_trans.curricular_area
        curricular_area_trans = curricular_area_orig.copy_for_translation(locale)
        curricular_area_trans.save()
        related_curricular_area_trans.content_type = curricular_area_trans
        related_curricular_area_trans.save()

    for related_topic_trans in trans_detail_page.related_topics.all():
        topic_orig = related_topic_trans.rcc_topic
        topic_trans = topic_orig.copy_for_translation(locale)
        topic_trans.save()
        related_topic_trans.rcc_topic = topic_trans
        related_topic_trans.save()

    trans_detail_page.alias_of = None
    trans_detail_page.save()
    return trans_detail_page
