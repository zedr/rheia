#!/usr/bin/env python
import os
import sys
import csv
import datetime

import rheia


def main():
    from django.contrib.auth.models import User

    if len(sys.argv) > 1:
        path = sys.argv[1]
        portico, _ = rheia.models.Client.objects.get_or_create(
            name="PortiCo"
        )
        product, _ = rheia.models.Product.objects.get_or_create(
            name="Rheia"
        )
        with open(path) as fd:
            reader = csv.reader(fd, delimiter=',')
            for row in reader:
                taskid, activity, notes, start_date, seconds, username = row
                try:
                    user = User.objects.get(username=username.strip())
                except User.DoesNotExist:
                    pass
                else:
                    activity_, _ = rheia.models.Activity.objects.get_or_create(
                        name=activity
                    )
                    day, month, year = [int(el) for el in start_date.split("-")]
                    dt = datetime.date(year + 2000, month, day)
                    data = {
                        "owner": user,
                        "activity": activity_,
                        "notes": notes,
                        "start_date": dt,
                        "duration": seconds,
                        "client": portico,
                        "product": product
                    }
                    rheia.models.LoggedTime.objects.create(**data)
                    print(data)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rheia_proj.settings")
    import django

    django.setup()
    main()
