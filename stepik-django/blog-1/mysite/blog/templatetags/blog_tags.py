
from django import template
from ..models import Post
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

# создание конкретно-прикладных шаблонных тегов 
@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {"latest_posts": latest_posts}

# создание конкретно-прикладного шаблонных фильтра 
@register.filter(name="markdown", is_safe=True)
def markdown_format(text):
    return mark_safe(markdown.markdown(text))



# Вы также научились создавать конкретно-прикладные шаблонные теги и фильтры Django,
# чтобы обеспечивать шаблонам конкретно-прикладные функциональности.