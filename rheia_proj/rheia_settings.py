from django.core.urlresolvers import reverse_lazy

from rheia_proj.settings import INSTALLED_APPS, SECRET_KEY

INSTALLED_APPS += ("rheia", )
LOGIN_REDIRECT_URL = reverse_lazy("whoami")
