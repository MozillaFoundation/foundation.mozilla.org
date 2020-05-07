#!/usr/bin/env python
import os
import sys

# Django runs twice to support live-reloading, so check Django's internal settings to determine whether or not
# to start the debugger.
if (os.environ.get("RUN_MAIN") or os.environ.get("WERKZEUG_RUN_MAIN")) and os.environ.get('VSCODE_DEBUGGER', False):
    import ptvsd # noqa
    ptvsd_port = 8001

    try:
        ptvsd.enable_attach(address=("0.0.0.0", ptvsd_port))
        print(f"Started ptvsd server at port {ptvsd_port}")
    except OSError:
        print(f"ptvsd port {ptvsd_port} already in use")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "networkapi.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa: F401
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
