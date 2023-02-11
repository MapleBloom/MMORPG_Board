from django.urls import path

from .views import (PostList, PostDetail, PostCreate, PostUpdate,
                    NewsList, NewsDetail, pass_view)


urlpatterns = [
    path('posts/', PostList.as_view(), name='posts_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
    path('post_update/<int:pk>/', PostUpdate.as_view(), name='post_update'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('pass/', pass_view, name='pass'),
]
