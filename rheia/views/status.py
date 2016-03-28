from django.shortcuts import render

from rheia.achievements.timely import streak_for_user
from rheia.security.decorators import private_resource


@private_resource(url_kwarg="name")
def status_view(request, name):
    """The status page of a user.
    """
    data = streak_for_user(request.user)
    streak = data["streak"]
    total = data["streak"]
    cup = None
    if total > 0:
        if streak >= 5 and streak < 10:
            cup = "bronze"
        elif streak >= 10 and streak < 15:
            cup = "silver"
        elif streak >= 15 and streak < 20:
            cup = "gold"
        elif streak >= 20:
            cup = "platinum"

    data.update({"cup": cup})
    return render(request, "rheia/status.html", data)
