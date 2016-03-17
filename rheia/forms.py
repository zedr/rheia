from django import forms
from django.forms import widgets

from rheia.models import LoggedTime
from rheia.fields.time import DurationField
from rheia.validators.time import is_valid_duration


class TimeForm(forms.ModelForm):
    start_time = forms.CharField(required=False)
    duration = DurationField(required=False,
                             validators=[is_valid_duration],
                             help_text=(
                                 "The duration of this activity "
                                 "(e.g. 1h 30m)."
                             ))
    notes = forms.CharField(required=False, widget=widgets.Textarea)

    class Meta(object):
        model = LoggedTime
        fields = ('start_date', 'start_time', 'duration', 'notes')
