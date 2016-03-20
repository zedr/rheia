from django import template
from django.core.urlresolvers import reverse

from rheia.serializers.universal import serialise
from rheia.queries.teams import get_user_teams

register = template.Library()

def _link_class(there_url, here_url):
    return "active" if there_url == here_url else "inactive"

@register.inclusion_tag("rheia/partials/sidebar.html", takes_context=True)
def user_sidebar(context):
    request = context['request']
    path = request.path
    user = request.user
    home_url = reverse("user", args=(user,))
    time_url = reverse("user_time", args=(user, ))
    if request.user.is_authenticated():
        return {
            "teams": serialise(get_user_teams(user)),
            "urls": {
                "home": {
                    "href": home_url,
                    "class": _link_class(home_url, path)
                },
                "time": {
                    "href": time_url,
                    "class": _link_class(time_url, path)
                }
            }
        }
