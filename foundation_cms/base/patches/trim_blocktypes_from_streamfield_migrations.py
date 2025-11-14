# via https://cynthiakiser.com/blog/2022/01/06/trimming-wagtail-migration-cruft.html?utm_source=chatgpt.com
# see convo github.com/wagtail/wagtail/issues/4298

# this will strip block_type out of streamfield migrations, keeping them light.
# turn this on only when absolutely necessary to squash heavy migrations
# preventing review apps from releasing.

import wagtail.fields


def deconstruct_without_block_definition(self):
    name, path, _, kwargs = super(wagtail.fields.StreamField, self).deconstruct()
    block_types = list()
    args = [block_types]
    return name, path, args, kwargs


wagtail.fields.StreamField.deconstruct = deconstruct_without_block_definition
