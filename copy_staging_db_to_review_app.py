import tempfile
from time import sleep

from tasks import PLATFORM_ARG

STAGING_APP = "foundation-mofostaging-net"


def execute_command(ctx, command: str, custom_error: str = ""):
    try:
        result = ctx.run(command, hide=False, warn=True, **PLATFORM_ARG)
        if result.failed:
            raise Exception(f"{custom_error}: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        raise Exception(f"{custom_error}: {e}") from e


def log_step(message: str):
    print(f"--> {message}\n", flush=True)


def log_step_completed(message: str):
    print(f"✔️  {message} completed.\n", flush=True)


def replace_placeholders_in_sql(review_app_name: str, input_file: str) -> str:
    with open(input_file, "r") as file:
        sql_content = file.read()

    sql_content = sql_content.replace("{DOMAIN}", review_app_name)
    sql_content = sql_content.replace("{HOSTNAME}", review_app_name)

    return sql_content


def main(ctx, review_app_name):
    log_step(f"The review app name is: {review_app_name}, if not, please cancel now...")
    sleep(5)

    log_step("Verifying if logged in Heroku")
    heroku_user = execute_command(ctx, "heroku whoami", "Verify that you are logged in Heroku CLI")
    print(f"Heroku user: {heroku_user}\n", flush=True)
    log_step_completed("Heroku login verification")

    log_step("Verifying if psql is installed")
    execute_command(ctx, "psql --version", "Verify that you have 'psql' installed")
    log_step_completed("psql installation verification")

    try:
        log_step("Enabling maintenance mode on the Review App")
        execute_command(ctx, f"heroku maintenance:on -a {review_app_name}")
        log_step_completed("Maintenance mode enabling")

        log_step("Scaling web dynos on Review App to 0")
        execute_command(ctx, f"heroku ps:scale -a {review_app_name} web=0")
        log_step_completed("Web dynos scaling to 0")

        log_step("Backing up Staging DB")
        execute_command(ctx, f"heroku pg:backups:capture -a {STAGING_APP}")
        log_step_completed("Staging DB backup")

        log_step("Backing up Review App DB")
        execute_command(ctx, f"heroku pg:backups:capture -a {review_app_name}")
        log_step_completed("Review App DB backup")

        log_step("Reset Review App DB")
        execute_command(ctx, f"heroku pg:reset -a '{review_app_name}' --confirm '{review_app_name}'")
        log_step_completed("Review App DB has been reset")

        log_step("Restoring the latest Staging backup to Review App")
        backup_staging_url = execute_command(ctx, f"heroku pg:backups:url -a {STAGING_APP}")
        execute_command(
            ctx, f"heroku pg:backups:restore --confirm {review_app_name} -a {review_app_name} '{backup_staging_url}'"
        )
        log_step_completed("Staging backup restoration to Review App")

        log_step("Executing cleanup SQL script")
        review_app_db_url = execute_command(ctx, f"heroku config:get -a {review_app_name} DATABASE_URL")

        # Replace placeholders and write to a temporary file
        sql_content = replace_placeholders_in_sql(review_app_name, "./cleanup.sql")
        with tempfile.NamedTemporaryFile(suffix=".sql", mode="w", delete=True) as temp_sql_file:
            temp_sql_file.write(sql_content)
            temp_sql_file.flush()
            execute_command(ctx, f"psql {review_app_db_url} -f {temp_sql_file.name}")

        log_step_completed("Cleanup SQL script execution")

        log_step("Running migrations")
        execute_command(ctx, f"heroku run -a {review_app_name} -- python ./manage.py migrate --no-input")
        log_step_completed("Migrations running")

    except Exception as e:
        log_step("Rolling back Review App")
        execute_command(ctx, f"heroku pg:backups:restore -a {review_app_name} --confirm {review_app_name}")
        print(e, flush=True)
        log_step_completed("Review App rollback")

    finally:
        log_step("Scaling web dynos on Review App to 1")
        execute_command(ctx, f"heroku ps:scale -a {review_app_name} web=1")
        log_step_completed("Web dynos scaling to 1")

        log_step("Disabling maintenance mode on Review App")
        execute_command(ctx, f"heroku maintenance:off -a {review_app_name}")
        log_step_completed("Maintenance mode disabling")
