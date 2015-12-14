from django.test import TestCase
from django.core.urlresolvers import reverse, NoReverseMatch
from rheia.tests.mixins import AuthenticatedTestsMixin


class UserViewsTests(AuthenticatedTestsMixin, TestCase):
    """Tests for the User views (login, logout, etc...).
    """

    def test_login_page_is_available(self):
        try:
            response = self.client.get(reverse("login"))
        except NoReverseMatch:
            self.fail("No view named 'login'")
        else:
            self.assertEqual(response.status_code, 200)

    def test_whoami_page_redirects_me_to_my_home_url(self):
        self.login()
        response = self.client.get(reverse("whoami"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], self.my_home_url)

    def test_i_can_access_my_user_page(self):
        self.login()
        response = self.client.get(self.my_home_url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_see_name_is_own_page(self):
        self.login()
        response = self.client.get(self.my_home_url)
        self.assertContains(response, self.user.username)

    def test_i_cannot_access_somebody_elses_page(self):
        self.login()
        response = self.client.get(reverse("user", args=(self.user.id + 1, )))
        self.assertEqual(response.status_code, 403)

    def test_can_access_own_time_page(self):
        self.login()
        response = self.client.get(reverse("user_time", args=(self.user.id, )))
        self.assertEqual(response.status_code, 200)
