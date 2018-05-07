from sys import platform
from shutil import copy

from invoke import task

# Workaround for homebrew installation of Python (https://bugs.python.org/issue22490)
import os
os.environ.pop('__PYVENV_LAUNCHER__', None)

ROOT = os.path.dirname(os.path.realpath(__file__))


@task(optional=['option', 'flag'])
def manage(ctx, command, option=None, flag=None):
    """Shorthand to manage.py"""
    with ctx.cd(ROOT):
        if option:
            ctx.run(f"pipenv run python network-api/manage.py {command} {option}")
        elif flag:
            ctx.run(f"pipenv run python network-api/manage.py {command} --{flag}")
        else:
            ctx.run(f"pipenv run python network-api/manage.py {command}")


@task
def runserver(ctx):
    """Start a web server"""
    manage(ctx, "runserver")


@task
def migrate(ctx):
    """Updates database schema"""
    manage(ctx, "migrate")


@task
def makemigrations(ctx):
    """Creates new migration(s) for apps"""
    manage(ctx, "makemigrations")


@task
def test(ctx):
    """Run tests"""
    manage(ctx, "test")


@task
def setup(ctx):
    """Prepare your dev environment after a fresh git clone"""
    with ctx.cd(ROOT):
        print("Copying default environment variables.")
        copy("env.default", ".env")
        print("Installing npm dependencies and build.")
        ctx.run("npm install && npm run build")
        print("Installing Python dependencies.")
        ctx.run("pipenv install --dev")
        print("Applying database migrations.")
        ctx.run("inv migrate")
        print("Updating the site domain.")
        ctx.run("inv manage update_site_domain")
        print("Creating superuser.")
        # Windows doesn't support pty, skipping this step
        if platform == 'win32':
            print("All done!\n"
                  "To create an admin user: pipenv run python network-api/manage.py createsuperuser\n"
                  "To start your dev server: inv runserver")
        else:
            ctx.run("pipenv run python network-api/manage.py createsuperuser", pty=True)
            print("All done! To start your dev server, run the following:\n inv runserver")
