import datetime as dt

from django import http
from django.views.generic import FormView
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

from rheia.forms.reports import ReportForm
from rheia.reports.utils import generate_report
from rheia.queries.teams import get_managed_users
from rheia.security.mixins import LoginRequiredMixin
from rheia.utils.users import fullname_or_username


def _s_to_date(s):
    return dt.datetime.strptime(s, "%Y-%m-%d")


def _title_from_user(user):
    return "{0}_{1}".format(
        slugify(fullname_or_username(user)),
        dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    )


class Reports(LoginRequiredMixin, FormView):
    """The report generation page.
    """
    template_name = "rheia/reports_form.html"
    form_class = ReportForm

    def get_form(self, **kwargs):
        form = super(Reports, self).get_form(**kwargs)
        form.fields["team_members"].queryset = get_managed_users(
            self.request.user
        )
        return form

    def post(self, request, *args, **kwargs):
        """Process the form and return the report as CSV.
        """
        form = self.get_form()
        managed_users = get_managed_users(self.request.user)
        try:
            target_user = managed_users.get(id=form.data["team_members"])
        except ObjectDoesNotExist:
            return http.HttpResponseBadRequest(
                "You cannot generate a report for this user."
            )
        else:
            from_date = _s_to_date(form.data["start_date"])
            to_date = _s_to_date(form.data["end_date"])

        response = http.HttpResponse(
            status=200,
            content_type="application/csv"
        )
        response['Content-Disposition'] = (
            'attachment; filename="{0}.csv"'.format(
                _title_from_user(target_user)
            )
        )
        response = generate_report(target_user, from_date, to_date, response)
        return response
