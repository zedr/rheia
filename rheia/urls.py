from django.conf.urls import url, include
from django.shortcuts import redirect

from rheia.views.auth import login, logout, whoami, user_detail_view
from rheia.views import time
from rheia.views import teams

from rheia import api

urlpatterns = [
    # Auth
    url("^login/", login, name="login"),
    url("^logout/", logout, name="logout"),
    url("^whoami/", whoami, name="whoami"),

    # Time
    url(
        "^time/(?P<uid>\d+)/",
        time.TimeDetail.as_view(),
        name="time"
    ),

    # Team
    url(
        "^teams/(?P<uid>[-_\w]+)/$",
        teams.TeamDetail.as_view(),
        name="team"
    ),
    url(
        "^teams/(?P<uid>[-_\w]+)/time$",
        time.TeamTime.as_view(),
        name="team_time"
    ),
    url(
        "^users/(?P<name>\w+)/$",
        user_detail_view,
        name="user"
    ),
    url(
        "^users/(?P<name>\w+)/time/$",
        time.UserTime.as_view(),
        name="user_time"
    ),
    url(
        "^users/(?P<name>\w+)/time/$",
        time.UserTime.as_view(),
        name="user_time"
    ),

    # API
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(api.router.urls)),

    # Redirect
    url("^$", lambda request: redirect("login"))
]
