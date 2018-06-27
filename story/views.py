from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import UserForm, ArticleForm, ChapterForm, CommentForm, UserEditForm, ProfileEditForm
from . models import Article, Chapter, Comment, Like, Profile, Contact
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action


@login_required
def newsfeed(request):
    # Display all actions by default
    actions = Action.objects.all().exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')

    return render(request, 'story/newsfeed.html', {'section': 'dashboard',
                                                      'actions': actions})


def edit(request):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        if request.method == 'POST':
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile updated successfully')
            else:
                messages.error(request, 'Error updating your profile')
        else:
            profile_form = ProfileEditForm(instance=request.user.profile)
            user_form = UserEditForm(instance=request.user)
        return render(request, 'story/edit.html', {"user_form": user_form,"profile_form": profile_form})


def user_list(request):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        profiles = Profile.objects.all()
        return render(request, 'story/user_list.html', {'users': profiles})


def my_profile(request):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        profile = Profile.objects.filter(user=request.user)
        return render(request, 'story/user_profile.html', {'profile': profile})

def display_profile(request, id):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        profile = get_object_or_404(Profile, pk=id)
        articles = Article.objects.filter(user=profile.user)
        return render(request, 'story/display_profile.html', {'profile': profile,'articles':articles})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        articles = Article.objects.exclude(user=request.user)
        query = request.GET.get("q")
        if query:
            all_articles=Article.objects.all()
            articles = all_articles.filter(
                Q(article_title__icontains=query) |
                Q(author__icontains=query)
            ).distinct()
            return render(request, 'story/search_results.html', {'articles': articles})
        else:
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
        m = Like.objects.filter(user=request.user, article=article)
        return render(request, 'story/read.html', {'article': article, 'm': m})


def show_like(request, article_id):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        article = get_object_or_404(Article, pk=article_id)
        m = Like.objects.filter(article=article)
        return render(request, 'story/show_like.html', {'article': article, 'm': m})


def create_chapter(request, article_id):
    form = ChapterForm(request.POST or None, request.FILES or None)
    article = get_object_or_404(Article, pk=article_id)
    if form.is_valid():
        article_chapters = article.chapter_set.all()
        for c in article_chapters:
            if c.part_title == form.cleaned_data.get("part_title"):
                context = {
                    'article': article,
                    'form': form,
                    'error_message': 'You already added that chapter',
                }
                return render(request, 'story/create_chapter.html', context)
        chapter = form.save(commit=False)
        chapter.article = article
        chapter.file = request.FILES['file']
        chapter.save()
        create_action(request.user, 'has added new chapter', chapter)
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
        query = request.GET.get("q")
        if query:
            all_articles = Article.objects.all()
            articles = all_articles.filter(
                Q(article_title__icontains=query) |
                Q(author__icontains=query)
            ).distinct()
            return render(request, 'story/search_results.html', {'articles': articles})
        else:
            return render(request, 'story/my_article.html', {'articles': articles})


def delete_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.delete()
    create_action(request.user, 'has added deleted article:', article)
    articles = Article.objects.filter(user=request.user)
    return render(request, 'story/my_article.html', {'articles': articles})


class ArticleUpdate(UpdateView):
    model = Article
    fields = ['author', 'article_title', 'genre', 'article_pic']


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
            create_action(request.user, 'has added new article:', article)
            return render(request, 'story/detail.html', {'article': article})
        context = {
            "form": form,
        }
        return render(request, 'story/create_article.html', context)


def add_comment(request, article_id):
    form = CommentForm(request.POST or None, request.FILES or None)
    article = get_object_or_404(Article, pk=article_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        create_action(request.user, 'has added commented on article', article)
        return render(request, 'story/reader_comment.html', {'article': article})
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'story/add_comment.html', context)


def comment(request, article_id):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        article = get_object_or_404(Article, pk=article_id)
        return render(request, 'story/view_comment.html', {'article': article})


def reader_comment(request, article_id):
    if not request.user.is_authenticated():
        return render(request, 'story/login.html')
    else:
        article = get_object_or_404(Article, pk=article_id)
        return render(request, 'story/reader_comment.html', {'article': article})


def add_like(request, article_id):
    like_article = get_object_or_404(Article, pk=article_id)
    mylike = Like.objects.filter(user=request.user, article=like_article)
    if mylike:
        mylike.delete()
    else:
        mylike = Like(user=request.user, article=like_article)
        mylike.save()
        create_action(request.user, 'has liked', like_article)
    m = Like.objects.filter(user=request.user, article=like_article)
    return render(request, 'story/read.html', {'article': like_article, 'm': m})

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
        profile = Profile.objects.create(user=user)
        profile.save()
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


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, ' has followed ', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                create_action(request.user, ' has unfollwed ', user)
                return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
