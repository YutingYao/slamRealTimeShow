"""slamShow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
#
#
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import pointCloud.url  # 先导入应用的urls模块
from pointCloud import views
from slamShow import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^users/', include('users.urls')),
    url(r'^testPoint/', include((pointCloud.url, 'pointCloud'), namespace='pointCloud')),  # 添加应用的路由
    # url(r'^books/$', views.BooksAPIVIew.as_view()),
    url(r'^books2/$', views.point_delete),
    url(r'^books_all/$', views.point_get),
    url(r'^pointClouds/(?P<pk>\d+)/$', views.BooksAPIVIew.as_view()),
    url(r'^startScan/$', views.start_scan),
    url(r'^stopScan/$', views.stop_scan),
    url(r'^point_cloud/$', views.add_point_cloud),
    url(r'^point_cloud/(?P<pk>\d+)/$', views.get_point_cloud),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()  # 设置静态文件 部署到服务器静态文件不这样设置
