from typing import Any, Generator


def find_key_values(d: Any, key: Any) -> Generator[Any, None, None]:
    # Can only check for keys in dictionaries
    if hasattr(d, "items"):
        for k, v in d.items():
            # First, let's check if this is the key we are looking for
            if k == key:
                yield v
            # Check if the value is a dictionary
            if isinstance(v, dict):
                # Repeat the process for the dictionary
                for result in find_key_values(v, key):
                    yield result
            # Check if the value is a list
            elif isinstance(v, list):
                # Repeat the process for each of the items in the list
                for item in v:
                    for result in find_key_values(item, key):
                        yield result
