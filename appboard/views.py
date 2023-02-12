from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Reply, News
from .filters import PostFilter, ReplyFilter, NewsFilter
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        if self.request.user.is_authenticated:
            replies = post.reply.all().filter(author=self.request.user).exclude(status='D')
            context['replies'] = replies
        return context


def reply_create(request, pk):
    text = request.POST.get('text')
    pk = request.POST.get('pk')
    post = Post.objects.get(pk=pk)
    user = request.user
    reply = Reply(text=text, post=post, author=user)
    reply.save()
    next = request.GET.get('next')
    send_mail(
        subject=f"Новый отклик на ваше объявление '{post}'",
        message=f"Уважаемый, {post.author}!\n\nВы получили новый отклик на ваше объявление '{post}'.\nПримите или отклоните его.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[post.author.email]
    )
    return HttpResponseRedirect(next)


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    ordering = '-time_in'
    template_name = 'board/replies_list.html'
    context_object_name = 'replies'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post__in=Post.objects.filter(author=self.request.user)).exclude(status='D')
        self.filterset = ReplyFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def reply_set_status(request):
    pk = request.POST.get('pk')
    reply = Reply.objects.get(pk=pk)
    print(request.GET)
    print(request.POST)
    if request.POST.get('accept'):
        reply.status = 'A'
    elif request.POST.get('reject'):
        reply.status = 'D'
    reply.save()
    status = reply.get_status_display()
    print(status)
    next = request.GET.get('next')
    send_mail(
        subject=f"Реакция на отклик по объявлению '{reply.post}'",
        message=f"Уважаемый, {reply.author}!\n\nВаш отклик '{reply}' на объявление '{reply.post}' {status}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reply.author.email]
    )
    return HttpResponseRedirect(next)

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
