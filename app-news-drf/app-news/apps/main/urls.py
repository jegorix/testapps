from django.urls import path
from . import views

urlpatterns = [
    #Categories
    path("categories/", views.CategoryListCreateView.as_view(), name="category-list"),
    path("categories/<slug:slug>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("categories/<slug:category_slug>/posts/", views.post_by_category, name="posts-by-category"),
    
    #Posts
    path('', views.PostListCreateView.as_view(), name='post-list'),
    path('my-post', views.MyPostView.as_view(), name='my-posts'),
    path('popular/', views.popular_posts, name='popular-posts'),
    path('recent/', views.recent_posts, name='recent-posts'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
]
