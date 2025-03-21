from django.contrib import admin
from .models import UserModel, RegisterAuditModel

admin.site.register(UserModel)
admin.site.register(RegisterAuditModel)