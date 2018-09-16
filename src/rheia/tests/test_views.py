from django.core.urlresolvers import reverse, NoReverseMatch

from rheia.tests.cases import RheiaTestCase
from rheia.models.time import LoggedTime


class UserViewsTests(RheiaTestCase):
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
        self.assertContains(response, self.user.last_name)

    def test_i_cannot_access_somebody_elses_page(self):
        self.login()
        response = self.client.get(
            reverse(
                "user",
                args=(self.some_other_user.username,)
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_can_access_own_time_page(self):
        self.login()
        response = self.client.get(
            reverse(
                "user_time",
                args=(self.user.username,)
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_i_cannot_access_somebody_s_time_page(self):
        self.login()
        response = self.client.get(
            reverse(
                "user_time",
                args=(self.some_other_user.username,)
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_i_can_submit_valid_data(self):
        self.login()
        url = reverse(
            "user_time",
            args=(self.user.username,)
        )
        response = self.client.post(
            url,
            {
                "client": 1,
                "product": 1,
                "activity": 1,
                "start_time": "12:00:00",
                "duration": "10m",
                "start_date": ["2016-03-17"],
                "notes": u"Hello"
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            LoggedTime.objects.filter(owner=self.user).get(notes="Hello")
        )

    def test_submitting_invalid_data_returns_400(self):
        self.login()
        response = self.client.post(
            reverse(
                "user_time",
                args=(self.some_other_user.username,)
            ),
            {"asasas": 1},
            follow=True
        )
        try:
            self.assertNotEqual(response.status_code, 200)
        except AssertionError:
            self.fail("Returned: {0} {1}".format(
                response.status_code, response.content
            ))
