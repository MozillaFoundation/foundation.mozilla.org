def skip_default_wrapper_on(*page_types):
    """
    Decorator that adds skip default wrapper behavior to blocks.
    Use "*" to indicate all pages should have full bleed.

    Usage:
        @skip_default_wrapper_on("HomePage", "NothingPersonalHomePage")
        class MyBlock(BaseBlock):
            pass

    Side effects:
        - Adds 'skip_default_wrapper' to the block's template context
        - Modifies the class's MRO (Method Resolution Order)
        - Replaces the original class with an enhanced version. The original class becomes a parent of the new class.
    """

    def decorator(block_class):
        # Create a mixin class dynamically inside the decorator
        # This allows us to inject behavior without modifying the original class
        class SkipDefaultWrapperMixin:
            def get_context(self, value, parent_context=None):
                context = super().get_context(value, parent_context)
                page = parent_context.get("page") if parent_context else None

                if "*" in page_types:
                    context["skip_default_wrapper"] = True
                elif page:
                    context["skip_default_wrapper"] = page.specific_class.__name__ in page_types
                else:
                    context["skip_default_wrapper"] = False

                return context

        # Combine mixin with original block
        # Mixin goes first so our get_context runs before the block's
        class DecoratedBlock(SkipDefaultWrapperMixin, block_class):
            pass

        # Preserve the original class's identity
        # This prevents issues with Wagtail's registration and Django's introspection
        DecoratedBlock.__name__ = block_class.__name__
        DecoratedBlock.__module__ = block_class.__module__

        # Return the enhanced class to replace the original
        return DecoratedBlock

    return decorator
