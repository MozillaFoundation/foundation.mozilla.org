import os
import re
import shutil
import subprocess
import tarfile
from pathlib import Path
from sys import platform

from invoke import exceptions, task

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
        "--extension js,jsx",
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
    with open(env_file) as f:
        env_vars = f.read()

    # We also need to make sure to use the correct db values based on our docker settings.
    username = dbname = "postgres"
    with open("docker-compose.yml") as d:
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
    # The docker image build will install node and python dependencies.
    ctx.run("docker-compose build")
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
    """Start the dev server without rebuilding frontend assets for a faster start up."""
    print("Starting the dev server without rebuilding frontend assets...")
    print("WARNING: Frontend assets may be outdated or missing if they haven't been built yet.")
    ctx.run("docker-compose -f docker-compose.yml -f docker-compose-lean.yml up")


@task
def sh(c, service="backend"):
    """
    Run bash in a local container
    """
    subprocess.run(["docker-compose", "exec", service, "bash"])


# Javascript shorthands
@task(aliases=["docker-npm"])
def npm(ctx, command):
    """Shorthand to npm. inv docker-npm \"[COMMAND] [ARG]\" """
    with ctx.cd(ROOT):
        # Tell user to use npm_install instead if command includes 'install' or 'ci'
        if "install" in command or "ci" in command:
            print("Please use 'inv npm-install' instead.")
            return

        ctx.run(f"docker-compose run --rm backend npm {command}")


@task(aliases=["docker-npm-exec"])
def npm_exec(ctx, command):
    """Run npm in running container, e.g for npm install."""
    with ctx.cd(ROOT):
        # Using 'exec' instead of 'run --rm' as /node_modules is not mounted.
        # To make this persistent, use 'exec' to run in the running container.
        try:
            ctx.run(f"docker-compose exec --user=root backend npm {command}")
        except exceptions.UnexpectedExit:
            print("This command requires a running container.\n")
            print("Please run 'inv start' or 'inv start-lean' in a separate terminal window first.")


@task(aliases=["docker-npm-install"])
def npm_install(ctx):
    """Install Node dependencies"""
    with ctx.cd(ROOT):
        npm_exec(ctx, "ci")


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
    djcheck(ctx)
    makemigrations_dryrun(ctx, args="--check")
    test_python(ctx)


@task(aliases=["docker-test-python"])
def test_python(ctx, file="", n="auto", verbose=False):
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
    djhtml(ctx, args="maintenance/ network-api/")


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
def _pip_compile_workaround(requirement_file, additional_commands=""):
    """
    A workaround to fix 'Device or resource busy' error when running
    pip-compile in docker container where the output file is a mounted volume.

    This is because pip-compile tries to replace the output file, and you can't replace
    mount points. However, you can write to them. So we work around this by using an
    unmounted .tmp file as intermediary, and then write the changes to the mounted file.
    """
    output_file = requirement_file.replace(".in", ".txt")
    temp_file = output_file + ".tmp"
    return (
        f"cp {output_file} {temp_file}&&pip-compile {requirement_file}"
        + " "
        + additional_commands
        + f" --output-file={temp_file}&&cp {temp_file} {output_file}&&rm {temp_file}"
    )


@task(aliases=["docker-pip-compile"], optional=["command"])
def pip_compile(ctx, filename="requirements.in", command=""):
    """Shorthand to pip-tools. inv pip-compile \"[filename]\" \"[COMMAND] [ARG]\" """
    with ctx.cd(ROOT):
        ctx.run(
            f"""docker-compose run --rm backend bash -c '{_pip_compile_workaround(filename, command)}'""",
            **PLATFORM_ARG,
        )


@task(aliases=["docker-pip-compile-lock"])
def pip_compile_lock(ctx):
    """Lock prod and dev dependencies"""
    with ctx.cd(ROOT):
        # Running in separate steps as the dev-requirements.in needs to read requirements.txt
        command = _pip_compile_workaround("requirements.in") + "&&"
        command = command + _pip_compile_workaround("dev-requirements.in")
        ctx.run(
            f"""docker-compose run --rm backend bash -c '{command}'""",
            **PLATFORM_ARG,
        )


@task(aliases=["docker-pip-sync"])
def pip_sync(ctx):
    """Sync your python virtualenv"""
    with ctx.cd(ROOT):
        try:
            ctx.run(
                # Using 'exec' instead of 'run --rm' as /dockerpythonvenv is not mounted.
                # To make this persistent, use 'exec' to run in the running container.
                "docker-compose exec backend ./dockerpythonvenv/bin/pip-sync requirements.txt dev-requirements.txt",
                **PLATFORM_ARG,
            )
        except exceptions.UnexpectedExit:
            print("This command requires a running container.\n")
            print("Please run 'inv start' or 'inv start-lean' in a separate terminal window first.")


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


@task(aliases=["staging-to-review-app"])
def staging_db_to_review_app(ctx, review_app_name):
    """
    Copy Staging DB to a specific Review App. inv staging-to-review-app \"[REVIEW_APP_NAME]\"
    """
    from copy_staging_db_to_review_app import main

    main(ctx, review_app_name)


@task(name="get-ffmpeg")
def compile_ffmpeg(ctx, output_dir="compiled-ffmpeg"):
    """
    Copy ffmpeg and ffprobe from a running dev container and archive it.
    If ../heroku-ffmpeg-static-builds exists, copy the tarball there too.
    Version is inferred from the built binary.
    Afterward, cleanup local copies of binaries and archive.
    """
    root = Path(__file__).resolve().parent
    output_path = root / output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    static_builds_dir = root.parent / "heroku-ffmpeg-static-builds"

    print("Copying ffmpeg and ffprobe from running dev container...")
    try:
        container_id = subprocess.check_output(["docker-compose", "ps", "-q", "backend"], text=True).strip()
        if not container_id:
            print("No running 'backend' container found. Please run 'inv start' first.")
            return
    except subprocess.CalledProcessError:
        print("Failed to find Docker container. Is Docker running?")
        return

    for binary in ("ffmpeg", "ffprobe"):
        subprocess.run(["docker", "cp", f"{container_id}:/usr/bin/{binary}", str(output_path / binary)], check=True)

    version_output = subprocess.check_output(
        ["docker", "exec", container_id, "/usr/bin/ffmpeg", "-version"], text=True
    )
    version = version_output.splitlines()[0].split()[2] if version_output else "unknown"
    print(f"Detected FFmpeg version: {version}")

    archive_path = output_path / f"ffmpeg-{version}-webp.tar.xz"
    print("Creating tarball...")
    with tarfile.open(archive_path, "w:xz") as tar:
        for binary in ("ffmpeg", "ffprobe"):
            tar.add(output_path / binary, arcname=binary)

    if static_builds_dir.exists():
        shutil.copy2(archive_path, static_builds_dir / archive_path.name)
        print(f"Copied tarball to: {static_builds_dir / archive_path.name}")
    else:
        print("Skipped copying: ../heroku-ffmpeg-static-builds does not exist.")
        print("Clone it from https://github.com/MozillaFoundation/heroku-ffmpeg-static-builds")

    print("Cleaning up local files...")
    for file in [output_path / "ffmpeg", output_path / "ffprobe", archive_path]:
        try:
            file.unlink()
            print(f"Deleted {file}")
        except FileNotFoundError:
            print(f"File already removed: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    print("Done.")
