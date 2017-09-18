
from django.conf.urls import url
from app01 import views

urlpatterns = [
    url("articleUpDown/$", views.articleUpDown),
    url("commentUpDown/$", views.commentUpDown),
    url("comment/$", views.comment),
    url("(?P<user_site>\w+)/$", views.showTime),
    url("(?P<user_site>\w+)/article/(?P<article_id>\d+)", views.articleDetail),
    url("(?P<user_site>\w+)/article2/(?P<article_id>\d+)", views.articleDetail2),
    url("(?P<user_site>\w+)/article/(?P<classify>category|tag)/(?P<para>\w+)", views.showTime),
    url("(?P<user_site>\w+)/article/(?P<classify>date)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)", views.showTime),
    url("article/(?P<classify>category|tag)/(?P<para>\w+)", views.index),
    url("article/(?P<classify>date)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)", views.index),
]
