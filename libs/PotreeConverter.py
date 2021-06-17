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


# TODO:根据文件路径，切割瓦片
def run_PotreeConverter_exe_tile(original_file_path, original_file_name, current_id, project_id):
    (only_file_name, ext) = os.path.splitext(original_file_name)
    # pts_out_src = CONFIG_FILE.SOURCE_POINT_CLOUD_PATH + only_file_name + "conver"  # TODO: 以前瓦片存放文件夹
    pts_out_src = CONFIG_FILE.TILE_PATH + only_file_name + "conver"  # TODO: 修改单独文件夹存放瓦片数据
    #  TODO: cmd 切割命令，需要修改为对应地址
    cmd_cut_xyz = CONFIG_FILE.POTREE_PATH + original_file_path + " -f xyzi" + " -o " + pts_out_src + " --overwrite"
    try:
        print('start cut tile')
        cut_process = subprocess.Popen(cmd_cut_xyz, shell=True)
        wait02 = cut_process.communicate()  # wait(timeout=86400) communicate

    except Exception as e:
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


if __name__ == '__main__':
    # cloud_js_path = run_e572las_and_PotreeConverter_exe(
    #     [
    #         "E:/服务器web3d/ShareCloudServer/media/scene_path/2020/06/23/0623173445_lwktq/station_path/06"
    #         "23174444/original_file/tongzhouqingzhensiMIN/tongzhouqingzhensiMIN.e57"])

    # print("run_e572las_and_PotreeConverter_exe_path", cloud_js_path)
    pass
