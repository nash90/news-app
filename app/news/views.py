from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.core import serializers
from django import forms

from .service.authentication import Signup
from .service.news_service import CategoryService
from .service.news_service import NewsService
from .service.news_service import CommentService
from .models import Category

user_not_supported =  {"error":"User not supported"}
method_not_supported = {"error":"method not supported"}
invalid_form = {"error":"invalid form"}

#### Controllers
def health(request):
    return HttpResponse("Application news portal Started", content_type="text/plain")

def home(request):
    if request.user.is_authenticated:
        categories = CategoryService().getAll()
        news = NewsService().getAll()
        context = {
            "categories":categories,
            "news":getPreviewNews(news),
            "trend":getTrendingNews()
        }
        return render(request, 'dashboard.html', context)
    else:
        categories = CategoryService().getAll()
        news = NewsService().getAll()
        
        context = {
            "categories":categories,
            "news":getPreviewNews(news),
            "trend":getTrendingNews()
        }
        return render(request, 'home.html', context)

def signup(request):
    signup = Signup()
    if request.method == 'POST':        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            signup.create_user(form)
            signup.login_user(form, request)
            return redirect('home')
    else:
        form = signup.create_form()

    categories = CategoryService().getAll()
    context = {
        "categories":categories,
        "form":form
    }
    return render(request, 'signup.html', context)

def newsdetail(request, news_id):
    news = NewsService().getById(news_id)
    comments = CommentService().getByNewsId(news_id)
    form = MessageForm(initial={'news_id':news_id})
    
    if (news.content_type_id == 1 and request.user.is_authenticated != 1):
        return HttpResponse("Signup to view news", content_type="text/plain")
    NewsService().updateViewCount(news_id)
    news.views = news.views +1
    context = {
        "news":news,
        "categories": getCategory(request),
        "comments": comments,
        "form":form,
        "trend":getTrendingNews()
    }
    #return JsonResponse(list(comments), safe=False)
    return render(request, 'content.html', context)

def newscategory(request):
    if request.user.is_authenticated:
        news = NewsService().getAllByCategoryId(request.GET.get('cat'))
        context = {
            "categories": getCategory(request),
            "news" : getPreviewNews(news),
            "trend": getTrendingNews()
        }
        return render(request, 'dashboard.html', context)
    else:
        news = NewsService().getPublicByCategoryId(request.GET.get('cat'))
        context = {
            "categories": getCategory(request),
            "news" : getPreviewNews(news),
            "trend": getTrendingNews()
        }
        return render(request, 'home.html', context)

def newscomment(request):
    if(request.method=="POST"):
        if request.user.is_authenticated:
            form = MessageForm(request.POST)
            if form.is_valid():
                #print("break point 1")
                form_data = dict(form.cleaned_data)
                form_data["user"] = request.user  
                CommentService().saveNewComment(form_data)
                return redirect('news-detail', news_id = form_data["news_id"])
            else:
                return JsonResponse(invalid_form, safe=False)
        else:
            return JsonResponse(user_not_supported, safe=False)
    else:
        return JsonResponse(method_not_supported, safe=False)

def newssearch(request):
    search_key = request.GET.get('search')
    news = NewsService().searchByKeyword(search_key)
    #print(news)
    categories = getCategory(request)
    context = {
        "categories":categories,
        "news":getPreviewNews(news),
        "trend":getTrendingNews()
    }
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'home.html', context)

## helper methods
def getPreviewNews(news):
    for item in news:
        item.content = item.content[0:200]
    return news

def getTrendingNews():
    mostCommentedNews = NewsService().getRecentMostCommentedNews()
    #print(mostCommentedNews)
    trending = []
    for news in mostCommentedNews:
        item = {}
        item["id"] = news["news_id"]
        item["title"] = news["news__title"]
        score = news["news__views"] * 1 + news["total"] * 5
        item["score"] = score
        trending.append(item)

    trending = sorted(trending, key=lambda k: k['score'], reverse=True) 

    return trending[:5]

def getCategory(request):
    if request.user.is_authenticated:
        return CategoryService().getAll()
    else:
        return CategoryService().getPublic()

class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea ,  label='Comment', max_length=100)
    news_id = forms.CharField()
    text.widget.attrs.update({'class':'form-control', 'rows':'5'})
    news_id.widget = forms.HiddenInput()

    

