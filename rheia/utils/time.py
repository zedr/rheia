from django.utils import timezone


def today():
    return timezone.datetime.today().date()
