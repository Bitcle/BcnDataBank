import csv

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET

from .forms import HourForm
from .models import BtcPrice


@require_GET
def hour(request):
    form = HourForm(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        prices = BtcPrice.objects.filter(date__range=[start, end])

        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        writer.writerow(['Date', 'Open', 'High', 'Low', 'Close'])
        for d in prices:
            writer.writerow([d.date, d.open, d.high, d.low, d.close])

        return response
    else:
        # TODO: error response should be more specific
        response = 'invalid parameter'
        return HttpResponseBadRequest(response)
