from django.urls import path
from .views import pass_view

urlpatterns = [
    # path('<int:pk>/profile/', ProfileUser.as_view(), name='profile_user'),
    # path('<int:pk>/upgrade', UserUpdate.as_view(), name='user_upgrade'),
    path('pass/', pass_view, name='pass'),
]
