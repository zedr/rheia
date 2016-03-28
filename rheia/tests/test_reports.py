from django.core.urlresolvers import reverse

from rheia.tests.cases import RheiaTestCase


class ReportsTests(RheiaTestCase):
    """Tests for the reports.
    """

    def test_can_access_reports_page_and_see_the_form(self):
        """The reports page is accessible.
        """
        self.login()
        response = self.client.get(reverse("reports"))
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, "Generate a report")
