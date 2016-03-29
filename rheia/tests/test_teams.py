from rheia.models import Client
from rheia.utils.users import fullname_or_username
from rheia.tests.cases import RheiaTestCase


class TeamTests(RheiaTestCase):
    """
    Tests for Rheia's team functionality.
    """

    def test_teams_can_be_assembled(self):
        self.assertEqual(self.team.members.count(), 1)

    def test_my_team_is_mentioned_in_my_user_page(self):
        self.login()
        response = self.client.get(self.my_home_url)
        self.assertContains(response, self.team.name)

    def test_my_team_has_its_own_page_and_lists_members(self):
        self.login()
        response = self.client.get(self.my_team_url)
        self.assertContains(response, fullname_or_username(self.user))
        self.assertContains(response,
                            fullname_or_username(self.some_other_user))

    def test_can_query_clients_by_assigned_teams(self):
        self.assertGreater(
            Client.objects.filter(team__leaders=self.user).count(),
            0
        )
