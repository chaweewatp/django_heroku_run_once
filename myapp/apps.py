
## solution 1 --notwork
# from django.apps import AppConfig
# class MyappConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'myapp'
#     run_already = False

#     def ready(self):
#         if MyappConfig.run_already: 
#             print('not run already')
#             return
#         MyappConfig.run_already = True
#         print("Hello")


# # solution 2 -- work on local but not on heroku
# from django.apps import AppConfig
# import os

# class CommandLineRunner(AppConfig):
#     name = 'myapp'

#     def ready(self):
#         run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE') 
#         if run_once is 'False':
#             print('not run first time')
#             return
#         os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True' 

#         # The code you want to run ONCE here
#         print("run second time")
#         os.environ['CMDLINERUNNER_RUN_ONCE'] = 'False' 


# solution 3
# I want to start ths scheduler only once,
# if WEB_CONCURRENCY is set and is greater than 1
# start the scheduler if the pid of this gunicorn is the same of the
# maximum pid of all gunicorn processes
import os
from django.apps import AppConfig
import psutil

def ready(self):
    startScheduler = True

    #check WEB_CONCURRENCY exists and is more than 1
    web_concurrency = os.environ.get("WEB_CONCURRENCY")
    if (web_concurrency):
        mypid = os.getpid()
        print("[%s] WEB_CONCURRENCY exists and is set to %s" % (mypid, web_concurrency))
        gunicorn_workers = int(web_concurrency)
        if (gunicorn_workers > 1):
            maxPid = self.getMaxRunningGunicornPid()
            if (maxPid == mypid):
                startScheduler = True
            else:
                startScheduler = False

    if (startScheduler):
        print("[%s] WILL START SCHEDULER", mypid)
    else:
        print("[%s] WILL NOT START SCHEDULER", mypid)

def getMaxRunningGunicornPid(self):
    running_pids = psutil.pids()
    maxPid = -1
    for pid in running_pids:
        proc = psutil.Process(pid)
        proc_name = proc.name()
        if (proc_name == "gunicorn"):
            if (maxPid < pid):
                maxPid = pid
    print("Max Gunicorn PID: %s", maxPid)
    return maxPid


