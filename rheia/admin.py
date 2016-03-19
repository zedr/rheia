from django.contrib import admin

from rheia import models

admin.site.register(models.LoggedTime)
admin.site.register(models.Approval)
admin.site.register(models.Activity)
admin.site.register(models.Client)
admin.site.register(models.Product)
admin.site.register(models.TaskId)
admin.site.register(models.Team)
