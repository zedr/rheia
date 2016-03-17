from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import BaseCreateView
from django.views.generic.list import ListView
from django import http

from rheia.forms import TimeForm
from rheia.models import LoggedTime
from rheia.views.mixins import LoginRequiredMixin
from rheia.security.decorators import private_resource


class UserTime(LoginRequiredMixin, BaseCreateView, ListView):
    model = LoggedTime
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

    @method_decorator(private_resource("name"))
    def get(self, *args, **kwargs):
        form = self.form_class()
        seconds = self.total_logged_seconds
        hours_total = (seconds / 60.0) / 60
        return self.render_to_response(
            {
                "csrfmiddlewaretoken": "sasa",
                "form": form,
                "object_list": self.object_list,
                "total_hours": "{0:.1f}".format(hours_total),
            }
        )

    def post(self, *args, **kwargs):
        return super(UserTime, self).post(*args, **kwargs)
