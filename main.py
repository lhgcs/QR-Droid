#!/usr/bin/env python3

'''
@Description: main
@Version: 1.0
@Autor: lhgcs
@Date: 2019-08-28 10:12:49
@LastEditors: Please set LastEditors
@LastEditTime: 2020-02-29 09:44:52
'''

import os
import sys
import json
import time

import cv2
import numpy as np

from CameraManager import CameraManager
from QRcodeUtil import qrcode_image_fast

import logging
# 日志格式
LOG_FORMAT = "[ %(asctime)s  %(levelname)s ] %(message)s"
# 输出到终端
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=LOG_FORMAT)

# 显示窗口
cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)


'''
@description: BGR三个通道的平均值
@param {type} 
@return: 
'''
def get_bgr_avg(frame):
    num = frame.size / frame.ndim
    avgB = np.sum(frame[:, :, 0]) / num
    avgG = np.sum(frame[:, :, 1]) / num
    avgR = np.sum(frame[:, :, 2]) / num
    return (avgB, avgG, avgR)

'''
@description: 获取图片
@param {type}
@return: 
'''
def get_image(camera):
    cnt = 0
    while cnt < 10:
        cnt += 1

        # 读取图像
        image = camera.get_frame_and_process()
        return image
        if image is not None:
            # 图像亮度正常
            if 68 < get_bgr_avg(image)[0] < 188:
                return image
            else:
                logging.error("image error")
            return image
                
        # 给摄像头调整曝光的时间
        time.sleep(0.01)
    return None

'''
@description: 查找摄像头
@param {type} 
@return: 
'''
def find_camera():
    dstDir = u"/dev"
    subStr = u"video"

    # 文件名
    deviceList = os.listdir(dstDir)
    if len(deviceList) <= 0:
        return []
    # 过滤
    deviceList = list(filter(lambda x: True == x.startswith(subStr), deviceList))
    # 截取数字
    deviceList = list(map(lambda x: int(x[len(subStr):]), deviceList))
    return deviceList

if __name__ == "__main__":
    lastTime = 0
    info = None
    isOpen = False

    # 查找摄像头
    deviceList = find_camera()
    if len(deviceList) <= 0:
        logging.error("can not find camera")
        exit(0)

    # 开启摄像头
    camera = CameraManager()
    for i in deviceList:
        if True == camera.open_camera(0):
            isOpen = True
            break
    if False == isOpen:
        logging.error("can not open camera")
    
    while isOpen:
        if cv2.waitKey(10) > 0:
            break

        # 获取帧
        image = get_image(camera)
        if image is None:
            logging.error("get image error")
            time.sleep(0.1)
            continue

        cv2.imshow("frame", image)
        if cv2.waitKey(10) > 0:
            break

        # 解析二维码
        qrcodeData = qrcode_image_fast(image)
        if qrcodeData is None:
            continue

        # 读取图像并解析二维码，如果在3秒内读到同样的字符串则不输出
        now = int(time.time())
        if info == qrcodeData and now - lastTime < 3:
            pass
        else:
            info = qrcodeData
            lastTime = now
            logging.info(info)
