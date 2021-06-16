import os
import json
import time
import shutil
from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.decorators import method_decorator
from libs.PotreeConverter import run_PotreeConverter_exe_tile
from libs.globleConfig import CONFIG_FILE
from libs.utils import set_scan_parameter
from pointCloud.models import PointCloudChunk, CirclePoint, ScanProject
from slamShow.settings import MEDIA_ROOT, global_thread_pool, TRACT_DATA_SET
from rest_framework import mixins, viewsets, permissions, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, \
    IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters
from django.core.cache import cache
from time import sleep
from pointCloud import serializers
from concurrent.futures import ProcessPoolExecutor
from pointCloud.serializers import PointCloudChunkSerializer, ScanProjectSerializer


# TODO: 下面是所有接口
# step 1、start scan, check is has folder for save scan data, modify scan status,
@csrf_exempt
def start_scan(request):
    """
    开始扫描
    路由： get /scan_init/
    """
    try:
        clear_list = {'CIRCLE_DATA': [], 'TRACT_DATA': [], 'point_cloud': [], 'stop': 'False'}
        cache.set_many(clear_list)

    except Exception as e:
        return HttpResponse({'message': 'cache clear failed'}, status=202)
    return JsonResponse({'message': '初始化成功'}, status=200)


# step 2、点云瓦片切割，并存储瓦片url
@csrf_exempt
def add_point_cloud(request):
    """
    stop scan
    路由： post /point_cloud/
    """
    try:
        json_bytes = request.body
        track_dict = json.loads(json_bytes)
        #  TODO: 根据data列表最后元素id切割数据
        current_point_cloud = track_dict['data'][-1]
        cache.set('TRACT_DATA', track_dict['data'])
        point_cloud_path = CONFIG_FILE.SOURCE_POINT_CLOUD_PATH + str(
            current_point_cloud['id']) + CONFIG_FILE.FILE_FORMAT  # TODO: 修改后的原始点云路径
        if os.path.isfile(point_cloud_path):  # 正式版本需要判断xyz后缀文件
            if CONFIG_FILE.PLATFORM_INFO['system'] == 'Windows':
                point_cloud_rename = str(current_point_cloud['id']) + ".xyz"  # xyz TODO: ubuntu 下不需要重命名
                point_cloud_repath = CONFIG_FILE.SOURCE_POINT_CLOUD_PATH + str(
                    track_dict['id']) + ".xyz"  # TODO: xyz 点云原始文件文件夹,ubuntu不需要重命名
                os.rename(point_cloud_path, point_cloud_repath)  # TODO: 对原始文件重命名，可能以后不需要
                # cloud_url = run_PotreeConverter_exe_tile(point_cloud_repath, point_cloud_rename)  # TODO: 瓦片切割程序，需要修改部分功能
            else:
                point_cloud_name = str(current_point_cloud['id']) + CONFIG_FILE.FILE_FORMAT  # xyz TODO: ubuntu 下不需要重命名
                thread_obj = global_thread_pool.executor.submit(run_PotreeConverter_exe_tile, point_cloud_path,
                                                                point_cloud_name, current_point_cloud['id'],
                                                                CONFIG_FILE.CURRENT_PROJECT['project_id'])

        else:
            # 点云不存在，直接跳过操作
            return JsonResponse({"message": '点云文件不存在'}, status=404)
        # CONFIG_FILE.CURRENT_PROJECT['point_cloud_id'] = current_point_cloud['id']

    except Exception as e:
        return HttpResponse(status=202)

    return JsonResponse({"message": 'OK'}, status=200)


# step 3、添加回环点
@csrf_exempt
def add_circle_point(request):
    """
    add circle point
    路由： post /circle_point/
    """
    try:
        json_bytes = request.body
        circle_point_dict = json.loads(json_bytes)
        cache.set('CIRCLE_DATA', circle_point_dict['circle_point'])

    except Exception as e:
        return JsonResponse(status=202)
    return JsonResponse(status=200)


# step 4、获取瓦片url
@csrf_exempt
def get_point_cloud(request):
    try:
        circle_list = cache.get('CIRCLE_DATA')
        track_list = cache.get('TRACT_DATA')
        point_list = cache.get('point_cloud')
        if point_list:  # 需要返回点云
            if circle_list is None:
                circle_list = []
            if track_list is None:
                track_list = []
            point_cloud_list = {
                "track": track_list,  # tract_data CONFIG_FILE.TRACT_DATA
                "point": point_list,
                "circle_point": circle_list,  # CONFIG_FILE.CIRCLE_DATA circle_point_list
                "message": True
            }
            return JsonResponse(point_cloud_list, safe=False)
        else:  # 不需要返回点云数据
            message_info = {
                "message": False,
                "cause": '点云瓦片数据不存在'
            }
            return JsonResponse(message_info, safe=False)
    except Exception as e:
        return JsonResponse(status=202)


# TODO：scan parameter set
@csrf_exempt
def scan_param(request):
    try:
        json_bytes = request.body
        set_params = json.loads(json_bytes)
        # TODO: 根据参数执行相应命令
        result = set_scan_parameter(set_params)
        if result:
            return JsonResponse({"message": 'OK'}, status=200)
        else:
            return JsonResponse({"message": 'failed'}, status=202)
    except Exception as e:
        return JsonResponse(status=202)


@csrf_exempt
def download_file(request):
    pass


# step 4、接受停止扫描状态
@csrf_exempt
def stop_scan(request):
    """
    stop scan
    路由： DELETE /scan_end/
    """
    try:
        cache.set('stop', 'True')
        print('停止扫描，停止数据请求操作，修改变量')

    except Exception as e:
        return HttpResponse(status=202)

    return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')  # 关闭 csrf 防护
class ScanProjectViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         # mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = ScanProjectSerializer  # 序列化类
    # queryset = ScanProject.objects.all()
    queryset = ScanProject.objects.filter(is_active=True).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            # 这里分成一个  个人列表的
            return serializers.ScanProjectListSerializer
        if self.action == 'partial_update' or self.action == 'update':
            # TODO: 判断是否是管理员 与自身用户
            return serializers.ScanProjectUpdateSerializer
        if self.action == "create":
            # TODO: 判断是否登录,与权限限制
            return serializers.ScanProjectUpdateSerializer
        if self.action == "retrieve":
            #  TODO: 判断是否登录
            return serializers.ScanProjectRetrieveSerializer
        return "未匹配上"  # I dont' know what you want for create/destroy/update.

    def get_queryset(self):
        qs = super().get_queryset()  # 调用父类方法
        return qs

    pass


# @csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')  # 关闭 csrf 防护
class PointCloudViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        # mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    serializer_class = PointCloudChunkSerializer  # 序列化类
    queryset = PointCloudChunk.objects.all()

    def get_serializer_class(self):
        #
        if self.action == 'list':
            # 这里分成一个  个人列表的
            print('list')
            return serializers.PointCloudChunkListSerializer
        if self.action == 'partial_update' or self.action == 'update':
            # TODO: 判断是否是管理员 与自身用户
            print('update')
            return serializers.PointCloudChunkUpdateSerializer
        if self.action == "create":
            # TODO: 判断是否登录,与权限限制
            print('create')
            return serializers.PointCloudChunkUpdateSerializer
        if self.action == "retrieve":
            #  TODO: 判断是否登录
            print('retrieve')
            return serializers.PointCloudChunkRetrieveSerializer
        return "未匹配上"  # I dont' know what you want for create/destroy/update.

    def get_queryset(self):
        qs = super().get_queryset()  # 调用父类方法
        return qs

    pass


@csrf_exempt
def download_file(request):
    pass


# 测试数据
@csrf_exempt
def get_project(request):
    # tract = cache.get('TRACT_DATA')
    # circle = cache.get('CIRCLE_DATA')
    # point = cache.get('point_cloud')
    project_dir = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST)  # 获取文件
    # print(project_list)
    project_list = []
    for item in project_dir:
        if item == 'delete':
            continue
        item_file = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST + item)  # 获取文件
        down_list = []
        if len(item_file) > 0:
            for item_name in item_file:
                item_name = CONFIG_FILE.BROWSE_PATH + item + '/' + item_name
                down_list.append(item_name)
            pass
        # 计算item内所有文件夹
        cloud_file = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/item/')  # 获取文件
        point_cloud_num = len(cloud_file)

        create_time = os.path.getmtime(CONFIG_FILE.DOWNLOAD_PATH_TEST + item)
        time_local = time.localtime(create_time / 1000)
        print('创建时间--', create_time)
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        track_point = []
        if 'transformations.pcd' in item_file:

            with open(CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/transformations.pcd', "r") as f:
                for line in f.readlines():
                    line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                    line = line.split()
                    # track_point = line[11:]
                    track_point.append(line)
                    # table = [int(i) for i in line[11:]]
                    # print(table)

            track_point = track_point[11:]
            print(track_point)
            pass
        item_data = {
            'name': item,
            'project_path': CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/',
            'down_file': down_list,
            'cloud_path': CONFIG_FILE.BROWSE_PATH + item + '/item/',
            'cloud_num': point_cloud_num,
            'create_time': create_time,
            'track': track_point,
            'browse': CONFIG_FILE.BROWSE_PATH
        }
        project_list.append(item_data)

    return JsonResponse(project_list, status=200, safe=False)


@csrf_exempt
def modify_project(request):
    json_bytes = request.body
    modify_dict = json.loads(json_bytes)
    result = shutil.rmtree(CONFIG_FILE.DOWNLOAD_PATH_TEST + modify_dict['path'])  # TODO: 删除目录及目录
    is_exists = os.path.exists(CONFIG_FILE.DOWNLOAD_PATH_TEST + modify_dict['path'])
    if is_exists:
        return JsonResponse({'message': '删除失败'}, status=202, safe=False)
    else:
        return JsonResponse({'message': 'OK'}, status=200, safe=False)
