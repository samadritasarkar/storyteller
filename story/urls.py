from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^read/(?P<article_id>[0-9]+)/$', views.read, name='read'),
    url(r'^create_article/$', views.create_article, name='create_article'),
    url(r'^(?P<article_id>[0-9]+)/create_chapter/$', views.create_chapter, name='create_chapter'),
    url(r'^(?P<article_id>[0-9]+)/delete_chapter/(?P<chapter_id>[0-9]+)/$', views.delete_chapter, name='delete_chapter'),
    url(r'^(?P<article_id>[0-9]+)/delete_article/$', views.delete_article, name='delete_article'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleUpdate.as_view(), name='update_article'),
    url(r'^my_article/$', views.my_article, name='my_article'),
]