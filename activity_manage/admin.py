from django.contrib import admin
from .models import ActModel, ActAttendModel, ActAuditModel


admin.site.register(ActModel)
admin.site.register(ActAttendModel)
admin.site.register(ActAuditModel)