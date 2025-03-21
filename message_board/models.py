from django.db import models
from user_manage.models import UserModel
from activity_manage.models import ActModel

# Create your models here.


# 活动页面的留言版，显示有哪些用户参与了活动，以及他们的留言，留言时间
# 一个用户可以参与多个活动，一个活动可以有多个用户参与
# 一个用户可以在多个活动中留言，一个活动可以有多个用户留言
class MessageActBoard(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    act = models.ForeignKey(ActModel, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, verbose_name='留言')
    message_time = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '活动留言板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message
    


# 用户页面的留言板，显示有哪些用户给该用户留言，留言时间
# 一个用户可以给多个用户留言，一个用户可以被多个用户留言

class MessageUserBoard(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user', verbose_name='用户')
    message_user = models.CharField(max_length=20, default='系统', verbose_name='留言用户')
    message_time = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    message = models.TextField(max_length=1000, verbose_name='留言')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '用户留言板'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.message
    

# 留言审核模型，用于记录留言审核信息，包括审核信息和审核状态，审核状态为0表示未审核，1表示审核通过，0表示审核不通过
# 一个留言只能有一条审核信息，一个审核信息只能对应一个留言

class MessageAuditModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    message = models.ForeignKey(MessageActBoard, on_delete=models.CASCADE, verbose_name='关联留言')
    message_audit = models.CharField(max_length=100, default='审核不通过', verbose_name='审核信息')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    is_active = models.BooleanField(max_length=1, default=1, verbose_name='是否可用')
    is_pass= models.BooleanField(max_length=1, default=0, verbose_name='是否通过')

    class Meta:
        verbose_name = '留言审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message.message