from apscheduler.schedulers.blocking import BlockingScheduler
import os

from networkapi.utility.delete_non_staff import find_and_delete

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "networkapi.settings")

scheduler = BlockingScheduler()

scheduler.add_job(find_and_delete, 'cron', day_of_week='sun', hour=2, timezone='US/Eastern')

scheduler.start()
