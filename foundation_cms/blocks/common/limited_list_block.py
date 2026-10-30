from wagtail import blocks


class LimitedListBlock(blocks.ListBlock):
    """A ListBlock whose editor stops at its min and max and shows how many items it holds."""

    # Migrations record a plain ListBlock: the limits only change the editor, so
    # migrations never need to import this class.
    canonical_module_path = "wagtail.blocks.ListBlock"

    def __init__(self, child_block, *, max_num, **kwargs):
        super().__init__(child_block, max_num=max_num, **kwargs)
        self.meta.form_attrs = {
            "data-controller": "list-limit",
            "data-list-limit-min-value": str(self.meta.min_num or 0),
            "data-list-limit-max-value": str(max_num),
        }

    # Wagtail checks this flag to keep treating the first argument as the child block.
    __init__.has_child_block_arg = True  # type: ignore[attr-defined]
