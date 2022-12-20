from django.core import exceptions
from django.db import models
from django.utils import text as text_utils
from wagtail.admin import edit_handlers as admin_panels
from wagtail.core import models as wagtail_models
from wagtail.snippets import models as snippet_models
from wagtail_localize import fields as localize_fields


@snippet_models.register_snippet
class BuyersGuideContentCategory(wagtail_models.TranslatableMixin, models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(max_length=100, null=False, blank=True, unique=True)

    panels = [admin_panels.FieldPanel("title")]

    translatable_fields = [localize_fields.TranslatableField('title')]

    class Meta(wagtail_models.TranslatableMixin.Meta):
        verbose_name = "Buyers Guide Content Category"
        verbose_name_plural = "Buyers Guide Content Categories"

    def __str__(self) -> str:
        return self.title

    def clean_slug(self):
        """
        We would really want the slugs to be only unique per locale.
        If we implement that with a UniqueConstraint or unique_together,
        Wagtail will crash if the constraint is violated.
        Wagtail does handle the simple unique requirement on the slug field gracefully.
        But, Wagtail Localize can not create a copy of the category for translation,
        because the slug is the same in the beginning and would violate the unique
        constraint.

        Therefore, we are using slugs that are unique regardless of locale but add
        the locale language code as part of the locale to avoid uniqueness issues
        when creating the copies for translation.

        See also: https://github.com/wagtail/wagtail/issues/8918

        We are checking if the slug is already in use manually, because the Wagtail form seems to fail some how to
        apply the uniqueness check when the slug field is not displayed. I guess it would also be confusing to the
        user to get an error for a field they don't see. If we were to show the slug field it would also be confusing,
        because we are overriding that field.

        """
        cleaned_slug = text_utils.slugify(f"{ self.locale.language_code } { self.title }")

        # Only update slug if necessary
        if self.slug != cleaned_slug:
            self.slug = cleaned_slug
            # Only validate slug if updated, because otherwise we are throwing when cleaning the existing one itself.
            if self.__class__.objects.filter(slug=self.slug).exists():
                raise exceptions.ValidationError({"title": "This title appears to be in use already."})

    def clean(self):
        """Clean the slug and clean the model."""
        self.clean_slug()
        super().clean()
