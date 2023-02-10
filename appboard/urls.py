from django.urls import path

from .views import pass_view, NewsList, NewsDetail


urlpatterns = [
    # path('<int:pk>/profile/', ProfileUser.as_view(), name='profile_user'),
    # path('<int:pk>/upgrade', UserUpdate.as_view(), name='user_upgrade'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('pass/', pass_view, name='pass'),
]
