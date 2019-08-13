import re
from sys import platform
from shutil import copy

from invoke import task

# Workaround for homebrew installation of Python (https://bugs.python.org/issue22490)
import os
os.environ.pop('__PYVENV_LAUNCHER__', None)

ROOT = os.path.dirname(os.path.realpath(__file__))

# Python commands's outputs are not rendering properly. Setting pty for *Nix system and
# "PYTHONUNBUFFERED" env var for Windows at True.
if platform == 'win32':
    PLATFORM_ARG = dict(env={'PYTHONUNBUFFERED': 'True'})
else:
    PLATFORM_ARG = dict(pty=True)

# The command for locale string abstraction is long and elaborate,
# so we build it here rather so that we don't clutter up the tasks.
locale_abstraction_instructions = " ".join([
    "makemessages",
    "-l de -l es -l fr -l pl -l pt",
    "--keep-pot",
    "--no-wrap",
    "--ignore=network-api/networkapi/wagtailcustomization/*",
    "--ignore=network-api/networkapi/wagtail_l10n_customization/*",
    "--ignore=network-api/networkapi/settings.py",
    "--ignore=network-api/networkapi/wagtailpages/__init__.py",
])


def create_docker_env_file(env_file):
    """Create a docker .env from an existing env file"""
    with open(env_file, 'r') as f:
        env_vars = f.read()
    # remove the double quote for docker-compose and python_dotenv compatibility reasons
    env_vars = env_vars.replace('"', '')
    # update the DATABASE_URL env
    new_db_url = "DATABASE_URL=postgres://postgres@postgres:5432/postgres"
    old_db_url = re.search('DATABASE_URL=.*', env_vars)
    env_vars = env_vars.replace(old_db_url.group(0), new_db_url)
    # update the ALLOWED_HOSTS
    new_hosts = "ALLOWED_HOSTS=*"
    old_hosts = re.search('ALLOWED_HOSTS=.*', env_vars)
    env_vars = env_vars.replace(old_hosts.group(0), new_hosts)

    # create the new env file
    with open('.docker.env', 'w') as f:
        f.write(env_vars)


# Tasks without Docker


@task(optional=['option', 'flag'])
def manage(ctx, command, option=None, flag=None):
    """Shorthand to manage.py. inv manage \"[COMMAND] [ARG]\". ex: inv manage \"runserver 3000\""""
    with ctx.cd(ROOT):
        ctx.run(f"pipenv run python network-api/manage.py {command}", **PLATFORM_ARG)


@task
def runserver(ctx):
    """Start a web server"""
    manage(ctx, "runserver 0.0.0.0:8000")


@task
def migrate(ctx):
    """Updates database schema"""
    manage(ctx, "migrate", flag="noinput")


@task
def makemigrations(ctx):
    """Creates new migration(s) for apps"""
    manage(ctx, "makemigrations")


@task
def l10n_sync(ctx):
    """Sync localizable fields in the database"""
    manage(ctx, "sync_page_translation_fields")


@task
def l10n_update(ctx):
    """Update localizable field data (copies from
    original unlocalized to default localized field)"""
    manage(ctx, "update_translation_fields")


@task
def makemessages(ctx):
    """Compile all template messages for localization"""
    manage(ctx, locale_abstraction_instructions)
    os.rename("network-api/locale/django.pot", "network-api/locale/templates/LC_MESSAGES/django.pot")


@task
def test(ctx):
    """Run tests"""
    print("Running flake8")
    ctx.run(f"pipenv run flake8 tasks.py network-api", **PLATFORM_ARG)
    print("Running tests")
    manage(ctx, "test")


@task
def setup(ctx):
    """Prepare your dev environment after a fresh git clone"""
    with ctx.cd(ROOT):
        print("Setting default environment variables.")
        if os.path.isfile(".env"):
            print("Keeping your existing .env")
        else:
            print("Creating a new .env")
            copy("env.default", ".env")
        print("Installing npm dependencies and build.")
        ctx.run("npm install && npm run build")
        print("Installing Python dependencies.")
        ctx.run("pipenv install --dev")
        print("Applying database migrations.")
        migrate(ctx)
        print("Updating localizable fields")
        l10n_sync(ctx)
        l10n_update(ctx)
        print("Creating fake data")
        manage(ctx, "load_fake_data")
        print("Updating block information")
        manage(ctx, "block_inventory")

        # Windows doesn't support pty, skipping this step
        if platform == 'win32':
            print("All done!\n"
                  "To create an admin user: pipenv run python network-api/manage.py createsuperuser\n"
                  "To start your dev server: inv runserver")
        else:
            print("Creating superuser.")
            ctx.run("pipenv run python network-api/manage.py createsuperuser", pty=True)
            print("All done! To start your dev server, run the following:\n inv runserver")


@task(aliases=["catchup"])
def catch_up(ctx):
    """Install dependencies and apply migrations"""
    print("Installing npm dependencies and build.")
    ctx.run("npm install && npm run build")
    print("Installing Python dependencies.")
    ctx.run("pipenv install --dev")
    print("Applying database migrations.")
    migrate(ctx)
    print("Updating localizable fields")
    l10n_sync(ctx)
    l10n_update(ctx)
    print("Updating block information")
    manage(ctx, "block_inventory")


# Tasks with Docker


@task
def docker_manage(ctx, command):
    """Shorthand to manage.py. inv docker.manage \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(f"docker-compose run --rm backend pipenv run python network-api/manage.py {command}", **PLATFORM_ARG)


@task
def docker_pipenv(ctx, command):
    """Shorthand to pipenv. inv docker.pipenv \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(f"docker-compose run --rm backend pipenv {command}")


@task
def docker_npm(ctx, command):
    """Shorthand to npm. inv docker.npm \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(f"docker-compose run --rm watch-static-files npm {command}")


@task
def docker_migrate(ctx):
    """Updates database schema"""
    docker_manage(ctx, "migrate --no-input")


@task
def docker_makemigrations(ctx):
    """Creates new migration(s) for apps"""
    docker_manage(ctx, "makemigrations")


@task
def docker_l10n_sync(ctx):
    """Sync localizable fields in the database"""
    docker_manage(ctx, "sync_page_translation_fields")


@task
def docker_l10n_update(ctx):
    """Update localizable field data (copies from original unlocalized to default localized field)"""
    docker_manage(ctx, "update_translation_fields")

@task
def docker_makemessages(ctx):
    """Compile all template messages for localization"""
    docker_manage(ctx, locale_abstraction_instructions)


@task
def docker_test_python(ctx):
    """Run python tests"""
    print("Running flake8")
    ctx.run("docker-compose run --rm backend pipenv run flake8 tasks.py network-api", **PLATFORM_ARG)
    print("Running tests")
    docker_manage(ctx, "test")


@task
def docker_test_node(ctx):
    """Run node tests"""
    print("Running tests")
    ctx.run("docker-compose run --rm watch-static-files npm run test", **PLATFORM_ARG)


@task
def docker_switching_branch(ctx):
    """Get a new database with fake data and rebuild images"""
    print("Stopping services first")
    ctx.run("docker-compose down")
    print("Deleting database")
    ctx.run("docker volume rm foundationmozillaorg_postgres_data")
    print("Rebuilding images and install dependencies")
    ctx.run("docker-compose build")
    print("Applying database migrations.")
    docker_migrate(ctx)
    print("Creating fake data")
    docker_manage(ctx, "load_fake_data")
    print("Updating localizable fields")
    docker_l10n_sync(ctx)
    docker_l10n_update(ctx)
    print("Updating block information")
    docker_manage(ctx, "block_inventory")


@task
def docker_new_db(ctx):
    """Delete your database and create a new one with fake data"""
    print("Stopping services first")
    ctx.run("docker-compose down")
    print("Deleting database")
    ctx.run("docker volume rm foundationmozillaorg_postgres_data")
    print("Applying database migrations.")
    docker_migrate(ctx)
    print("Creating fake data")
    docker_manage(ctx, "load_fake_data")
    print("Updating localizable fields")
    docker_l10n_sync(ctx)
    docker_l10n_update(ctx)
    print("Updating block information")
    docker_manage(ctx, "block_inventory")


@task(aliases=["docker-catchup"])
def docker_catch_up(ctx):
    """Rebuild images and apply migrations"""
    print("Stopping services first")
    ctx.run("docker-compose down")
    print("Rebuilding images and install dependencies")
    ctx.run("docker-compose build")
    print("Applying database migrations.")
    docker_migrate(ctx)
    print("Updating localizable fields")
    docker_l10n_sync(ctx)
    docker_l10n_update(ctx)
    print("Updating block information")
    docker_manage(ctx, "block_inventory")


@task
def docker_setup(ctx):
    """Prepare your dev environment after a fresh git clone"""
    with ctx.cd(ROOT):
        print("Setting default environment variables.")
        if os.path.isfile(".env"):
            print("Copying your existing .env to .docker.env")
            create_docker_env_file(".env")
        else:
            if os.path.isfile('.docker.env'):
                print("Keeping your existing .docker.env.")
            else:
                print("Creating a new .docker.env")
                create_docker_env_file("env.default")
        print("Building Docker images")
        ctx.run("docker-compose build", **PLATFORM_ARG)
        print("Applying database migrations.")
        docker_migrate(ctx)
        print("Updating localizable fields")
        docker_l10n_sync(ctx)
        docker_l10n_update(ctx)
        print("Creating fake data")
        docker_manage(ctx, "load_fake_data")
        print("Updating block information")
        docker_manage(ctx, "block_inventory")

        # Windows doesn't support pty, skipping this step
        if platform == 'win32':
            print("All done!\n"
                  "To create an admin user:\n"
                  "docker-compose run --rm backend pipenv run python network-api/manage.py createsuperuser\n"
                  "To start your dev server:\n"
                  "docker-compose up")
        else:
            print("Creating superuser.")
            ctx.run(
                "docker-compose run --rm backend pipenv run python network-api/manage.py createsuperuser",
                pty=True
            )
            print("All done! To start your dev server, run the following:\n docker-compose up")
