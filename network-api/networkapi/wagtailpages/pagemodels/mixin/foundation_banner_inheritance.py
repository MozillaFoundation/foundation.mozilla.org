# A mixin that imparts banner inheritance for whatever model it gets tacked onto
class FoundationBannerInheritanceMixin():

    def get_banner(self, root=None):
        if root is None:
            root = self.get_ancestors()[1].specific

        if self.banner is None:
            parent = self.get_parent().specific
            valid = isinstance(parent, FoundationBannerInheritanceMixin) and parent != root
            if valid:
                return parent.get_banner(root)
            else:
                return None

        return self.banner
