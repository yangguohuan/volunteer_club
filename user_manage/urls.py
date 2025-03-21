from django.urls import path
from user_manage import views

app_name = 'user_manage'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register',views.register_view, name='register'),
    path('login',views.login_view, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('user_info', views.user_info_view, name='user_info'),
    path('change_info', views.change_info_view, name='change_info'),
    path('user_list', views.user_list, name='user_list')
]