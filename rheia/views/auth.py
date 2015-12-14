from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound)

from rheia.views.decorators import redirect_to
from rheia import defaults


@csrf_exempt
@redirect_to(reverse_lazy("whoami"), force=True)
def login(request):
    return django_login(
        request,
        template_name="rheia/login.html",
        extra_context={
            "title": defaults.APP_NAME,
            "site_header": defaults.APP_NAME + " Login"
        }
    )


@login_required(login_url=defaults.LOGIN_URL)
def whoami(request):
    return redirect(reverse("user", args=(request.user.id,)))


@login_required(login_url=defaults.LOGIN_URL)
def user(request, uid):
    try:
        uid = int(uid)
    except TypeError:
        return HttpResponseNotFound("Unknown id")
    else:
        if request.user.id == uid:
            return HttpResponse("Hello, " + request.user.username + "!")
        else:
            return HttpResponseForbidden(
                "You are not allowed to access this resource."
            )
