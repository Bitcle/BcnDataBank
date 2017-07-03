from django.db import models


class BtcPrice(models.Model):
    time = models.DateTimeField(null=True)
    open = models.DecimalField(max_digits=16, decimal_places=8)
    close = models.DecimalField(max_digits=16, decimal_places=8)
    high = models.DecimalField(max_digits=16, decimal_places=8)
    low = models.DecimalField(max_digits=16, decimal_places=8)


# Wilson is mei mei god.


class BtcHistory(models.Model):
    date = models.DateField()
    price = models.DecimalField(max_digits=16, decimal_places=8)
