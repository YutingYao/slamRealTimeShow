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

router = routers.DefaultRouter()
urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path(r'api/scanStatus/', views.scan_status),
    path(r'api/startScan/', views.start_scan),
    path(r'api/stopScan/', views.stop_scan),
    path(r'api/webStartScan/', views.start_scan_web),
    path(r'api/webStopScan/', views.end_scan),
    path(r'api/device_ready/', views.device_ready),
    path(r'api/controlPoint/', views.add_control),
    path(r'api/point_cloud/', views.add_point_cloud),
    path(r'api/all_point_cloud/', views.get_point_cloud),
    path(r'api/circle_point/', views.add_circle_point),
    path(r'api/get_param/', views.get_param_show),  # 获取参数
    path(r'api/scan_param/', views.scan_param),
    path(r'api/get_params/', views.get_param),
    path(r'api/download/', views.download_file),  # 下载文件，可能不需要借口
    path(r'api/modify/', views.modify_project),  # 文件删除
    path(r'api/project/', views.get_project),  # 获取所有项目数据
    path(r'api/bag/', views.get_bag),  # 获取所有项目数据
    path(r'api/test_project/', views.get_test_project),  # 获取所有项目数据
    path(r'api/modify_bag/', views.modify_bag),  # 文件删除
    # path(r'api/test_add_data/', views.test_add_project),  # 获取所有项目数据
    path(r'api/test2/', views.test_websocket),  # 获取所有项目数据
]
# point_cloud/id/ 获取瓦片点云路径url、id等数据
urlpatterns += static('api' + settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()  # 设置静态文件 部署到服务器静态文件不这样设置
