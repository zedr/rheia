from django.db import models
from django.contrib.auth import models as auth_models


class BaseCategory(models.Model):
    """The abstract model for the Categories.
    """
    name = models.CharField(max_length=1024)
    first_created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        abstract = True

    def __str__(self):
        return self.name


class Client(BaseCategory):
    """A Client of the organisation.
    """

    def serialise(self):
        return {
            "name": self.name,
        }


class Product(BaseCategory):
    """A Project or a Product associated with a particular Client.
    """


class TaskId(BaseCategory):
    """A Task or TicketId.
    """
    client = models.ForeignKey(Client, null=True)
    product = models.ForeignKey(Product, null=True)

    class Meta(object):
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Activity(BaseCategory):
    """An Activity.
    """

    class Meta(object):
        verbose_name_plural = "Activities"
