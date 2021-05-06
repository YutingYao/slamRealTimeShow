import os

from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from libs.PotreeConverter import test_read_point_cloud_dir, test_run_PotreeConverter_exe, read_conver_dir, \
    read_point_cloud_dir, read_track, read_point_cloud_file, run_PotreeConverter_exe_tile
from pointCloud.models import BookInfo, PointCloudChunk
from slamShow.settings import MEDIA_ROOT
import json
import shutil
from time import sleep
from libs.GeneratorMap import move_file_test, mymovefile

from concurrent.futures import ProcessPoolExecutor


# def index(request, city, year):
#     """
#     index视图
#     :param request: 包含了请求信息的请求对象
#     :return: 响应对象
#     """
#     # TODO: 获取url中值
#     # print('city=%s' % city)
#     # print('year=%s' % year)
#     """
#         获取请求参数request
#     """
#     a = request.GET.get('a')
#     b = request.GET.get('b')
#     alist = request.GET.getlist('a')
#     print(a)  # 3
#     print(b)  # 2
#     print(alist)  # ['1', '3']
#     # url = reverse('pointCloud:index')  # 返回 /users/index/
#     # print('打印reverse url=>:', url)
#     return HttpResponse("hello the world!")


# @csrf_exempt
# def get_post(request):
#     a = request.POST.get('a')
#     b = request.POST.get('b')
#     alist = request.POST.getlist('a')
#     print(a)
#     print(b)
#     print(alist)
#     return HttpResponse('OK')


# @csrf_exempt
# def get_body_json(request):
#     # print(request.META)
#     print(request.method)
#     print(request.user)
#     print(request.path)
#     print(request.encoding)
#     print(request.FILES)
#     json_str = request.body
#     # json_str = json_str.decode()  # python3.6 无需执行此步 method
#     req_data = json.loads(json_str)
#     # print(req_data['a'])
#     # print(req_data['b'])
#     return HttpResponse('OK')


# def test_get_queryset(pk, point_cloud_number, conver_number):
#     if point_cloud_number <= conver_number:
#         # print('存在点云数据，点云数据已经全部切割完毕')
#         return None
#
#     # 调用父类方法 获取当前点云项目中最大id
#     # file_path = os.path.join(MEDIA_ROOT, '/test').replace('\\', '/')
#     test_path = os.path.join('http://192.168.1.46:8000/media/', 'pointCloud')
#     # print('打印文件路径=>:', test_path)
#     # max_qs = super().get_queryset().filter(cloud_project='点云测试').aggregate(Max('cloud_id'))
#     max_qs = {"cloud_id__max": conver_number}
#     max_id = max_qs['cloud_id__max']
#     if max_id is None:
#         max_id = -1
#     # print('???max_id???', max_id)
#     read_list = test_read_point_cloud_dir(max_id)
#     print('返回需要切割文件=>:', read_list)
#     complete_cloud_list = []
#     if read_list:
#         # print('打印所有read_list=>', read_list)
#         for point_cloud_item in read_list:
#             # print('遍历需要切割文件', point_cloud_item)
#             if os.path.isfile(point_cloud_item['path']):
#                 (only_file_name, ext) = os.path.splitext(point_cloud_item['file'])
#                 tree_url = test_run_PotreeConverter_exe(point_cloud_item['file'])
#                 # print('?????返回点云url=>:', tree_url)
#                 point_item = {
#                     "cloud_project": '点云测试',
#                     "cloud_name": '点云名字',
#                     "cloud_url": tree_url,
#                     "cloud_id": int(only_file_name),
#                 }
#                 complete_cloud_list.append(point_item)
#
#     if complete_cloud_list:
#         for item in complete_cloud_list:  # test_list
#             # (only_file_name, ext) = os.path.splitext(item)
#             book = PointCloudChunk(
#                 cloud_project=item['cloud_project'],
#                 cloud_name=item['cloud_name'],
#                 cloud_url=item['cloud_url'],
#                 cloud_id=item['cloud_id']
#             )
#             book.save()
#     # 对列表进行过滤 大于某一个值得数据 获取当前点云项目中最新帧点云数据
#     # qs = super().get_queryset().filter(cloud_project='点云测试', cloud_id__gt=max_id)  # 调用父类方法
#     # qs_all = super().get_queryset().all()  # 调用父类方法
#     # 两种方案，一种每次请求并切割瓦片，返回当前切割后的数据；第二种方案根据websocket发送
#     # return qs
#     # return JsonResponse(data=data_list, status=200, safe=False)


def generate_tile(pk, point_cloud_number, conver_number):
    if point_cloud_number <= conver_number:
        return None
    pts_src_name = MEDIA_ROOT + "/pointCloud"
    list_dir = os.listdir(pts_src_name)  # 读取点云文件夹所有文件
    cut_file_list = []
    if pk == 99999:
        pk = -1

    for file_item in list_dir:  # 遍历文件夹内有效文件
        (test_name, test_ext) = os.path.splitext(file_item)
        if int(test_name) > pk:
            print('pk-->test_name----> :', pk, ' ->', test_name)
            file_item_path = pts_src_name + '/' + file_item
            item = {
                "path": file_item_path,
                "file": file_item,
            }
            cut_file_list.append(item)

    complete_cloud_list = []
    if cut_file_list:
        for point_cloud_item in cut_file_list:
            if os.path.isfile(point_cloud_item['path']):
                (only_file_name, ext) = os.path.splitext(point_cloud_item['file'])
                tree_url = test_run_PotreeConverter_exe(point_cloud_item['file'])
                point_item = {
                    "cloud_project": '点云测试',
                    "cloud_name": '点云名字',
                    "cloud_url": tree_url,
                    "cloud_id": int(only_file_name),
                }
                complete_cloud_list.append(point_item)

    if complete_cloud_list:
        for item in complete_cloud_list:  # test_list
            pointCloudUrl = PointCloudChunk(
                cloud_project=item['cloud_project'],
                cloud_name=item['cloud_name'],
                cloud_url=item['cloud_url'],
                cloud_id=item['cloud_id']
            )
            pointCloudUrl.save()


class PointAPIVIew(View):
    """
    增加点云数据
    """

    @csrf_exempt
    def get(self, request, pk):
        """
        查询点云数据，根据pk值进行点云切割
        路由：GET /PointCloudChunk/
        """
        point_cloud_path = MEDIA_ROOT + "/pointCloud"  # 点云原始文件文件夹
        conver_path = MEDIA_ROOT + "/conver"  # 点云瓦片文件夹
        track_path = MEDIA_ROOT + "/track"  # 点云轨迹文件夹
        conver_number = read_conver_dir(conver_path)  # 读取点云瓦片数量
        point_cloud_number = read_point_cloud_dir(point_cloud_path)  # 读取原始点云数量

        pk = int(pk)
        print(pk, type(pk))
        # TODO: 点云文件夹没有点云数据    if (pk != 99999) & (point_cloud_number == 0 | point_cloud_number == conver_number):
        if ((pk == 99999) & (conver_number != 0)) | ((pk != 99999) & (point_cloud_number == conver_number)):
            print('不符合瓦片标准')
            message_info = {
                "message": False
            }
            if pk == 99999:  # 首次请求，存在瓦片返回数据
                queryset2 = PointCloudChunk.objects.all()
                point_list = []
                print('pk 值 和 类型 =>:', pk, type(pk))
                for point_cloud_item in queryset2:
                    point_list.append({
                        'cloud_id': point_cloud_item.cloud_id,
                        'cloud_name': point_cloud_item.cloud_name,
                        'cloud_url': point_cloud_item.cloud_url,
                        'cloud_project': point_cloud_item.cloud_project,
                    })
                track_data = read_track(track_path)  # 读取轨迹数据
                test_list_point = {
                    "track": track_data,
                    "point": point_list,
                    "message": True
                }
                return JsonResponse(test_list_point, safe=False)
            else:  # 非首次请求，不需要切割，不用返回点云数据
                return JsonResponse(message_info, safe=False)

        else:  # pk != 99999
            generate_tile(pk, point_cloud_number, conver_number)  # 生成瓦片，并将瓦片id、cloud.js写入数据库
        # if (pk == 99999) & point_cloud_number != 0 & conver_number == 0:
        # if (pk == 99999) & conver_number != 0:
        # 不需要返回点云数据时，不会执行这里
        queryset2 = PointCloudChunk.objects.all()
        point_list = []
        print('pk 值 和 类型 =>:', pk, type(pk))
        for point_cloud_item in queryset2:
            if pk != 99999:  # 判断是否是初次请求或者刷新页面后的请求
                if point_cloud_item.cloud_id > int(pk):
                    point_list.append({
                        'cloud_id': point_cloud_item.cloud_id,
                        'cloud_name': point_cloud_item.cloud_name,
                        'cloud_url': point_cloud_item.cloud_url,
                        'cloud_project': point_cloud_item.cloud_project,
                    })
            else:
                point_list.append({
                    'cloud_id': point_cloud_item.cloud_id,
                    'cloud_name': point_cloud_item.cloud_name,
                    'cloud_url': point_cloud_item.cloud_url,
                    'cloud_project': point_cloud_item.cloud_project,
                })

        track_data = read_track(track_path)  # 读取轨迹数据
        test_list_point = {
            "track": track_data,
            "point": point_list,
            "message": True
        }
        if point_list:  # 需要返回点云
            return JsonResponse(test_list_point, safe=False)
        else:  # 不需要返回点云数据
            message_info = {
                "message": False
            }
            return JsonResponse(message_info, safe=False)

    @csrf_exempt
    def post(self, request):
        """
        新增图书
        路由：POST /books/
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = BookInfo.objects.create(
            btitle=book_dict.get('btitle'),
            bpub_date=datetime.strptime(book_dict.get('bpub_date'), '%Y-%m-%d').date()
        )

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            # 'image': book.image.url if book.image else ''
        }, status=201)

    @csrf_exempt
    def delete(self, request):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.all()
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()

        return HttpResponse(status=204)


class BookAPIView(View):
    @csrf_exempt
    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            # 'image': book.image.url if book.image else ''
        })

    @csrf_exempt
    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.btitle = book_dict.get('btitle')
        book.bpub_date = datetime.strptime(book_dict.get('bpub_date'), '%Y-%m-%d').date()
        book.save()

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            # 'image': book.image.url if book.image else ''
        })

    @csrf_exempt
    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()

        return HttpResponse(status=204)


class PointCloudAPIView(View):
    @csrf_exempt
    def get(self, request):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.all()  # BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            # 'image': book.image.url if book.image else ''
        })

    @csrf_exempt
    def put(self, request):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.btitle = book_dict.get('btitle')
        book.bpub_date = datetime.strptime(book_dict.get('bpub_date'), '%Y-%m-%d').date()
        book.save()

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            # 'image': book.image.url if book.image else ''
        })

    @csrf_exempt
    def delete(self, request):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.all()
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()

        return HttpResponse(status=204)


# @csrf_exempt
# def point_get(request):
#     """
#     删除图书
#     路由： DELETE /books/<pk>/
#     """
#     try:
#         point_list = PointCloudChunk.objects.all()
#         # print("book")
#         # for item in point_list:
#         #     print('点云=>:', item)
#     except PointCloudChunk.DoesNotExist:
#         return HttpResponse(status=404)
#
#     return HttpResponse({"all_book2": "book"})


# TODO: 下面是所有接口
# step 1、接受开始扫描状态
@csrf_exempt
def start_scan(request):
    """
    开始扫描
    路由： get /scan_init/
    """
    try:
        print('开始扫描，进行扫描初始化')
        pcd_path = MEDIA_ROOT + "/pointCloud"
        tile_path = MEDIA_ROOT + "/conver"
        track_path = MEDIA_ROOT + "/track/transformations.txt"
        shutil.rmtree(pcd_path)
        shutil.rmtree(tile_path)
        # with open(track_path, 'a+', encoding='utf-8') as f:
        #     f.truncate(0)
        # sleep(1)
        os.mkdir(pcd_path)
        os.mkdir(tile_path)
        point_cloud = PointCloudChunk.objects.all()
        point_cloud.delete()

    except PointCloudChunk.DoesNotExist:
        return HttpResponse(status=404)

    return HttpResponse(status=200)


# step 4、接受停止扫描状态
@csrf_exempt
def stop_scan(request):
    """
    stop scan
    路由： DELETE /scan_end/
    """
    try:
        # point_list = PointCloudChunk.objects.all()
        # print("book")
        # for item in point_list:
        #     print('点云=>:', item)
        print('停止扫描，停止数据请求操作，修改变量')
        pool = ProcessPoolExecutor(3)
        sources_file = "D:/test/test_move/abc.zip"
        target_file = "D:/test/test_move_2/abc.zip"
        index_last = target_file.rfind('/')  # 返回最右边（最后一次）的字符位置
        test_target_file = target_file[0:index_last]
        print('index_last=>:', index_last, test_target_file)
        # all_path = "D:\\test\\test_move\\abc1.zip D:/test/test_move_2/abc1.zip"
        # future = pool.submit(move_file_test, (sources_file, target_file))
        # future = pool.submit(mymovefile, (sources_file, target_file))
        # move_file_test(all_path)

    except PointCloudChunk.DoesNotExist:
        return HttpResponse(status=202)

    return HttpResponse(status=200)


# step 2、点云瓦片切割，并存储瓦片url
@csrf_exempt
def add_point_cloud(request):
    """
    stop scan
    路由： post /point_cloud/
    """
    try:
        track_path = MEDIA_ROOT + "/track/trackPoint.txt"
        json_bytes = request.body
        # json_str = json_bytes.decode()
        track_dict = json.loads(json_bytes)
        # 轨迹点获取,从请求体中获取轨迹数据
        track_point = str(track_dict['id']) + ' ' + str(track_dict['x']) + ' ' + str(track_dict['y']) + ' ' + \
                      str(track_dict['z']) + ' ' + str(track_dict['i']) + ' ' + str(track_dict['er']) + ' ' + str(
            track_dict['ep']) + ' ' + \
                      str(track_dict['ey']) + ' ' + str(track_dict['d'])
        # print('当前估计点数据=>:', track_point)
        point_cloud_path = MEDIA_ROOT + "/pointCloud/" + str(track_dict['id']) + ".pcd"  # 点云原始文件文件夹
        if os.path.isfile(point_cloud_path):  # 正式版本需要判断xyz后缀文件
            # point_cloud_name = str(track_dict['id']) + ".pcd"
            point_cloud_rename = str(track_dict['id']) + ".xyz"
            point_cloud_repath = MEDIA_ROOT + "/pointCloud/" + str(track_dict['id']) + ".xyz"  # 点云原始文件文件夹
            os.rename(point_cloud_path, point_cloud_repath)
            print('点云存在')
            cloud_url = run_PotreeConverter_exe_tile(point_cloud_repath, point_cloud_rename)
            if cloud_url is None:  # 如果cloud_url 为 None 说明切割瓦片失败
                os.rename(point_cloud_repath, point_cloud_path)  # 瓦片切割失败，将xyz重新修改为pcd
                return HttpResponse(status=202)
            point_cloud_url = PointCloudChunk(
                cloud_project='点云项目',
                cloud_name='点云名称',
                cloud_url=cloud_url,
                cloud_id=str(track_dict['id'])
            )
            point_cloud_url.save()
            print('cloud_url=>:', cloud_url)
            # 点云存在,进行点云切割

        else:
            # 点云不存在，直接跳过操作
            print('点云不存在', point_cloud_path)
            return HttpResponse(status=404)
        # 轨迹点追加
        with open(track_path, 'a+') as f:
            # json_str = json.dumps(dict, indent=0)
            f.write(track_point)
            f.write('\n')
            f.close()


    except PointCloudChunk.DoesNotExist:
        return HttpResponse(status=202)

    return HttpResponse(status=201)


# step 3、获取瓦片url
@csrf_exempt
def get_point_cloud(request, pk):
    track_path = MEDIA_ROOT + "/track"  # trackPoint.txt  transformations.txt
    current_id = int(pk)
    # if request == current_id:
    # queryset2 = None  # PointCloudChunk.objects.all()
    if current_id == 999999:
        queryset2 = PointCloudChunk.objects.filter(cloud_id_lt=10)
    else:
        max_cloud_id = current_id + 9
        queryset2 = PointCloudChunk.objects.filter(cloud_id_gte=current_id, cloud_id_lt=max_cloud_id)
    point_list = []
    for point_cloud_item in queryset2:
        if current_id != 999999:  # 判断是否是初次请求或者刷新页面后的请求
            if point_cloud_item.cloud_id > current_id:
                point_list.append({
                    'cloud_id': point_cloud_item.cloud_id,
                    'cloud_name': point_cloud_item.cloud_name,
                    'cloud_url': point_cloud_item.cloud_url,
                    'cloud_project': point_cloud_item.cloud_project,
                })
        else:
            point_list.append({
                'cloud_id': point_cloud_item.cloud_id,
                'cloud_name': point_cloud_item.cloud_name,
                'cloud_url': point_cloud_item.cloud_url,
                'cloud_project': point_cloud_item.cloud_project,
            })

    if point_list:  # 需要返回点云
        point_list_length = len(point_list)
        track_data = read_track(track_path)  # 读取轨迹数据
        # if current_id != 99999:
        #     valid_track_data = track_data[:point_list_length]
        # else:
        #     valid_track_data = track_data[:point_list_length]
        test_list_point = {
            "track": track_data,
            "point": point_list,
            "message": True
        }
        return JsonResponse(test_list_point, safe=False)
    else:  # 不需要返回点云数据
        message_info = {
            "message": False
        }
        return JsonResponse(message_info, safe=False)


# 清除数据库所有数据--正式版本不需要此功能，直接在开始扫描状态接口中清空数据库
@csrf_exempt
def point_delete(request):
    """
    删除所有的点
    路由： DELETE /books/<pk>/
    """
    try:
        book = PointCloudChunk.objects.all()
    except PointCloudChunk.DoesNotExist:
        return HttpResponse(status=404)

    book.delete()

    return HttpResponse(status=204)


# 测试获取单个瓦片url
@csrf_exempt
def get_single_point_cloud(request, pk):
    track_path = MEDIA_ROOT + "/track"  # trackPoint.txt  transformations.txt
    current_id = int(pk)
    # if request == current_id:
    # queryset2 = None  # PointCloudChunk.objects.all()
    if current_id == 999999:
        queryset2 = PointCloudChunk.objects.filter(cloud_id=0)
    else:
        # max_cloud_id = current_id + 9
        queryset2 = PointCloudChunk.objects.filter(cloud_id=pk)
    point_list = []
    for point_cloud_item in queryset2:
        if current_id != 999999:  # 判断是否是初次请求或者刷新页面后的请求
            if point_cloud_item.cloud_id >= current_id:
                point_list.append({
                    'cloud_id': point_cloud_item.cloud_id,
                    'cloud_name': point_cloud_item.cloud_name,
                    'cloud_url': point_cloud_item.cloud_url,
                    'cloud_project': point_cloud_item.cloud_project,
                })
        else:
            point_list.append({
                'cloud_id': point_cloud_item.cloud_id,
                'cloud_name': point_cloud_item.cloud_name,
                'cloud_url': point_cloud_item.cloud_url,
                'cloud_project': point_cloud_item.cloud_project,
            })

    if point_list:  # 需要返回点云
        point_list_length = len(point_list)
        track_data = read_track(track_path)  # 读取轨迹数据
        # if current_id != 99999:
        #     valid_track_data = track_data[:point_list_length]
        # else:
        #     valid_track_data = track_data[:point_list_length]
        test_list_point = {
            "track": track_data,
            "point": point_list,
            "message": True
        }
        return JsonResponse(test_list_point, safe=False)
    else:  # 不需要返回点云数据
        message_info = {
            "message": False
        }
        return JsonResponse(message_info, safe=False)


# step 4、添加回环点
@csrf_exempt
def add_circle_point():
    pass
