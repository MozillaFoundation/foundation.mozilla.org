from django.apps import AppConfig
from django.conf import settings


class FoundationCMSConfig(AppConfig):
    name = "foundation_cms.base"

    def ready(self):
        # Import a patch for wagtail-localize image blocks
        import foundation_cms.base.patches.wagtail_localize_image_block  # noqa: F401

        if settings.TRIM_STREAMFIELD_MIGRATIONS is True:
            import foundation_cms.base.patches.trim_streamfield_migrations  # noqa: F401
