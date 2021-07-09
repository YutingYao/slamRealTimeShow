#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# __author__ = 'jiawenquan'
# __date__ = '2018/5/17 0017 16:29'

import subprocess
from libs.globleConfig import CONFIG_FILE

# logger = logging.getLogger(__name__)
# logger = logging.getLogger('django')


# TODO: 执行参数设置命令
def set_scan_parameter(set_params):
    # ['calc', 'mspaint', 'notepad', 'write', 'osk'] ['calc', r'mkdir C:\Users\peiqi\Desktop\1_conver\test2']
    # start = datetime.datetime.now()
    for cmd_v in set_params.values():
        try:
            print('cmd_v--->:', CONFIG_FILE.SCAN_SET[cmd_v])
            # cut_process = subprocess.Popen(cmd_v, shell=True)
            # a = cut_process.communicate()
            # print('打印结果=>:', a)  # TODO：获取修改后的值, 需要添加是否修改成功判断, 如果没修改成功需要，再次修改-直到成功为止
        except Exception as e:
            print("？？？？？？？？？？？？===== process timeout 执行失败结束进程 ======")
            # cut_process.kill()
    # sleep(0.3)  # TODO: 等待一秒钟检查是否已经修改参数
    # end = datetime.datetime.now()
    # print('花费时间=>:', end - start)
    return True


def task():
    print('我会被每分钟执行一次，并且将内容输出到log文件中')
