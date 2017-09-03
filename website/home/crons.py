import os 
from time import gmtime, strftime

from django_cron import CronJobBase, Schedule

from .scripts import *

# Explanation: http://stackoverflow.com/questions/1432924/python-change-the-scripts-working-directory-to-the-scripts-own-directory

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except Exception as ex:
    print('os.chdir(os.path.dirname(sys.argv[0])) failed')        

# Explanation: http://stackoverflow.com/a/17649098
class RunCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.run_cron_job'  # a unique code

    def do(self):
        self.running_cron_job()


    def running_cron_job(self):
        print('Path at terminal when executing this file')
        print(os.getcwd() + '\n')
        print('Running scheduled cron task')

        f = open('history.txt', 'a+')
        f.write('Performing scheduled task on: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        f.write('\n')

        f.close()


class TaskReadMALShowsIndividual(CronJobBase):
    RUN_EVERY_MINS = 1 # 60 * 24 * 1 - 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # RUN_EVERY_MINS = 1200
    #
    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    code = 'home.task_read_MAL_shows_individual'

    def do(self):
        print('Running task to read individual show data')
        script_read_MAL_shows(write_individual_entry=True, write_aggregated_entry=False)
        # self.running_cron_job()

    def running_cron_job(self):
        f = open('history.txt', 'a+')
        f.write('Performing TaskReadMALShowsIndividual on: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        f.write('\n')

        f.close()


class TaskReadMALShowsAggregated(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7 - 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_read_MAL_shows_aggregated'

    def do(self):
        print('Running task to read aggregated show data')
        script_read_MAL_shows(write_individual_entry=False, write_aggregated_entry=True)
        # self.running_cron_job()

    def running_cron_job(self):
        f = open('history.txt', 'a+')
        f.write('Performing TaskReadMALShowsAggregated on: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        f.write('\n')

        f.close()


class TaskReadMALShowsMaster(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7 - 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_read_MAL_shows_master'

    def do(self):
        print('Running task to read aggregated and individual show data')
        script_read_MAL_shows(write_individual_entry=True, write_aggregated_entry=True)
        # self.running_cron_job()

    def running_cron_job(self):
        f = open('history.txt', 'a+')
        f.write('Performing TaskReadMALShowsMaster on: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        f.write('\n')

        f.close()


class TaskUpdateUserData(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7 - 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_read_update_user_data'

    def do(self):
        print('Running task to update user data')
        script_update_user_data(verbose=True,max_users=10000, start_point=0)
        # self.running_cron_job()

    def running_cron_job(self):
        f = open('history.txt', 'a+')
        f.write('Performing TaskUpdateUserData on: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        f.write('\n')

        f.close()


class TaskWriteBasicStats(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 1 - 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_write_extended_stats'

    def do(self):
        print('Running task to write extended stats')
        script_write_extended_stats(verbose=True, max_users=10000, max_shows=2000, item_rec=False)
        # self.running_cron_job()

    def running_cron_job(self):
        f = open('history.txt', 'a+')
        f.write('Performing TaskWriteBasicStats on: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        f.write('\n')

        f.close()


class TaskWriteExtendedStats(CronJobBase):
    RUN_EVERY_MINS = 1 #60 * 24 * 7 - 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.task_write_extended_stats'

    def do(self):
        print('Running task to write extended stats')
        script_write_extended_stats(verbose=True, max_users=10000, max_shows=500)
        # self.running_cron_job()

    def running_cron_job(self):
        f = open('history.txt', 'a+')
        f.write('Performing TaskWriteExtendedStats on: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        f.write('\n')

        f.close()

