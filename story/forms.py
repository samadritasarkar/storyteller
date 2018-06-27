from django import forms
from django.contrib.auth.models import User
from . models import Article, Chapter, Comment, Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = ['part_title', 'file']


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['article_title', 'genre', 'article_pic']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
