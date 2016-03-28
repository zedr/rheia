import datetime as dt

from rheia.models import LoggedTime
from rheia.achievements.timely import streak_for_user
from rheia.tests.cases import RheiaTestCase


class AchievementsTests(RheiaTestCase):
    """Tests for the achievements.
    """
    def test_4_week_streak_gets_cup(self):
        """A user who completes their time every week gets a cup.
        """
        now = dt.datetime.now()
        days = 30

        for idx in range(days):
            # The team needs to log 7.5 hours daily.
            LoggedTime.objects.create(
                owner=self.user,
                first_created=now,
                start_date=now.today() - dt.timedelta(days=idx),
                duration=4 * 60 * 60
            )
            LoggedTime.objects.create(
                owner=self.user,
                first_created=now,
                start_date=now.today() - dt.timedelta(days=idx),
                duration=3.5 * 60 * 60
            )

        self.assertEqual(streak_for_user(self.user), 30)
