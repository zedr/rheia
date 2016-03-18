from django.db import models


class BaseCategory(models.Model):
    """The abstract model for the Categories.
    """
    name = models.CharField(max_length=1024)
    first_created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        abstract = True

    def __str__(self):
        return "{0}: {1}".format(
            self._meta.model_name.title(),
            self.name
        )


class Client(BaseCategory):
    """A Client of the organisation.
    """


class Product(BaseCategory):
    """A Project or a Product associated with a particular Client.
    """


class TaskId(BaseCategory):
    """A Task or TicketId.
    """
    client = models.ForeignKey(Client, null=True)
    product = models.ForeignKey(Product, null=True)


class Activity(BaseCategory):
    """An Activity.
    """

    class Meta(object):
        verbose_name_plural = "Activities"
