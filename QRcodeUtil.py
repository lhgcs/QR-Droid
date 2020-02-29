#!/usr/bin/env python3

'''
@Description: 二维码生成及识别
@Version: 1.0
@Autor: lhgcs
@Date: 2019-05-27 10:33:35
@LastEditors: Please set LastEditors
@LastEditTime: 2020-02-29 09:33:40
'''


import os
import time

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar


'''
@description: 解析本地文件二维码图片
@param {type} 
@return: 
'''
def qrcode_image_local_file(imagePath):
    if not os.path.exists(imagePath):
        raise FileExistsError(imagePath)
    return pyzbar.decode(Image.open(imagePath), symbols=[pyzbar.ZBarSymbol.QRCODE])#解码

'''
@description: 解析图片
@param {type} 
@return: 
'''
def qrcode(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # # 提取二维码的边界框的位置
        # (x, y, w, h) = barcode.rect
        # # 画出二维码的边界框
        # cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)

        # 提取二维码数据
        barcodeData = barcode.data.decode("utf-8")
        # 提取二维码类型
        barcodeType = barcode.type

        # # 在图像上绘制二维码数据
        # text = "{} ({})".format(barcodeData, barcodeType)
        # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (225, 225, 225), 2)

        # 向终端打印条形码数据和条形码类型
        # print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        return barcodeData
    return None

'''
@description: 解析二维码图片
@param {type} 
@return: 
'''
def qrcode_image_fast(image):
    if image is None:
        return None

    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    row = gray.shape[0]
    col = gray.shape[1]
    
    # 只识别正中心的1/2的图像
    # gray = gray[int(row/4):int(row-row/4), int(col/4):int(col-col/4)]

    # 解析
    data = qrcode(gray)
    if data is not None:
        return data

    # 不确定摄像头是否镜像，对图像进行水平翻转，垂直翻转，水平垂直翻转
    li = [1, 0, -1]
    for i in li:
        data = qrcode(cv2.flip(gray, i, dst=None))
        if data is not None:
            return data
    return None
