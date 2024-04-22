from django.urls import path
from . import views

app_name = 'pzauth'

urlpatterns = [
    path('login', views.pzlogin, name='login'),
    path('logout', views.pzlogin, name='logout'),
    path('register', views.register, name='register'),
    path('captcha',views.send_email_captcha,name='email_captcha')
]