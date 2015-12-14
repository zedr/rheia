from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import BaseFormView, BaseCreateView
from django.views.generic.list import ListView

from rheia.form import TimeForm
from rheia.models import LoggedTime
from rheia.views.mixins import LoginRequiredMixin


class UserTime(LoginRequiredMixin, BaseCreateView, ListView):
    model = LoggedTime
    form_class = TimeForm
    template_name = "rheia/time.html"

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

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response(
            {
                "form": form,
                "object_list": self.object_list
            }
        )
