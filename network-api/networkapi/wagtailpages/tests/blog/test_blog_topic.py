from django import test

from networkapi.wagtailpages.factory import blog as blog_factories
from networkapi.wagtailpages.pagemodels.blog import blog as blog_models


class TestBlogPageTopics(test.TestCase):
    def test_factory(self):
        blog_factories.BlogPageTopicFactory()

    def test_get_topics_method(self):
        # Clearing test instance of any existing topics
        blog_models.BlogPageTopic.objects.all().delete()

        test_topic = blog_factories.BlogPageTopicFactory(name="Test_Topic_1")
        blog_factories.BlogPageTopicFactory(name="Test_Topic_2")
        blog_factories.BlogPageTopicFactory(name="Test_Topic_3")

        # Creating a list of all created BlogPageTopics sorted by name,
        # with an additional option of "All".
        list_of_sorted_topics = [
            ("All", "All"),
            ("Test_Topic_1", "Test_Topic_1"),
            ("Test_Topic_2", "Test_Topic_2"),
            ("Test_Topic_3", "Test_Topic_3"),
        ]

        topic_choices_from_method = test_topic.get_topics()

        self.assertEqual(list_of_sorted_topics, topic_choices_from_method)
