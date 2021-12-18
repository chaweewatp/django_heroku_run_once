
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


## solution 2

from django.apps import AppConfig
import os

class CommandLineRunner(AppConfig):
    name = 'myapp'

    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE') 
        if run_once is not None:
            print('not run first time')
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True' 

        # The code you want to run ONCE here
        print("run second time")
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'False' 

