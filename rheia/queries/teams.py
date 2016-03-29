import itertools

from django.contrib.auth.models import User
from django.db.models.query_utils import Q

from rheia.models import Team


def get_user_teams(user):
    """Get the teams for this user.
    """
    qs = Team.objects.filter(Q(members=user) | Q(leaders=user)).distinct()
    return qs.order_by("name")


def get_managed_users(user):
    """Get all the users that are managed by a given user
    """
    if user.is_superuser:
        return User.objects.filter()
    else:
        return User.objects.filter(members__leaders=user)
