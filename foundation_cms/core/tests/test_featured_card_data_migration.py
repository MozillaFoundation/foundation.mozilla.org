from importlib import import_module
from unittest.mock import Mock

from django.test import SimpleTestCase

migration = import_module("foundation_cms.core.migrations.0093_strip_featured_card_blocks")


def page_model_with(rows):
    model = Mock()
    model.objects.all.return_value.iterator.return_value = iter(rows)
    return model


class FeaturedCardDataMigrationTests(SimpleTestCase):
    def test_removes_block_from_page_and_revision_preserving_other_blocks(self):
        before = {"type": "rich_text", "value": "<p>Keep this.</p>", "id": "before"}
        featured = {
            "type": "featured_card_block",
            "value": {"heading": "Remove this"},
            "id": "featured",
        }
        after = {"type": "quote", "value": {"quote": "Keep this too."}, "id": "after"}
        expected_body = [before, after]

        page = Mock()
        page.body = [before, featured, after]

        revision = Mock()
        revision.content = {"body": [before, featured, after]}

        empty_model = page_model_with([])
        revision_model = Mock()
        revision_model.objects.filter.return_value.iterator.return_value = iter([revision])

        content_type_queryset = Mock()
        content_type_queryset.values_list.return_value = [1]
        content_type_model = Mock()
        content_type_model.objects.filter.return_value = content_type_queryset

        models = {
            ("core", "GeneralPage"): page_model_with([page]),
            ("wagtailcore", "Revision"): revision_model,
            ("contenttypes", "ContentType"): content_type_model,
        }

        historical_apps = Mock()
        historical_apps.get_model.side_effect = lambda app, model: models.get((app, model), empty_model)

        migration.strip_featured_card_blocks(historical_apps, schema_editor=None)

        self.assertEqual(page.body, expected_body)
        page.save.assert_called_once_with(update_fields=["body"])

        self.assertEqual(revision.content["body"], expected_body)
        revision.save.assert_called_once_with(update_fields=["content"])
