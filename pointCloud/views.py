# -*- coding: utf-8 -*-
import os
import sys
import operator
from rest_framework.decorators import action
# sys.path.append("/opt/ros/noetic/lib/python3/dist-packages")
# import rospy
# from std_msgs.msg import String

import subprocess
import json
import time
import shutil
from libs.WebSocket import send_message
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from libs.PotreeConverter import run_PotreeConverter_exe_tile
from libs.globleConfig import CONFIG_FILE
from libs.utils import set_scan_parameter
from libs.scanParams import set_modify_params
from slamShow.settings import global_thread_pool
from django.core.cache import cache
from slamShow.settings import MEDIA_ROOT
from pointCloud.models import ConfigInfo
from django.views import View


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
        CONFIG_FILE.scanParameter = {
            'loopback': True,
            'optimize': False,
            'noSample': True,
            'sample': True,
            'mode': 'indoor',
        }
        CONFIG_FILE.SCAN_STATUS = 'pending'
        if CONFIG_FILE.OPEN_SOCKET:
            send_message(CONFIG_FILE.SCAN_STATUS)  # 发送给前端状态值

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
        # print('add data-->:', track_dict)
        #  TODO: 根据data列表最后元素id切割数据
        current_point_cloud = track_dict['data'][-1]
        if current_point_cloud['id'] < 2:
            if os.path.exists(CONFIG_FILE.TILE_PATH):
                project_dir = os.listdir(CONFIG_FILE.TILE_PATH)
                if len(project_dir) > 2:
                    shutil.rmtree(CONFIG_FILE.TILE_PATH)  # 删除目录，包括目录下的所有文件
                    os.mkdir(CONFIG_FILE.TILE_PATH)
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
        return JsonResponse({'message': 'faild'}, status=202)
    return JsonResponse({'message': 'OK'}, status=200)


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


@csrf_exempt
def get_param_show(request):
    try:
        return JsonResponse(CONFIG_FILE.scanParameter, status=200)
    except Exception as e:
        return JsonResponse(status=202)


# TODO：scan parameter set
@csrf_exempt
def scan_param_copy(request):
    try:
        json_bytes = request.body
        set_params = json.loads(json_bytes)
        # TODO: 根据参数执行相应命令
        # result = set_scan_parameter(set_params)
        result = set_modify_params(set_params['set_params'])
        print('canshu---', result)
        if result['message'] == 'OK':
            CONFIG_FILE.scanParameter = set_params['save_params_show']
            return JsonResponse({"message": 'OK'}, status=200)
        else:
            return JsonResponse({"message": 'failed'}, status=202)
    except Exception as e:
        return JsonResponse({"message": 'err'}, status=202)


# TODO：scan parameter set
@csrf_exempt
def scan_param(request):
    try:
        json_bytes = request.body
        set_params = json.loads(json_bytes)
        # TODO: 根据参数执行相应命令
        # result = set_scan_parameter(set_params)
        result = set_modify_params(set_params['set_params'])
        print('canshu---', result)
        if result['message'] == 'OK':
            # CONFIG_FILE.scanParameter = set_params['save_params_show']
            CONFIG_FILE.SCAN_PARAMS['otherParam'] = set_params['save_params_show']
            CONFIG_FILE.SCAN_PARAMS['selected_mode'] = set_params['mode']
            return JsonResponse({"message": 'OK'}, status=200)
        else:
            return JsonResponse({"message": 'failed'}, status=202)
    except Exception as e:
        return JsonResponse({"message": 'err'}, status=202)


# TODO：scan parameter set
@csrf_exempt
def get_param(request):
    try:
        # return JsonResponse(CONFIG_FILE, status=200)
        return JsonResponse({'paramas': CONFIG_FILE.SCAN_PARAMS}, status=200)
    except Exception as e:
        return JsonResponse(status=202)


# TODO：scan parameter set
@csrf_exempt
def scan_status(request):
    try:
        # return JsonResponse(CONFIG_FILE, status=200)
        return JsonResponse({'status': CONFIG_FILE.SCAN_STATUS,
                             'socket': CONFIG_FILE.OPEN_SOCKET,
                             'orientation': CONFIG_FILE.SCREEN_ORIENTATION}, status=200)
    except Exception as e:
        return JsonResponse(status=202)


# TODO: start scan
# TODO: start scan
@csrf_exempt
def start_scan_web(request):
    cmd = """/bin/bash -c '''source /opt/ros/noetic/setup.bash && rostopic pub /chatter std_msgs/String "data: '开启扫描程序'"'''"""
    # cmd = '''source /opt/ros/noetic/setup.bash && rostopic pub /chatter std_msgs/String "data: '开启扫描程序'"'''
    # ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # out, err = ex.communicate()
    # status = ex.wait()
    os.popen(cmd)
    # 初始化cache
    clear_list = {'CIRCLE_DATA': [], 'TRACT_DATA': [], 'point_cloud': [], 'stop': 'False'}
    cache.set_many(clear_list)
    CONFIG_FILE.scanParameter = {
        'loopback': True,
        'optimize': False,
        'noSample': True,
        'sample': True,
        'mode': 'indoor',
    }
    CONFIG_FILE.SCAN_STATUS = 'pending'
    # if CONFIG_FILE.OPEN_SOCKET:
    #     send_message(CONFIG_FILE.SCAN_STATUS)  # 发送给前端状态值
    return JsonResponse({'message': 'OK'})


# TODO: end scan
@csrf_exempt
def end_scan(request):
    try:
        cmd = """/bin/bash -c '''source /opt/ros/noetic/setup.bash && rostopic pub /chatter std_msgs/String "data: '保存'"'''"""

        # os.popen(cmd)
        # ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        # out, err = ex.communicate()
        # status = ex.wait()
        # print("cmd out: ", out )
        # print("cmd err: ", err )
        # if out:
        #     return JsonResponse({'message': 'OK','data':time.time()})
        # else:
        #     return JsonResponse({'message': err,'data':time.time()})
        os.popen(cmd)
        CONFIG_FILE.SCAN_STATUS = 'stop'
        return JsonResponse({'message': 'OK'})
    except Exception as e:
        return JsonResponse({'message': 'failed', 'data': time.time()})


# TODO: end scan
@csrf_exempt
def add_control(request):
    try:
        # control_cmd()
        # return JsonResponse({'message': 'OK'}, status=200)
        cmd = """/bin/bash -c '''source /opt/ros/noetic/setup.bash && rostopic pub /chatter std_msgs/String "data: '添加控制点'"'''"""

        # os.popen(cmd)
        # ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        # out, err = ex.communicate()
        # status = ex.wait()
        # print("cmd out: ", out )
        # print("cmd err: ", err )
        # if out:
        #     return JsonResponse({'message': 'OK','data':time.time()})
        # else:
        #     return JsonResponse({'message': err,'data':time.time()})
        os.popen(cmd)
        return JsonResponse({'message': 'OK'})
    except Exception as e:
        return JsonResponse({'message': 'failed', 'data': time.time()})


@csrf_exempt
def device_ready(request):
    try:
        CONFIG_FILE.SCAN_STATUS = 'noStart'  # 修改状态值
        if CONFIG_FILE.OPEN_SOCKET:
            send_message(CONFIG_FILE.SCAN_STATUS)  # 发送给前端状态值
        return JsonResponse({'message': 'OK'})
    except  Exception as e:
        return JsonResponse({'message': 'failed'})


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
        CONFIG_FILE.SCAN_STATUS = 'stop'
        if CONFIG_FILE.OPEN_SOCKET:
            send_message(CONFIG_FILE.SCAN_STATUS)  # 发送给前端状态值
        print('停止扫描，停止数据请求操作，修改变量')

    except Exception as e:
        return HttpResponse(status=202)

    return HttpResponse(status=200)


@csrf_exempt
def download_file(request):
    pass


# 第一版获取project列表
@csrf_exempt
def get_project(request):
    try:
        project_dir = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST)  # 获取文件
        project_list = []
        for item in project_dir:
            if item == 'delete':
                continue
            if os.path.isfile(CONFIG_FILE.DOWNLOAD_PATH_TEST + item):
                continue
            item_file = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST + item)  # 获取文件
            down_list = []
            if len(item_file) > 0:
                for item_name in item_file:
                    if item_name == 'item' or item_name == 'TILE':
                        continue
                    item_name = CONFIG_FILE.BROWSE_PATH + item + '/' + item_name
                    down_list.append(item_name)

            # 计算item内所有文件夹
            if os.path.exists(CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/TILE/'):  # 获取文件
                cloud_file = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/TILE/')  # 获取文件
                point_cloud_num = len(cloud_file)
            else:
                point_cloud_num = 0

            create_time = os.path.getmtime(CONFIG_FILE.DOWNLOAD_PATH_TEST + item)
            time_local = time.localtime(create_time)
            # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            track_point = []
            read_track_url = ''
            if 'transformations.pcd' in item_file:
                # 由于读取轨迹点耗时较长，修改为浏览时读取--轨迹列表保存为空，添加读取轨迹url
                # read_track_url = CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/transformations.pcd'
                read_track_url = CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/transformations.pcd'

            item_data = {
                'name': item,
                'project_path': CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/',
                'down_file': down_list,
                'cloud_path': CONFIG_FILE.BROWSE_PATH + item + '/TILE/',
                'cloud_num': point_cloud_num,
                'create_time': create_time,
                'track': track_point,
                'browse': CONFIG_FILE.BROWSE_PATH,
                'read_track_url': read_track_url
            }
            project_list.append(item_data)
    except:
        return JsonResponse({'message': 'Failed'}, status=202, safe=False)

    return JsonResponse({'message': 'OK', 'list': project_list}, status=200, safe=False)


#  第一版获取project列表,优化json 对下载文件item进行排序
@csrf_exempt
def get_project_list(request):
    try:
        project_dir = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST)  # 获取文件
        project_list = []
        num_str = '1234567890'
        for item in project_dir:
            if item == 'delete':
                continue
            if os.path.isfile(CONFIG_FILE.DOWNLOAD_PATH_TEST + item):
                continue
            item_file = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST + item)  # 获取文件
            fix_name_list = []
            down_list = []
            down_list_sort = []
            multi_attribute_list = []
            if len(item_file) > 0:
                for item_name in item_file:
                    if item_name == 'item' or item_name == 'TILE':
                        continue
                    item_name_path = CONFIG_FILE.BROWSE_PATH + item + '/' + item_name
                    file_data = {
                        'path': item_name_path,
                        'name': item_name,
                        'sort': 0
                    }
                    num = ''
                    if 'globalCloudAll' in item_name:
                        for item_let in item_name:
                            if item_let in num_str:
                                num += item_let
                        print('num--', num)
                        file_data['sort'] = int(num)
                        multi_attribute_list.append(file_data)
                    elif 'bag' in item_name:
                        pass
                    else:
                        fix_name_list.append(file_data)

            multi_attribute_list.sort(key=lambda x: x['sort'])
            fix_name_list.sort(key=lambda x: x['name'])

            fix_name_list.reverse()
            for fix_item in fix_name_list:
                multi_attribute_list.insert(0, fix_item)
            for multi_item in multi_attribute_list:
                item_dict = {
                    'path': multi_item['path'],
                    'name': multi_item['name']
                }
                down_list.append(multi_item['path'])
                down_list_sort.append(item_dict)

            # 计算item内所有文件夹
            if os.path.exists(CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/TILE/'):  # 获取文件
                cloud_file = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/TILE/')  # 获取文件
                point_cloud_num = len(cloud_file)
            else:
                point_cloud_num = 0
            create_time = os.path.getmtime(CONFIG_FILE.DOWNLOAD_PATH_TEST + item)
            # time_local = time.localtime(create_time)
            # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            track_point = []
            read_track_url = ''
            if 'transformations.pcd' in item_file:
                # 由于读取轨迹点耗时较长，修改为浏览时读取--轨迹列表保存为空，添加读取轨迹url
                # read_track_url = CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/transformations.pcd'
                read_track_url = CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/transformations.pcd'
            item_data = {
                'name': item,
                'project_path': CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/',
                'down_file': down_list,
                'cloud_path': CONFIG_FILE.BROWSE_PATH + item + '/TILE/',
                'cloud_num': point_cloud_num,
                'create_time': create_time,
                'track': track_point,
                'browse': CONFIG_FILE.BROWSE_PATH,
                'read_track_url': read_track_url
            }
            project_list.append(item_data)
    except:
        return JsonResponse({'message': 'Failed'}, status=202, safe=False)

    return JsonResponse(project_list, status=200, safe=False)


@csrf_exempt
def read_track(request):
    json_bytes = request.body
    read_dict = json.loads(json_bytes)
    track_point = []
    with open(read_dict['url'], "r") as f:
        readLinesFilter = f.readlines()[11:]
        for line in readLinesFilter:
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            line = line.split()
            # track_point = line[11:]
            lineDict = {
                'id': int(line[3]),
                'x': float(line[0]),
                'y': float(line[1]),
                'z': float(line[2]),
                'er': float(line[4]),
                'ep': float(line[5]),
                'ey': float(line[6]),
            }

            track_point.append(lineDict)
    return JsonResponse({'track': track_point})


# 获取bag数据
@csrf_exempt
def get_bag(request):
    project_dir = os.listdir(CONFIG_FILE.BAG_PATH)  # 获取文件
    # print('project_dir-->:', project_dir)
    project_list = []
    for item in project_dir:
        if os.path.isfile(CONFIG_FILE.BAG_PATH + item):
            create_time = os.path.getmtime(CONFIG_FILE.BAG_PATH + item)
            # 'down_file' 下载使用url,window下使用media拼接路径, ubuntu 下使用 nginx 映射 位置 加 文件相对路径
            # 'name' 带后缀格式文件名称  文件下载使用
            # 'path' 文件在系统中的真实路径，修改文件名称使用
            # 'create_time' 获取文件创建时间（秒），根据使用排序
            file_item = {
                'down_file': CONFIG_FILE.BAG_DOWNLOAD + item,
                'name': item,
                'path': CONFIG_FILE.BAG_PATH + item,
                'create_time': create_time
            }
            project_list.append(file_item)
    list2 = sorted(project_list, key=operator.itemgetter('create_time'), reverse=True)
    project_list = list2
    # print(list2)
    return JsonResponse(project_list, status=200, safe=False)


@csrf_exempt
def modify_bag(request):
    json_bytes = request.body
    modify_dict = json.loads(json_bytes)
    if modify_dict['rename']:
        try:
            rename = CONFIG_FILE.BAG_PATH + modify_dict['rename']
            os.rename(modify_dict['path'], rename)
            return JsonResponse({'message': 'OK'})
        except Exception as f:
            return JsonResponse({'message': '修改失败'})

    elif modify_dict['delete']:
        print(123)
        # result = shutil.rmtree(modify_dict['path'])  # TODO: 删除目录及目录
        try:
            result = os.remove(modify_dict['path'])
            is_exists = os.path.exists(modify_dict['path'])
            return JsonResponse({'message': 'OK'})
        except Exception as f:
            return JsonResponse({'message': '删除失败'})


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


@csrf_exempt
def test_websocket(request):
    # SimpleEcho.handleMessage()
    send_message('pending')  # 以后修改为实际状态值
    return JsonResponse({'message': 'OK'}, status=200, safe=False)


@csrf_exempt
def get_test_project(request):
    # 读取文件
    tract_data = cache.get('TRACT_DATA')
    if tract_data:
        pass
    else:
        # 读取文件
        tract_data = []
        file_url = MEDIA_ROOT + '/point2/transformations23.txt'  # point2-5/point2/transformations.txt  point2
        with open(file_url, 'r', encoding='utf-8') as f:
            lists = f.readlines()
            for line in lists:
                line_list = line.split()
                print('line--', line)
                print('line_list--', line_list)
                item_dict = {
                    'id': int(line_list[3]),
                    'x': float(line_list[0]),
                    'y': float(line_list[1]),
                    'z': float(line_list[2]),
                    'er': float(line_list[4]),
                    'ep': float(line_list[5]),
                    'ey': float(line_list[6]),
                }
                tract_data.append(item_dict)

        CONFIG_FILE.test_track_list = tract_data

        # print(tract_data)
    point_list = cache.get('point_cloud')
    if point_list:
        pass
    else:
        point_list = []
    tract_data_list = cache.get('TRACT_DATA')
    if tract_data_list:
        pass
    else:
        tract_data_list = []
    tract_data_list.extend(CONFIG_FILE.test_track_list[CONFIG_FILE.point_index: CONFIG_FILE.point_index + 5])
    cache.set('TRACT_DATA', tract_data_list)
    for item in [1, 2, 3, 4, 5]:
        # point_index = len(point_list)
        # CONFIG_FILE.point_index += 1
        # cache.set('TRACT_DATA', tract_data)
        # cloud_url = '/GOSLAMtemp/' + only_file_name + "conver/cloud.js"
        # cloud_url = MEDIA_ROOT + '/point/item/' + str(point_index) + '_conver/cloud.js'
        cloud_url = 'api/media/point2/item/' + str(CONFIG_FILE.point_index) + '_conver/cloud.js'
        # cloud_url = 'api/media/point2-5/item/' + str(CONFIG_FILE.point_index) + '_conver/cloud.js'
        # point_cloud_list = cache.get('point_cloud')
        point_cloud = {
            'cloud_id': CONFIG_FILE.point_index,
            'cloud_name': '点云名称',
            'cloud_url': cloud_url,
            'cloud_project': '点云项目',
            'project': 0
        }
        point_list.append(point_cloud)
        CONFIG_FILE.point_index += 1
    cache.set('point_cloud', point_list)
    if len(point_list) > 1:
        point_cloud_list = {
            "track": tract_data_list,  # tract_data CONFIG_FILE.TRACT_DATA
            "point": point_list,
            "message": True
        }
    else:
        point_cloud_list = {
            "track": tract_data_list,  # tract_data CONFIG_FILE.TRACT_DATA
            "point": point_list,
            "message": True
        }

    # if point_cloud_list is not None:
    #     point_cloud_list.append(point_cloud)
    # else:
    #     point_cloud_list = [point_cloud]
    # cache.set('point_cloud', point_cloud_list)  # 设置缓存数据
    return JsonResponse(point_cloud_list)


@csrf_exempt
def modify_config(request):
    json_bytes = request.body
    modify_dict = json.loads(json_bytes)
    print(modify_dict)
    for key in modify_dict:
        print('key----', key)
        print(CONFIG_FILE.SCREEN_ORIENTATION)
        CONFIG_FILE.SCREEN_ORIENTATION = modify_dict['SCREEN_ORIENTATION']
        print('修改', CONFIG_FILE.SCREEN_ORIENTATION)
    return JsonResponse({'message': 'OK'}, status=200, safe=False)


@csrf_exempt
def disk(request):
    st = os.statvfs(folder)
    space = st.f_bavail * st.f_frsize / 1024 / 1024 // 1024
    return JsonResponse({'message': 'OK', 'space': space}, status=200, safe=False)


@csrf_exempt
def config(request):
    if request.method == 'POST':
        ConfigInfo.objects.create(is_record=True)
        return JsonResponse({'is_record': 'ok'}, status=200, safe=False)
    elif request.method == 'GET':
        get_info = ConfigInfo.objects.all()[0]
        return JsonResponse({'is_record': get_info.is_record}, status=200, safe=False)

    elif request.method == 'PATCH':
        json_bytes = request.body
        modify_dict = json.loads(json_bytes)
        get_info = ConfigInfo.objects.all()[0]
        get_info.is_record = modify_dict['is_record']
        get_info.save()
    elif request.method == 'DELETE':
        get_info = ConfigInfo.objects.get(id=1)
        get_info.delete()
        return JsonResponse({'is_record': 'ok'}, status=200, safe=False)
    return JsonResponse({'is_record': get_info.is_record}, status=200, safe=False)

