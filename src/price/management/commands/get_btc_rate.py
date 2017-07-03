import datetime
from threading import Thread
import time

import pytz
import requests

from django.core.management.base import BaseCommand

from price.models import BtcPrice


TIME_ZONE = pytz.timezone('Asia/Taipei')


class Command(BaseCommand):
    help = 'Get Bitcoin rate from bitoex'

    def handle(self, *args, **options):
        HourlyTicker().start()


def next_hour(dt):
    next_dt = dt + datetime.timedelta(hours=1)
    return next_dt.replace(minute=0, second=0, microsecond=0)


class HourlyTicker:

    def fetch_hourly_data(self, trigger_time):
        BtcRateFetcher(fetch_until=next_hour(trigger_time)).fetch()

    def start(self):
        while True:
            now = datetime.datetime.now(TIME_ZONE)
            next_tick = next_hour(now)
            sleep_time = (next_tick - now).seconds

            print('HourlyTicker tick at', now)
            t = Thread(
                target=self.fetch_hourly_data,
                kwargs={'trigger_time': now},
                daemon=True
            )
            t.start()
            # 5 seconds is added to ensure it doesn't wake up too early.
            time.sleep(sleep_time + 5)


class BtcRateFetcher:

    def __init__(self, fetch_until):
        self.data = []
        self.fetch_time = datetime.datetime.now(TIME_ZONE)
        self.fetch_until = fetch_until

    def fetch(self):
        minutes_count = int((self.fetch_until - self.fetch_time).total_seconds()) // 60
        print('BtcRateFetcher starts fetching...')
        print('BtcRateFetcher will fetch', minutes_count, 'times')
        for i in range(minutes_count):
            if datetime.datetime.now(TIME_ZONE) >= self.fetch_until:
                break
            Thread(target=self.query, daemon=True).start()
            time.sleep(60)
        self.save_rates()

    def query(self):
        retry_time = 0
        while retry_time < 3:
            query_data = self._query(timeout=15)
            if query_data:
                self.data.append(query_data)
                print('query result:', query_data)
                break
            else:
                retry_time += 1
                print('query failed:', 'retry #' + str(retry_time))

    def _query(self, timeout):
        r = requests.get('https://www.bitoex.com/api/v1/get_rate', timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            data_datetime = datetime.datetime.fromtimestamp(data['timestamp'], TIME_ZONE)
            if self._validate_data_time(datetime.datetime.now(TIME_ZONE), data_datetime):
                return data
            else:
                return None
        else:
            return None

    def _validate_data_time(self, tick_time, data_time):
        if datetime.timedelta() <= abs(data_time - tick_time) < datetime.timedelta(minutes=1):
            return True
        else:
            return False

    def save_rates(self):
        if not self.data:
            return

        self.data.sort(key=lambda d: d['timestamp'])
        for d in self.data:
            d['avg'] = (d['buy'] + d['sell']) / 2
        open = self.data[0]['avg']
        close = self.data[-1]['avg']
        high = max(self.data, key=lambda d: d['avg'])['avg']
        low = min(self.data, key=lambda d: d['avg'])['avg']

        BtcPrice.objects.create(
            time=self.fetch_time.replace(minute=0, second=0, microsecond=0),
            open=open, close=close, high=high, low=low)
