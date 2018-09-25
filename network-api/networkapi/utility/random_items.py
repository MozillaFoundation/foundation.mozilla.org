from random import choices, randint


def get_random_items(model):
    items = model.objects.all()
    return choices(items, k=randint(0, len(items)))
