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

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank 

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
    
    comments = post.comments.filter(active=True)
    form = CommentForm()
    
    
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




def post_share(request, post_id):
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
        form = EmailPostForm()
    
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
    
    
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            search_query = SearchQuery(query, config="russian")
            search_vector = SearchVector('title', 'body', config='russian')
            search_rank = SearchRank(search_vector, search_query)
            
            results = Post.published.annotate(
                search=search_vector,
                rank=search_rank
            ).filter(search=query).order_by("-rank")
            
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})