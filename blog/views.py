from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post


class PostListView(ListView):  # аналог функции post_list()
    queryset = Post.published.all()
    # это свой менеджер модели который вернет список постов в обратном порядке публикации
    # queryset - когда свой менеджер, model = Post.objects.all() - чтобы использовать стандартный
    context_object_name = 'posts'
    # переменная контекста
    paginate_by = 3
    # постраничное отображение. По 3 объекта на странице
    template_name = 'blog/post/list.html'
    # использование указанного шаблона


def post_list(request):  # main page (сейчас не используется. Был заменен классом-обработчиком)
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
