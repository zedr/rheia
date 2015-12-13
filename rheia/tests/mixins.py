from django.contrib.auth.models import User


class AuthenticatedTestsMixin(object):
    """A mixin for test-cases that employ authenticated users.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='my_user',
            email='my_user@example.com',
            password='top_secret'
        )
