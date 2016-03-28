from django import forms
from django.contrib.auth.models import User

from rheia.forms.inputs import DatePickerInput
from rheia.utils.time import today_as_text, a_week_ago_as_text


class ReportForm(forms.Form):
    """A form for generating reports.
    """
    team_members = forms.ModelChoiceField(
        User.objects.all(),
        help_text="Select the username of the team-member.",
    )
    start_date = forms.DateField(
        initial=a_week_ago_as_text,
        widget=DatePickerInput(
            format="%Y-%m-%d",
            options={
                # Highlight today
                "todayHighlight": True,
                # Start on Monday
                "weekStart": 1
            }
        )
    )
    end_date = forms.DateField(
        initial=today_as_text,
        widget=DatePickerInput(
            format="%Y-%m-%d",
            options={
                # Highlight today
                "todayHighlight": True,
                # Start on Monday
                "weekStart": 1
            }
        )
    )
