from django.conf.urls import url

from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns = [
    # 每个路由信息都需要使用url函数来构造 (?P<city>[a-z]+)/(?P<year>\d{4})/ get_body_json
    # url(r'^index/([a-z]+)/(\d{4})/$', views.index, name='index'),
    # url(r'^index/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.index, name='index'),
    # url(r'^post_index/$', views.get_post, name='post_index'),
    # url(r'^post_json_index/$', views.get_body_json, name='get_body_json'),
]
