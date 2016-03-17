from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from django.contrib.auth.views import (
    login as django_login,
    logout as django_logout)

from rheia import defaults
from rheia.security.decorators import private_resource


@csrf_exempt
def login(request):
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
def user(request, name):
    context = RequestContext(request, {"user": request.user})
    return render(request, "rheia/user.html", context)
