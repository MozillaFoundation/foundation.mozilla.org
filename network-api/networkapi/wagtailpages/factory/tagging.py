from random import shuffle

tags = [
    'mozilla', 'iot', 'privacy', 'security', 'internet health',
    'digital inclusion', 'advocacy', 'policy']


def add_tags(post):
    shuffle(tags)

    for tag in tags[0:3]:
        post.tags.add(tag)
