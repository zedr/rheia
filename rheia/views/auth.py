from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import (
    login as django_login,
    logout as django_logout)

from rheia import defaults
from rheia.queries.teams import get_user_teams
from rheia.security.decorators import private_resource
from rheia.serializers.universal import serialise


def _user_detail_url(user):
    return reverse("user", args=(user.username,))


@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return redirect(_user_detail_url(request.user))
    else:
        return django_login(
            request,
            template_name="rheia/login.html",
            extra_context={
                "title": defaults.APP_NAME,
                "site_header": defaults.APP_NAME + " Login"
            }
        )


def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
    return redirect(reverse("login"))


@login_required(login_url=defaults.LOGIN_URL)
def whoami(request):
    return redirect(reverse("user", args=(request.user.username,)))


@private_resource("name")
@login_required(login_url=defaults.LOGIN_URL)
def user_detail_view(request, name):
    context = RequestContext(request, {
        "user": request.user,
        "teams_count": get_user_teams(request.user).count()
    })
    return render(request, "rheia/user.html", context)
