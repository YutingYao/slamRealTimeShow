#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = 'jiawenquan'
__date__ = '2018/5/17 0017 16:29'

from PIL import Image
import time, base64, os, random
import logging

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


# str_base64 = """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"""
# print(base64_turn_png(str_base64, path=None, image_type="cover"))


def task():
    print('我会被每分钟执行一次，并且将内容输出到log文件中')
