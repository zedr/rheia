from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError

from bootstrap3_datepicker.widgets import DatePickerInput

from rheia.models import LoggedTime
from rheia.fields.time import DurationField
from rheia.validators.time import is_valid_duration
from rheia.models import categories
from rheia.utils.time import today_as_text


class _DatePickerInput(DatePickerInput):
    @property
    def media(self):
        # TODO: find a better way to do the override...
        media = super(_DatePickerInput, self).media
        media._css = {'all': ("css/datepicker3.css",)}
        media._js = ("js/lib/bootstrap-datepicker.js",)
        return media


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
    start_date = forms.DateField(
        initial=today_as_text,
        widget=_DatePickerInput(
            format="%Y-%m-%d",
            options={
                # Highlight today
                "todayHighlight": True,
                # Start on Monday
                "weekStart": 1
            }
        )
    )
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

    class Media(object):
        js = ("js/form/time.js",)

    @property
    def assigned_clients(self):
        return self.fields["client"].queryset

    def clean(self):
        """
        Ensure the user is associated with the targeted client.
        :return:
        """
        cleaned_data = super(TimeForm, self).clean()
        duration = cleaned_data["duration"]
        if duration == 0:
            cleaned_data["duration"] = None
        client = cleaned_data.get("client", None)
        if client and client not in self.assigned_clients:
            raise ValidationError(
                "You are not associated with this Client: {0}".format(client)
            )
        return cleaned_data
