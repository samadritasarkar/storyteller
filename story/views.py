from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import UserForm, ArticleForm, ChapterForm
from . models import Article, Chapter
from django.views.generic.edit import UpdateView

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        articles = Article.objects.exclude(user=request.user)
        return render(request, 'story/index.html', {'articles': articles})

def detail(request, article_id):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        article = get_object_or_404(Article, pk=article_id)
        return render(request, 'story/detail.html', {'article': article})

def read(request,article_id):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        article = get_object_or_404(Article, pk=article_id)
        return render(request, 'story/read.html', {'article': article})

def create_chapter(request, article_id):
    form = ChapterForm(request.POST or None, request.FILES or None)
    article = get_object_or_404(Article, pk=article_id)
    if form.is_valid():
        article_chapters = article.chapter_set.all()
        article.parts = article.parts + 1
        for c in article_chapters:
            if c.part_title == form.cleaned_data.get("part_title"):
                context = {
                    'article': article,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'story/create_chapter.html', context)
        chapter = form.save(commit=False)
        chapter.article = article
        chapter.file = request.FILES['file']
        chapter.save()
        return render(request, 'story/detail.html', {'article': article})
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'story/create_chapter.html', context)

def delete_chapter(request, article_id, chapter_id):
    article = get_object_or_404(Article, pk=article_id)
    chapter = Chapter.objects.get(pk=chapter_id)
    chapter.delete()
    return render(request, 'story/detail.html', {'article': article})

def my_article(request):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        articles = Article.objects.filter(user=request.user)
        return render(request, 'story/my_article.html', {'articles': articles})

def delete_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.delete()
    articles = Article.objects.filter(user=request.user)
    return render(request, 'story/my_article.html', {'articles': articles})

class ArticleUpdate(UpdateView):
    model = Article
    fields = ['author', 'article_title', 'genre', 'article_pic']

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'story/login.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                articles = Article.objects.filter()
                return render(request, 'story/index.html', {'articles': articles})
            else:
                return render(request, 'story/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'story/login.html', {'error_message': 'Invalid login'})
    return render(request, 'story/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                articles = Article.objects.all()
                return render(request, 'story/index.html', {'articles': articles})
    context = {
        "form": form,
    }
    return render(request, 'story/register.html', context)

def create_article(request):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        form = ArticleForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.author = request.user.username
            article.article_pic = request.FILES['article_pic']
            article.save()
            return render(request, 'story/detail.html', {'article': article})
        context = {
            "form": form,
        }
        return render(request, 'story/create_article.html', context)


