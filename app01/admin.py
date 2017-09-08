from django.contrib import admin

# Register your models here.

from app01.models import UserInfo, UserFans, MyBlog, Category, Article, ArticleDetail, Comment, ArticleUpDown, CommentUp, Tag, Article2Tag

admin.site.register(UserInfo)
admin.site.register(UserFans)
admin.site.register(MyBlog)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(ArticleDetail)
admin.site.register(Comment)
admin.site.register(ArticleUpDown)
admin.site.register(CommentUp)
admin.site.register(Tag)
admin.site.register(Article2Tag)