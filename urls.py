
from . import views
from django.conf.urls import url


urlpatterns = [
    url('frequency/', views.frequency),
    url('keyword/', views.check_keyword),
    url('length/', views.article_length),
    url('title/', views.check_title),
    url('slug/', views.check_slug),
    url('internal_links/', views.check_internal_links),
    url('title_in_article/', views.check_title_in_article),
]
