from django.apps import AppConfig


class FoundationCMSConfig(AppConfig):
    name = "foundation_cms.base"

    def ready(self):
        # Import a patch for wagtail-localize image blocks
        import foundation_cms.base.patches.wagtail_localize_image_block
