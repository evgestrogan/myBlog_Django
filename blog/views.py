from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post, Comment
from taggit.models import Tag


class PostListView(ListView):  # аналог функции post_list() (сейчас не используется. Был заменен функцией-обработчиком)
    queryset = Post.published.all()
    # это свой менеджер модели который вернет список постов в обратном порядке публикации
    # queryset - когда свой менеджер, model = Post.objects.all() - чтобы использовать стандартный
    context_object_name = 'posts'
    # переменная контекста
    paginate_by = 3
    # постраничное отображение. По 3 объекта на странице
    template_name = 'blog/post/list.html'
    # использование указанного шаблона


def post_list(request, tag_slug=None):  # main page
    object_list = Post.published.all()
    # это свой менеджер модели который вернет список постов в обратном порядке публикации
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
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
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):  # page with post
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # commit = False - значит что объект модели создан, но не сохранен в БД
            new_comment.post = post
            # добавляем ForeignKey в модель Comment
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == "POST":
        # выполнится после того как пользователь заполнит форму и отправит уже POST запрос
        form = EmailPostForm(request.POST)
        # создание объекта формы используя полученные данные
        if form.is_valid():
            cd = form.cleaned_data
            # если форма валидна то мы получаем введенные данные
            # form.cleaned_data - словарь с полями формы и их значениями
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({} recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            # текст заголовка
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            # текст сообщения
            send_mail(subject, message, '', [cd['to']])
            sent = True
    else:
        # в этом случае сработает если GET запрос и потому выведется пустая форма
        form = EmailPostForm()
        # создание объекта фомы и вывод его
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
