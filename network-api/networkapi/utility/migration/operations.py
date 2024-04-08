from wagtail.blocks.migrations.operations import BaseBlockOperation


class AlterStreamChildBlockDataOperation(BaseBlockOperation):
    def __init__(self, block, operation):
        """Alter the data of a child block in a StreamField.

        Args:
            block (str): The key of the block type to alter.
            operation (callable): A function that takes a block value and returns a
                new block value.
        """
        super().__init__()
        self.block = block
        self.operation = operation

    def apply(self, block_value):
        mapped_block_value = []
        for child_block in block_value:
            if child_block["type"] == self.block:
                new_block = self.operation(child_block)
                mapped_block_value.append(new_block)
            else:
                mapped_block_value.append(child_block)
        return mapped_block_value

    @property
    def operation_name_fragment(self):
        return f"alter_stream_child_data_from_{self.block}"
