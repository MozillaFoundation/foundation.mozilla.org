from wagtail.admin.forms import WagtailAdminModelForm, WagtailAdminPageForm


class BuyersGuideProductCategoryForm(WagtailAdminModelForm):
    def clean_name(self):
        instance = self.instance
        set = instance.__class__.objects
        name = self.cleaned_data["name"]
        duplicate = set.filter(name__iexact=name).exclude(pk=instance.pk)

        if hasattr(instance, 'locale'):
            duplicate = duplicate.filter(locale=instance.locale)

        if duplicate.exists():
            self.add_error("name", "A category with this name already exists.")

        return name

    def clean_parent(self):
        parent = self.cleaned_data["parent"]
        if parent:
            if parent.parent:
                self.add_error("parent", "Categories can only be two levels deep.")
            if self.instance == parent:
                self.add_error("parent", "A category cannot be a parent of itself.")
        return parent


# Max number validation for blog page topics. We are using a custom form to avoid
# an issue where the `ValidationError` raised in the page's `clean` method is
# not caught by Wagtail. Instead of displaying the `ValidationError` as a message to 
# the editor, the admin crashes with a 500 error. Using the custom form gets around
# that issue. 
class BlogPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super(BlogPageForm, self).clean()
        topics = cleaned_data['topics']
        if topics.count() > 2:
            self.add_error('topics', 'Please select 2 topics max.')

        return cleaned_data
