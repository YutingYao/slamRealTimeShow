#！/usr/bin/env python3
import sys
# sys.path.append("/opt/ros/noetic/lib/python3/dist-packages")
# import rospy
# from std_msgs.msg import String
import subprocess
import json






def param_str_to_dict(str_param):
    print('str_param.', str_param)
    dict_param = {}
    str_param = '{"' + \
        str_param[:-1].replace(': ', '": ').replace('\n', ', "') + "}"
    print('zhuanuan--str_param--', str_param)
    dict_param = eval(str_param)
    for (key, value) in dict_param.items():
        if type(value) == float:
            dict_param[key] = round(value, 3)
    return dict_param


def param_dict_to_str(dict_param):
    str_param = str(dict_param)
    str_param = json.dumps(str_param).replace('"', '').replace(
        'False', 'false').replace('True', 'true')
    return str_param


def aabb_cmd():
    aabb_cmd = '''rosservice call /lio_sam/get_image_projection_param "{change_param: false, lidarForwardRange: 0.0, lidarBackRange: 0.0,
         lidarRightRange: 0.0,jection_param "{change_param: false,   lidarLeftR  #lidarLef  lida  li    lidarLeftRange: 0.0,
          lidarTopRange: 0.0, lidarBottomRange: 0.0}"'''
    ex = subprocess.Popen(aabb_cmd, stdout=subprocess.PIPE, shell=True)


def set_size(out_dict):
    print('???????????????set_size1')
    size_cmd = '''rosservice call /lio_sam/get_feature_extraction_param "change_param: true , mappingSurfLeafSize: '''
    seze_value = out_dict['mappingSurfLeafSize'] + '"'
    size_cmd = size_cmd + seze_value
    ex = subprocess.Popen(size_cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    print('???????????????set_size2')

def get_all_params1():
    # 获取参数的命令
    cmd = """/bin/bash -c '''source /opt/ros/noetic/setup.bash && source /catkin_ws/devel/setup.bash && rosservice call /lio_sam/get_optimization_param "{change_param: false}"'''"""
    # cmd = '''rosservice call /lio_sam/get_optimization_param "{change_param: false}"'''
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    print('out--', out)
    print('err--', err)
    # 得到返回值字符串
    outstr = out.decode()
    # 把字符串转化成字典
    param_dict = param_str_to_dict(outstr)
    return param_dict


def get_all_params():
    # 获取参数的命令
    cmd = """/bin/bash -c '''source /opt/ros/noetic/setup.bash && source /catkin_ws/devel/setup.bash && rosservice call /lio_sam/get_optimization_param "{change_param: false}"'''"""
    # cmd = '''rosservice call /lio_sam/get_optimization_param "{change_param: false}"'''
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    print('out--', out)
    print('err--', err)
    # 得到返回值字符串
    outstr = out.decode()
    # 把字符串转化成字典
    param_dict = param_str_to_dict(outstr)
    return param_dict


def set_modify_params(modify_params):
    param_dict = get_all_params()
    # TODO： 在这里 通过  修改 param_dict 设置新的参数值
    # param_dict['start_work'] = True
    # param_dict['surroundingKeyframeSearchRadius'] = 4.0
    for modify_item in modify_params:
        param_dict[modify_item['key']] = modify_item['value']
    print('???????modify-----', param_dict)
    # 把字典转换成字符
    str_param = param_dict_to_str(param_dict)

    # 修改参数
    str_param = str_param.replace("'success': true", "'change_param': true")

    cmd = '''rosservice call /lio_sam/get_optimization_param '''
    cmd = "/bin/bash -c '''source /opt/ros/noetic/setup.bash && source /catkin_ws/devel/setup.bash && " +cmd + '"' + str_param + '"' + "'''"  #+ '"""' 
    # cmd = cmd + '"' + str_param + '"'
    
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    print('??????????????????????????????out', out)

    # 获取参数的命令
    
    # cmd = '''rosservice call /lio_sam/get_feature_extraction_param "{change_param: false}"'''
    cmd = """/bin/bash -c '''source /opt/ros/noetic/setup.bash && source /catkin_ws/devel/setup.bash && rosservice call /lio_sam/get_feature_extraction_param "{change_param: false}"'''"""

    
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    print('out--', out)
    print('err--', err)
    # 得到返回值字符串
    outstr = out.decode()
    # 把字符串转化成字典
    param_dict_ = param_str_to_dict(outstr)
    param_dict_['odometrySurfLeafSize'] = param_dict['mappingSurfLeafSize']
    


    print('param_dict--', param_dict)
    # 把字典转换成字符
    str_param = param_dict_to_str(param_dict_)

    # 修改参数
    str_param = str_param.replace("'success': true", "'change_param': true")
    print("str_param:::",str_param) # {'change_param': true, 'odometrySurfLeafSize': 0.05}
    cmd = '''rosservice call /lio_sam/get_feature_extraction_param '''
    cmd =  "/bin/bash -c '''source /opt/ros/noetic/setup.bash && source /catkin_ws/devel/setup.bash && " + cmd + '"' + str_param + '"' + "'''"  
    
    
    

    # print('cmdcmdcmdcmd', cmd)
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    print('??????????????????????????????out', out)


    if err == None:
        return {'message': 'OK', 'out': out}
    else:
        return {'message': 'faile', 'out': err}


def perform_cmd(cmd_type):
    
    print(sys.path)
    pub_wait = rospy.Publisher('/chatter', String, queue_size=1)
    rospy.init_node('pub_string', anonymous=True, disable_signals=True)
    pub_wait.publish('开启扫描程序')  # cmd_type


def control_cmd():
    print(sys.path)
    pub_control_point = rospy.Publisher('lio_sam/add_control_point', String, queue_size=1)
    rospy.init_node('pub_string', anonymous=True, disable_signals=True)
    pub_control_point.publish('添加控制点')


# def perform_cmd(cmd):
#     ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
#     out, err = ex.communicate()
#     status = ex.wait()
#     print('???out??????????---', out)
#     print('???err??????????---', err)
#     if out:
#         return {'message': 'Ok'}
#     else:
#         return {'message': 'NO'}


# ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
# out, err = ex.communicate()
# status = ex.wait()
#
# # 得到返回值字符串
# outstr = out.decode()

# # 把字符串转化成字典
# param_dict = param_str_to_dict(outstr)



# param_dict: {
# 'success': False,
# 'start_work': False,
# 'save_fragment': False,
# 'save_original': True,
# 'save_corner': True,
# 'save_surf': False,
# 'save_transformations': True,
# 'secondary_optimization': ##False,
# 'environment_mode': 2,
# 'keyframe_isolation': 0,
# 'isolation_height': 1.2,
# 'loopClosure_isolation_height': 1.9,
# 'mappingCornerLeafSize': 0.02,
# 'mappingSurfLeafSize': 0.2,
# 'surroundingkeyframeAddingDistThreshold': 0.25,
# 'surroundingkeyframeAddingAngleThreshold': 0.12,
# 'surroundingKeyframeDensity': 0.2,
# 'surroundingKeyframeSearchRadius': 4.0}


# TODO：套娃操作

