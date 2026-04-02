from django.utils.text import slugify

from foundation_cms.base.models.abstract_base_page import Topic

TOPIC_NAMES = [
    "Artificial Intelligence",
    "Privacy",
    "Security",
    "Open Web",
    "Democracy",
    "Health",
    "Education",
    "Environment",
    "Human Rights",
    "Media",
]


def generate_topics():
    topics = []
    for name in TOPIC_NAMES:
        topic, _ = Topic.objects.get_or_create(
            slug=slugify(name),
            defaults={"name": name},
        )
        topics.append(topic)
    return topics
