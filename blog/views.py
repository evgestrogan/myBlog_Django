from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from blog.models import Post


def post_list(request):  # main page
    object_list = Post.published.all()
    # это свой менеджер модели который вернет список постов в обратном порядке публикации
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    # извлекаем из запроса GET-параметр page, который указывает текущую страницу
    try:
        posts = paginator.page(page)
        # получаем список объектов на нужной странице
    except PageNotAnInteger:
        posts = paginator.page(1)
        # если указанный параметр page не является целым числом, обращаемся к первой странице
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        # если page больше, чем общее кол-во страниц, то возвращаем последнюю
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):  # page with post
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

