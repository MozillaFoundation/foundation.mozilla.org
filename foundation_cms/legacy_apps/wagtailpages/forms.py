from wagtail.admin.forms import WagtailAdminPageForm


class BlogPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Overriding the blog page's admin form in order to make promote tab's
        # "search image" and "search description" fields required.
        self.fields["search_description"].required = True
        self.fields["search_image"].required = True

    def clean(self):
        cleaned_data = super().clean()
        # Max number validation for blog page topics. We are using the admin form's clean method
        # instead of the page model's, because validation through the page model's method would
        # return a 500 error to the user instead of an admin form error.
        topics = cleaned_data["topics"]
        if topics.count() > 2:
            self.add_error("topics", "Please select 2 topics max.")

        return cleaned_data


# Similar validation to the BlogPageForm, but for the Blog Index page
# and its field 'related_topics'.
class BlogIndexPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()
        topics = cleaned_data["related_topics"]
        if topics.count() > 7:
            self.add_error("related_topics", "Please select 7 topics max.")

        return cleaned_data
