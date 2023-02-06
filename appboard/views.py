from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User


def pass_view(request):
    context = {}
    return HttpResponse(render(request, 'board/pass.html', context))
