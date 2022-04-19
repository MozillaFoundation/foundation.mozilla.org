import datetime


def days_ago(n: int):
    return datetime.date.today() - datetime.timedelta(days=n)


def translate_detail_page(detail_page, locale):
    # Requires previous tree synchronization
    trans_detail_page = detail_page.get_translation(locale)

    for research_author_trans in trans_detail_page.research_authors.all():
        # The through model is already for the new locale after the tree sync,
        # but the related model is not.
        author_profile_orig = research_author_trans.author_profile
        author_profile_trans = author_profile_orig.copy_for_translation(locale)
        author_profile_trans.save()
        research_author_trans.author_profile = author_profile_trans
        research_author_trans.save()

    for related_topic_trans in trans_detail_page.related_topics.all():
        topic_orig = related_topic_trans.research_topic
        topic_trans = topic_orig.copy_for_translation(locale)
        topic_trans.save()
        related_topic_trans.research_topic = topic_trans
        related_topic_trans.save()

    for related_region_trans in trans_detail_page.related_regions.all():
        region_orig = related_region_trans.research_region
        region_trans = region_orig.copy_for_translation(locale)
        region_trans.save()
        related_region_trans.research_region = region_trans
        related_region_trans.save()

    trans_detail_page.alias_of = None
    trans_detail_page.save()
    return trans_detail_page
