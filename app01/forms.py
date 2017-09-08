#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "DaChao"
# Date: 2017/9/6

from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class RegForm(forms.Form):

    username = forms.CharField(min_length=1,
                               max_length=11,
                               widget=forms.TextInput(attrs={"class": "text username", "placeholder": "请输入账号"}),
                               error_messages={'required': '用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "text password", "placeholder": "请输入密码"}),
                               error_messages={'required': '密码不能为空'})
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "text re_password", "placeholder": "请再次输入密码"}),
                                  error_messages={'required': '密码不能为空'})
    mail = forms.EmailField(widget=forms.EmailInput(attrs={"class": "text mail", "placeholder": "请输入邮箱"}),
                            error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    valid_code = forms.CharField(widget=forms.EmailInput(attrs={"class": "text valid_code", "placeholder": "请输入验证码", "style": "color: #FFFFFF !important; position:absolute; z-index:100;", }),
                                 error_messages={'required': '验证码不能为空'})

    def __init__(self, request, *args, **kwargs):
        # forms.Form.__init__(self, *args, **kwargs)  # 继承父辈的方法一
        super(RegForm, self).__init__(*args, **kwargs)  # 继承父辈的方法二
        self.request = request

    def clean_username(self):
        if self.cleaned_data["username"].isdigit() or self.cleaned_data["username"].isalpha():
            raise ValidationError("用户名必须包含数字和字符！")
        else:
            return self.cleaned_data["username"]

    def clean_password(self):
        if len(self.cleaned_data["password"]) < 2:
            raise ValidationError("密码必须大于1位！")
        else:
            return self.cleaned_data["password"]

    def clean_valid_code(self):
        if self.cleaned_data["valid_code"].upper() == self.request.session["valid_code"].upper():
            return self.cleaned_data["valid_code"]
        else:
            raise ValidationError("验证码错误！")

    def clean(self):
        '''
        全局钩子，
        注意：password在局部钩子未通过后，为无,直接字典取值，会报错
        :return:
        '''
        if self.cleaned_data.get("password") != self.cleaned_data.get("re_password"):
            raise ValidationError("密码必须一致！")
        else:
            return self.cleaned_data
