from django.db import models
from django.utils import timezone
from django.contrib.auth import models as auth_models


class LoggedTime(models.Model):
    """The basic unit of time that is aggregated to form the TimeSheet.
    """
    # The person who is logging the time.
    owner = models.ForeignKey(auth_models.User)

    first_created = models.DateTimeField(auto_now_add=True)

    last_modified = models.DateTimeField(auto_now=True)

    # The day on which the time was logged.
    start_date = models.DateField(default=timezone.now, null=False)

    # The time at which the time was logged (optional)
    start_time = models.TimeField(default=None, null=True)

    # The quantity of time, in seconds, that was logged.
    elapsed_seconds = models.IntegerField(null=True, default=None)

    @property
    def is_closed(self):
        """Have we finished logging this time?
        """
        return False if self.elapsed_seconds is None else True
