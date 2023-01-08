from django import forms
from captcha.fields import CaptchaField

class PostForm(forms.Form):
    username = forms.CharField(max_length=28, initial='請輸入會員帳號')
    pwd = forms.CharField(max_length=28, initial='請輸入密碼', widget=forms.PasswordInput())
    captcha = CaptchaField()