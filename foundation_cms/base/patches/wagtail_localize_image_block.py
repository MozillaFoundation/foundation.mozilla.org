from wagtail_localize.segments.extract import StreamFieldSegmentExtractor


def safe_handle_image_block(self, block, image_block_value, raw_value=None):
    """
    Patched version of wagtail_localize.segments.extract.StreamFieldSegmentExtractor.handle_image_block
    Adds a guard so raw_value=None won't break with AttributeError.
    """
    # PATCH- bail early if raw_value is None or not a dict
    # @TODO remove all of this once wagtail-localize is patched for it.
    if raw_value is None or not isinstance(raw_value, dict):
        return []

    # Remaining code from wagtail-localize's `handle_image_block` method
    segments = []

    for field_name, block_type in block.child_blocks.items():
        if raw_value.get("type") and raw_value.get("value"):
            # for top-level ImageBlock, raw_value has a
            # {"type": "field_name", "value": {"image": X, "alt_text": "", "caption": ""}} format.
            # whereas if the ImageBlock is part of a StructBlock, ListBlock or StreamBlock, we
            # only get the "value" part.
            raw_value = raw_value.get("value")

        try:
            block_raw_value = raw_value.get(field_name)
            block_value = image_block_value if field_name == "image" else block_raw_value
        except (KeyError, TypeError):
            # e.g. raw_value is None, or is that from chooser
            block_raw_value = None
            block_value = None

        if isinstance(block_type, blocks.CharBlock) and block_value is None:
            block_value = ""

        segments.extend(
            segment.wrap(field_name)
            for segment in self.handle_block(block_type, block_value, raw_value=block_raw_value)
        )

    return segments


# Monkeypatch it in
StreamFieldSegmentExtractor.handle_image_block = safe_handle_image_block
