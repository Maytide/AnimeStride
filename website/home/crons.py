from time import gmtime, strftime

from django_cron import CronJobBase, Schedule

from .scripts import script_read_MAL_shows


class RunCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.run_cron_job'  # a unique code

    def do(self):
        self.running_cron_job()


    def running_cron_job(self):
        print('Running scheduled cron task')

        f = open('history.txt', 'a+')
        f.write('Performing scheduled task on: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        f.write('\n')

        f.close()


class TaskReadMALShowsIndividual(CronJobBase):
    RUN_EVERY_MINS = 60*24

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # RUN_EVERY_MINS = 1200
    #
    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    code = 'home.task_read_MAL_shows_individual'

    def do(self):
        print('Running task to read invidual show data')
        script_read_MAL_shows(write_individual_entry=True, write_aggregated_entry=False)
