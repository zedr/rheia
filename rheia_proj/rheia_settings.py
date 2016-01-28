from django.core.urlresolvers import reverse_lazy

from rheia_proj.settings import INSTALLED_APPS, SECRET_KEY

INSTALLED_APPS += ("rheia", "bootstrap3")
LOGIN_REDIRECT_URL = reverse_lazy("whoami")
