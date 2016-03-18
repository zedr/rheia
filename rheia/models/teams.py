from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from rheia.models import categories
from rheia.utils.users import fullname_or_username


class Team(models.Model):
    """
    A group of people, having a leader.
    """
    name = models.CharField(max_length=1024, unique=True)
    uid = models.CharField(max_length=1024, unique=True, editable=False)
    leaders = models.ManyToManyField(User, blank=False)
    members = models.ManyToManyField(
        User,
        blank=True,
        related_name="members"
    )
    clients = models.ManyToManyField(categories.Client, blank=True)
    notes = models.TextField(max_length=4096, blank=True)

    def __str__(self):
        return "{0}: {1} (Leader: {2})".format(
            self._meta.model_name.title(),
            self.name.title(),
            ", ".join(self.leader_names)
        )

    @property
    def leader_names(self):
        for leader in self.leaders.all():
            yield fullname_or_username(leader)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    @property
    def url(self):
        return reverse_lazy("team", args=(self.uid,))

    def serialise(self):
        return {
            "name": self.name,
            "uid": self.uid,
            "href": self.url
        }
