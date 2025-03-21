from django.shortcuts import redirect, render
from .models import MessageActBoard, MessageUserBoard
from activity_manage.models import ActModel
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def message_board_view(request, act_id):
    try:
        act = ActModel.objects.get(id=act_id, is_active=1)
    except ActModel.DoesNotExist:
        return HttpResponse('error: 活动不存在')
    
    if request.method == 'POST':
        MessageActBoard.objects.create(act=act, user=request.user, message=request.POST['message_act_board'])
        return redirect('activity_manage:attend_act', act_id=act_id)
    else:
        return HttpResponse('请使用POST请求')


@login_required  
def message_list_view(request):
    message_list = MessageUserBoard.objects.filter(user=request.user, is_active=1).order_by('-message_time')
    return render(request, 'message_board/message_board.html', {'message_list': message_list})



@login_required
def delete_message_view(request, l_id):
    try:
        message = MessageUserBoard.objects.get(id=l_id, user=request.user, is_active=1)
        message.is_active = 0
        message.save()
        return redirect('message_board:message_list')
    except MessageUserBoard.DoesNotExist:
        return HttpResponse('error: 信息不存在')
    