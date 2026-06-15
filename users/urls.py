from django.urls import path,include

from .views import *
app_name = 'users'

urlpatterns = [
    path('', signup,name='signup'),
    path('signin/', signin, name='signin'),
    path('verify_code/', verify_code, name='verify_code'),
    path('re_send_code/', re_send_code, name='re_send_code'),
    path('signout/', signout, name='signout'),
   
]
