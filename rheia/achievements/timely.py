import datetime as dt

from django.db.models import Sum

from rheia.models import LoggedTime


def streak_for_user(user):
    """Calculate the streak for a given user, returning the number of days the
    user has consistently logged their data on time.

    :param user: the user
    :type user: :class:`django.contrib.auth.models.User`
    :return: the length of the streak, backwards from now.
    :rtype: int
    """
    today = dt.datetime.now()
    qs = LoggedTime.objects.filter(owner=user)
    qs = qs.extra({"created": "date(first_created)"})
    qs = qs.values("created")
    qs = qs.annotate(daily_total=Sum("duration"))
    qs = qs.order_by("-first_created")
    return qs.count()
