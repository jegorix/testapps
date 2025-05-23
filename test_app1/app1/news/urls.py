from django.urls import path
from . import views

urlpatterns = [
    # path('', views.news_home, name='news_home'),
    path('', views.NewsHome.as_view(), name='news_home'),
    path('create/', views.ArticleCreateView.as_view(), name = 'create'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
    path('<int:pk>/update/',views.NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
]
