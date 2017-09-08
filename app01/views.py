from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
from app01.models import CaptchaTestForm
from app01 import forms
import json
from django.db.models import Avg, Min, Sum, Max, Count

# 非ajax方法，且有验证码

# def login(request):
#
#     if request.method == "POST":
#         login_form = CaptchaTestForm(request.POST)
#         username = request.POST["username"]
#         password = request.POST["password"]
#
#         user = auth.authenticate(username=username, password=password)  # auto的方法，认证user，返回True
#
#         if user  :
#             auth.login(request, user)  # login user登陆
#             return redirect("/index/")
#         else:
#             print("error")
#     else:
#         login_form = CaptchaTestForm()
#     return render(request, "login.html", {"login_form": login_form, })

def login(request):
    '''
    登陆
    :param request:
    :return:
    '''
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        valid_code = request.POST.get("valid_code", "")

        if valid_code.upper() == request.session["valid_code"].upper():
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                print(request.POST)
                return HttpResponse('{"status":"success"}')  #content_type='application/json'
            else:
                return HttpResponse('{"status":"error"}')
        else:
            return HttpResponse('{"status":"code_error"}')
    return render(request, "login.html")


@login_required()
def logout(request):
    '''
    登出
    :param request:
    :return:
    '''
    auth.logout(request)
    auth.logout(request)
    return render(request, "login.html")


# 非form形式
# def register(request):
#     error_messages = ""
#
#     if request.method == "POST":
#         username = request.POST.get("username")  # get方法可以设置默认值
#         # print("user:", username)
#         password = request.POST.get("password", None)
#         # print("pwd:",password)
#         re_password = request.POST.get("re_password", None)
#
#         if not username:
#             error_messages = "用户不能为空"
#         elif not password or not re_password:
#             error_messages = "密码不能为空"
#         elif password != re_password:
#             error_messages = "密码不一致"
#         elif User.objects.filter(username=username):  # User需要提前引用，旗下有很多功能呢
#             error_messages = "用户已存在"
#         else:
#             User.objects.create_user(username=username, password=password)
#
#             return redirect("/login/")
#     form_obj = forms.RegForm()
#
#     return render(request, "register.html", {"error_messages": error_messages, "form_obj": form_obj, })


def register(request):
    '''
    注册
    :param request:
    :return:
    '''
    if request.is_ajax():
        form_obj = forms.RegForm(request, request.POST)
        response = {
            "flag": False,
            "errors": ""
        }

        if form_obj.is_valid():
            print(form_obj.cleaned_data)  # {"username":"ffdsgfds","password":2134szdf,...}
            username = form_obj.cleaned_data["username"]
            password = form_obj.cleaned_data["password"]
            mail = form_obj.cleaned_data["mail"]
            User.objects.create_user(username=username, password=password)
            response["flag"] = True
        else:
            errors = form_obj.errors  # ERRORdict:  {"username":[],"password":[],....}
            print("errors!!!====", errors)
            response["errors"] = errors
        return HttpResponse(json.dumps(response))

    form_obj = forms.RegForm(request.POST)
    return render(request, "register.html", {"form_obj": form_obj})


def index(request):
    '''
    主页
    :param request:
    :return:
    '''
    user = request.user.is_authenticated()
    username = request.user.username
    return render(request, "index.html", {"user": user, "username": username, })


def valid_code(request):
    '''
    验证码
    :param request:
    :return:
    '''
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    import random
    f = BytesIO()
    img = Image.new(mode='RGB', size=(120, 30),
                    color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    draw = ImageDraw.Draw(img, mode='RGB')

    font = ImageFont.truetype("app01/static/fonts/kumo.ttf", 28)

    code_list = []
    for i in range(5):
        char = random.choice([chr(random.randint(65, 90)), str(random.randint(1, 9))])
        code_list.append(char)
        draw.text([i * 24, 0], char, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                  font=font)

    img.save(f, "png")

    valid_code = ''.join(code_list)

    request.session["valid_code"] = valid_code

    return HttpResponse(f.getvalue())


# 个人界面

def show_time(request):

    Artcile.objects.values("category__blog").aggregate()

    return HttpResponse("OK")



# 测试代码

def test(request):
    if request.method == "POST":
        print("OK")
        user = request.POST.get("username", "")
        print(user)
    return render(request, "test_ajax.html")


# 模版全局变量

def func(request):
    from MyBlog import settings
    return {"func": settings.FUNCTION, }
