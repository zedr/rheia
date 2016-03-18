from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rheia.models import categories


class AuthenticatedTestsMixin(object):
    """A mixin for test-cases that employ authenticated users.
    """
    user_name = "my_user"
    user_pass = "top_secret"

    def setUp(self):
        super(AuthenticatedTestsMixin, self).setUp()
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
    """A mixin test-cases that depend on the presence of categories.

    This mixin will also associated the test client user with one Project
    category.
    """

    def setUp(self):
        """Create a few categories and associate them to a user.
        """
        super(CategoriesMixin, self).setUp()
        category = categories.Client.objects.create(
            name="TCD"
        )
        category.assigned_users.add(self.user)
        category.save()
        self.categories = {"clients": [category]}
        categories.Product.objects.create(name="Rheia")
        categories.Activity.objects.create(name="Software development")
