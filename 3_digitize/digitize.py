# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 13:53:26 2021

@author: 鍾政儒
"""
import cv2
import os

import numpy as np 
import csv
#import matplotlib.pyplot as plt

path = "./Lead_img_dmnoviolate_nooverlapping" #資料夾目錄 
Save_Path = "./Save_csv_dmnoviolate_nooverlapping"

def sortList(list, sortIndex, delimiter):
    temp1 = []
    temp2 = []
    for i in range(len(list)):
        temp1.append(list[i].split(delimiter))
    temp1.sort(key = lambda s: int(s[sortIndex]))
    for i in range(len(temp1)):
        string=''
        for j in range(len(temp1[i])):
            if j == len(temp1[i])-1:
                string = string + temp1[i][j]
                temp2.append(string)
            else:
                string = string + temp1[i][j] + delimiter
    # print(temp2)
    return temp2

def imgResize(img_type, img, shape):
    
    if img_type == 1:
        img = img[ 0:shape[0], int(shape[1]/13):int(shape[1]/13*7) ]   
    elif img_type ==2:
        img = img[ 0:shape[0], 5:int(shape[1]/12.5*12)+5 ]  

    if img.shape[1] >= 1024:
        img_resize = cv2.resize(img,(1024,round(img.shape[0]*1024/img.shape[1])),interpolation=cv2.INTER_AREA)
    else:
        img_resize = cv2.resize(img,(1024,round(img.shape[0]*1024/img.shape[1])),interpolation=cv2.INTER_CUBIC)

    # ret, img_resize = cv2.threshold(img_resize,200,255,cv2.THRESH_BINARY)

    return img_resize
    
    # type 3 ~ 13 待做

def digitize(img, shape):

    digitizeArr = []
    previousPosition = int(shape[0]/2)
    checkBlack = False
    minPosition = 999

    for i in range(shape[1]):
        blackPointTopPosition = []
        for j in range(shape[0]):
            if img[j, i] == 255:
                checkBlack = False
            else:
                if checkBlack == False:
                    blackPointTopPosition.append(j)
                    checkBlack = True
                else:
                    continue
        if len(blackPointTopPosition) != 0: 
            distance = [abs(x - previousPosition) for x in blackPointTopPosition]
            position = blackPointTopPosition[distance.index(min(distance))]
            digitizeArr.append(shape[0]-position)
            previousPosition = position
            if  shape[0]-position < minPosition:
                minPosition = shape[0]-position
        else:
            digitizeArr.append(shape[0]-previousPosition)
            if  shape[0]-previousPosition < minPosition:
                minPosition = shape[0]-previousPosition

    print('minPosition ', minPosition)
    for i in range(len(digitizeArr)):
        temp = digitizeArr[i] - minPosition
        digitizeArr[i] = temp
        
    return digitizeArr


def saveCSV(EKGname, lead_1to12):
    """
    Save each lead values to csv file
    input:EKG number, lead values
    output:csv file
    """
#    FILEname = os.path.join(".\EKG value files", EKGname+".csv")
    FILEname =  EKGname + ".csv"
    # 開啟輸出的 CSV 檔案
    with open(FILEname, 'w', newline='') as csvfile:
        
      # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
      # 寫入13列資料
        writer.writerows(lead_1to12)

if __name__ == '__main__':
# =============================================================================
    #copy from main file
# =============================================================================
# #    img = cv2.imread("./EKG/00823815/1/00823815_20170912_EKG_1_1_6.jpg") #用第一型的心電圖當範例來源圖片
# #    img = cv2.imread("./Sample_Image/2.jpg")
# #    img = cv2.imread("./EKG/00721757/1/00721757_20100608_EKG_1_1_7.jpg") #有8mv的(V1~V6)
# =============================================================================
#    img = cv2.imread("./Save_Img/3/1/20170815_OT_1_1_3.jpg")
    EKGs = os.listdir(path)
    EKGs = sortList(EKGs, 1, '_')
    # print('EKGs = ', EKGs, '\n') #測試data資料夾下所有檔案名稱是否有誤

    try:
        os.makedirs(Save_Path)
        print('make save dir')
        # 檔案已存在的例外處理
    except FileExistsError:
        print('save dir exist')

    for EKG in EKGs: #遍歷資料夾 
        print(EKG)
        if os.path.isfile(Save_Path + '/' + EKG + '.csv'):
            print("csv exist, skip\n")
            continue
        else:
            img_type =  int(EKG.split('_')[0])
            leadPath = os.path.join(path, EKG) #產生檔案的絕對路徑
            leads = os.listdir(leadPath)
            if len(leads) != 12:
                continue
            else:
                leads = sortList(leads, 0, '.')
                imgArr = []
                with open(Save_Path + '/' + EKG + '.csv', 'w', newline='') as csvfile:
                    for i in range(len(leads)):
                        print("lead ",i+1)
                        img = cv2.imread(leadPath + '/' + leads[i], cv2.IMREAD_GRAYSCALE)
                        shape = img.shape
                        img_resize = imgResize(img_type, img, shape)

                        #影像增強
                        blur_img = cv2.GaussianBlur(img_resize, (0, 0), 20)
                        img_resize = cv2.addWeighted(img_resize, 1.2, blur_img, -0.2, 0)
                        ret, img_resize = cv2.threshold(img_resize,200,255,cv2.THRESH_BINARY)

                        shape = img_resize.shape
                        #數位化
                        digitizeArr = digitize(img_resize, shape)
                        writer = csv.writer(csvfile)
                        writer.writerows([digitizeArr])
