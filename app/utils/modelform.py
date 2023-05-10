# 导入django的shortcuts使用函数返回的参数,到达html或者是直接返回或重定向
from django.shortcuts import render, HttpResponse, redirect
# 导入要使用到的数据库模块
from app.models import *
# 使用到这里面时可以抛出异常
from django.core.exceptions import ValidationError
# 使用到这个core中的validators里面的添加验证器
from django.core import validators
# 使用到分页时,需要向上取整
import math
# 由于靓号列表中返回的内容,但是前端页面显示的是代码,与逾期不一样,是字符串而不是编译为html,需要标记为安全的
from django.utils.safestring import mark_safe
from app.utils.bootstrap import BootStrapModelForm
from django import forms


#  ################################  ModelForm  ################################
# 使用到ModelForm就要用到django的一个类forms，所以要导入

class UserModelForm(BootStrapModelForm):
    # 单独给name加上校验，例如长度校验最大为3，由于这里重新定义了name，那么在被页面使用的时候就是下面这种校验了
    # name = forms.CharField(max_length=3, label="请输入用户名")
    #  models中的定义是：name = models.CharField(verbose_name="姓名", max_length=64)
    class Meta:
        model = UserInfo  # 注意这里是用model而不是models，因为我们只是用到几个，而不是这张表的全部字段

        # 这里定义这个fields的字段是哪一些
        fields = ["name", "password", "account", "age", "create_time", "zone", "depart", "gender"]
        """ 下面这么写给每一个都加上样式也可以，但是这么做会比较麻烦 """
        """ fields这里面的内容是【一个字段名+字段对应的对象，典型的例子部门depart】
        {'name': <django.forms.fields.CharField object at 0x000002979134F4F0> 
         'password': <django.forms.fields.CharField object at 0x000002979134F400>
         'account': <django.forms.fields.DecimalField object at 0x000002979134F5B0>
         'age': <django.forms.fields.IntegerField object at 0x000002979134F3D0>, ......
        """
        #   = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }
        """ 使用下面这种方法，比较开发 """

    # 重新定义__init__的方法


# 下面这个方法中的form来自上面这个类

class PrettyNumForm(BootStrapModelForm):
    mobile = forms.CharField(
        label='手机号码',
        max_length=11, min_length=11,
        error_messages={
            'max_length': '手机号不能超过11位数字！',
            'min_length': '手机号不能少于11位数字！',
            'required': '请输入手机号！',
        },
        validators=[validators.RegexValidator(r'^1[3-9]\d{9}$', '输入的手机号格式有误,请重新输入!')],
    )

    class Meta:
        model = PrettyNum
        # 验证:方式1 mobile 这个字段用户在输入时的格式

        # fields = ["mobile", "price", "level", "status", "zone"]
        fields = '__all__'  # 默认所有字段
        # exclude = ["mobile"]  # 排除哪个字段

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if PrettyNum.objects.filter(mobile=txt_mobile).exists():
            raise ValidationError("手机号已存在,请修改!")

    # 验证:方式2 mobile 这个字段用户在输入时的格式
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data["mobile"]
    #     if len(txt_mobile) != 11:
    #         raise ValidationError("输入的手机号格式有误,请重新输入!")
    #     return txt_mobile


class PrettyEditNumForm(BootStrapModelForm):
    # mobile = forms.CharField(
    #     label="手机号码",
    #     disabled=True,  # 设置该字段编辑的时候只显示而不可编辑
    #     validators = [validators.RegexValidator(r'^1[3-9]\d{9}$', '输入的手机号格式有误,请重新输入!')],
    #
    # )
    class Meta:
        model = PrettyNum
        fields = '__all__'  # 默认所有字段
        # exclude = ["zone"]  # 可以设置不显示哪个字段,也就是编辑的时候不显示给用户编辑


    # 钩子函数用法
    def clean_mobile(self):
        # 当前编辑的是哪一行ID:self.instance.pk  pk是主键
        txt_mobile = self.cleaned_data["mobile"]  # 获取用户输入的号码
        exists = PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("该手机号已存在")
        return txt_mobile


