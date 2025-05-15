from django.core.exceptions import ValidationError
from wagtail.admin.forms import WagtailAdminModelForm


class NavMenuForm(WagtailAdminModelForm):
    def clean(self):
        cleaned_data = super().clean()
        enable_blog_dropdown = cleaned_data.get("enable_blog_dropdown")

        # Make sure that there are featured blog topics if the blog dropdown is enabled
        featured_blog_topics_formset = self.formsets["featured_blog_topics"]
        number_of_featured_blog_topics = featured_blog_topics_formset.total_form_count()
        if enable_blog_dropdown and number_of_featured_blog_topics == 0:
            error = ValidationError("You must add at least one featured blog topic if the blog dropdown is enabled")
            self.add_error(None, error)
            self.add_error("enable_blog_dropdown", error)

        # Make sure that there is a label for the blog button if the blog dropdown is enabled
        blog_button_label = cleaned_data.get("blog_button_label")
        if enable_blog_dropdown and not blog_button_label:
            self.add_error(
                "blog_button_label", "You must provide a label for the blog button if the blog dropdown is enabled"
            )

        return cleaned_data
