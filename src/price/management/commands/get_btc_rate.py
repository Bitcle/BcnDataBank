import datetime
from threading import Thread
import time

import pytz
import requests

from django.core.management.base import BaseCommand

from price.models import BtcRate


TIME_ZONE = pytz.timezone('Asia/Taipei')


class Command(BaseCommand):
    help = 'Get Bitcoin rate from bitoex'

    def handle(self, *args, **options):
        BtcRateFetcher().start()


class Ticker:
    tick_interval = 1

    def tick(self, trigger_time):
        raise NotImplementedError

    def start(self, *args, **kwargs):
        while True:
            t = Thread(
                target=self.tick,
                kwargs={'trigger_time': datetime.datetime.now(TIME_ZONE)},
                daemon=True
            )
            t.start()
            time.sleep(self.tick_interval)


class BtcRateFetcher(Ticker):
    tick_interval = 60

    def tick(self, trigger_time):
        time_limit = self._next_minute(trigger_time)
        while datetime.datetime.now(TIME_ZONE) < time_limit:
            r = requests.get('https://www.bitoex.com/api/v1/get_rate', timeout=12)
            if r.status_code == 200:
                data = r.json()
                data_datetime = datetime.datetime.fromtimestamp(data['timestamp'], TIME_ZONE)
                if not self.validate_data_time(trigger_time, data_datetime):
                    continue
                self.save_data(data)
                print(trigger_time, data)
                return

    def _next_minute(self, dt):
        next_dt = dt + datetime.timedelta(minutes=1)
        return next_dt.replace(second=0, microsecond=0)

    def validate_data_time(self, tick_time, data_time):
        if datetime.timedelta() <= abs(data_time - tick_time) < datetime.timedelta(minutes=1):
            return True
        else:
            return False

    def save_data(self, data):
        data_datetime = datetime.datetime.fromtimestamp(data['timestamp'], TIME_ZONE)
        BtcRate.objects.create(datetime=data_datetime, buy=data['buy'], sell=data['sell'])
