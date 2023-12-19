from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models


admin.site.register(models.CustomUser)
admin.site.register(models.Profile)
admin.site.register(models.Connection)
admin.site.register(models.Post)
admin.site.register(models.Comment)

