from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('bloggers/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger_detail'),
    path('blogs/<int:pk>/create/', views.CreateCommentView.as_view(), name='create'),
    path('create_blog/', views.CreateBlogView.as_view(), name='create_blog'),
]