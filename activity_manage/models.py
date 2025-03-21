from datetime import datetime
from django.db import models
from user_manage.models import UserModel

# Create your models here.


# 活动模型

class ActModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    title = models.CharField(max_length=100, default='', verbose_name='标题')
    content = models.TextField(max_length=200, default='', verbose_name='内容')
    act_time = models.DateTimeField(default=datetime.now)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    is_active = models.BooleanField(max_length=1, default=1, verbose_name='是否可用')
    image = models.ImageField(upload_to='media', verbose_name='活动图片')

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
    
# 活动参与模型, 用于记录用户参与的活动
# 一个用户可以参与多个活动, 一个活动可以被多个用户参与
class ActAttendModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    act = models.ForeignKey(ActModel, on_delete=models.CASCADE, verbose_name='关联活动')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    is_active = models.BooleanField(max_length=1, default=1, verbose_name='是否可用')

    class Meta:
        verbose_name = '活动参与'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.act.title
    


# 审核模块
class ActAuditModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    act = models.ForeignKey(ActModel, on_delete=models.CASCADE, verbose_name='关联活动')
    message = models.CharField(max_length=100, default='审核不通过', verbose_name='审核信息')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    is_active = models.BooleanField(max_length=1, default=1, verbose_name='是否可用')

    class Meta:
        verbose_name = '活动审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.act.title