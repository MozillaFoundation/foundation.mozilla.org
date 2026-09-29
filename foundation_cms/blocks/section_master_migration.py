"""Pure, opt-in prototype transformations; no database writes."""

from copy import deepcopy
from uuid import NAMESPACE_URL, uuid5

from .section_master_block import SECTION_BLOCK_NAMES


def wrap_sections(body):
    """Wrap eligible runs, preserving child values, IDs, and sibling order."""
    result, run = [], []

    def flush():
        if run:
            section_id = str(uuid5(NAMESPACE_URL, "section-master:" + run[0]["id"]))
            result.append(
                {
                    "type": "section_master",
                    "id": section_id,
                    "value": {"label": "", "padding": "regular", "rhythm": "regular", "content": run.copy()},
                }
            )
            run.clear()

    for child in deepcopy(body):
        if child["type"] in SECTION_BLOCK_NAMES and child.get("id"):
            run.append(child)
        else:
            flush()
            result.append(child)
    flush()
    return result


def unwrap_sections(body, created_ids):
    """Reverse only wrappers recorded by the caller, preserving manual sections."""
    result = []
    for child in deepcopy(body):
        if child["type"] == "section_master" and child["id"] in created_ids:
            result.extend(child["value"]["content"])
        else:
            result.append(child)
    return result
