from django.db.models import SET_NULL, CharField, ForeignKey
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.base.models.abstract_base_page import AbstractBasePage
from foundation_cms.constants import DEFAULT_RICH_TEXT_FEATURES


class AbstractProfilePage(AbstractBasePage):
    """
    Abstract base for pages that represent a profile.
    Provides identity fields on top of AbstractBasePage.
    """

    image = ForeignKey(
        get_image_model_string(),
        null=True,
        on_delete=SET_NULL,
        related_name="+",
        verbose_name="Profile Image",
        help_text="Profile image or headshot.",
    )
    role = CharField(
        max_length=255,
        help_text="Professional title or role.",
    )
    bio = RichTextField(
        help_text="Brief introductory bio.",
        features=DEFAULT_RICH_TEXT_FEATURES,
    )
    location = CharField(
        max_length=255,
        help_text="Country or location of the profile.",
    )

    content_panels = AbstractBasePage.content_panels + [
        FieldPanel("title", heading="Full Name"),
        FieldPanel("image"),
        FieldPanel("role"),
        FieldPanel("bio"),
        FieldPanel("location"),
    ]

    translatable_fields = AbstractBasePage.translatable_fields + [
        SynchronizedField("image"),
        TranslatableField("role"),
        TranslatableField("bio"),
        TranslatableField("location"),
    ]

    search_fields = AbstractBasePage.search_fields + [
        index.SearchField("role", boost=6),
        index.SearchField("bio", boost=4),
        index.SearchField("location", boost=2),
    ]

    class Meta:
        abstract = True
