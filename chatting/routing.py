from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
    # ws://127:0.0.1:8000/ws/echo
    re_path(r'ws/chat/(?P<username>[^/]+)/(?P<user_id>[^/]+)/(?P<room_id>[^/]+)/$',ChatConsumer.as_asgi()),
    # re_path(r'ws/teacher/$',TeacherConsumer.as_asgi()),
    # re_path(r'ws/answer/$',AnswerConsumer.as_asgi()),

]