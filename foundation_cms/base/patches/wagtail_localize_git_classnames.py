"""
Patch for wagtail-localize-git compatibility with Wagtail 7.0

Wagtail 7.0 removed the 'classnames' parameter from MenuItem classes in favor of 'classname'.
wagtail-localize-git 0.15.0 still uses the old 'classnames' parameter, causing:
TypeError: MenuItem.__init__() got an unexpected keyword argument 'classnames'

This patch automatically converts 'classnames' to 'classname' to maintain compatibility.

@TODO: Remove this patch when wagtail-localize-git releases a version compatible with Wagtail 7.0.
"""

from wagtail.admin.menu import MenuItem


def patched_menuitem_init(original_init):
    """
    Decorator to patch MenuItem.__init__ to handle classnames -> classname conversion
    """

    def wrapper(self, *args, **kwargs):
        # Convert 'classnames' to 'classname' if present
        if "classnames" in kwargs:
            # If both classnames and classname are present, prioritize classname
            if "classname" not in kwargs:
                kwargs["classname"] = kwargs["classnames"]
            # Remove the deprecated classnames parameter
            kwargs.pop("classnames")

        # Call the original __init__ method
        return original_init(self, *args, **kwargs)

    return wrapper


# Store original method for potential restoration
_original_menuitem_init = MenuItem.__init__

# Apply the patch
MenuItem.__init__ = patched_menuitem_init(_original_menuitem_init)
