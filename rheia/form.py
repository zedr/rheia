from django import forms

from rheia.models import LoggedTime


class TimeForm(forms.ModelForm):
    start_time = forms.CharField(required=False)

    class Meta(object):
        model = LoggedTime
        fields = ('start_date', 'start_time', 'seconds')
