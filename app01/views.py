from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
# from django.contrib.auth.models import User
from app01.admin import UserInfo as User
from django.contrib.auth.decorators import login_required

# Create your views here.
from app01.models import CaptchaTestForm
from app01 import forms
import json
from django.db.models import Avg, Min, Sum, Max, Count, F, Q
from app01.models import Article, Comment, ArticleUpDown, CommentUp, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
                return HttpResponse('{"status":"success"}')  # content_type='application/json'
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


def index(request, **kwargs):
    '''
    主页
    :param request:
    :return:
    '''
    user = request.user.is_authenticated()
    username = request.user.username
    article_list = Article.objects.all()
    category_list = Article.objects.values("category__name").annotate(Count("nid"))
    tag_list = Article.objects.values("tags__title").annotate(Count("nid"))
    date_list = Article.objects.datetimes("create_time", "day", order="DESC").annotate(Count("nid"))

    if kwargs.get("classify"):
        obj = kwargs.get("classify")
        if obj == "category":
            obj_name = kwargs.get("para")
            article_list = Article.objects.filter(category__name=obj_name)
        elif obj == "tag":
            obj_name = kwargs.get("para")
            article_list = Article.objects.filter(tags__title=obj_name)
        elif obj == "date":
            year_n = kwargs.get("year")
            month_n = kwargs.get("month")
            day_n = kwargs.get("day")
            article_list = Article.objects.filter(create_time__year=year_n, create_time__month=month_n,
                                                  create_time__day=day_n)

    return render(request, "index.html",
                  {"user": user,
                   "username": username,
                   "article_list": article_list,
                   "category_list": category_list,
                   "tag_list": tag_list,
                   "date_list": date_list,
                   })


# 个人管理后台

def myEditBack(request, usersite):
    article_list = Article.objects.filter(blog__user__username=usersite)

    article_obj = Paginator(article_list, 3)
    page = request.GET.get('page')
    try:
        articles = article_obj.page(page)
    except PageNotAnInteger:
        articles = article_obj.page(1)
    except EmptyPage:
        articles = article_obj.page(article_obj.num_pages)

    return render(request, "myEditBack.html", {
        "article_obj": article_obj,
        "articles": articles
    })


# 添加文章

def addArticle(request):
    if request.method == "POST":
        content = request.POST.get("article_content")

        return render(request, "showContent.html", {"content": content})

    return render(request, "addArticle.html")


# 删除文章

def delArticle(request):
    if request.method == 'POST':
        try:
            article_id = request.POST.get('article_id', 0)
            Article.objects.filter(nid=article_id).delete()
        except Exception as e:
            print(e)
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        return HttpResponse('{"status":"success"}', content_type='application/json')


# 个人界面

def showTime(request, **kwargs):
    """
    博主界面
    :param request:
    :return:
    """
    username = kwargs.get("user_site")
    article_list = Article.objects.filter(blog__user__username=username)
    category_list = article_list.values("category__name").annotate(Count("nid"))
    tag_list = article_list.values("tags__title").annotate(Count("nid"))
    date_list = article_list.datetimes("create_time", "day", order="DESC").annotate(Count("nid"))
    article_num = len(article_list)

    if kwargs.get("classify"):
        obj = kwargs.get("classify")
        if obj == "category":
            obj_name = kwargs.get("para")
            article_list = article_list.filter(category__name=obj_name)
        elif obj == "tag":
            obj_name = kwargs.get("para")
            article_list = article_list.filter(tags__title=obj_name)
        elif obj == "date":
            year_n = kwargs.get("year")
            month_n = kwargs.get("month")
            day_n = kwargs.get("day")
            article_list = article_list.filter(create_time__year=year_n, create_time__month=month_n,
                                               create_time__day=day_n)

    return render(request, "showTime.html",
                  {"username": username,
                   "article_list": article_list,
                   "category_list": category_list,
                   "tag_list": tag_list,
                   "date_list": date_list,
                   "article_num": article_num,
                   })


# 文章内容

def articleDetail(request, user_site, article_id):
    article_obj = Article.objects.filter(nid=article_id).first()
    comment_obj = Comment.objects.filter(article_id=article_id)

    return render(request, "articleDetail.html", {
        "article_obj": article_obj,
        "comment_obj": comment_obj
    })


# 文章内容，第二种：多级评论
def articleDetail2(request, user_site, article_id):
    if request.is_ajax():

        comment_list = Comment.objects.filter(article_id=article_id).values("nid", "content", "parent_id_id", "create_time", "up_count", "down_count", "user__nickname")
        # print("comment_list", comment_list)

        import collections

        comment_dict = collections.OrderedDict()

        i = 0
        for comment in comment_list:
            i +=1
            comment["children_comments"] = []
            comment["id"] = i
            comment["create_time"] = str(comment["create_time"])[:16]
            comment_dict[comment["nid"]] = comment

        ret = []

        for comment in comment_dict:
            if comment_dict[comment]["parent_id_id"]:
                pid = comment_dict[comment]["parent_id_id"]
                comment_dict[pid]["children_comments"].append(comment_dict[comment])
            else:
                ret.append(comment_dict[comment])
        print("ret", ret)

        return HttpResponse(json.dumps(ret))

    # comment_list = Comment.objects.all()
    #
    # # print("comment_list", comment_list)  # [obj,obj]
    #
    # comment_list2 = Comment.objects.values("nid", "content", "parent_id_id")
    #
    # print("comment_list2", comment_list2)

    article_obj = Article.objects.filter(nid=article_id).first()
    comment_list = Comment.objects.filter(article_id=article_id)

    return render(request, "articleDetail2.html", {
        "comment_list": comment_list,
        "article_obj": article_obj
    })


# 文章点赞

def articleUpDown(request):
    article_id = request.POST.get("article_id")
    user_id = request.user.nid

    response = {"flag": True}
    if ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id):
        response["flag"] = False
    else:
        ArticleUpDown.objects.create(user_id=user_id, article_id=article_id)
        Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)

    return HttpResponse(json.dumps(response))


# 评论点赞

def commentUpDown(request):
    comment_id = request.POST.get("comment_id")
    user_id = request.user.nid

    response = {"flag": True}
    if CommentUp.objects.filter(user_id=user_id, comment_id=comment_id):
        response["flag"] = False
    else:
        CommentUp.objects.create(user_id=user_id, comment_id=comment_id)
        Comment.objects.filter(nid=comment_id).update(up_count=F("up_count") + 1)

    return HttpResponse(json.dumps(response))


# 评论

def comment(request):
    user_id = request.user.nid
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")

    if request.POST.get("parent_comment_id"):
        parent_comment_id = int(request.POST.get("parent_comment_id"))
        comment_obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content,
                                             parent_id_id=parent_comment_id)
    else:
        comment_obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content)
    Article.objects.filter(nid=article_id).update(comment_count=F("comment_count") + 1)

    responses = {"comment_id": comment_obj.nid,
                 "comment_createTime": str(comment_obj.create_time)[:16],
                 "up_count": comment_obj.up_count,
                 "down_count": comment_obj.down_count}

    return HttpResponse(json.dumps(responses))


# 验证码

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


# 模版全局变量

def func(request):
    from MyBlog import settings
    return {"func": settings.FUNCTION, }
