from django.core.urlresolvers import reverse
from django.test import TestCase

from rheia.tests.mixins import AuthenticatedTestsMixin


class FormsTests(AuthenticatedTestsMixin, TestCase):
    """Tests for the forms
    """

    @property
    def user_time_url(self):
        return reverse("user_time", args=(self.user.id,))

    def test_user_time_page_has_form(self):
        """The page the user can log time has a form.
        """
        self.login()
        response = self.client.get(self.user_time_url)
        self.assertContains(response, "Log time")
        self.assertContains(response, "Submit")
