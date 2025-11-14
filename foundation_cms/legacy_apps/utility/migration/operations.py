import inspect

from django.utils.deconstruct import deconstructible
from django.utils.module_loading import import_string
from wagtail.blocks.migrations.operations import BaseBlockOperation


def _to_dotted(fn_or_path: object) -> str:
    # Accept a dotted path or a function object; always return dotted path
    if isinstance(fn_or_path, str):
        return fn_or_path
    if inspect.isfunction(fn_or_path):
        # Disallow lambdas/closures/partials because they aren't importable
        if fn_or_path.__name__ == "<lambda>" or fn_or_path.__module__ is None:
            raise ValueError("Operation must be an importable function, not a lambda/closure.")
        return f"{fn_or_path.__module__}.{fn_or_path.__name__}"
    raise TypeError("operation must be a dotted path string or a function")


@deconstructible
class AlterStreamChildBlockDataOperation(BaseBlockOperation):
    def __init__(self, block: str, operation):
        """
        block: the child block type to alter, e.g. 'linkbutton'
        operation: dotted path string or function taking a block dict -> new block dict
        """
        super().__init__()
        self.block = block
        # Store as dotted path so it's serializable
        self.operation_path = _to_dotted(operation)

    def deconstruct(self):
        # Return (import_path, args, kwargs) so Django can rebuild this op
        return (
            "foundation_cms.legacy_apps.utility.migration.operations.AlterStreamChildBlockDataOperation",
            [self.block, self.operation_path],
            {},
        )

    def apply(self, block_value):
        transform = import_string(self.operation_path)
        mapped_block_value = []
        for child_block in block_value:
            if child_block["type"] == self.block:
                new_block = transform(child_block)
                mapped_block_value.append(new_block)
            else:
                mapped_block_value.append(child_block)
        return mapped_block_value

    @property
    def operation_name_fragment(self):
        # Optional: include op name for clearer migration names
        try:
            op_name = self.operation_path.rsplit(".", 1)[-1]
        except Exception:
            op_name = "op"
        return f"alter_stream_child_data_from_{self.block}_{op_name}"
