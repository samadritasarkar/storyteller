from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.urlresolvers import reverse


class Article(models.Model):
    user = models.ForeignKey(User, default=1)
    author = models.CharField(max_length=250)
    article_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    article_pic = models.FileField()
    parts = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('article')

    def __str__(self):
        return self.article_title + ' - ' + self.author


class Chapter(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    part_title = models.CharField(max_length=250)
    file = models.FileField()

    def __str__(self):
        return self.part_title

