from rheia.models import LoggedTime
from rheia.tests.cases import RheiaTestCase


class ApprovalsTests(RheiaTestCase):
    """
    Tests for the time-sheet approval system.
    """

    def test_logged_time_can_be_approved(self):
        time = LoggedTime.objects.create(
            owner=self.some_other_user,
        )
        time.approve(self.user)
        self.assertTrue(time.is_approved)
