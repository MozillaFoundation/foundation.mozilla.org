from django import template
from django.conf import settings

register = template.Library()


# Serves localized versions of the YouTube Regrets 2021 report pdf
@register.simple_tag(takes_context=True)
def yt2021report(context):
    document_root = settings.MEDIA_URL + 'documents/'
    if settings.USE_S3:
        document_root = settings.MEDIA_URL + settings.AWS_LOCATION + '/documents/'

    report_url = document_root + 'Mozilla_YouTube_Regrets_Report.pdf'
    if context['request'].LANGUAGE_CODE == "de":
        report_url = document_root + 'Mozilla_YouTube_Regrets_Report_German.pdf'

    return report_url
