import functools

from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def private_resource(url_kwarg="username"):
    def outer(view):
        """A decorator for resources that are accessible only by their owners.

        :param view: the view of the resource
        """

        @functools.wraps(view)
        def inner(request, *args, **kwargs):
            """
            :type request: :class:`django.http.HttpRequest`
            """
            try:
                url_username = request.resolver_match.kwargs.get(url_kwarg)
            except KeyError:
                return http.HttpResponseServerError(
                    "View configuration error. "
                    "Please contact the administrator."
                )
            else:
                if request.user.is_authenticated():
                    if url_username == request.user.username:
                        return view(request, *args, **kwargs)
                    else:
                        return http.HttpResponseForbidden(
                            "You are not authorized to access this resource."
                        )
                else:
                    return redirect(reverse("login"))

        return inner

    return outer
