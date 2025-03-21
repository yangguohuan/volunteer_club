from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    user_type = models.DecimalField(max_digits=1, decimal_places=0, default=1, verbose_name='用户类型') # 1 为志愿者，2 为长者 ，3 为长者家属， 4 为管理员
    service_duration = models.DecimalField(max_digits=100, max_length=100, decimal_places=0, default=0, verbose_name='服务时长')
    signature = models.TextField(max_length=200, verbose_name='个性签名')
    data_added = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
    

# 注册审核模型，用于记录用户注册审核信息，包括审核信息和审核状态，审核状态为0表示未审核，1表示审核通过，0表示审核不通过
# 一个用户只能有一条注册审核信息，一个注册审核信息只能对应一个用户

class RegisterAuditModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    message = models.CharField(max_length=100, default='审核不通过', verbose_name='审核信息')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    is_active = models.BooleanField(max_length=1, default=1, verbose_name='是否可用')
    is_pass= models.BooleanField(max_length=1, default=0, verbose_name='是否通过')

    class Meta:
        verbose_name = '注册审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username