from apscheduler.schedulers.blocking import BlockingScheduler

from networkapi.utility.delete_non_staff import delete_non_staff

scheduler = BlockingScheduler()

scheduler.add_job(delete_non_staff, 'interval', week=1)

scheduler.start()
