from django.db.models.query_utils import Q

from rheia.models import Team


def get_user_teams(user):
    """Get the teams for this user.
    """
    qs = Team.objects.filter(Q(members=user) | Q(leaders=user)).distinct()
    return qs.order_by("name")
