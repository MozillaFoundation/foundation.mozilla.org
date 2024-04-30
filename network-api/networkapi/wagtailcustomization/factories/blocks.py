from wagtail_factories.blocks import StructBlockFactory


class ExtendedStructBlockFactory(StructBlockFactory):
    @classmethod
    def _construct_struct_value(cls, block_class, params):
        """Use value_class defined on model's Meta to create the StructValue instance."""
        struct_value_class = cls._meta.model().meta.value_class
        return struct_value_class(
            block_class(),
            [(name, value) for name, value in params.items()],
        )
