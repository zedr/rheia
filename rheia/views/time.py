from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import BaseCreateView
from django.views.generic.list import ListView

from rheia.form import TimeForm
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
            log.seconds for log in self.object_list if log.seconds is not None
        )

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    @property
    def object_list(self):
        return self.get_queryset()

    def get_success_url(self):
        return reverse_lazy("user_time", args=(self.request.user.id,))

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(UserTime, self).form_valid(form)

    @method_decorator(private_resource("name"))
    def get(self, *args, **kwargs):
        form = self.form_class()
        seconds = self.total_logged_seconds
        hours_total = (seconds / 60.0) / 60

        return self.render_to_response(
            {
                "form": form,
                "object_list": self.object_list,
                "total_hours": "{0:.1f}".format(hours_total),
            }
        )
