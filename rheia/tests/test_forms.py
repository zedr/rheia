from django.test import TestCase

from rheia.tests.mixins import AuthenticatedTestsMixin

class FormsTests(AuthenticatedTestsMixin, TestCase):
    """Tests for the forms
    """
    def test_user_page_has_form(self):
        """The user page has a form for logging time.
        """
        self.login()
        response = self.client.get(self.my_home_url)
        self.assertContains(response, "Log Time")

