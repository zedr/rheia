from django.core.urlresolvers import reverse_lazy

from rheia_proj.settings import INSTALLED_APPS

INSTALLED_APPS += tuple(["rheia"])
LOGIN_REDIRECT_URL = reverse_lazy("whoami")
