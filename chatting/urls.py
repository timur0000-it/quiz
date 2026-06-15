from django.urls import path,include

from .views import *
app_name = 'chatting'

urlpatterns = [
    path('all_rooms/', all_rooms, name='all_rooms'),
    path('create_room/', create_room, name='create_room'),
    path('delete_room/<int:room_id>', delete_room, name='delete_room'),
    path('chat_room/<int:room_id>', chat_room, name='chat_room'),
    path('teacher_cabinet/', teacher_cabinet, name='teacher_cabinet'),
]
