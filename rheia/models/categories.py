from django.db import models


class BaseCategory(models.Model):
    """The abstract model for the Categories.
    """
    name = models.CharField(max_length=1024)
    first_created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        abstract = True


class Client(BaseCategory):
    """A Client of the organisation.
    """


class Product(BaseCategory):
    """A Project or a Product associated with a particular Client.
    """


class TaskId(BaseCategory):
    """A Task or TicketId.
    """


class Activity(BaseCategory):
    """An Activity.
    """

    class Meta(object):
        verbose_name_plural = "Activities"
