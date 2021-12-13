from wagtail.admin.forms import WagtailAdminModelForm


class BuyersGuideProductCategoryForm(WagtailAdminModelForm):
    def clean_parent(self):
        parent = self.cleaned_data["parent"]
        if parent:
            ancestors = parent.get_ancestors(inclusive=True)
            if len(ancestors) > 2:
                self.add_error("parent", "Categories can only be three levels deep.")
            if self.instance in ancestors:
                self.add_error("parent", "A category cannot be a decendent of itself.")
        return parent
