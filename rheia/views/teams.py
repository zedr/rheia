from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rheia.models import Team
from rheia.utils.cache import cache_on_view
from rheia.utils.users import fullname_or_username


def _names(users):
    for user in users:
        yield fullname_or_username(user)


class TeamDetailView(DetailView):
    """The detail view for a team.
    """
    model = Team
    context_object_name = "team"
    template_name = "rheia/team.html"
    slug_url_kwarg = "uid"
    slug_field = "uid"

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

    def check_for_leadership(self):
        return self.check_if_user_in_group(self.request.user, self.leaders)

    def check_for_membership(self):
        return self.check_if_user_in_group(self.request.user, self.members)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object = team = self.get_object()
        is_a_leader = self.check_for_leadership()
        if is_a_leader or self.check_for_membership():
            return self.render_to_response(
                {
                    "team_name": team.name,
                    "roster": (
                        ("Leaders", _names(self.leaders)),
                        ("Members", _names(self.members)),
                    ),
                    "is_a_leader": is_a_leader,
                }
            )
        else:
            return render(
                request,
                "rheia/generic.html",
                {
                    "title": "Forbidden",
                    "message": "You are not a member of this group."
                }
            )
