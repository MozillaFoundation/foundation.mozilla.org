import logging

from wagtail.signals import page_published, page_unpublished

from .utils import get_search_backend_for_locale

logger = logging.getLogger(__name__)


def _locale_code(page):
    try:
        return page.locale.language_code
    except Exception:
        return None


def _index_page(page):
    try:
        backend, _ = get_search_backend_for_locale(_locale_code(page))
        backend.add(page)
    except Exception:
        logger.exception("Failed to index page pk=%s", page.pk)


def _deindex_page(page):
    try:
        backend, _ = get_search_backend_for_locale(_locale_code(page))
        backend.delete(page)
    except Exception:
        logger.exception("Failed to deindex page pk=%s", page.pk)


def _handle_publish(sender, instance, **kwargs):
    _index_page(instance)


def _handle_unpublish(sender, instance, **kwargs):
    _deindex_page(instance)


page_published.connect(_handle_publish, dispatch_uid="search_multilingual_index_publish")
page_unpublished.connect(_handle_unpublish, dispatch_uid="search_multilingual_index_unpublish")
