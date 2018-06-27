from django.contrib import admin

from .models import Article, Chapter, Comment, Profile, Like

admin.site.register(Article)
admin.site.register(Chapter)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Like)

