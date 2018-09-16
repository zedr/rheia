from django.core.urlresolvers import reverse

from rheia.models import LoggedTime
from rheia.tests.cases import RheiaTestCase


class TimeFieldTests(RheiaTestCase):
    """
    Tests for the Time field that is displayed in the forms.
    """
    @property
    def user_time_url(self):
        return reverse("user_time",  args=(self.user.username, ))

    def test_form_field_is_visible_in_the_time_page(self):
        self.login()
        response = self.client.get(self.user_time_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Duration")

    def test_can_submit_valid_time_duration_strings_to_time_form(self):
        self.login()
        response = self.client.post(
            self.user_time_url,
            {
                "client": 1,
                "product": 1,
                "activity": 1,
                "start_time": "12:00:00",
                "duration": "30m",
                "start_date": ["2016-03-17"],
                "notes": u"Hello"
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            LoggedTime.objects.get(duration=30 * 60)
        )

    def test_cannot_submit_invalid_time_duration_strings_to_time_form(self):
        self.login()
        response = self.client.post(
            self.user_time_url,
            {
                "start_time": "12:00:00",
                "duration": "30m 10x",
                "start_date": ["2016-03-17"],
                "notes": u"Hello"
            },
            follow=True
        )
        self.assertEqual(response.status_code, 400)
