import csv
from collections import defaultdict
from io import StringIO

from rheia.models import LoggedTime
from rheia.utils.users import fullname_or_username


def generate_stats(time):
    """Generate stats about logged time.
    """
    stats = defaultdict(float)
    for item in time:
        if item.activity and item.hours:
            stats[item.activity.name] += item.hours
    return [
        {
            "label": k,
            "value": v
        }
        for k, v in stats.items()
    ]


def generate_report(user, from_date, to_date, flo=None):
    """Generate a report for a given user.

    :param user: the user for which a report should be generated
    :type user: :class:`django.contrib.auth.models.User`
    """
    qs = LoggedTime.objects.filter(
        owner=user,
        start_date__gte=from_date,
        start_date__lte=to_date,
        duration__isnull=False
    )
    fd = flo or StringIO()
    writer = csv.writer(fd, delimiter="\t")
    if qs.count():
        writer.writerow(
            (
                "Name",
                "Date",
                "Hours",
                "Client",
                "Product",
                "Task",
                "Activity",
                "Approved",
                "Notes"
            )
        )
        for item in qs:
            writer.writerow(
                [
                    fullname_or_username(user),
                    item.start_date,
                    "{0}.{1}".format(item.hours, item.minutes),
                    item.client.name,
                    item.product.name,
                    item.task_id.name if item.task_id else "n/a",
                    item.activity.name,
                    item.is_approved,
                    item.notes
                ]
            )
    return fd
