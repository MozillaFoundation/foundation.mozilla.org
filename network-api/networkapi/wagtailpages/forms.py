from wagtail.admin.forms import WagtailAdminModelForm


class BuyersGuideProductCategoryForm(WagtailAdminModelForm):
    def clean_name(self):
        instance = self.instance
        set = instance.__class__.objects
        name = self.cleaned_data["name"]

        if instance.hasattr('locale'):
            duplicate = set.filter(
                name__iexact=name,
                locale=instance.locale,
            ).exclude(pk=instance.pk)
        else:
            duplicate = set.filter(name__iexact=name).exclude(pk=instance.pk)

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