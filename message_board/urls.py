from django.urls import path
from message_board import views

app_name = 'message_board'
urlpatterns = [
    path('message_board/<int:act_id>', views.message_board_view, name='message_board'),
    path('message_list/', views.message_list_view, name='message_list'),
    path('delete_message/<int:l_id>', views.delete_message_view, name='delete_message'),
]