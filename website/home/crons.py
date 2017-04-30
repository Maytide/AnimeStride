from time import gmtime, strftime

from django_cron import CronJobBase, Schedule

from .scripts import *


# Explanation: http://stackoverflow.com/a/17649098
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
        print('Running task to read individual show data')
        script_read_MAL_shows(write_individual_entry=True, write_aggregated_entry=False)


class TaskReadMALShowsAggregated(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_read_MAL_shows_aggregated'

    def do(self):
        print('Running task to read aggregated show data')
        script_read_MAL_shows(write_individual_entry=False, write_aggregated_entry=True)


class TaskReadMALShowsMaster(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_read_MAL_shows_master'

    def do(self):
        print('Running task to read aggregated and individual show data')
        script_read_MAL_shows(write_individual_entry=True, write_aggregated_entry=True)


class TaskUpdateUserData(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_read_update_user_data'

    def do(self):
        print('Running task to update user data')
        script_update_user_data(verbose=True,max_users=10000, start_point=0)


class TaskWriteExtendedStats(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_write_extended_stats'

    def do(self):
        print('Running task to write extended stats')
        script_write_extended_stats(verbose=True, max_users=10000, max_shows=500)

