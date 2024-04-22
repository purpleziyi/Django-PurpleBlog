from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail

from pzauth.models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User

User = get_user_model()



# Create your views here.
@require_http_methods(['GET', 'POST'])
def pzlogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():  # 如果验证成功
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password): # 如果此用户存在且密码也正确
                # 登录  (params分别是request 和 需要登录的user对象)
                login(request, user)
                user.is_authenticated     # Django内置user有is_authenticated属性，该属性可以判断用户有没有登录
                # 判断是否需要记住我
                if not remember:
                    # 如果没有点击记住我，那么就要设置过期时间为0，即浏览器关闭后就会过期
                    request.session.set_expiry(0)
                # 如果点击了，那么就什么都不做，使用默认的2周的过期时间
                return redirect('/')
            else:
                print('Email or password is incorrect!')
                # form.add_error('email', '邮箱或者密码错误！')
                # return render(request, 'login.html', context={"form": form})
                return redirect(reverse('pzauth:login'))

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password) # create_user会将pwd加密后存储
            return redirect(reverse('pzauth:login'))
        else:
            print(form.errors)
            # 重新跳转到登录页面
            return redirect(reverse('pzauth:register'))
            # return render(request, 'register.html', context={"form": form})

def pzlogout(request):
    logout(request)
    return redirect('/')


def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": 'must provide email'})
    # Generate verification code （Take a random 4-digit number）
    captcha = "".join(random.sample(string.digits, 4))  # samlpe: ['0', '2', '9', '8']
    # store to database
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail("purpleblog registration verification code", message=f"your verification code is：{captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code": 200, "message": "Email verification code sent successfully！"})