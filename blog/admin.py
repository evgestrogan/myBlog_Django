from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # регистрация в админке и вывод определеных столбцов БД в списке объектов этой модели
    list_filter = ('status', 'created', 'publish', 'author')
    # блок фильтрации статей по полям
    search_fields = ('title', 'body')
    # строка поиска
    prepopulated_fields = {'slug': ('title',)}
    # автозаполнение поля slug на основе поля title
    raw_id_fields = ('author',)
    # при заполнении модели поле author выводет id пользователей а не их логины
    # raw_id_fields для выбора ForeignKey из модели с тысячами элементов, потому что раскрывающийся список выбора по умолчанию неудобен для множества элементов
    date_hierarchy = 'publish'
    # ссылки для навигации по датам
    ordering = ('status', 'publish')
    # сортировка статей по определенным полям



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
