from django.db.models.query_utils import Q

from rheia.models import Team


def get_user_teams(user):
    return Team.objects.filter(
        Q(members=user) | Q(leaders=user)
    )
