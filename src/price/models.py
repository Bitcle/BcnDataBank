from django.db import models


class BtcPrice(models.Model):
    date = models.DateTimeField()
    open = models.DecimalField(max_digits=16, decimal_places=8)
    close = models.DecimalField(max_digits=16, decimal_places=8)
    high = models.DecimalField(max_digits=16, decimal_places=8)
    low = models.DecimalField(max_digits=16, decimal_places=8)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=8)
    volume_currency = models.DecimalField(max_digits=20, decimal_places=8)
    weighted_price = models.DecimalField(max_digits=20, decimal_places=8)


class BtcHistory(models.Model):
    date = models.DateField()
    price = models.DecimalField(max_digits=16, decimal_places=8)
