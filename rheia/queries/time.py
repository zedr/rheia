from rheia.models.time import LoggedTime


def get_time_for_team(team, prefetch=True):
    """Get all the logged time for a given team.
    """
    time_qs = LoggedTime.objects.filter(

    )
    return time_qs
