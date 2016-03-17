from django.db import models
from django.utils import timezone
from django.contrib.auth import models as auth_models

from rheia.utils.time import today


class LoggedTime(models.Model):
    """The basic unit of time that is aggregated to form the TimeSheet.
    """
    # The person who is logging the time.
    owner = models.ForeignKey(auth_models.User)

    # When this entry was created.
    first_created = models.DateTimeField(auto_now_add=True)

    # The last time this entry was modified.
    last_modified = models.DateTimeField(auto_now=True)

    # The day on which the time was logged.
    start_date = models.DateField(default=today, null=False)

    # The time at which the time was logged (optional)
    start_time = models.TimeField(default=None, null=True)

    # The quantity of time, in seconds, that was logged.
    seconds = models.IntegerField(null=True, default=None)

    # Notes about this entry.
    notes = models.TextField(null=True, max_length=4096, default=None)

    @property
    def minutes(self):
        if self.seconds:
            return round(self.seconds / 60.0, 1)
        else:
            return 0

    @property
    def hours(self):
        if self.minutes:
            return round(self.minutes / 60.0, 1)
        else:
            return 0

    @property
    def start_datetime(self):
        return timezone.datetime.combine(self.start_date, self.start_time)

    @property
    def timedelta(self):
        if self.seconds:
            return timezone.timedelta(0, self.seconds)

    @property
    def end_datetime(self):
        if self.seconds and self.start_date and self.start_time:
            return self.start_datetime + self.timedelta

    @property
    def end_date(self):
        end_datetime = self.end_datetime
        if end_datetime:
            return end_datetime.date()

    @property
    def end_time(self):
        end_datetime = self.end_datetime
        if end_datetime:
            return end_datetime.time()

    @property
    def is_active(self):
        """Is this time currently being tracked?
        """
        return True if self.seconds is None else False

    def __unicode__(self):
        if self.seconds is None:
            return u"Time unit by {0} logged on {1} (in progress)".format(
                self.owner.username, self.start_date.isoformat()
            )
        else:
            return u"Time unit ({0} seconds) by {1} logged on {2}".format(
                self.seconds, self.owner.username, self.start_date.isoformat()
            )
