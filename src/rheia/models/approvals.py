from django.db import models
from django.contrib.auth.models import User


class Approval(models.Model):
    """An approval for logged time.
    """
    approved = models.DateTimeField(auto_now_add=True)
    approver = models.ForeignKey(User)
    time = models.ForeignKey("LoggedTime")
