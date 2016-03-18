from django.test import TestCase

from rheia.tests.mixins import AuthenticatedTestsMixin, CategoriesMixin


class RheiaTestCase(CategoriesMixin, AuthenticatedTestsMixin, TestCase):
    """
    A test case for Rheia.
    """


__all__ = (
    RheiaTestCase.__name__,
)
