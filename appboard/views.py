from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import News
from .filters import NewsFilter
# from .forms import NewsCkEditorForm


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


# class CreateNewsView(LoginRequiredMixin, ImageUploadView, CreateView):
#     raise_exception = False
#     form_class = NewsCkEditorForm
#
#     def form_valid(self, form):
#         if form.author and form.author == self.request.user:
#             response = super().form_valid(form)
#             return response
#         elif not form.author:
#             print(form.author)
#             newform = form.save(commit=False)
#             newform.author = self.request.user
#             print(form.author)
#             response = super().form_valid(form)
#             return response
#         else:
#             return False


def pass_view(request):
    context = {}
    return HttpResponse(render(request, 'board/pass.html', context))
