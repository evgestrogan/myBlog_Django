from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # собственный объект карты сайта
    changeFreq = 'weekly'
    # частота обновления страниц
    priority = 0.9
    # степень совпадения страниц с тематикой сайта

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
