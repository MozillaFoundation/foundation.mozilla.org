from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import TranslatableMixin
from wagtail.search import index
from wagtail_localize import fields as localize_fields


class BaseTaxonomy(TranslatableMixin):
    """
    Base class for taxonomy models.

    Fields:
    - name: The name of the taxonomy (required).
    - slug: The slug is auto-generated from the name but can be customized if needed. It needs to be unique per locale.

    Meta:
    - abstract: Indicates that this class is an abstract base class.
    - ordering: The default ordering of instances based on the name field.
    - unique_together: Defines uniqueness constraints for locale and slug.

    Search Fields:
    - name: Allows partial matching for searching by name.
    - locale_id: Allows filtering by locale.

    Translatable Fields:
    - name: The name field is translatable.
    - slug: The slug field is synchronized across translations.

    Methods:
    - __str__: Returns the string representation of the taxonomy instance (name)
    - validate_unique: Validates the uniqueness of the taxonomy instance, considering the locale.

    Note: This is an abstract base class and should be subclassed for concrete taxonomic models.
    """

    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(
        max_length=100,
        null=False,
        blank=False,
        help_text=(
            "The slug is auto-generated from the name, but can be customized if needed. "
            "It needs to be unique per locale."
        ),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta(TranslatableMixin.Meta):
        abstract = True
        ordering = ["name"]
        unique_together = TranslatableMixin.Meta.unique_together + [
            ("locale", "slug"),
        ]

    search_fields = [
        index.AutocompleteField("name"),
        index.FilterField("locale_id"),
    ]

    translatable_fields = [
        localize_fields.TranslatableField("name"),
        localize_fields.SynchronizedField("slug"),
    ]

    def __str__(self):
        return self.name

    def validate_unique(self, exclude=None):
        """
        Validate the uniqueness of the taxonomy instance, excluding the locale field if specified.

        Parameters:
        - exclude: A list of fields to exclude from uniqueness validation.

        Returns:
        - None if the instance is unique.
        - ValidationError if the instance is not unique.
        """
        if exclude and "locale" in exclude:
            exclude.remove("locale")
        return super().validate_unique(exclude)
