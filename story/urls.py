from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^read/(?P<article_id>[0-9]+)/$', views.read, name='read'),
    url(r'^comment/(?P<article_id>[0-9]+)/$', views.comment, name='comment'),
    url(r'^add_like/(?P<article_id>[0-9]+)/$', views.add_like, name='add_like'),
    url(r'^show_like/(?P<article_id>[0-9]+)/$', views.show_like, name='show_like'),
    url(r'^reader_comment/(?P<article_id>[0-9]+)/$', views.reader_comment, name='reader_comment'),
    url(r'^create_article/$', views.create_article, name='create_article'),
    url(r'^(?P<article_id>[0-9]+)/create_chapter/$', views.create_chapter, name='create_chapter'),
    url(r'^(?P<article_id>[0-9]+)/add_comment/$', views.add_comment, name='add_comment'),
    url(r'^(?P<article_id>[0-9]+)/delete_chapter/(?P<chapter_id>[0-9]+)/$', views.delete_chapter, name='delete_chapter'),
    url(r'^(?P<article_id>[0-9]+)/delete_article/$', views.delete_article, name='delete_article'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleUpdate.as_view(), name='update_article'),
    url(r'^my_article/$', views.my_article, name='my_article'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^display_profile/(?P<id>[0-9]+)/$', views.display_profile, name='display_profile'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
]
