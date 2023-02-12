from django.urls import path

from .views import (PostList, PostDetail, PostCreate, PostUpdate,
                    reply_create,
                    NewsList, NewsDetail, pass_view)


urlpatterns = [
    path('posts/', PostList.as_view(), name='posts_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
    path('post_update/<int:pk>/', PostUpdate.as_view(), name='post_update'),
    # path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:pk>/reply_create/', reply_create, name='reply_create'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('pass/', pass_view, name='pass'),
]
