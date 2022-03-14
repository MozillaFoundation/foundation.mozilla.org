from itertools import chain, combinations
import factory
import random
from networkapi.wagtailpages.models import Homepage


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# Create a list of dictionaries containing every factory params permutation possible. ex: [{'group': True},
# {'group': True, 'active': True}, ...]
def generate_variations(factory_model):
    for variation in powerset(factory_model._meta.parameters.keys()):
        yield {k: True for k in variation}


# Create fake data for every permutation possible
def generate_fake_data(factory_model, count):
    for kwargs in generate_variations(factory_model):
        for i in range(count):
            factory_model.create(**kwargs)


# reseed the Faker RNG used by factory using seed
def reseed(seed):
    random.seed(seed)
    faker = factory.faker.Faker._get_faker(locale='en-US')
    faker.random.seed(seed)


# get a reference to the site's home page
def get_homepage(will_generate=False):
    try:
        return Homepage.objects.get(title='Homepage')
    except Homepage.DoesNotExist as ex:
        # In some cases, we will want to catch this exception and generate a homepage,
        # and in others we'll want to bail out on the load_fake_data task with an error.
        raise ex


def get_random_objects(model, max_count=5):
    """
    Return randnom objects up to a maximum number.

    The maximum is not guranteed to be reached. Rather at least one object of
    the given `model` is returned, but never more than `max_count`.

    Objects are not duplicated.

    """
    objects = list(model.objects.all())
    count = len(objects)

    random.shuffle(objects)

    available_max = min(count, max_count)
    random_max = random.randint(1, available_max)

    for i in range(0, random_max):
        yield objects[i]
