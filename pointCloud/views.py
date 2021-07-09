# -*- coding: utf-8 -*-
import os
import sys
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
                             'socket': CONFIG_FILE.OPEN_SOCKET}, status=200)
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
    # print("cmd out: ", out )
    # print("cmd err: ", err )
    os.popen(cmd)
    return JsonResponse({'message': 'OK'})
    # if out:
    #     return JsonResponse({'message': 'OK','data':time.time()})
    # else:
    #     return JsonResponse({'message': err,'data':time.time()})

    
 
    # except Exception as e:
    #     return JsonResponse(status=202)


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
        return JsonResponse({'message': 'OK'})
    except Exception as e:
        return JsonResponse({'message': 'failed','data':time.time()})


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
        return JsonResponse({'message': 'failed','data':time.time()})

@csrf_exempt
def device_ready(request):
    try:
        CONFIG_FILE.SCAN_STATUS = 'noStart'    # 修改状态值
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
        if os.path.isfile(CONFIG_FILE.DOWNLOAD_PATH_TEST + '/' + item):
            continue
        item_file = os.listdir(CONFIG_FILE.DOWNLOAD_PATH_TEST + item)  # 获取文件
        down_list = []
        if len(item_file) > 0:
            for item_name in item_file:
                if item_name == 'item' or item_name == 'TILE':
                    continue
                item_name = CONFIG_FILE.BROWSE_PATH + item + '/' + item_name
                down_list.append(item_name)
            pass
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
        if 'transformations.pcd' in item_file:
            with open(CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/transformations.pcd', "r") as f:
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
        item_data = {
            'name': item,
            'project_path': CONFIG_FILE.DOWNLOAD_PATH_TEST + item + '/',
            'down_file': down_list,
            'cloud_path': CONFIG_FILE.BROWSE_PATH + item + '/TILE/',
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

@csrf_exempt
def test_websocket(request):
    # SimpleEcho.handleMessage()
    send_message('这是发送值')  # 以后修改为实际状态值
    return JsonResponse({'message': 'OK'}, status=200, safe=False)
