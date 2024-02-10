

from django import forms
from django.forms import widgets
from app01.models import Userinfo
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
class UserForms(forms.Form):
    username = forms.CharField(max_length=12,
                               min_length=3,
                               error_messages={'required': '该字段不能为空'},
                               label='用户名'
                               )
    password = forms.CharField(max_length=12,
                               min_length=6,
                               error_messages={'required': '该字段不能为空'},
                               label='密码',
                               widget=widgets.PasswordInput())
    re_password = forms.CharField(max_length=12,
                                  min_length=6,
                                  error_messages={'required': '该字段不能为空'},
                                  label='确认密码',
                                  widget=widgets.PasswordInput())
    telephone = forms.CharField(min_length=11,
                                error_messages={'required': '该字段不能为空'},
                                label='手机号')


    def clean_username(self):
        user = self.cleaned_data.get('username')
        print(user)
        userinfo = Userinfo.objects.filter(username=user).filter()

        if not userinfo:
            return user
        else:
            raise ValidationError('该用户已注册')


    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')

        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')