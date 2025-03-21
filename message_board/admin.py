from django.contrib import admin
from .models import MessageActBoard, MessageUserBoard, MessageAuditModel

# Register your models here.
admin.site.register(MessageActBoard)
admin.site.register(MessageUserBoard)
admin.site.register(MessageAuditModel)