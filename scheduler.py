# encoding: utf-8

import importlib
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app import gui

bg_scheduler = BackgroundScheduler()


def load_all_jobs():
    plugins_dir = os.path.join(os.path.dirname(__file__), 'jobs')

    for file in os.listdir(plugins_dir):
        if not file.endswith('.py'):
            continue
        try:
            module_name = file[:-3]
            module_name = f'jobs.{module_name}'
            module = importlib.import_module(module_name)
            if hasattr(module, 'get_cronjobs'):
                add_jobs(module.get_cronjobs())
        except Exception as e:
            gui.log(f'load job error: {e}')


def add_jobs(job_configs):
    for cfg in job_configs:
        bg_scheduler.add_job(cfg['func'], CronTrigger.from_crontab(cfg['cron']))
        print(f'add job: {cfg["cron"]} {cfg["func"].__name__}')
        gui.log(f'add job: {cfg["cron"]} {cfg["func"].__name__}')


def start_scheduler():
    load_all_jobs()

    bg_scheduler.start()


def stop_scheduler():
    bg_scheduler.shutdown()


if __name__ == '__main__':
    load_all_jobs()
