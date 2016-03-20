from django.core.urlresolvers import reverse_lazy

from rheia_proj.settings import (
    INSTALLED_APPS, SECRET_KEY, STATIC_URL, ROOT_URLCONF
)
import mimetypes

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)

INSTALLED_APPS += (
    "rheia",
    "bootstrap3",
    "bootstrap3_datepicker",
    "rest_framework"
)
LOGIN_REDIRECT_URL = reverse_lazy("whoami")
DEBUG = True
