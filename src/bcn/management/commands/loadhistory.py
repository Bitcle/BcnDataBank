import datetime
import requests

from django.core.management.base import BaseCommand

from price.models import BtcPrice


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://www.bitoex.com/charts/price_history'
        response = requests.get(url)
        for data in response.json():
            date = datetime.datetime.fromtimestamp(data['date'] / 1000)
            BtcPrice.objects.create(date=date, close=data['price'])
