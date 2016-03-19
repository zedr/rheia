import json

from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models.query_utils import Q
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import BaseCreateView
from django import forms

from rheia.forms import TimeForm
from rheia.models import time, categories, approvals
from rheia.security.decorators import private_resource
from rheia.security.mixins import LoginRequiredMixin
from rheia.views.teams import TeamDetail
from rheia.queries.time import get_time_for_team


class TimeDetail(DetailView):
    """
    The resource for a particular unit of time.
    """
    slug_url_kwarg = "uid"
    slug_field = "id"
    model = time.LoggedTime
    template_name = "rheia/time_detail.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = time = self.get_object()
        if time.owner != request.user:
            try:
                time.client.team_set.get(leaders=request.user)
            except (AttributeError, ObjectDoesNotExist):
                return http.HttpResponseForbidden(
                    "You cannot access this resource"
                )
        return super(TimeDetail, self).dispatch(request, *args, **kwargs)

    def set_approval(self):
        try:
            approvals.Approval.objects.get_or_create(
                time=self.object,
                defaults={
                    "approver": self.request.user,
                }
            )
        except Exception as exc:
            raise

    def remove_approval(self):
        try:
            approvals.Approval.objects.get(time=self.object).delete()
        except ObjectDoesNotExist:
            pass

    def post(self, request, *args, **kwargs):
        if request.META.get("HTTP_ACCEPT", "").startswith("application/json"):
            payload = request.POST.dict()
            try:
                is_approved = payload["approved"]
            except KeyError:
                return http.HttpResponseBadRequest(
                    "Cannot process your request."
                )
            else:
                if is_approved:
                    self.set_approval()
                else:
                    self.remove_approval()
                return http.HttpResponse(
                    json.dumps({"success": True}),
                    content_type="application/json"
                )
        else:
            return http.HttpResponseBadRequest(
                "Not supported"
            )


class UserTime(LoginRequiredMixin, BaseCreateView, ListView):
    model = time.LoggedTime
    form_class = TimeForm
    template_name = "rheia/time.html"

    @property
    def total_logged_seconds(self):
        return sum(
            log.duration for log in self.object_list
            if log.duration is not None
        )

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    @property
    def object_list(self):
        return self.get_queryset()

    def get_success_url(self):
        return reverse_lazy("user_time", args=(self.request.user.username,))

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(UserTime, self).form_valid(form)

    def form_invalid(self, form):
        response = super(UserTime, self).form_invalid(form)
        response.status_code = http.HttpResponseBadRequest.status_code
        return response

    def get_assigned_clients(self):
        """Get the Clients that are assigned to this user.
        """
        user = self.request.user
        return categories.Client.objects.filter(
            Q(team__leaders=user) | Q(team__members=user)
        )

    def get_activities(self):
        """Get all the available activities.
        """
        return categories.Activity.objects.all()

    def get_products(self):
        """Get all the available products
        """
        return categories.Product.objects.all()

    def get_form(self, *args):
        form = super(UserTime, self).get_form(*args)
        form.fields["client"].queryset = self.get_assigned_clients()
        return form

    @method_decorator(private_resource("name"))
    def get(self, *args, **kwargs):
        form = self.get_form()
        if self.get_activities().count() and self.get_products().count():
            if form.assigned_clients.count():
                seconds = self.total_logged_seconds
                hours_total = (seconds / 60.0) / 60
                return self.render_to_response(
                    {
                        "csrfmiddlewaretoken": "sasa",
                        "form": form,
                        "time_sheets": self.object_list,
                        "show_author": False,
                        "total_hours": "{0:.1f}".format(hours_total),
                    }
                )
            else:
                return render(
                    self.request,
                    template_name="rheia/generic.html",
                    status=403,
                    context={
                        "title": "Forbidden",
                        "message": (
                            "You do not have any Clients "
                            "currently associated with you. "
                            "Please contact an administrator for assistance."
                        )
                    }
                )
        return render(
            self.request,
            template_name="rheia/generic.html",
            status=501,
            context={
                "title": "Not supported",
                "message": (
                    "The administrator has not yet completed the required "
                    "Category configuration for this instance of Rheia. "
                )
            }
        )

    @method_decorator(private_resource("name"))
    def post(self, *args, **kwargs):
        return super(UserTime, self).post(*args, **kwargs)


class TeamTime(TeamDetail):
    """A read-only view on the time-sheets of a team.
    """
    template_name = "rheia/team_time.html"

    def get_context_data(self, **kwargs):
        data = super(TeamTime, self).get_context_data(**kwargs)
        data.update(
            {
                "time_sheets": (
                    get_time_for_team(self.team)
                ),
                "media": forms.Media(
                    js=("js/table/approval.js",)
                )
            }
        )
        return data

    @method_decorator(ensure_csrf_cookie)
    def get(self, *args, **kwargs):
        return super(TeamTime, self).get(*args, **kwargs)
