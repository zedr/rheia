from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import BaseCreateView
from django.views.generic.list import ListView

from rheia.form import TimeForm
from rheia.models import LoggedTime
from rheia.views.mixins import LoginRequiredMixin


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

    def get(self, *args, **kwargs):
        form = self.form_class()
        hours_total = self.total_logged_seconds / 360
        return self.render_to_response(
            {
                "form": form,
                "object_list": self.object_list,
                "total_hours": "{0:.1f}".format(hours_total)
            }
        )
