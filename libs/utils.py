#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = 'jiawenquan'
__date__ = '2018/5/17 0017 16:29'

from PIL import Image
import time, base64, os, random
import logging
import subprocess
import datetime

logger = logging.getLogger(__name__)
logger = logging.getLogger('django')


# logger.error("错误")
# logger.info("警告")

# 用来生成指定尺寸的封面图
def make_thumb(path, size_width, size_height):
    ratio = size_width / size_height

    try:
        pixbuf = Image.open(path)
    except IOError:
        # print("Error: 没有找到文件或读取文件失败")
        logger.error("Error: 没有找到文件或读取文件失败:", path)
        return None

    # pixbuf = Image.open(path)
    width, height = pixbuf.size
    if width < size_width or height < size_height:
        # 如果 长或者宽 小于缩略图尺寸  那么不用 .thumbnail 方法调整尺寸，换用 .resize调整尺寸
        if width / height >= ratio:
            # 过宽的情况 以高度作为缩放标准
            width = (size_height / height) * width
            height = size_height
            # pixbuf.thumbnail((width, height), Image.ANTIALIAS)
            pixbuf = pixbuf.resize((int(width), int(height)))

            redundant_size = (width - size_width) / 2

            region = (redundant_size, 0, width - redundant_size, size_height)
            # 裁切图片
            pixbuf = pixbuf.crop(region)
        elif width / height <= ratio:
            # 过高的情况 以宽度作为缩放标准
            height = (size_width / width) * height
            width = size_width
            # pixbuf.thumbnail((width, height), Image.ANTIALIAS)
            pixbuf = pixbuf.resize((int(width), int(height)))

            redundant_size = (height - size_height) / 2
            region = (0, redundant_size, size_width, height - redundant_size)
            pixbuf = pixbuf.crop(region)

    elif width / height >= ratio:
        # 过宽的情况 以高度作为缩放标准
        width = (size_height / height) * width
        height = size_height
        pixbuf.thumbnail((width, height), Image.ANTIALIAS)

        redundant_size = (width - size_width) / 2

        region = (redundant_size, 0, width - redundant_size, size_height)
        # 裁切图片
        pixbuf = pixbuf.crop(region)


    elif width / height <= ratio:
        # 过高的情况 以宽度作为缩放标准
        height = (size_width / width) * height
        width = size_width
        pixbuf.thumbnail((width, height), Image.ANTIALIAS)

        redundant_size = (height - size_height) / 2
        region = (0, redundant_size, size_width, height - redundant_size)
        pixbuf = pixbuf.crop(region)

    return pixbuf


# 用来生成指定尺寸的封面图
def make_auto_thumb(path, size_length=720):
    """
    把图片的最长边缩放到 size_length的尺寸
    缩放图片的 长宽比例不变
    :param path: 图片路径
    :param size_length: 最长边的缩放尺寸
    :return: pixbuf
    """
    ratio = size_length / size_length

    try:
        pixbuf = Image.open(path)
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
        logger.error("Error: 没有找到文件或读取文件失败:", path)

        return None

    # pixbuf = Image.open(path)
    width, height = pixbuf.size

    if width < size_length and height < size_length:
        return pixbuf


    elif width / height >= ratio:
        # 过宽的情况 以高度作为缩放标准
        width = size_length
        height = (size_length / width) * height
        pixbuf.thumbnail((width, height), Image.ANTIALIAS)




    elif width / height <= ratio:
        # 过高的情况 以宽度作为缩放标准
        width = size_length
        height = (size_length / width) * height
        pixbuf.thumbnail((width, height), Image.ANTIALIAS)

    return pixbuf


def base64_turn_png(str_base64, path=None, image_type="avatar"):
    """
    这里存在极少数会出现 同一秒 写入图片的bug
    base64 字符串保存为 png 图片
    :param str_base64:      base64
    :param path:            path 写入的文件路径 默认为None 根据时间自动生成路径  默认是头像的保存路径
    :param image_type:      avatar 默认头像   cover 模型的封面图
    :return:  path or None  返回media 文件夹下分割处理后的路径   转化失败返回 None
    """
    # print(type)
    if not path:

        if image_type == "avatar":
            # 自动生成头像图片路径
            # 系统当前时间年份
            year = time.strftime('%Y')
            # 月份
            month = time.strftime('%m')
            # 日期
            # day = time.strftime('%d')
            # 具体时间 小时分钟毫秒
            mdhms = time.strftime('%m%d%H%M%S')

            str_random = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], 5))

            # u"./media/file/" + year + "/" + month + "/" + day + "/" + mdhms + "/%s" % name
            path = u'./media/head_portrait/%s/%s/%s%s%s' % (year, month, mdhms, str_random, ".png")

        elif image_type == "cover":
            # 自动生成头像图片路径
            # 系统当前时间年份

            year = time.strftime('%Y')
            # 月份
            month = time.strftime('%m')
            # 日期
            # day = time.strftime('%d')
            # 具体时间 小时分钟毫秒
            mdhms = time.strftime('%m%d%H%M%S')
            str_random = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f', 'e', 'd', 'c', 'b', 'a'], 5))
            # u"./media/file/" + year + "/" + month + "/" + day + "/" + mdhms + "/%s" % name
            path = u'./media/cover/%s/%s/%s%s%s' % (year, month, mdhms, str_random, ".png")

    try:
        img_data = base64.b64decode(str_base64)

        fpath, fname = os.path.split(path)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径

        file = open(path, 'wb')
        file.write(img_data)
        file.close()
    except (RuntimeError, TypeError, NameError):  # as 加原因参数名称
        # print('Exception: ', RuntimeError, TypeError, NameError)
        logger.error('Exception: ', RuntimeError, TypeError, NameError, path)

        return None
    # print(path.split("media/")[1])
    return path.split("media/")[1]


# TODO: 执行参数设置命令
def set_scan_parameter(set_params):
    # ['calc', 'mspaint', 'notepad', 'write', 'osk'] ['calc', r'mkdir C:\Users\peiqi\Desktop\1_conver\test2']
    # start = datetime.datetime.now()
    for cmd in ['Date']:
        try:
            cut_process = subprocess.Popen(cmd, shell=True)
            a = cut_process.communicate()
            print('打印结果=>:', a)  # TODO：获取修改后的值, 需要添加是否修改成功判断, 如果没修改成功需要，再次修改-直到成功为止
        except Exception as e:
            # print("？？？？？？？？？？？？===== process timeout 执行失败结束进程 ======")
            cut_process.kill()
    # sleep(0.3)  # TODO: 等待一秒钟检查是否已经修改参数
    # end = datetime.datetime.now()
    # print('花费时间=>:', end - start)
    return True


def task():
    print('我会被每分钟执行一次，并且将内容输出到log文件中')
