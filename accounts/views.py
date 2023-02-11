from django.shortcuts import render
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group

from .forms import SignUpForm, ConfirmationSignUpForm
from .permissions import ProfileUserPermissionRequiredMixin


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('signup_mail_sent')


def signup_mail_sent_view(request):
    context = {}
    logout(request)
    return HttpResponse(render(request, 'registration/signup_email_sent.html', context))


class ConfirmationSignUp(UpdateView):
    raise_exception = True
    form_class = ConfirmationSignUpForm
    model = User
    template_name = 'registration/confirmation_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.cleaned_data.get('user')
        user.is_active = True
        user_auth = Group.objects.get(name="user_auth")
        user.groups.add(user_auth)
        user.save()
        return response


class ProfileUser(LoginRequiredMixin, ProfileUserPermissionRequiredMixin, DetailView):
    raise_exception = False
    permission_required = ('auth.view_user',)
    model = User
    template_name = 'accounts/profile_user.html'
    context_object_name = 'user'
