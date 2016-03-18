from django.utils import timezone


def today():
    return timezone.datetime.today().date()


def today_as_text():
    return today().strftime("%Y-%m-%d")
