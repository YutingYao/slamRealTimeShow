import subprocess
import json
import time
# import rospy
# from std_msgs.msg import String
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import asyncio
import threading


# from websockets import serve


def param_str_to_dict(str_param):
    dict_param = {}
    str_param = '{"' + \
                str_param[:-1].replace(': ', '": ').replace('\n', ', "') + "}"
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
    size_cmd = '''rosservice call /lio_sam/get_feature_extraction_param "change_param: true,mappingSurfLeafSize: '''
    seze_value = out_dict['mappingSurfLeafSize'] + '"'
    size_cmd = size_cmd + seze_value

    ex = subprocess.Popen(size_cmd, stdout=subprocess.PIPE, shell=True)


def get_all_params():
    # 获取参数的命令
    cmd = '''rosservice call /lio_sam/get_optimization_param "{change_param: false}"'''
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

    # 把字典转换成字符
    str_param = param_dict_to_str(param_dict)

    # 修改参数
    str_param = str_param.replace("'success': false", "'change_param': true")

    cmd = '''rosservice call /lio_sam/get_optimization_param '''

    cmd = cmd + '"' + str_param + '"'

    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    out_dict = param_str_to_dict(out)
    # aabb_cmd()  # 设置aabb
    # set_size(out_dict)  # # 设置size
    return {'message': 'OK',
            'out_value': out,
            'err_value': err}


def perform_cmd_test(cmd):
    ex = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    # if out:
    #     return {'message': 'Ok'}
    # else:
    #     return {'message': 'NO'}


def perform_cmd(cmd_type):
    pub_wait = rospy.Publisher('/chatter', String, queue_size=1)
    rospy.init_node('pub_string', anonymous=True)
    pub_wait.publish(cmd_type)


# futures = [...]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(futures))
# async def echo(websocket, path):
#     async for message in websocket:
#         await websocket.send(message)
#
# async def main():
#     async with serve(echo, "localhost", 8765):
#         await asyncio.Future()  # run forever
#
# asyncio.run(main())


# class SimpleEcho(WebSocket):
#
#     def handleMessage(self):
#         # echo message back to client self.data
#         self.sendMessage('收到消息发送消息')
#
#     def handleConnected(self):
#         print(self.address, 'connected')
#
#     def handleClose(self):
#         print(self.address, 'closed')
#
#
#
#
# server = SimpleWebSocketServer('', 9006, SimpleEcho)
#
# test_send = SimpleEcho(server)
# def fun_timer():
#     print('Hello Timer!')
#     print('等待10秒发送')
#     test_send.handleMessage()
#     # server.send('函数发送消息')
#
#
# timer = threading.Timer(10, fun_timer)
# timer.start()
#
#
# server.serveforever()

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
