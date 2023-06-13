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
        "--all",
        "--keep-pot",
        "--no-wrap",
        "--ignore=network-api/networkapi/wagtailcustomization/*",
        "--ignore=network-api/networkapi/settings.py",
        "--ignore=network-api/networkapi/wagtailpages/templates/wagtailpages/pages/dear_internet_page.html",
        "--ignore=dockerpythonvenv/*",
    ]
)

locale_abstraction_instructions_js = " ".join(
    [
        "makemessages",
        "-d djangojs",
        "--all",
        "--keep-pot",
        "--no-wrap",
        "--ignore=node_modules",
        "--ignore=dockerpythonvenv/*",
        "--ignore=network-api",
        "--ignore=cypress",
    ]
)


def create_env_file(env_file):
    """Create or update an .env to work with a docker environment"""
    with open(env_file, "r") as f:
        env_vars = f.read()

    # We also need to make sure to use the correct db values based on our docker settings.
    username = dbname = "postgres"
    with open("docker-compose.yml", "r") as d:
        docker_compose = d.read()
        username = re.search("POSTGRES_USER=(.*)", docker_compose).group(1) or username
        dbname = re.search("POSTGRES_DB=(.*)", docker_compose).group(1) or dbname

    # Update the DATABASE_URL env
    new_db_url = f"DATABASE_URL=postgresql://{username}@postgres:5432/{dbname}"
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
def l10n_block_inventory(ctx, stop=False):
    """
    Update the block inventory.

    To stop the containers after the command has run, pass `stop=True`.

    """
    print("* Updating block information")
    manage(ctx, "block_inventory", stop=stop)


@task(aliases=["create-super-user"])
def createsuperuser(ctx, stop=False):
    """
    Create a superuser with username and password 'admin'.

    To stop the containers after the command is run, pass the `--stop` flag.
    """
    manage(ctx, "create_admin", stop=stop)


def initialize_database(ctx, slow=False):
    """
    Initialize the database.

    To stop all containers after each management command, pass `slow=True`.
    """
    print("* Applying database migrations.")
    migrate(ctx, stop=slow)

    print("* Creating fake data")
    manage(ctx, "load_fake_data", stop=slow)

    print("* Sync locales")
    manage(ctx, "sync_locale_trees", stop=slow)

    l10n_block_inventory(ctx, stop=slow)

    createsuperuser(ctx, stop=slow)


@task(aliases=["docker-new-db"])
def new_db(ctx, slow=False):
    """
    Delete your database and create a new one with fake data.

    If you are experiencing 'too many clients' errors while running this command, try
    to pass the `--slow` flag. This will make sure that the containers are stopped
    between the management commands and prevent that issue.

    """
    print("* Starting the postgres service")
    ctx.run("docker-compose up -d postgres")
    print("* Delete the database")
    ctx.run("docker-compose run --rm postgres dropdb --if-exists wagtail -hpostgres -Ufoundation")
    print("* Create the database")
    ctx.run("docker-compose run --rm postgres createdb wagtail -hpostgres -Ufoundation")
    initialize_database(ctx, slow=slow)
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
    print("\n* Start your dev server with:\n inv start or docker-compose up")


@task(aliases=["new-env", "docker-new-env"])
def setup(ctx):
    """Get a new dev environment and a new database with fake data"""
    with ctx.cd(ROOT):
        print("* Setting default environment variables")
        if os.path.isfile(".env"):
            print("* Stripping quotes and making sure your DATABASE_URL and ALLOWED_HOSTS are properly setup")
            create_env_file(".env")
        else:
            print("* Creating a new .env")
            create_env_file("env.default")
        print("* Stopping project's containers and delete volumes if necessary")
        ctx.run("docker-compose down --volumes")
        print("* Building Docker images")
        ctx.run("docker-compose build")
        initialize_database(ctx)
        print("\n* Start your dev server with:\n inv start or docker-compose up.")


@task(aliases=["start", "docker-start"])
def start_dev(ctx):
    """Start the dev server"""
    with ctx.cd(ROOT):
        ctx.run("docker-compose up")


@task(aliases=["start-lean", "docker-start-lean"])
def start_lean_dev(ctx):
    """Start the dev server without rebuilding frontend assets for a faster start up. \nWarning: this may use outdated frontend assets."""
    ctx.run("docker-compose -f docker-compose.yml -f docker-compose-lean.yml up")


# Javascript shorthands
@task(aliases=["docker-npm"])
def npm(ctx, command):
    """Shorthand to npm. inv docker-npm \"[COMMAND] [ARG]\" """
    with ctx.cd(ROOT):
        ctx.run(f"docker-compose run --rm backend npm {command}")


@task(aliases=["docker-npm-install"])
def npm_install(ctx):
    """Install Node dependencies"""
    with ctx.cd(ROOT):
        ctx.run("docker-compose run --rm backend npm ci")


@task(aliases=["copy-stage-db"])
def copy_staging_database(ctx):
    with ctx.cd(ROOT):
        ctx.run("node copy-db.js")


@task(aliases=["copy-prod-db"])
def copy_production_database(ctx):
    with ctx.cd(ROOT):
        ctx.run("node copy-db.js --prod")


# Python shorthands
@task
def pyrun(ctx, command, stop=False):
    """
    Shorthand to commands with the activated Python virutalenv.

    To stop the containers after the command has been run, pass the `--stop` flag.
    """
    with ctx.cd(ROOT):
        ctx.run(
            f'docker-compose run --rm backend bash -c "source ./dockerpythonvenv/bin/activate && {command}"',
            **PLATFORM_ARG,
        )
        if stop:
            ctx.run("docker-compose stop")


@task(aliases=["docker-manage"])
def manage(ctx, command, stop=False):
    """
    Shorthand to manage.py.

    inv docker-manage \"[COMMAND] [ARG]\"

    To stop the containers after the command has been run, pass the `--stop` flag.
    """
    command = f"python network-api/manage.py {command}"
    pyrun(ctx, command, stop=stop)


@task(aliases=["docker-djcheck"])
def djcheck(ctx, stop=False):
    """
    Django system check framework.

    To stop the containers after the command has run, pass the `--stop` flag.
    """
    print("Running system check framework...")
    manage(ctx, "check", stop=stop)


@task(aliases=["docker-migrate"])
def migrate(ctx, stop=False):
    """
    Update the database schema.

    To stop the containers after the command has run, pass the `--stop` flag.
    """
    manage(ctx, "migrate --no-input", stop=stop)


@task(aliases=["docker-makemigrations"])
def makemigrations(ctx, args=""):
    """
    Creates new migration(s) for apps. Optional: --args=""
    """
    manage(ctx, f"makemigrations {args}")


@task(aliases=["docker-makemigrations-dryrun"])
def makemigrations_dryrun(ctx, args=""):
    """
    Show new migration(s) for apps without creating them. Optional: --args=""
    """
    manage(ctx, f"makemigrations {args} --dry-run")


# Tests
@task(aliases=["docker-test"])
def test(ctx):
    """Run tests."""
    test_python(ctx)


@task(aliases=["docker-test-python"])
def test_python(ctx, file="", n="1", verbose=False):
    """
    Run python tests.

    Example calls:
    - test_python(ctx)
    - test_python(ctx, file="test_something.py")
    - test_python(ctx, n=4, verbose=True)

    Parameters:
    - ctx: Context object (provided by Invoke)
    - file: Optional string representing the path to a specific test file to run.
    - n: Optional integer or string 'auto' representing the number of parallel tests to run.
    Default is 'auto' which allows pytest to automatically determine the optimal number.
    - verbose: Optional boolean flag indicating whether to print verbose output during testing. Default is False.
    """

    djcheck(ctx)
    makemigrations_dryrun(ctx, args="--check")
    parallel = f"-n {n}" if n != "1" else ""
    v = "-v" if verbose else ""
    # Don't run coverage if a file is specified
    cov = "" if file else "--cov=network-api/networkapi --cov-report=term-missing"
    command = f"pytest {v} {parallel} {file} --reuse-db {cov}"
    pyrun(ctx, command)


# Linting
@task
def lint(ctx):
    """Run linting."""
    lint_html(ctx)
    lint_css(ctx)
    lint_js(ctx)
    lint_python(ctx)


@task
def lint_html(ctx):
    """Run HTML linting."""
    # Skipping djlint format checking because it has consistency issues and issues with blocktrans.
    # This should change when formatting is moved to a version using and AST.
    # See also: https://github.com/Riverside-Healthcare/djLint/issues/493
    # djlint_check(ctx)
    #
    # Use djhtml indent checking until format checking with djlint becomes possible.
    djhtml_check(ctx)
    djlint_lint(ctx)


@task
def lint_css(ctx):
    """Run CSS linting."""
    npm(ctx, "run lint:css")


@task
def lint_js(ctx):
    """Run JavaScript linting."""
    npm(ctx, "run lint:js")


@task
def lint_python(ctx):
    """Run Python linting."""
    flake8(ctx)
    isort_check(ctx)
    black_check(ctx)


# Formatting
@task
def format(ctx):
    """Run formatters."""
    format_html(ctx)
    format_css(ctx)
    format_js(ctx)
    format_python(ctx)


@task
def format_html(ctx):
    """Run HTML formatting."""
    # Skipping djlint formatting because it has consistency issues and issues with blocktrans.
    # This should change when formatting is moved to a version using and AST.
    # See also: https://github.com/Riverside-Healthcare/djLint/issues/493
    # djlint_format(ctx)
    #
    # Indent HTML until full formatting with djlint becomes possible
    djhtml_format(ctx)


@task
def format_css(ctx):
    """Run css formatting."""
    npm(ctx, "run fix:css")


@task
def format_js(ctx):
    """Run javascript formatting."""
    npm(ctx, "run fix:js")


@task
def format_python(ctx):
    """Run python formatting."""
    isort(ctx)
    black(ctx)


# Tooling
@task(help={"args": "Override the arguments passed to black."})
def black(ctx, args=None):
    """Run black code formatter."""
    args = args or "."
    pyrun(ctx, command=f"black {args}")


@task
def black_check(ctx):
    """Run black code formatter in check mode."""
    black(ctx, ". --check")


@task(help={"args": "Override the arguments passed to djhtml."})
def djhtml(ctx, args=None):
    """Run djhtml code indenter."""
    args = args or "-h"
    pyrun(ctx, command=f"djhtml {args}")


@task
def djhtml_check(ctx):
    """Run djhtml code indenter in check mode."""
    djhtml(ctx, args="-c maintenance/ network-api/")


@task
def djhtml_format(ctx):
    """Run djhtml code indenter in formatting mode."""
    djhtml(ctx, args="-i maintenance/ network-api/")


@task(help={"args": "Override the arguments passed to djlint."})
def djlint(ctx, args=None):
    """Run djlint code formatter and linter."""
    args = args or "."
    pyrun(ctx, command=f"djlint {args}")


@task
def djlint_check(ctx):
    """Run djlint in format checking mode."""
    djlint(ctx, ". --check")


@task
def djlint_format(ctx):
    """Run djlint formatting mode."""
    djlint(ctx, ". --reformat --quiet")


@task
def djlint_lint(ctx):
    """Run djlint in linting mode."""
    djlint(ctx, ". --lint")


@task
def flake8(ctx):
    """Run flake8."""
    pyrun(ctx, "flake8 .")


@task(help={"args": "Override the arguments passed to isort."})
def isort(ctx, args=None):
    """Run isort code formatter."""
    args = args or "."
    pyrun(ctx, command=f"isort {args}")


@task
def isort_check(ctx):
    """Run isort code formatter in check mode."""
    isort(ctx, ". --check-only")


@task(help={"args": "Override the arguments passed to mypy."})
def mypy(ctx, args=None):
    """Run mypy type checking on the project."""
    args = args or "network-api"
    pyrun(ctx, command=f"mypy {args}")


# Pip-tools
@task(aliases=["docker-pip-compile"])
def pip_compile(ctx, command):
    """Shorthand to pip-tools. inv pip-compile \"[COMMAND] [ARG]\" """
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


# Translation
@task(aliases=["docker-makemessages"])
def makemessages(ctx):
    """Extract all template messages in .po files for localization"""
    ctx.run("./translation-management.sh import")
    manage(ctx, locale_abstraction_instructions)
    manage(ctx, locale_abstraction_instructions_js)
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
