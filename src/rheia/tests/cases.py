from django.test import TestCase

from rheia.tests.mixins import UsersMixin, CategoriesMixin, TeamsMixin


class RheiaTestCase(TeamsMixin, CategoriesMixin, UsersMixin, TestCase):
    """
    A test case for Rheia.
    """


__all__ = (
    RheiaTestCase.__name__,
)
