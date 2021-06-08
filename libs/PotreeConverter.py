#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020/6/10 11:39
#  @Author  : allen_jia
#  @Site    :
#  @File    : PotreeConverter.py
#  @Software: PyCharm
import os
import shutil
import subprocess
from multiprocessing import Process, Pool
import logging
from slamShow.settings import MEDIA_ROOT
# from libs.globleConfig import CURRENT_PROJECT, POTREE_PATH, SOURCE_POINT_CLOUD_PATH
from libs.globleConfig import CONFIG_FILE
from pointCloud.models import PointCloudChunk
from django.core.cache import cache

logger = logging.getLogger(__name__)
logger = logging.getLogger('django')
complete_list = [1, 2, 3, 4, 5]
complete_load_index = -1


# logger.error("错误")
# logger.info("警告")
# TODO: list src
def run_e572las_exe(list_src):
    list_laz_src = []
    for src in list_src:

        (filepath, tempfilename) = os.path.split(src)
        (filename, extension) = os.path.splitext(tempfilename)
        laz_src_name = os.path.join(filepath, filename + ".laz").replace('\\', '/')
        cmdstr = r".\potree\windowsE57PotreeConverter\e572las.exe -v -i " + src + " -o " + laz_src_name
        print(cmdstr)
        myPopenObj01 = subprocess.Popen(cmdstr)
        try:

            wait01 = myPopenObj01.wait(timeout=43200)
            print("wait:", wait01)

            if wait01 != 0:
                logger.error("e57 to laz failure!", src + " " + laz_src_name)
                print("e57 to laz failure!")
                continue
                # return None
            if not os.path.exists(laz_src_name):
                continue
                # return None
            print("e57 to laz succeed!")
            logger.info("e57 to laz failure!", src + " " + laz_src_name)
            list_laz_src.append(laz_src_name)
            # return laz_src_name
        except Exception as e:
            print("===== process timeout 执行失败结束进程 ======")
            logger.error(repr(e), "===== process timeout 执行失败结束进程 ======", src + " " + laz_src_name)
            myPopenObj01.kill()
            # return None

    # TODO: 得到此文件夹中 las、laz 以外的全部文件夹，文件，全部删除，
    return list_laz_src


def run_PotreeConverter_exe(list_src):
    laz_src_name = ""
    out_src = ""
    for src in list_src:
        (filepath, tempfilename) = os.path.split(src)
        (filename, extension) = os.path.splitext(tempfilename)
        laz_src_name += " " + src
        out_src = filepath.replace('\\', '/')
    print(laz_src_name)
    cmdstr = r".\potree\windowsE57PotreeConverter\PotreeConverter.exe " + laz_src_name + " -o " + out_src + " --overwrite"
    print(cmdstr)
    # "PotreeConverter.exe pumpACartesian.laz -o pumpACartesianOut --overwrite"
    myPopenObj01 = subprocess.Popen(cmdstr)
    try:

        wait02 = myPopenObj01.wait(timeout=86400)
        if wait02 != 0:
            print("laz Potree Converter failure!")
            logger.error("laz Potree Converter failure!", src + " " + laz_src_name)

            return None
        print("laz Potree Converter succeed!")
        logger.info("laz Potree Converter succeed!", src + " " + laz_src_name)
        (filepath, tempfilename) = os.path.split(list_src[0])
        cloud_js_path = os.path.join(filepath, "cloud.js").replace('\\', '/')
        print(cloud_js_path)
        if not os.path.exists(cloud_js_path):
            return None

        # TODO: 删除此路径之外的的文件（data，temp，cloud.js,sources.json）
        return cloud_js_path
    except Exception as e:
        print("===== process timeout 执行失败结束进程 ======")
        logger.error(repr(e), "===== process timeout 执行失败结束进程 ======", src + " " + laz_src_name)

        myPopenObj01.kill()

        # TODO: 清空文件夹
        return None


# 测试切割点云程序
def test_run_PotreeConverter_exe(file_name):
    # print('打印点云原始file_name=》：', file_name)
    # 缺少文件路径保存保存逻辑
    # pts_src_name = "C:/Users/peiqi/Desktop/测试点云/python_progress/" + file_name
    pts_src_name = MEDIA_ROOT + "/pointCloud/" + file_name
    # pts_src_name = file_name
    (only_file_name, ext) = os.path.splitext(file_name)
    # pts_out_src = MEDIA_ROOT + "/pointCloud/tile/" + only_file_name + "_conver"
    pts_out_src = MEDIA_ROOT + "/conver/" + only_file_name + "_conver"
    # cmdstr = r".\potree\windowsE57PotreeConverter\PotreeConverter.exe " + laz_src_name + " -o " + out_src + " --overwrite"
    cmdstr = r".\potree\windowsE57PotreeConverter\PotreeConverter.exe " + pts_src_name + " -o " + pts_out_src + " --overwrite"
    cmdstrxyz = r".\potree\windowsE57PotreeConverter\PotreeConverter.exe " + pts_src_name + " -f xyzi" + " -o " + pts_out_src + " --overwrite"
    print('********>:', file_name)
    # if int(only_file_name) > complete_load_index:
    #     complete_load_index = only_file_name
    # "PotreeConverter.exe pumpACartesian.laz -o pumpACartesianOut --overwrite"
    test_path = 'http://192.168.1.46:8000/media/conver/' + only_file_name + "_conver/"
    myPopenObj01 = subprocess.Popen(cmdstr)
    try:

        wait02 = myPopenObj01.wait(timeout=86400)
        if wait02 != 0:
            # print("laz Potree Converter failure!")
            # logger.error("laz Potree Converter failure!", src + " " + laz_src_name)
            print("？？？？？？？？？？？wait02 != 0")
            return None
        # print("laz Potree Converter succeed!")
        # logger.info("laz Potree Converter succeed!", src + " " + laz_src_name)
        # (filepath, tempfilename) = os.path.split(list_src[0])
        # cloud_js_path = os.path.join(filepath, "cloud.js").replace('\\', '/')
        # print(cloud_js_path)
        # if not os.path.exists(cloud_js_path):
        #     return None

        # TODO: 删除此路径之外的的文件（data，temp，cloud.js,sources.json）
        # return cloud_js_path  test_path pts_out_src
        return test_path + 'cloud.js'
    except Exception as e:
        print("？？？？？？？？？？？？===== process timeout 执行失败结束进程 ======")
        # logger.error(repr(e), "===== process timeout 执行失败结束进程 ======", src + " " + laz_src_name)

        myPopenObj01.kill()

        # TODO: 清空文件夹
        return None
    return pts_out_src + '/cloud.js'


# TODO:根据文件路径，切割瓦片
def run_PotreeConverter_exe_tile(original_file_path, original_file_name, current_id, project_id):
    (only_file_name, ext) = os.path.splitext(original_file_name)
    pts_out_src = CONFIG_FILE.SOURCE_POINT_CLOUD_PATH + only_file_name + "conver"  # TODO: 修改后的瓦片存放地址
    #  TODO: cmd 切割命令，需要修改为对应地址
    cmd_cut_xyz = CONFIG_FILE.POTREE_PATH + original_file_path + " -f xyzi" + " -o " + pts_out_src + " --overwrite"
    # cut_process = subprocess.Popen(cmd_cut_xyz, shell=True)
    # ubuntu 下面命令
    # clouds_path = '/api/media/conver/' + only_file_name + "_conver/"
    try:
        print('start cut tile')
        cut_process = subprocess.Popen(cmd_cut_xyz, shell=True)
        wait02 = cut_process.communicate()  # wait(timeout=86400) communicate
        # if wait02 != 0:
        #     # print("？？？？？？？？？？？wait02 != 0")
        #     return None
        # 如果文件不存在，则切割失败 cloud_js_path = os.path.join(filepath, "cloud.js").replace('\\', '/')
        # if not os.path.exists(pts_out_src + '/cloud.js'):
        #     print('文件切割失败')
        #     return None

    except Exception as e:
        # print("？？？？？？？？？？？？===== process timeout 执行失败结束进程 ======")
        cut_process.kill()
        return None

    cloud_url = '/GOSLAMtemp/' + only_file_name + "conver/cloud.js"
    # point_cloud_url = PointCloudChunk(
    #     cloud_project='点云项目',
    #     cloud_name='点云名称',
    #     cloud_url=cloud_url,
    #     cloud_id=current_id,
    #     project_id=project_id
    # )
    # point_cloud_url.save()
    point_cloud_list = cache.get('point_cloud')
    point_cloud = {
        'cloud_id': current_id,
        'cloud_name': '点云名称',
        'cloud_url': cloud_url,
        'cloud_project': '点云项目',
        'project': project_id
    }
    print('write point--', point_cloud)
    if point_cloud_list is not None:
        point_cloud_list.append(point_cloud)
    else:
        point_cloud_list = [point_cloud]
    cache.set('point_cloud', point_cloud_list)  # 设置缓存数据
    # if os.path.isfile(cloud_url):  # 如果cloud_url 为 None 说明切割瓦片失败

    # return 'GOSLAMtemp/' + only_file_name + "conver/" + 'cloud.js'  # clouds_path  pts_out_src + '/cloud.js'


# 读取文件夹，获取文件夹内所有文件信息
def test_read_point_cloud_dir(max_id):
    # MEDIA_ROOT
    # pts_src_name = "C:/Users/peiqi/Desktop/测试点云/python_progress"
    pts_src_name = MEDIA_ROOT + "/pointCloud"
    tile_src_name = MEDIA_ROOT + "/conver"
    # test_path = os.path.join('http://192.168.1.46.com/media/', 'pointCloud')
    try:
        # complete_list.append(666)
        # print('打印本地数据后=>', complete_list)
        list_dir = os.listdir(pts_src_name)
        # print('打印需要切割文件=》：', list_dir)
        number_list = list(range(0, len(list_dir)))
        different_value = 0
        copy_point_dir_num = []
        for item_index in list_dir:
            (item_index_name, item_index_ext) = os.path.splitext(item_index)
            copy_point_dir_num.append(int(item_index_name))
            # if int(item_index_name) not in number_list:
            #     print('item_index_name--->', item_index_name)
            #     different_value += 1
        for item_number in number_list:
            if item_number not in copy_point_dir_num:
                print('item_index_name--->', item_index_name)
                different_value += 1
        max_id += different_value
        print('max_id-->', max_id)
        temporary_list = []
        for item in list_dir:

            (only_file_name, ext) = os.path.splitext(item)
            if item in temporary_list:
                pass
            if os.path.isfile(pts_src_name + '/' + item):
                # print('打印only_file_name=》：', only_file_name)
                if int(only_file_name) >= max_id:
                    item_path = pts_src_name + '/' + item
                    copy_item = {
                        "file": item,
                        "path": item_path
                    }
                    # complete_list.append(copy_item)
                    temporary_list.append(copy_item)
                    # print('打印需要切割文件1=>:', temporary_list)
    except Exception as e:
        print('文件夹遍历出错', e)
        return None
    # print('打印需要切割文件2=>:', temporary_list)
    return temporary_list


# 读取瓦片文件  返回瓦片文件夹内  文件存在数量
def read_conver_dir(conver_path):
    try:
        list_dir = os.listdir(conver_path)
        conver_length = len(list_dir)
    except Exception as e:
        return None
    return conver_length


# 读取瓦片文件  返回点云文件数量
def read_point_cloud_dir(point_cloud_path):
    try:
        list_dir = os.listdir(point_cloud_path)
        point_cloud_number = len(list_dir)
        for item in list_dir:
            pass

    except Exception as e:
        print('文件夹遍历出错', e)
        return None
    return point_cloud_number


# TODO: 读取轨迹文件返回轨迹数据
def read_track(track_path):
    try:
        list_dir = os.listdir(track_path)
        if len(list_dir) > 0:
            # track_file = track_path + "/" + list_dir[0]
            track_file = track_path + "/" + "transformations.txt"
            read_string_list = open(track_file).read().splitlines()
            track_file_list = []
            for item in read_string_list:
                item = item.split(" ")
                for index, item_value in enumerate(item):
                    if index != 7:
                        item[index] = float(item_value)
                track_file_list.append(item)


    except Exception as e:
        print('文件夹遍历出错', e)
        return None
    return track_file_list


# 读取指定点云文件，存在返回True, 否则返回False
def read_point_cloud_file(point_cloud_path):
    try:
        list_dir = os.isfile(point_cloud_path)
        point_cloud_number = len(list_dir)
        for item in list_dir:
            pass

    except Exception as e:
        print('文件夹遍历出错', e)
        return None
    return point_cloud_number


# 创建项目文件夹
def test_move_file(original_path='', target_path=''):
    # os.path.exists(path)
    f1 = "C:/Users/peiqi/Desktop/测试点云/python_progress/0.pts"
    f2 = MEDIA_ROOT + '/pointCloud'
    shutil.move(f1, f2)


# TODO: list src
def run_e572las_and_PotreeConverter_exe(list_src):
    list_laz_path = run_e572las_exe(list_src)
    print(list_laz_path)
    cloud_js_path = run_PotreeConverter_exe(list_laz_path)

    return cloud_js_path


def testCache():
    cache.set('TRACK_DATA', '1111111', 60 * 15)



if __name__ == '__main__':
    # cloud_js_path = run_e572las_and_PotreeConverter_exe(
    #     [
    #         "E:/服务器web3d/ShareCloudServer/media/scene_path/2020/06/23/0623173445_lwktq/station_path/06"
    #         "23174444/original_file/tongzhouqingzhensiMIN/tongzhouqingzhensiMIN.e57"])

    # print("run_e572las_and_PotreeConverter_exe_path", cloud_js_path)
    cloud_js_path = run_PotreeConverter_exe([
        "E:/服务器web3d/ShareCloudServer/media/scene_path/2020/06/23/0623173445_lwktq/station_path/06"
        "23174444/original_file/tongzhouqingzhensiMIN/tongzhouqingzhensiMIN.e57"])
    print("cloud_js_path", cloud_js_path)
