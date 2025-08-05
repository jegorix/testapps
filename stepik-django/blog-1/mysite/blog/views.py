from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return render(
        request=request,
        template_name="blog/post/list.html",
        context={"posts": posts}
    )

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    

    return render(request=request,
                  template_name="blog/post/detail.html",
                  context={"post": post})
