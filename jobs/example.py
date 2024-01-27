# encoding: utf-8
from datetime import datetime
from typing import List

from app import gui


def get_cronjobs() -> List:
    return [
        {
            'id': 'tick_example',
            'cron': '0/1 * * * *',
            'func': tick
        }
    ]


def tick():
    gui.log('Tick! The time is: %s' % datetime.now())
