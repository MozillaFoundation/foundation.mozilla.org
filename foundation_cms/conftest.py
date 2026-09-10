import pytest
from django.utils import translation


@pytest.fixture(autouse=True)
def reset_active_language():
    """Reset the thread-local active language after every test."""
    # Tests call translation.activate() without ever undoing it, so the language
    # otherwise leaks into later tests sharing the worker process.
    yield
    translation.deactivate()
