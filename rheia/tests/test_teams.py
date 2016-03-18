from rheia.tests.cases import RheiaTestCase
from rheia.models.teams import Team


class TeamTests(RheiaTestCase):
    """
    Tests for Rheia's team functionality.
    """

    def create_my_team(self):
        team = Team.objects.create(name="TCD Group B")
        team.save()
        team.leaders = (self.user,)
        team.members = (self.some_other_user,)
        team.save()
        self.team = team

    def test_teams_can_be_assembled(self):
        self.create_my_team()
        self.assertEqual(self.team.members.count(), 1)

    def test_my_team_is_mentioned_in_my_user_page(self):
        self.login()
        self.create_my_team()
        response = self.client.get(self.my_home_url)
        self.assertContains(response, self.team.name)
