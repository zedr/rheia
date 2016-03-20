from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rheia.utils.cache import cache_on_view
from rheia.security.decorators import private_resource


class TeamResourceMixin(object):
    """A mixin for team views that are reserved for their leaders or members.
    """
    allow_members = True

    def check_if_user_in_group(self, user, group):
        return True if user in group else False

    @property
    @cache_on_view
    def leaders(self):
        return self.object.leaders.all()

    @property
    @cache_on_view
    def members(self):
        return self.object.members.all()

    @property
    @cache_on_view
    def clients(self):
        return self.object.clients.all()

    def check_for_leadership(self):
        return self.check_if_user_in_group(self.request.user, self.leaders)

    def check_for_membership(self):
        return self.check_if_user_in_group(self.request.user, self.members)

    def get_context_data(self, **kwargs):
        data = super(TeamResourceMixin, self).get_context_data(**kwargs)
        data.update(
            {
                "team_name": self.team.name,
                "team_time_url": self.team.time_url,
                "is_a_leader": self.viewed_by_leader,
            }

        )
        return data

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.team = self.get_object()
        self.viewed_by_leader = self.check_for_leadership()
        if not self.viewed_by_leader:
            if not self.allow_members or not self.check_for_membership():
                return render(
                    request,
                    "rheia/generic.html",
                    {
                        "title": "Forbidden",
                        "message": "You are not a member of this group."
                    }
                )
        return super(TeamResourceMixin, self).dispatch(
            request, *args, **kwargs
        )


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class PrivateResourceMixin(object):
    @method_decorator(private_resource)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
