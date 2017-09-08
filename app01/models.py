from django.db import models

# Create your models here.
from django import forms
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.BigAutoField(primary_key=True, verbose_name="编号")
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    telephone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    avatar = models.FileField(upload_to='./img/avatar/', verbose_name='头像')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  through_fields=('user', 'follower'))

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class UserFans(models.Model):
    """
    互粉关系表
    """
    nid = models.AutoField(primary_key=True, verbose_name='编号')
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers')

    class Meta:
        verbose_name = "互粉关系"
        verbose_name_plural = verbose_name
        unique_together = [
            ('user', 'follower'),
        ]


class MyBlog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客信息"
        verbose_name_plural = verbose_name


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(verbose_name='分类标题', max_length=32)

    blog = models.ForeignKey(verbose_name='所属博客', to='MyBlog', to_field='nid')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博主个人文章分类表"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    文章
    """
    nid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='MyBlog', to_field='nid')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "GoLang"),
    ]

    article_type_id = models.IntegerField(choices=type_choices, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True, default=1)
    content = models.TextField(verbose_name='文章内容', )

    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')

    class Meta:
        verbose_name = "文章内容"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    parent_id = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')

    up_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    article = models.ForeignKey("Article", null=True)
    UpOrDown = models.BooleanField(verbose_name='是否赞', default=False)

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name


class CommentUp(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    comment = models.ForeignKey("Comment", null=True)


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='MyBlog', to_field='nid')


class
    (models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]


class CaptchaTestForm(forms.Form):
    '''
    验证码captcha组件
    '''
    from captcha.fields import CaptchaField

    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField()
