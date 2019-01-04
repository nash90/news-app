from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health', views.health, name='health'),
    path('pages/signup',views.signup,name='signup-page'),
    path('pages/news/<int:news_id>', views.newsdetail, name='news-detail'),
    path('pages/news', views.newscategory, name='news-category'),
    path('pages/comment', views.newscomment, name='news-comment'),
    path('pages/search',views.newssearch, name='news-search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)