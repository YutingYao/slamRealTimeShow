# -*- coding:utf-8 -*-
import threading
import time
import json
from libs.WebSocket import send_message

cancel_tmr = False


class SendHistoryCloud:
    def __init__(self):
        self.cloud_list = []
        self.max_id = 0
        self.cloud_id = 0
        self.timer = None

    def start(self):
        dict_data = {
            history_cloud_id: self.cloud_id,
            type: 'history'
        }
        send_message(json.dumps(dict_data))  # 发送给前端状态值
        self.timer = threading.Timer(0.5, start).start()

    # 开始定时任务
    def heart_beat(self):
        # 每隔3秒执行一次
        self.timer = threading.Timer(0.5, heart_beat).start()

    def stop(self):
        # 取消定时器
        self.timer.cancel()
        self.timer = None
