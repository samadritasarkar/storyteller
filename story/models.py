from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def get_absolute_url(self):
        return reverse('display_profile', kwargs={'id': self.pk})

    def __str__(self):
        return self.user.username


class Article(models.Model):
    user = models.ForeignKey(User, default=1)
    author = models.CharField(max_length=250)
    article_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    article_pic = models.FileField()
    parts = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('read', kwargs={'article_id': self.id})

    def __str__(self):
        return self.article_title + ' - ' + self.author


class Chapter(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    part_title = models.CharField(max_length=250)
    file = models.FileField()

    def __str__(self):
        return self.part_title


class Comment(models.Model):
    user = models.ForeignKey(User, default=1)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.user) + '-' + str(self.text)


class Like(models.Model):
    user = models.ForeignKey(User, default=1)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))
