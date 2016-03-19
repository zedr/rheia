"""Rheia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.shortcuts import redirect

from rheia.views.auth import login, logout, whoami, user_detail_view
from rheia.views import time
from rheia.views import teams

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

    # Redirect
    url("^$", lambda request: redirect("login"))
]
