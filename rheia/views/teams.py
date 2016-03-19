from django.views.generic import DetailView

from rheia.models import Team
from rheia.utils.users import fullname_or_username
from rheia.security.mixins import TeamResourceMixin


def _all_names(users):
    for user in users:
        yield fullname_or_username(user)


class TeamDetail(TeamResourceMixin, DetailView):
    """The detail view for a team.
    """
    model = Team
    context_object_name = "team"
    template_name = "rheia/team.html"
    slug_url_kwarg = "uid"
    slug_field = "uid"

    def get_context_data(self, **kwargs):
        data = super(TeamDetail, self).get_context_data(**kwargs)
        data.update(
            {
                "roster": (
                    ("Clients", (client.name for client in self.clients)),
                    ("Leaders", _all_names(self.leaders)),
                    ("Members", _all_names(self.members)),
                ),
            }
        )
        return data
