from sys import stdout

from invoke import task

# Workaround for homebrew installation of Python (https://bugs.python.org/issue22490)
import os
os.environ.pop('__PYVENV_LAUNCHER__', None)

ROOT = os.path.dirname(os.path.realpath(__file__))


@task
def manage(ctx, command):
    """Shorthand to manage.py"""
    with ctx.cd(ROOT):
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


@task(optional=['fakedata'], help={'fakedata': 'Generate fake data for testing and local development'})
def setup(ctx, fakedata=False):
    """Prepare your dev environment"""
    with ctx.cd(ROOT):
        stdout.write("Copying default environment variables.\n")
        ctx.run("cp env.default .env")
        stdout.write("Installing npm dependencies and build.\n")
        ctx.run("npm install && npm run build")
        stdout.write("Installing Python dependencies.\n")
        ctx.run("pipenv install")
        stdout.write("Applying database migrations.\n")
        ctx.run("inv migrate")
        stdout.write("Updating the site domain.\n")
        ctx.run("inv manage update_site_domain")
        if fakedata:
            stdout.write("Generating fake data.\n")
            ctx.run("inv manage load_fake_data")
        stdout.write("Creating superuser.\n")
        ctx.run("pipenv run python network-api/manage.py createsuperuser", pty=True)
        stdout.write("All done! To start your dev server, run the following:\n inv runserver\n")


@task
def update(ctx):
    """Update project's dependencies"""
    ctx.run("pipenv update")
