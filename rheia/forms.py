from django import forms
from django.forms import widgets

from rheia.models import LoggedTime
from rheia.fields.time import DurationField
from rheia.validators.time import is_valid_duration
from rheia.models import categories


class TimeForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        categories.Client.objects.all(),
        help_text="The related client."
    )
    product = forms.ModelChoiceField(
        categories.Product.objects.all(),
        help_text="The related product or project."
    )
    taskid = forms.ModelChoiceField(
        categories.TaskId.objects.all(),
        required=False,
        help_text="An optional task or ticket ID."
    )
    activity = forms.ModelChoiceField(categories.Activity.objects.all())
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
        fields = (
            'client',
            'product',
            'taskid',
            'activity',
            'start_date',
            'start_time',
            'duration',
            'notes'
        )
