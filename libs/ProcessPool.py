#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020/6/8 21:01
#  @Author  : allen_jia
#  @Site    :
#  @File    : ProcessPool.py
#  @Software: PyCharm
# -*- coding: utf-8 -*-
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from django.test import TestCase

#   Create your tests here.
#   ponit 单词写错,
#   上传 原来的删除
from concurrent.futures.thread import ThreadPoolExecutor

import logging

logger = logging.getLogger(__name__)
logger = logging.getLogger('django')

# logger.error("错误")
# logger.info("警告")

class ProcessPool(object):
    def __init__(self):

        # 线程池
        self.executor = ProcessPoolExecutor(20)
        # 用于存储每个项目批量任务的期程
        self.future_dict = {}

        self.lock = threading.Lock()

    # 检查某个项目是否有正在运行的批量任务
    def is_project_thread_running(self, project_id):

        future = self.future_dict.get(project_id, None)
        if future and future.running():
            # 存在正在运行的批量任务
            return True
        return False

    # 展示所有的异步任务
    def check_future(self):

        data = {}
        for project_id, future in self.future_dict.items():
            data[project_id] = future.running()
        return data

    def __del__(self):

        self.executor.shutdown()

    # 主线程中的全局线程池
    # global_thread_pool的生命周期是Django主线程运行的生命周期

def batch_thread(self):
    global_process_pool.lock.acquire()  # TODO: 获取锁
    try:
        ...
        global_process_pool.lock.release()
    except Exception:
        trace_log = traceback.format_exc()
        logger.error('异步任务执行失败:\n %s' % trace_log)
        global_process_pool.lock.release()  # TODO: 释放锁


if __name__ == '__main__':

    global_process_pool = ProcessPool()

    # 提交一个异步任务
    # future = global_thread_pool.executor.submit(batch_thread, project_id)
    future = global_process_pool.executor.map(batch_thread, "project_id")  # 任务函数,任务id

    global_process_pool.future_dict["project_id"] = future
    # 检查异步任务
    if global_process_pool.is_project_thread_running("project_id"):
        raise exceptions.ValidationError(detail='存在正在处理的批量任务，请稍后重试')


    # 查看所有异步任务
    def check_future(request):
        data = global_process_pool.check_future()
        # return HttpResponse(status=status.HTTP_200_OK, content=json.dumps(data))
