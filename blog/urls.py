from django.urls import path
from blog import views

app_name = 'blog'
# пространство имен приложения
urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         # извлечение значений из URL'a. <parametr> возвращается в виде строки,
         # потому мы используем конвертер
         views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share')
]