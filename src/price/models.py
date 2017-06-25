from django.db import models


class BtcPrice(models.Model):
    date = models.DateField()
    open = models.DecimalField(null=True, max_digits=16, decimal_places=8)
    close = models.DecimalField(max_digits=16, decimal_places=8)
    high = models.DecimalField(null=True, max_digits=16, decimal_places=8)
    low = models.DecimalField(null=True, max_digits=16, decimal_places=8)
    volume_btc = models.DecimalField(null=True, max_digits=20, decimal_places=8)
    volume_currency = models.DecimalField(null=True, max_digits=20, decimal_places=8)
    weighted_price = models.DecimalField(null=True, max_digits=20, decimal_places=8)
