import datetime as dt

from django.contrib.auth.models import User
from django.test import TestCase

from rheia.achievements.timely import streak_for_user


class AchievementsTests(TestCase):
    """Tests for the achievements.
    """
    fixtures = ("test_streak.json", )

    def test_4_week_streak_gets_cup(self):
        """A user who completes their time every week gets a cup.
        """
        user = User.objects.get()
        results = streak_for_user(user, until=dt.date(2016, 3, 28))
        self.assertEqual(results["streak"], 5)
