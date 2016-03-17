from django.test import TestCase
from django.db import IntegrityError

from rheia.models import LoggedTime
from rheia.tests.mixins import AuthenticatedTestsMixin


class LoggedTimeTests(AuthenticatedTestsMixin, TestCase):
    """Tests for the LoggedTime model.
    """

    def test_cannot_create_logged_time_without_start_date(self):
        """A logged-time item *must* have a start date.
        """
        with self.assertRaises(IntegrityError):
            logged = LoggedTime.objects.create(
                owner=self.user,
                start_date=None
            )
            logged.save()

    def test_can_create_logged_time_and_query_it(self):
        """A logged-time item can be created and saved in the database.
        """
        LoggedTime.objects.create(owner=self.user).save()
        self.assertGreater(LoggedTime.objects.count(), 0)

    def test_can_be_closed(self):
        """If a value is set for the elapsed_seconds field, the item is closed.
        """
        logged = LoggedTime.objects.create(
            owner=self.user,
        )
        logged.save()
        self.assertTrue(logged.is_active)

        logged.duration = 60
        logged.save()
        self.assertFalse(logged.is_active)
