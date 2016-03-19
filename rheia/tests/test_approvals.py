from django.test import Client

from rheia.models import LoggedTime
from rheia.tests.cases import RheiaTestCase


class ApprovalsTests(RheiaTestCase):
    """
    Tests for the time-sheet approval system.
    """

    def setUp(self):
        super(ApprovalsTests, self).setUp()
        self.logged_time = LoggedTime.objects.create(
            owner=self.some_other_user,
            client=self.categories["clients"][0]
        )

    def test_logged_time_can_be_approved(self):
        self.logged_time.approve(self.user)
        self.assertTrue(self.logged_time.is_approved)

    def test_logged_time_can_be_approved_through_the_web(self):
        self.login()
        self.assertFalse(self.logged_time.is_approved)
        response = self.client.post(
            self.logged_time.url,
            {
                "approved": True
            },
            HTTP_ACCEPT="application/json"

        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.logged_time.is_approved)

