import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils import timezone
from django.contrib.auth import models as auth_models

from rheia.utils.time import today
from rheia.models import categories
from rheia.models import approvals


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
    duration = models.IntegerField(null=True, default=None)

    # The associated Client
    client = models.ForeignKey(categories.Client, null=True)

    # The associated Product
    product = models.ForeignKey(categories.Product, null=True)

    # The associated Task ID (optional)
    task_id = models.ForeignKey(categories.TaskId, null=True)

    # The associated Activity
    activity = models.ForeignKey(categories.Activity, null=True)

    # Notes about this entry.
    notes = models.TextField(null=True, max_length=4096, default=None)

    @property
    def minutes(self):
        if self.duration:
            return int(round(self.duration / 60.0, 0))
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
        if self.duration:
            return timezone.timedelta(0, self.duration)

    @property
    def end_datetime(self):
        if self.duration and self.start_date and self.start_time:
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
        return True if self.duration is None else False

    @property
    def is_approved(self):
        """This time has been approved.
        """
        try:
            approvals.Approval.objects.get(time=self)
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def approve(self, user):
        """Approve this time, attributing the action to a user.
        """
        approvals.Approval.objects.create(
            time=self,
            approver=user
        )

    @property
    def url(self):
        return reverse_lazy("time", args=(self.id,))

    def __unicode__(self):
        if self.duration is None:
            return u"Time unit by {0} logged on {1} (in progress)".format(
                self.owner.username, self.start_date.isoformat()
            )
        else:
            return u"Time unit ({0} seconds) by {1} logged on {2}".format(
                self.duration, self.owner.username, self.start_date.isoformat()
            )
