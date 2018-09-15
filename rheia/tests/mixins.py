from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rheia.models import categories
from rheia.models import teams


class UsersMixin(object):
    """A mixin for test-cases that employ authenticated users.
    """
    user_name = "my_user"
    user_pass = "top_secret"

    def setUp(self):
        super(UsersMixin, self).setUp()
        self.user = User.objects.create_user(
            username=self.user_name,
            email='my_user@example.com',
            password=self.user_pass
        )
        self.some_other_user = User.objects.create_user(
            username="somebody_else",
            email="someone@example.com",
            password="mumbo_jumbo"
        )

    def login(self):
        return self.client.login(
            username=self.user_name,
            password=self.user_pass
        )

    @property
    def my_home_url(self):
        return "http://testserver" + reverse(
            "user",
            args=(self.user.username,)
        )


class CategoriesMixin(object):
    """A mixin for test-cases that depend on the presence of categories.

    This mixin will also associated the test client user with one Project
    category.
    """

    def setUp(self):
        """Create a few categories and associate them to a user.
        """
        super(CategoriesMixin, self).setUp()
        client = categories.Client.objects.create(
            name="TCD"
        )
        product = categories.Product.objects.create(name="Rheia")
        activity = categories.Activity.objects.create(
            name="Software development"
        )
        self.categories = {
            "clients": [client],
            "products": [product],
            "activities": [activity]
        }


class TeamsMixin(object):
    """A mixin for test-cases that depend on the presence of teams.

    It depends on the UsersMixin.
    """
    become_leader = True
    become_member = False

    def setUp(self):
        super(TeamsMixin, self).setUp()
        self.create_my_team()

    def create_my_team(self):
        team = teams.Team.objects.create(name="TCD Group B")
        team.save()
        try:
            team.clients.add(self.categories["clients"][0])
        except (AttributeError, KeyError, IndexError):
            pass

        if self.become_leader:
            team.leaders.add(self.user)
        elif self.become_member:
            team.members.add(self.user)
        team.members.add(self.some_other_user)
        team.save()
        self.team = team

    @property
    def my_team_url(self):
        # Force evaluation of the lazy object
        return str(self.team.url)
