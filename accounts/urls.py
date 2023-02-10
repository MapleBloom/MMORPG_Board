from django.urls import path

from .views import ProfileUser, SignUp, signup_mail_sent_view, ConfirmationSignUp


urlpatterns = [
    path('<int:pk>/profile/', ProfileUser.as_view(), name='profile_user'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup_mail_sent/', signup_mail_sent_view, name='signup_mail_sent'),
    path('<int:pk>/confirmation_signup/', ConfirmationSignUp.as_view(), name='confirmation_signup'),
]
