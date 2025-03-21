import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ActModel, ActAttendModel
from message_board.models import MessageUserBoard



# 管理员添加活动

@login_required
def add_act_view(request):



    if request.user.username != 'admin':
        return HttpResponse('只有管理员可以添加、删除、修改活动')
    
    if request.method == 'POST':
        # 获取上传的文件和表单数据
        image = request.FILES.get('pic')
        title = request.POST.get('title')
        content = request.POST.get('content')
        act_time = request.POST.get('act_time')

        # 确保目录存在
        media_path = os.path.join(settings.BASE_DIR, 'static', 'media')
        os.makedirs(media_path, exist_ok=True)

        # 保存图片到 /static/media/ 目录下
        image_path = os.path.join(media_path, image.name)
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # 保存路径到数据库（相对路径）
        relative_image_path = f'static/media/{image.name}'
        ActModel.objects.create(
            user=request.user,
            image=relative_image_path,
            title=title,
            content=content,
            act_time=act_time
        )

        # 重定向到活动列表页面
        return redirect('activity_manage:admin_list')
    
    return render(request, 'activity_manage/add_act.html')




# 管理员修改活动

@login_required
def change_view(request, a_id):

    if request.user.username != 'admin':
        return HttpResponse('只有管理员可以添加、删除、修改活动')
    else:
        try:
            form = ActModel.objects.get(id=a_id, is_active=1)
        except Exception:
            return HttpResponse('未匹配到参数')
        if request.method == 'POST':
            form.title = request.POST['title']
            form.content = request.POST['content']
            form.save()
            return redirect('activity_manage:admin_list')
        context = {'a_id': form.id, 'form': form}
        return render(request, 'activity_manage/act_info.html', context)



# 普通用户查看活动列表

def list_view(request):
    act_list = ActModel.objects.filter(is_active=1).order_by('-date_added')
    context = {'act_list': act_list}
    return render(request, 'activity_manage/act_list.html', context)




# 管理员删除活动

@login_required
def delete_view(request, a_id):
    if request.user.username == 'admin':
        act_info = ActModel.objects.get(is_active=1, id=a_id)
        act_info.is_active = 0
        act_info.save()
        return redirect('activity_manage:admin_list')
    else:
        return HttpResponse('只有管理员可以添加、删除、修改活动')



# 管理员后台管理活动列表

@login_required
def admin_list_view(request):
    if request.user.username == 'admin':
        act_list = ActModel.objects.filter(is_active=1).order_by('-date_added')
        context = {'act_list': act_list}
        return render(request, 'activity_manage/admin_act_list.html', context)
    else:
        return HttpResponse('只有管理员可以添加、删除、修改活动')
    



# 普通用户查看活动详情，以及留言板，参加活动

@login_required
def attend_act_view(request, act_id):
    act_info = ActModel.objects.get(id=act_id)
    list = message_list(act_info)     # 获取留言板信息
    user_list = ActAttendModel.objects.filter(act=act_info, is_active=1)
    had_attend = 0
    for i in user_list:
        if i.user == request.user:
            had_attend = 1
            break
    context = {'act_info': act_info, 'message_list': list, 'user_list': user_list, 'had_attend': had_attend}

    if request.method == 'POST':
        act_attend = ActAttendModel.objects.filter(act=act_info, is_active=1, user=request.user)
        if act_attend:
            return HttpResponse('您已经参加过该活动')
        ActAttendModel.objects.create(user=request.user, act=act_info)  # 参加活动
        notice(request.user, f'您已成功参加标题为 - {act_info.title} - 的活动')  # 通知用户参加活动成功
        return HttpResponse('参加成功，请留意系统通知')
    else:
        return render(request, 'activity_manage/attend_act.html', context)

        
    
# 普通用户查看自己参加的活动

@login_required
def my_act_view(request):
    attend_list = ActAttendModel.objects.filter(user=request.user, is_active=1).order_by('-date_added')
    context = {'attend_list': attend_list}
    return render(request, 'activity_manage/attend_list.html', context)


# 普通用户取消参加活动

@login_required
def cancel_attend_view(request, act_id):
    if request.method == 'POST':
        try:
            act_attend = ActAttendModel.objects.get(id=act_id, is_active=1, user=request.user)
        except ActAttendModel.DoesNotExist:
            return HttpResponse('您未参加该活动')
        act_attend.is_active = 0
        act_attend.save()
        notice(request.user, f'您已取消参加标题为 - {act_attend.act.title} - 的活动')  # 通知用户参加活动成功
        return redirect('activity_manage:attend_list')
    else:
        return HttpResponse('非法请求')
    


#
# 以下非视图函数
#
# 获取留言板信息,并按照时间排序，最新的在最前面，普通函数，不是视图函数

def message_list(act):
    from message_board.models import MessageActBoard
    message_list = MessageActBoard.objects.filter(act=act, is_active=1).order_by('-message_time')
    return message_list



## 通知函数，给用户发送通知
# 通知用户参加活动成功,参数为用户对象，活动标题
# 该函数不是视图函数，只是一个普通函数

def notice(user, message, *username):
    if username:
        message = MessageUserBoard.objects.create(user=user, username=username, message=message)
    else:
        message = MessageUserBoard.objects.create(user=user, message=message)
    message.save()