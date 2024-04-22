from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': 'Please pass in the username! ',
        "max_length": 'The length of username is between 2 and 20! ',
        "min_length": 'The length of the username is between 2 and 20! '
    })
    email = forms.EmailField(error_messages={"required": 'Please enter your email！', 'invalid': 'Please enter a correct email!'})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()  # 判断该邮箱是否已经存在
        if exists:
            raise forms.ValidationError('This email has been registered!')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')   # 首先拿到captcha
        email = self.cleaned_data.get('email')       # 还需要将email拿到，以便匹配captcha是否正确

        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first() # 若存在则返回第一条数据
        if not captcha_model:   # 当邮箱和验证码不存在于表中，即邮箱和验证码有误时
            raise forms.ValidationError("Captcha and email do not match!")
        captcha_model.delete()   # 存在于表中的话，则用完之后就把captcha删除
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": 'Please enter your email！', 'invalid': 'Please enter a correct email!'})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)
