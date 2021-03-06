from django.urls import path
from blog import views
from .feeds import LatestPostsFeed

app_name = 'blog'
# пространство имен приложения
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         # извлечение значений из URL'a. <parametr> возвращается в виде строки,
         # потому мы используем конвертер
         views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search')
]