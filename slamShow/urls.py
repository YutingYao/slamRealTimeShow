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


from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

import pointCloud.url  # 先导入应用的urls模块
from pointCloud import views
from slamShow import settings
from pointCloud.views import PointCloudViewSet, ScanProjectViewSet

router = routers.DefaultRouter()
router.register(r'point_cloud_test', PointCloudViewSet, basename='scene')  # TODO: 任意用户查、 所属用户与管理用户，增删改查
router.register(r'scan_project', ScanProjectViewSet, basename='scan')  # TODO: 任意用户查、 所属用户与管理用户，增删改查
urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path(r'api/startScan/', views.start_scan),
    path(r'api/stopScan/', views.stop_scan),
    path(r'api/point_cloud/', views.add_point_cloud),
    path(r'api/all_point_cloud/', views.get_point_cloud),
    path(r'api/circle_point/', views.add_circle_point),
    path(r'api/scan_param/', views.scan_param),
    path(r'api/download/', views.download_file),  # 下载文件，可能不需要借口
    path(r'api/modify/', views.modify_project),  # 文件删除
    path(r'api/project/', views.get_project),  # 获取所有项目数据
]
# point_cloud/id/ 获取瓦片点云路径url、id等数据
urlpatterns += static('api' + settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()  # 设置静态文件 部署到服务器静态文件不这样设置
