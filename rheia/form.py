from django.forms import ModelForm

from rheia.models import LoggedTime


class TimeForm(ModelForm):
    class Meta(object):
        model = LoggedTime
        fields = ('start_date', )
