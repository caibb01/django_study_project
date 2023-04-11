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


# 部门管理
def depart_list(request):
    """获取部门列表数据"""
    if request.method == "GET":
        # 获取数据库的部门列表数据，返回一行一行，每一行是一个对象
        depart_list = Department.objects.all()
    return render(request, 'depart_list.html', {"depart_list": depart_list})


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户POST提交过来的数据
    title = request.POST.get("title")

    # 将用户提交的数据保存到数据库
    Department.objects.create(title=title)

    # 重定向到部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""

    # 获取ID http://127.0.0.1:8000/depart/delete/?id=?
    mid = request.GET.get("id")

    # 到数据库删除对应的数据
    Department.objects.filter(id=mid).delete()

    # 重定向到部门列表
    return redirect("/depart/list/")


# http://127.0.0.1:8000/depart/8/edit/
# http://127.0.0.1:8000/depart/2/edit/
# http://127.0.0.1:8000/depart/5/edit/
# 上面这个就是html中的/depart/{{ obj.id }}/edit，然后和urls中的正则<int:edit_id>
def depart_edit(request, edit_id):
    """修改部门"""
    if request.method == "GET":
        # 根据edit_id 获取数据的[obj.id]
        row_object = Department.objects.filter(id=edit_id).first()
        return render(request, 'depart_edit.html', {"titles": row_object})

    # 获取用户提交的标题
    edit_title = request.POST.get("edit_title")

    # 根据ID找到数据库中的数据并进行更新
    Department.objects.filter(id=edit_id).update(title=edit_title)

    # 重定向会部门列表
    return redirect("/depart/list/")


# 用户管理
def user_list(request):
    """获取用户列表"""
    user_list = UserInfo.objects.all()
    # for u in user_list:
    #     print(
    #         u.id,
    #         u.name,
    #         u.password,
    #         u.age,
    #         u.create_time.strftime("%Y-%m-%d-%H-%M"),
    #         u.depart.title,
    #         u.get_gender_display(),
    #         u.zone
    #     )
    return render(request, 'user_list.html', {"user_list": user_list})


def user_add(request):
    """添加用户"""
    # 将参数作为字典放到前端获取的位置
    context = {'gender_choices': UserInfo.gender_choices,
               'depart_list': Department.objects.all()
               }
    if request.method == "GET":
        return render(request, "user_add.html", context)
    name = request.POST.get("name")
    password = request.POST.get("pwd")
    account = request.POST.get("ac")
    age = request.POST.get("age")
    create_time = request.POST.get("ctime")
    zone = request.POST.get("zone")
    depart_id = request.POST.get("depart")
    gender_id = request.POST.get("gender")
    print(depart_id, name)

    # 添加到数据库中
    UserInfo.objects.create(name=name, password=password, account=account, age=age, create_time=create_time, zone=zone
                            , depart_id=depart_id, gender=gender_id)
    return redirect("/user/list/")


#  ################################  ModelForm  ################################
# 使用到ModelForm就要用到django的一个类forms，所以要导入
from django import forms


class UserModelForm(forms.ModelForm):
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
    def __init__(self, *args, **kwargs):
        # 继承父类__init__的方法
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加"class": "form-control",
        for name, field in self.fields.items():
            # if name == "age":
            #     continue # 这里可以设置指定字段的样式
            # print(name, field)  # 查看返回的内容是什么
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


# 下面这个方法中的form来自上面这个类
def user_model_list_add(request):
    """ 添加用户 （ModelForm版本） """
    if request.method == "GET":
        form = UserModelForm()  # 实例化字段
        return render(request, 'user_modeladd.html', {"form": form})
    # 用户POST提交数据，数据校验
    form_data = UserModelForm(data=request.POST)
    if form_data.is_valid():
        # 如果数据合法 保存到数据库
        # {'name': '王志伟444', 'password': '41234', 'account': Decimal('123125'), 'age': 3, 'create_time': datetime.datetime(2022, 2, 8, 0, 0, tzinfo=backports.zoneinfo.ZoneI
        # nfo(key='UTC')), 'zone': '北京', 'depart': <Department: HR部门>, 'gender': 2}
        print(form_data.cleaned_data)
        form_data.save()
        return redirect('/user/list')
    return render(request, 'user_modeladd.html', {"form": form_data})


def user_model_edit(request, nid):
    """ 编辑用户 """

    # 由于读取GET和编辑保存POST时都需要知道是哪一条数据，故而可以把获取的数据统一放到这里来
    row_object = UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        # row_object = UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form})

    # 编辑数据时，填写后的内容要保存到哪一条数据需要，所以还需要写下面这一行
    # row_object = UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # save是默认保存的是用户输入的所有数据，如果想要在用户输入以外的字段增加值：
        # form.instance.字段 = 值
        form.instance.age = 15
        form.save()
        return redirect('/user/list')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    """  删除用户  """
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')


#  靓号管理

def prettynum_list(request):
    """ 靓号列表 """
    """ 手机号的分页功能 """
    # 获取查询返回的page是第几页
    from app.utils.pagination import Pagination
    Pagination(request)

    # page = request.GET. get("page", "1")
    # page = int(page)

    # # 设置每页要展示的数目
    # page_size = 10
    # # 给返回的数据设置切片    # 给用户返回第几页的内容
    # begin_n = (int(page) - 1) * page_size
    # end_n = int(page) * page_size
    # 查询结果总共有多少条数,相当于多少个页面
    total = int(PrettyNum.objects.all().count())
    max_page = math.ceil(total / page_size)
    # 根据查出的结果,根据页面一页要展示多少条数进行切片展示
    form = PrettyNum.objects.all().order_by("-level")[begin_n:end_n]

    page_str_list = []

    # 首页
    ele = '<li><a href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(ele)
    # 上一页
    if page > 1:
        ele = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        ele = '<li ><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(ele)

    # 页面
    # 设置显示当前页的前五页和后五页
    plus = 5
    # 当分页小于5页时,那就直接显示当前10页,判断极小值
    if page <= plus:
        start_page = 1
        end_page = plus * 2 + 1
    # 如果分页大于5页时,则需要判断极大值
    else:  # 如果当前页值+5页后 比 数据库页面最大值还大 那么就要起始值就应该是x , 结束值应该是数据库的最大页面值+1 因为索引取头不取尾
        if page + plus > max_page:
            start_page = max_page - plus * 2  # 这里就应该是从后往前推了
            end_page = max_page + 1
        else:
            start_page = page - plus
            end_page = page + plus + 1
    for i in range(start_page, end_page):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
        # page_str_list = mark_safe("".join(page_str_list)) 不能这么写 AttributeError: 'SafeString' object has no attribute 'append'
        # 证明这个字符串是安全的,以便在前端页面展示
        # 下一页
    if page < max_page:
        ele = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        ele = '<li><a href="?page={}">下一页</a></li>'.format(max_page)
    page_str_list.append(ele)
    ele = '<li><a href="?page={}">尾页</a></li>'.format(max_page)
    page_str_list.append(ele)

    search_string = """
    <li>
       <form style="float: right" method="get">
           <input type="text" name="page" class="form-control"
                  style="position: relative;float: left;display: inline-block;width: 180px;border-radius: 10;"
                  placeholder="请输入要跳转至的页面数">
           <button class="btn btn-default" type="submit">跳转</button>
       </form>
    </li>
    """
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))

    """ 手机号的搜索功能 """
    # 获取页面传来的get的num内容,通过内容进行搜索,并返回给页面
    search_num = request.GET.get("num", '')
    # 将查询的条件字典化
    search_dict = {"mobile__contains": search_num}
    return render(request, 'prettynum_list.html',
                  {"form": form, "search_num": search_num, "page_str_list": page_string})


class PrettyNumForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, fild in self.fields.items():
            fild.widget.attrs = {"class": "form-control", "placeholder": fild.label}

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


def prettynum_add(request):
    if request.method == 'GET':
        form = PrettyNumForm()
        return render(request, 'prettynum_add.html', {"form": form})
    # 接收页面返回的内容
    prettynum_add_data = PrettyNumForm(data=request.POST)
    # 判断是否合法,合法就保存到数据库并重定向到主页
    if prettynum_add_data.is_valid():
        prettynum_add_data.save()
        return redirect("/prettynum/list")
    return render(request, 'prettynum_add.html', {"form": prettynum_add_data})


class PrettyEditNumForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, fild in self.fields.items():
            fild.widget.attrs = {"class": "form-control", "placeholder": fild.label}

    # 钩子函数用法
    def clean_mobile(self):
        # 当前编辑的是哪一行ID:self.instance.pk  pk是主键
        txt_mobile = self.cleaned_data["mobile"]  # 获取用户输入的号码
        exists = PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("该手机号已存在")
        return txt_mobile


def prettynum_edit(request, nid):
    # 展示编辑页面的数据为所点击的数据
    row_object = PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditNumForm(instance=row_object)
        return render(request, 'prettynum_edit.html', {"form": form})
    form = PrettyEditNumForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.instance.zone = "北京"
        form.save()
        return redirect("/prettynum/list")
    return render(request, 'prettynum_edit.html', {"form": form})


def prettynum_delete(request, nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect("/prettynum/list")
    # return render(request, 'prettynum_edit.html', {"form": form})
