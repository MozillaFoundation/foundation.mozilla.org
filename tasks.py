import os
import re
from sys import platform

from invoke import task

ROOT = os.path.dirname(os.path.realpath(__file__))
LOCALE_DIR = os.path.realpath(os.path.abspath("network-api/locale"))

# Python commands's outputs are not rendering properly. Setting pty for *Nix system and
# "PYTHONUNBUFFERED" env var for Windows at True.
if platform == "win32":
    PLATFORM_ARG = dict(env={"PYTHONUNBUFFERED": "True"})
else:
    PLATFORM_ARG = dict(pty=True)

# The command for locale string abstraction is long and elaborate,
# so we build it here rather so that we don't clutter up the tasks.
locale_abstraction_instructions = " ".join(
    [
        "makemessages",
        "--keep-pot",
        "--no-wrap",
        "--ignore=network-api/networkapi/wagtailcustomization/*",
        "--ignore=network-api/networkapi/wagtail_l10n_customization/*",
        "--ignore=network-api/networkapi/settings.py",
        "--ignore=network-api/networkapi/wagtailpages/__init__.py",
        "--ignore=dockerpythonvenv/*",
    ]
)


def create_env_file(env_file):
    """Create or update an .env to work with a docker environment"""
    with open(env_file, "r") as f:
        env_vars = f.read()

    # We need to strip the quotes because Docker-compose considers them as part of the env value.
    env_vars = env_vars.replace('"', "")

    # We also need to make sure to use the correct db values based on our docker settings.
    username = dbname = "postgres"
    with open("docker-compose.yml", "r") as d:
        docker_compose = d.read()
        username = re.search("POSTGRES_USER=(.*)", docker_compose).group(1) or username
        dbname = re.search("POSTGRES_DB=(.*)", docker_compose).group(1) or dbname

    # Update the DATABASE_URL env
    new_db_url = (
        f"DATABASE_URL=postgresql://{username}@postgres:5432/{dbname}"
    )
    old_db_url = re.search("DATABASE_URL=.*", env_vars)
    env_vars = env_vars.replace(old_db_url.group(0), new_db_url)

    # update the ALLOWED_HOSTS
    new_hosts = "ALLOWED_HOSTS=*"
    old_hosts = re.search("ALLOWED_HOSTS=.*", env_vars)
    env_vars = env_vars.replace(old_hosts.group(0), new_hosts)

    # create the new env file
    with open(".env", "w") as f:
        f.write(env_vars)


# Project setup and update
def l10n_block_inventory(ctx):
    print("* Updating localizable fields")
    l10n_sync(ctx)
    l10n_update(ctx)
    print("* Updating block information")
    manage(ctx, "block_inventory")


def create_super_user(ctx):
    preamble = "from django.contrib.auth.models import User;"
    create = "User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
    manage(ctx, f'shell -c "{preamble} {create}"')
    print("\nCreated superuser `admin` with password `admin`.")


@task(aliases=["docker-new-db"])
def new_db(ctx):
    """Delete your database and create a new one with fake data"""
    print("* Starting the postgres service")
    ctx.run("docker-compose up -d postgres")
    print("* Delete the database")
    ctx.run("docker-compose run --rm postgres dropdb --if-exists wagtail -h postgres -U foundation")
    print("* Create the database")
    ctx.run("docker-compose run --rm postgres createdb wagtail -h postgres -U foundation")
    print("* Applying database migrations.")
    migrate(ctx)
    print("* Creating fake data")
    manage(ctx, "load_fake_data")
    l10n_block_inventory(ctx)
    create_super_user(ctx)
    print("Stop postgres service")
    ctx.run("docker-compose down")


@task(aliases=["docker-catchup", "catchup"])
def catch_up(ctx):
    """Rebuild images, install dependencies, and apply migrations"""
    print("* Stopping services first")
    ctx.run("docker-compose down")
    print("* Rebuilding images and install dependencies")
    ctx.run("docker-compose build")
    print("* Install Node dependencies")
    npm_install(ctx)
    print("* Sync Python dependencies")
    pip_sync(ctx)
    print("* Applying database migrations.")
    migrate(ctx)
    print("* Updating block information.")
    l10n_block_inventory(ctx)
    print("\n* Start your dev server with:\n docker-compose up")


@task(aliases=["new-env", "docker-new-env"])
def setup(ctx):
    """Get a new dev environment and a new database with fake data"""
    with ctx.cd(ROOT):
        print("* Setting default environment variables")
        if os.path.isfile(".env"):
            print(
                "* Stripping quotes and making sure your DATABASE_URL and ALLOWED_HOSTS are properly setup"
            )
            create_env_file(".env")
        else:
            print("* Creating a new .env")
            create_env_file("env.default")
        print("* Stopping project's containers and delete volumes if necessary")
        ctx.run("docker-compose down --volumes")
        print("* Building Docker images")
        ctx.run("docker-compose build")
        print("* Install Node dependencies")
        npm_install(ctx)
        print("* Creating a Python virtualenv")
        ctx.run(
            "docker-compose run --rm backend python -m venv dockerpythonvenv",
            **PLATFORM_ARG,
        )
        print("Done!")
        print("* Updating pip")
        ctx.run(
            "docker-compose run --rm backend ./dockerpythonvenv/bin/pip install -U pip==20.0.2",
            **PLATFORM_ARG,
        )
        print("* Installing pip-tools")
        ctx.run(
            "docker-compose run --rm backend ./dockerpythonvenv/bin/pip install pip-tools",
            **PLATFORM_ARG,
        )
        print("* Sync Python dependencies")
        pip_sync(ctx)
        print("* Applying database migrations.")
        migrate(ctx)
        print("* Creating fake data.")
        manage(ctx, "load_fake_data")
        print("* Updating block information.")
        l10n_block_inventory(ctx)
        create_super_user(ctx)

        print("\n* Start your dev server with:\n docker-compose up")


# Javascript shorthands
@task(aliases=["docker-npm"])
def npm(ctx, command):
    """Shorthand to npm. inv docker-npm \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(f"docker-compose run --rm watch-static-files npm {command}")


@task(aliases=["docker-npm-install"])
def npm_install(ctx):
    """Install Node dependencies"""
    with ctx.cd(ROOT):
        ctx.run("docker-compose run --rm watch-static-files npm install")


# Django shorthands
@task(aliases=["docker-manage"])
def manage(ctx, command):
    """Shorthand to manage.py. inv docker-manage \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(
            f"docker-compose run --rm backend ./dockerpythonvenv/bin/python network-api/manage.py {command}",
            **PLATFORM_ARG,
        )


@task(aliases=["docker-migrate"])
def migrate(ctx):
    """Updates database schema"""
    manage(ctx, "migrate --no-input")


@task(aliases=["docker-makemigrations"])
def makemigrations(ctx):
    """Creates new migration(s) for apps"""
    manage(ctx, "makemigrations")


# Tests
@task(aliases=["docker-test"])
def test(ctx):
    """Run both Node and Python tests"""
    test_node(ctx)
    test_python(ctx)


@task(aliases=["docker-test-python"])
def test_python(ctx):
    """Run python tests"""
    print("* Running flake8")
    ctx.run(
        "docker-compose run --rm backend ./dockerpythonvenv/bin/python -m flake8 tasks.py network-api",
        **PLATFORM_ARG,
    )
    print("* Running tests")
    manage(ctx, "test")


@task(aliases=["docker-test-node"])
def test_node(ctx):
    """Run node tests"""
    print("* Running tests")
    ctx.run("docker-compose run --rm watch-static-files npm run test")


# Localisation
@task(aliases=["docker-l10n-sync"])
def l10n_sync(ctx):
    """Sync localizable fields in the database"""
    manage(ctx, "sync_page_translation_fields")


@task(aliases=["docker-l10n-update"])
def l10n_update(ctx):
    """Update localizable field data (copies from original unlocalized to default localized field)"""
    manage(ctx, "update_translation_fields")


@task(aliases=["docker-makemessages"])
def makemessages(ctx):
    """Extract all template messages in .po files for localization"""
    ctx.run("./translation-management.sh import")
    manage(ctx, locale_abstraction_instructions)
    ctx.run("./translation-management.sh export")


@task(aliases=["docker-compilemessages"])
def compilemessages(ctx):
    """Compile the latest translations"""
    with ctx.cd(ROOT):
        ctx.run(
            "docker-compose run --rm -w /app/network-api backend "
            "../dockerpythonvenv/bin/python manage.py compilemessages",
            **PLATFORM_ARG,
        )


# Pip-tools
@task(aliases=["docker-pip-compile"])
def pip_compile(ctx, command):
    """Shorthand to pip-tools. inv pip-compile \"[COMMAND] [ARG]\""""
    with ctx.cd(ROOT):
        ctx.run(
            f"docker-compose run --rm backend ./dockerpythonvenv/bin/pip-compile {command}",
            **PLATFORM_ARG,
        )


@task(aliases=["docker-pip-compile-lock"])
def pip_compile_lock(ctx):
    """Lock prod and dev dependencies"""
    with ctx.cd(ROOT):
        ctx.run(
            "docker-compose run --rm backend ./dockerpythonvenv/bin/pip-compile",
            **PLATFORM_ARG,
        )
        ctx.run(
            "docker-compose run --rm backend ./dockerpythonvenv/bin/pip-compile dev-requirements.in",
            **PLATFORM_ARG,
        )


@task(aliases=["docker-pip-sync"])
def pip_sync(ctx):
    """Sync your python virtualenv"""
    with ctx.cd(ROOT):
        ctx.run(
            "docker-compose run --rm backend ./dockerpythonvenv/bin/pip-sync requirements.txt dev-requirements.txt",
            **PLATFORM_ARG,
        )
