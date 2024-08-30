import random
from datetime import datetime, timedelta, timezone
from itertools import chain, combinations
from typing import Union

import factory
from django.db import models

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
    faker = get_faker()
    faker.random.seed(seed)


def get_faker():
    return factory.faker.Faker._get_faker(locale="en-US")


# get a reference to the site's home page
def get_homepage(will_generate=False):
    try:
        return Homepage.objects.get(title="Homepage")
    except Homepage.DoesNotExist as ex:
        # In some cases, we will want to catch this exception and generate a homepage,
        # and in others we'll want to bail out on the load_fake_data task with an error.
        raise ex


def get_random_objects(
    source: Union[models.Model, models.QuerySet],
    max_count: int = 0,
    exact_count: int = 0,
) -> models.QuerySet:
    """
    Return queryset of random objects.

    Provide a model or queryset as the `source` from which the random objects will
    be taken.

    Specifying `exact_count` takes precedent over `max_count`.

    When you define `exact_count` this is the number of random objects returned.

    When you define `max_count` a random number of objects in the range from 1 to
    `max_count` is returned.

    When neither is specified, all available objects are returned.

    In either case, when there are not enough objects, all objects are returned in
    random order.

    Objects are not duplicated.

    """
    if not isinstance(source, models.QuerySet):
        queryset = source.objects.all()
    else:
        queryset = source
    primary_keys = list(queryset.values_list("pk", flat=True))
    random.shuffle(primary_keys)

    count = len(primary_keys)
    if not count:
        # No items available, return empty queryset.
        return queryset.none()

    if exact_count:
        return_max = min(count, exact_count)
    elif max_count:
        available_max = min(count, max_count)
        return_max = random.randint(1, available_max)
    else:
        return_max = count

    primary_keys_slice = primary_keys[:return_max]
    return queryset.filter(pk__in=primary_keys_slice)


def get_random_date():
    base = datetime(2024, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    random_date = base - timedelta(
        days=random.randint(0, 365 * 3),
        hours=random.randint(0, 24),
        minutes=random.randint(0, 60),
        seconds=random.randint(0, 60),
    )

    return random_date
