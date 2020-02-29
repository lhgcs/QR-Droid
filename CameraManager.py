#!/usr/bin/env python3

'''
@Description: 摄像头工具类
@Version: 1.0
@Autor: lhgcs
@Date: 2019-08-29 14:57:14
@LastEditors: Please set LastEditors
@LastEditTime: 2020-02-29 09:14:44
'''


import time

import cv2
import numpy as np


class CameraManager(object):

    def __init__(self):
        self.__deviceNum = -1
        self.__capture = None
        self.__widget = 1024
        self.__height = 768
        self.__exposureAdjustTime = 0
        self.__exposureAdjustSpace = 700

    def __del__(self):
        if self.__capture is not None:
            self.__capture.release()
        cv2.destroyAllWindows()

    '''
    @description: 摄像头是否打开啊
    @param {type} 
    @return: 
    '''
    def is_open(self):
        if self.__capture is None:
            return False
        return True if self.__capture.isOpened() else False

    '''
    @description: 打开指定摄像头
    @param {type} 
    @return: 
    '''
    def open_camera(self, devideNum):
        num = int(devideNum)
        if num >= 0:
            self.__capture = cv2.VideoCapture(num)
            if self.__capture.isOpened():
                print("camera " + str(num) + " opened")
                self.__set_frame()
                self.__deviceNum = num
                return True

        self.__deviceNum = -1
        self.__capture = None
        return False

    '''
    @description: 尝试打开摄像头
    @param {type} 
    @return: 
    '''
    def try_open_camera(self):
        num = 20

        while num >= 0:
            if self.open_camera(num):
                return True
            num -=1
        
        self.__deviceNum = -1
        self.__capture = None
        return False
    
    '''
    @description: 设置帧参数
    @param {type} 
    @return: 
    '''
    def __set_frame(self):

        # PC端
        self.__capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1);    # 开启自动曝光
        # self.__capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3);      # 开启手动曝光
        # ARM
        # self.__capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75); # 开启自动曝光
        # self.__capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25); # 开启手动曝光

        # self.__capture.set(cv2.CAP_PROP_AUTO_WB, 0)         # 关闭自动白平衡
        self.__capture.set(cv2.CAP_PROP_AUTO_WB, 1)         # 开启自动白平衡

        # self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.__widget);   # 宽度
        # self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__height);  # 高度
        # self.__capture.set(cv2.CAP_PROP_FPS, 10);           # 帧率
        # self.__capture.set(cv2.CAP_PROP_CONTRAST,50);       # 对比度 50
        # self.__capture.set(cv2.CAP_PROP_SATURATION, 50);    # 饱和度 50
        # self.__capture.set(cv2.CAP_PROP_HUE, 0);            # 色调 50
        # self.__capture.set(cv2.CAP_PROP_EXPOSURE, 50);      # 曝光 50
        # self.__capture.set(cv2.CAP_PROP_BRIGHTNESS, 1);     # 亮度 1

        # 编码格式
        self.__capture.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter.fourcc('M','J','P','G'))

    '''
    @description: BGR三个通道的平均值
    @param {type} 
    @return: 
    '''
    def __get_bgr_avg(self, frame):
        num = frame.size / frame.ndim
        avgB = np.sum(frame[:, :, 0]) / num
        avgG = np.sum(frame[:, :, 1]) / num
        avgR = np.sum(frame[:, :, 2]) / num
        return (avgB, avgG, avgR)

    '''
    @description: 调整曝光
    @param {type} 
    @return: 
    '''
    def __auto_exposure(self, value, isAuto):
        if 0 == isAuto:
            return

        ret = self.__capture.get(cv2.CAP_PROP_AUTO_EXPOSURE)
        # 手动调节曝光
        if 0.25 == ret or 3 == ret:
            exposure = self.__capture.get(cv2.CAP_PROP_EXPOSURE)
            if value < 100:

                if 0.25 == ret:
                    exposure += 0.01
                    exposure = 1 if exposure > 1 else exposure
                else:
                    exposure += 5
                    exposure = 255 if exposure > 255 else exposure

                self.__capture.set(cv2.CAP_PROP_EXPOSURE, exposure)
            elif value > 150:

                if 0.25 == ret:
                    exposure -= 0.01
                    exposure = 0 if exposure < 0 else exposure
                else:
                    exposure -= 5
                    exposure = 0 if exposure < 255 else exposure

                self.__capture.set(cv2.CAP_PROP_EXPOSURE, exposure)
        else:
            print("auto:", ret)

    '''
    @description: 校正曝光
    @param {type} 
    @return: 
    '''
    def __adjust(self, frame):
        if time.time() - self.__exposureAdjustTime > self.__exposureAdjustSpace:
            avgB, avgG, avgR = self.__get_bgr_avg(frame)
            self.__auto_exposure((avgB + avgG + avgR) / 3, 1)
            self.__exposureAdjustTime = time.time()

    '''
    @description: 获取帧并处理
    @param {type} 
    @return: 
    '''
    def get_frame_and_process(self, image_process=None):
        if self.is_open():
            # 读取图像
            ret,frame = self.__capture.read()
            if True == ret and frame is not None:
                if image_process is not None:
                    dst = image_process(frame)
                    return dst
                return frame
            else:
                print("can not get frame")
        return None

    '''
    @description: 显示
    @param {type} 
    @return: 
    '''
    def show(self, image):
        if image is not None:
            cv2.imshow("frame", image)
            cv2.waitKey(100)
        else:
            print("image is none")
