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


@register.simple_tag(takes_context=True)
def yt2022data_wrapper_url(context):
    if context['request'].LANGUAGE_CODE == "fr":
        return 'https://datawrapper.dwcdn.net/w8veu/'
    if context['request'].LANGUAGE_CODE == "de":
        return 'https://datawrapper.dwcdn.net/iHxzV/'
    if context['request'].LANGUAGE_CODE == "es":
        return 'https://datawrapper.dwcdn.net/QIjQb/'
    if context['request'].LANGUAGE_CODE == "nl":
        return 'https://datawrapper.dwcdn.net/d8LI4/'
    if context['request'].LANGUAGE_CODE == "pt-BR":
        return 'https://datawrapper.dwcdn.net/KhNFD/'
    else:
        return 'https://datawrapper.dwcdn.net/kl3jI/'

