from django.urls import path
from activity_manage import views

app_name = 'activity_manage'
urlpatterns =[
    path('add', views.add_act_view, name='add'),
    path('change/<int:a_id>', views.change_view, name='change'),
    path('act_list', views.list_view, name='act_list'),
    path('delete/<int:a_id>', views.delete_view, name='delete'),
    path('admin_list', views.admin_list_view, name='admin_list'),
    path('attend_act/<int:act_id>', views.attend_act_view, name='attend_act'),
    path('attend_list', views.my_act_view, name='attend_list'),
    path('cancel_attend/<int:act_id>', views.cancel_attend_view, name='cancel_attend'),
]