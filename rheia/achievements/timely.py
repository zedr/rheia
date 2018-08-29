import datetime as dt

from collections import defaultdict

from django.db.models import Sum

from rheia.models import LoggedTime
from rheia import defaults


def streak_for_user(user, until=None):
    """Calculate the streak for a given user, returning the number of days the
    user has consistently logged their data on time.

    :param user: the user
    :type user: :class:`django.contrib.auth.models.User`
    :return: the length of the streak, backwards from now, and the total count
        of logged time.
    :rtype: dict
    """
    days = 0
    limit = (until or dt.date.today()).strftime("%Y-%m-%d")

    qs = LoggedTime.objects.filter(owner=user)
    qs = qs.extra({"modified": "date(last_modified)"})
    qs = qs.extra({"start": "date(start_date)"})
    qs = qs.values("modified", "start")
    qs = qs.annotate(daily_total=Sum("duration"))
    qs = qs.order_by("-start_date")

    time_ns = defaultdict(int)
    count = qs.count()

    if count:
        first = qs[0]
        if first["start"] == first["modified"] == limit:
            for item in qs:
                start = item["start"]
                if start == item["modified"]:
                    time_ns[start] += item["daily_total"] or 0
            for start, duration in sorted(time_ns.items(), reverse=True):
                if duration >= defaults.SECONDS_PER_DAY:
                    days += 1

    return {
        "streak": days,
        "total": count
    }

