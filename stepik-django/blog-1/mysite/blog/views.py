from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    
    try:
        posts = paginator.page(page_number)
        
    except PageNotAnInteger:
        posts = paginator.page(1)
    
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(
        request=request,
        template_name="blog/post/list.html",
        context={"posts": posts,
                 "tag": tag}
    )



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post,)
    
    # добавляем комментарии
    comments = post.comments.filter(active=True)
    form = CommentForm()
    
    # загружаем похожие посты (по тегам)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    
    #Добавляем поле same_tags = количество тегов у каждого поста
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))
    similar_posts = similar_posts.order_by("-same_tags", "-publish")[:4]
    
    # similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    

    return render(request=request,
                  template_name="blog/post/detail.html",
                  context={"post": post,
                           "comments": comments,
                           "form": form,
                           "similiar_posts": similar_posts})



# логика рекомендации поста по e-mail
def post_share(request, post_id):
    print("REQUEST: ", request.user.username)
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    
    sent = False
    
    if request.method == "POST":
        form = EmailPostForm(request.POST)  
        if form.is_valid():
            
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = f"{cd["name"]} recommends you read {post.title}"
            
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd["name"]}'s ({cd['email']}) comments: {cd["comments"]}"
                
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [cd['to']])
            
            sent = True
            
    else:
        initial_values = {}
        
        if request.user.is_authenticated:
            initial_values = {
                "name": request.user.username,
                "email": request.user.email
            }
            
        form = EmailPostForm(initial=initial_values)
    
    return render(request=request,
                  template_name='blog/post/share.html',
                  context={
                      "post": post,
                      "form": form,
                      "sent": sent
                  })



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    
    comment_post = request.POST.copy()
    if request.user.is_authenticated:
        comment_post["name"] = request.user.name
        comment_post["email"] = request.user.email
    
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        
    return render(request=request,
                  template_name="blog/post/comment.html",
                  context={"post": post,
                           "form": form,
                           "comment": comment})
    
    
    
    
    # реализация поискового механизма, используя PostgreSQL
    
# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
    
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
            
#             search_vector = (
#                 SearchVector('title', weight="A", config='russian') + 
#                 SearchVector('body', weight="B", config='russian') + 
#                 SearchVector('title', weight="A", config='english') + 
#                 SearchVector('body', weight="B", config='english')
#                 )
                
#             search_query = (
#                 SearchQuery(query, config="russian") | 
#                 SearchQuery(query, config="english")
#                 )
            
#             search_rank = SearchRank(search_vector, search_query)
            
#             results = Post.published.annotate(
#                 rank=search_rank
#             ).filter(rank__gte=0.3).order_by("-rank")
            
#     return render(request,
#                   'blog/post/search.html',
#                   {'form': form,
#                    'query': query,
#                    'results': results})


# Поиск по триграммному сходству
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by("-similarity")
            
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
    
    
    
# В этом модуле вы реализовали систему тегирования, интегрировав стороннее приложение в свой проект.

# Вы сгенерировали рекомендуемые посты, используя сложные наборы запросов QuerySet.

# Вы также научились создавать конкретно-прикладные шаблонные теги и фильтры Django,
# чтобы обеспечивать шаблонам конкретно-прикладные функциональности.

# Создали карту сайта, чтобы поисковые системы имели возможность сканировать ваш сайт.

# Затем вы разработали в своем блоге поисковый механизм, используя полнотекстовый поисковый механизм PostgreSQL.