from datetime import datetime

from django import forms


class HourForm(forms.Form):
    start = forms.CharField()
    end = forms.CharField()

    @classmethod
    def _validate_date(cls, date_string):
        try:
            return datetime.strptime(date_string, '%Y-%m-%d-%H')
        except ValueError:
            raise forms.ValidationError('invalid date')

    def clean_start(self):
        start = self._validate_date(self.cleaned_data['start'])
        return start

    def clean_end(self):
        end = self._validate_date(self.cleaned_data['end'])
        return end
