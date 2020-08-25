# A mixin that imparts banner inheritance for whatever model it gets tacked onto
class FoundationBannerInheritanceMixin():

    def get_banner(self):
        if self.banner is None:
            ancestors = self.get_ancestors()
            root = ancestors[1].specific
            # note: we need to reverse get_ancestors, because by default
            # this gives a list that starts at the root, and then gets more
            # specific, ending in the direct parent. We want to check in the
            # opposite direction: start at the parent until we hit the root.
            for page in ancestors.reverse():
                page = page.specific
                if page == root:
                    return None
                valid = isinstance(page, FoundationBannerInheritanceMixin)
                if valid and page.banner is not None:
                    return page.banner

        return self.banner
