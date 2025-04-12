from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView

# Create your views here.

# def news_home(request):
#     news = Articles.objects.order_by('-date')
#     return render(request, 'news/news_home.html', {'news': news})

class NewsHome(ListView):
    model = Articles
    template_name = 'news/news_home.html'
    context_object_name = 'news'
    ordering = ['-date']



class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/detail_news.html'
    context_object_name = 'article'


class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/create.html'

    form_class = ArticlesForm

class NewsDeleteView(DeleteView):
    model = Articles
    template_name = "news/news_delete.html"
    success_url = '/news/'
    context_object_name = 'article'







# def create(request):
#     error = ''
#     if request.method == 'POST':
#         form = ArticlesForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#         else:
#             error = 'Форма заполнена неверно'
#
#
#     form = ArticlesForm()
#     data = {
#         'form': form,
#         'error': error
#     }
#     return render(request, 'news/create.html', {'form': form})

class ArticleCreateView(CreateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm
    success_url = '/news/'
