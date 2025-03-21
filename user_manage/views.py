from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import UserModel
from .forms import UserLoginForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser


# Create your views here.


def index_view(request):
    return render(request, 'user_manage/index.html')


def register_view(request):
    if request.method == 'POST':
        msg = ''

        username = request.POST['username']
        if UserModel.objects.filter(username=username):
            msg = '用户名已存在'

        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            msg = '两次密码不一致'
        if password == '' or username == '':
            msg = '用户名或密码不能为空'

        email = request.POST['email']
        if email == '':
            msg = '邮箱不能为空'

        user_type = request.POST['user_type']
        if user_type == '':
            msg = '用户类型不能为空'


        # 如果没有输出错误信息代表，进入注册
        if msg:
            return render(request, 'user_manage/register.html', {'msg': msg})
        else:
            hashed_password = make_password(password)
            user = UserModel.objects.create(username=username, password=hashed_password, email=email, user_type=user_type)
            user.save()
            login(request, user)
            msg = '注册成功，请完善个人信息'
            return render(request, 'user_manage/user_info.html', {'msg': msg})
    else:
        return render(request, 'user_manage/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('user_manage:index')
        return HttpResponse('用户名或密码错误')
    elif request.method == 'GET':
        form = UserLoginForm
        context = {'form': form}
        return render(request, 'user_manage/login.html', context)
    else:
        return HttpResponse('请求方法错误')


@login_required
def logout_view(request):
    logout(request)
    return redirect('user_manage:index')

@login_required
def user_info_view(request):
    context = {'user': request.user}
    return render(request, 'user_manage/user_info.html', context)

@login_required
def change_info_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        signature1 = request.POST['signature']
        user = UserModel.objects.get(username=request.user.username)
        user.email = email
        user.signature = signature1
        user.save()
        return redirect('user_manage:user_info')
    else:
        return HttpResponse('请求方法错误')


def user_list(request):
    u_list = UserModel.objects.all()
    serializer = UserSerializer(u_list, many=True)
    return JsonResponse(serializer.data, safe=False)