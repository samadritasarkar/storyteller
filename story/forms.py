from django import forms
from django.contrib.auth.models import User
from . models import Article, Chapter

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = ['part_title', 'file']


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['article_title', 'genre', 'article_pic']
