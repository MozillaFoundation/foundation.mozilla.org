from django.contrib.contenttypes.models import ContentType
from django.test import SimpleTestCase
from django.urls import reverse
from django.utils.html import format_html, mark_safe

from foundation_cms.legacy_apps.reports.templatetags import report_tags


class RenderContentTypeTagTests(SimpleTestCase):
    def test_render_content_type(self):
        content_type = ContentType(app_label="myapp", model="mymodel")
        expected_link = reverse(
            "wagtailadmin_pages:type_use",
            kwargs={
                "content_type_app_name": content_type.app_label,
                "content_type_model_name": content_type.model,
            },
        )
        expected_name = "Mymodel"

        result = report_tags.render_content_type(content_type)

        self.assertHTMLEqual(result, format_html("<a href='{}'>{}</a>", expected_link, expected_name))
        self.assertIsInstance(result, str)
        self.assertTrue(mark_safe(result))


class RenderContentTypesTagTests(SimpleTestCase):
    def test_render_list_of_content_types(self):
        content_types = [
            ContentType(app_label="myapp", model="mymodel1"),
            ContentType(app_label="myapp", model="mymodel2"),
            ContentType(app_label="myapp", model="mymodel3"),
        ]
        expected_link_1 = reverse(
            "wagtailadmin_pages:type_use",
            kwargs={
                "content_type_app_name": content_types[0].app_label,
                "content_type_model_name": content_types[0].model,
            },
        )
        expected_link_2 = reverse(
            "wagtailadmin_pages:type_use",
            kwargs={
                "content_type_app_name": content_types[1].app_label,
                "content_type_model_name": content_types[1].model,
            },
        )
        expected_link_3 = reverse(
            "wagtailadmin_pages:type_use",
            kwargs={
                "content_type_app_name": content_types[2].app_label,
                "content_type_model_name": content_types[2].model,
            },
        )

        expected_html = """
            <a href='{}'>{}</a>, <a href='{}'>{}</a>, <a href='{}'>{}</a>
        """.format(
            expected_link_1,
            "Mymodel1",
            expected_link_2,
            "Mymodel2",
            expected_link_3,
            "Mymodel3",
        )

        result = report_tags.render_content_types(content_types)

        self.assertHTMLEqual(result, expected_html)
        self.assertIsInstance(result, str)
        self.assertTrue(mark_safe(result))


class PageTypesBlockTagTests(SimpleTestCase):
    def test_page_types_block(self):
        content_types = [
            ContentType(app_label="myapp", model="mymodel1"),
            ContentType(app_label="myapp", model="mymodel2"),
            ContentType(app_label="myapp", model="mymodel3"),
            ContentType(app_label="myapp", model="mymodel4"),
        ]

        result = report_tags.page_types_block(content_types)

        self.assertIsInstance(result, dict)
        self.assertIn("content_types_shown", result)
        self.assertIn("content_types_hidden", result)
        self.assertIn("count_hidden", result)
        self.assertEqual(result["content_types_shown"], content_types[:3])
        self.assertEqual(result["content_types_hidden"], content_types[3:])
        self.assertEqual(result["count_hidden"], 1)


class BlockNameTagTests(SimpleTestCase):
    def test_block_name(self):
        page_block = {
            "block": "myapp.mymodel.MyBlock",
            "count": 1,
        }

        result = report_tags.block_name(page_block)

        self.assertIsInstance(result, dict)
        self.assertIn("full_name", result)
        self.assertIn("short_name", result)
        self.assertEqual(result["full_name"], "myapp.mymodel.MyBlock")
        self.assertEqual(result["short_name"], "MyBlock")
