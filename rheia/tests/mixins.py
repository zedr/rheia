from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class AuthenticatedTestsMixin(object):
    """A mixin for test-cases that employ authenticated users.
    """
    user_name = "my_user"
    user_pass = "top_secret"

    def setUp(self):
        self.user = User.objects.create_user(
            username=self.user_name,
            email='my_user@example.com',
            password=self.user_pass
        )

    def login(self):
        return self.client.login(
            username=self.user_name,
            password=self.user_pass
        )

    @property
    def my_home_url(self):
        return "http://testserver" + reverse("user", args=(self.user.id,))

