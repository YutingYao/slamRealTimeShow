#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
from multiprocessing import Process
from slamShow.settings import MEDIA_ROOT
from libs.globleConfig import CONFIG_FILE
from django.core.cache import cache


# TODO:根据文件路径，切割瓦片
def run_PotreeConverter_exe_tile(original_file_path, original_file_name, current_id, project_id):
    (only_file_name, ext) = os.path.splitext(original_file_name)
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
    point_cloud_list = cache.get('point_cloud')
    point_cloud = {
        'cloud_id': current_id,
        'cloud_name': '点云名称',
        'cloud_url': cloud_url,
        'cloud_project': '点云项目',
        'project': project_id
    }
    if point_cloud_list is not None:
        point_cloud_list.append(point_cloud)
    else:
        point_cloud_list = [point_cloud]
    cache.set('point_cloud', point_cloud_list)  # 设置缓存数据
    if CONFIG_FILE.OPEN_SOCKET:
        circle_list = cache.get('CIRCLE_DATA')
        track_list = cache.get('TRACT_DATA')
        track_list = track_list[point_cloud.cloud_id]
        send_message({'status': 'null', 'cloud': {
            "track": [track_list],  # tract_data CONFIG_FILE.TRACT_DATA
            "point": [point_cloud],
            "circle_point": circle_list,  # CONFIG_FILE.CIRCLE_DATA circle_point_list
            "message": True
        }})  # 发送给前端状态值


if __name__ == '__main__':
    print("cloud_js_path")
