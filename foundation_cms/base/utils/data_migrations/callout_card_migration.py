# foundation_cms/base/utils/callout_card_migration.py
from wagtail.blocks.migrations.operations import (
    RemoveStructChildrenOperation,
    RenameStreamChildrenOperation,
    RenameStructChildrenOperation,
)

CALLOUT_CARD_OPERATIONS_AND_BLOCK_PATHS = [
    (
        RenameStreamChildrenOperation(old_name="card", new_name="callout_card"),
        "timely_activations_cards.cards",
    ),
    (
        RenameStructChildrenOperation(old_name="category", new_name="headline"),
        "timely_activations_cards.cards.callout_card",
    ),
    (
        RenameStructChildrenOperation(old_name="title", new_name="subheading"),
        "timely_activations_cards.cards.callout_card",
    ),
    (
        RenameStructChildrenOperation(old_name="text", new_name="body"),
        "timely_activations_cards.cards.callout_card",
    ),
    (
        RemoveStructChildrenOperation(name="link"),
        "timely_activations_cards.cards.callout_card",
    ),
]
