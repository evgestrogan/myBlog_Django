from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post

register = template.Library()
# используется для регестрации пользовательских тегов и фильтров в системе


@register.simple_tag
def total_posts():
    # объявление тега, реализованного в виде функции, и обернутого в декоратор
    # для регестрации нового тега
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
# регестрация тэга с помощью декоратора и указывается шаблон,
# который будет использоваться для формирования HTML
def show_latest_posts(count=5):
    # инклюзивный тэг, с помощью которого можно задействовать переменные контекста,
    # возвращаемые тэгом, для формирования шаблона
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
# фильр форматирования markdown, который форматирует корректный HTML при отображении статьи
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
