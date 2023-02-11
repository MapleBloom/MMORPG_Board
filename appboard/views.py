from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, News
from .filters import PostFilter, NewsFilter
from .forms import PostForm
from .permissions import ChangePermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'board/posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'board/post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = False
    permission_required = ('appboard.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'


class PostUpdate(LoginRequiredMixin, ChangePermissionRequiredMixin, UpdateView):
    raise_exception = False
    permission_required = ('appboard.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'


class NewsList(ListView):
    model = News
    ordering = '-time_in'
    template_name = 'board/news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'board/news_detail.html'
    context_object_name = 'new'


def pass_view(request):
    context = {}
    return HttpResponse(render(request, 'board/pass.html', context))
