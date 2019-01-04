from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import F
from django.db.models import Count
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings

from ..models import Category
from ..models import News
from ..models import Comment


class NewsService():
    def __init__(self):
        pass

    def getAll(self):
        news = None
        try:
            news = News.objects.all()
        except Exception as e: raise Http404("DB Error: Cant get all news")
        return news
    
    def getById(self, id):
        news = None
        try:
            news = News.objects.get(id=id)
        except Exception as e: raise Http404("DB Error: Cant get news by id")
        return news
    
    def getPublic(self):
        try:
            news = News.objects.filter(content_type_id=2)
        except Exception as e: raise Http404("DB Error: Cant get public news")
        return news

    def getAllByCategoryId(self, id):
        try:
            news = News.objects.filter(category_id=id)
        except Exception as e: raise Http404("DB Error: Cant get news by category id")
        return news

    def getPublicByCategoryId(self, id):
        try:
            news = News.objects.filter(category_id=id, content_type_id=2)
        except Exception as e: raise Http404("DB Error: cant get public news by category")
        return news

    def searchByKeyword(self, keyword):
        try:
            news = News.objects.filter(Q(content__icontains=keyword) | Q(title__icontains=keyword))
        except Exception as e: raise Http404("DB Error: cant get searched news")
        return news

    def updateViewCount(self, news_id):
        try:
            News.objects.filter(id=news_id).update(views=F('views')+1)
        except Exception as e: raise Http404("DB Error: cant update the view count")
    
    def getRecentMostCommentedNews(self):
        try:
            check_date = timezone.now() + relativedelta(months=-settings.RECENT_NEWS_MONTH)
            news = Comment.objects.filter(news__publish_date__gt=check_date).values('news_id', 'news__title', 'news__views').annotate(total=Count('news_id'))
            return news
        except Exception as e: raise Http404("DB Error: cant get the most commented news")  


class CategoryService():
    def __init__(self):
        pass
    
    def getAll(self):
        try:
            categories = Category.objects.all()
        except Exception as e: raise Http404("DB Error: cant get all categories")
        return categories 

    def getPublic(self):
        try:
            categories = Category.objects.filter(content_type_id=2)
        except Exception as e: raise Http404("DB Error: cant get public categories")
        return categories

class CommentService():
    def __init__(self):
        pass
    
    def getByNewsId(self, news_id):
        try:
            comments = Comment.objects.filter(news_id=news_id)
        except Exception as e: raise Http404("DB Error: cant get comment by news id")
        return comments 

    def saveNewComment(self, form_data):
        try:
            news = NewsService().getById(form_data["news_id"])
            comments = Comment(text=form_data["text"], news = news, user = form_data["user"])        
            comments.save()
        except Exception as e: raise Http404("DB Error: Could not save comment")

