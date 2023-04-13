6# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 5 2021

@author: 鍾政儒
"""
import cv2
import os
import time
import find_range as fr

import numpy as np 
import csv

path = "./Save_Img_detailDate" #資料夾目錄 
Save_Path = "./Lead_img_detailDate"

def delete_grid(img, Loc, imgType):
    """
    delete points of EKG graph's grid
    input:EKG graph,lead Location
    ouput:the EKG graph which has no grid point
    """
    (l, r, b, t) = Loc
    print('(l,r,b,t) = ',Loc,'w = ',Loc[1]-Loc[0],'h = ',Loc[3]-Loc[2])
# =============================================================================
#lead去格線
    if(imgType == 2):
        for row in range(b,t):
            for col in range(l,r):
                if img[row,col] == 0:
                    if(row == b  or col == l or row == t-1 or row == t-2 or col == r-1 or col == r-2):
                        img[row,col] = 255
                    else:
                        #if 方格周圍沒點 方格四點變白
                            if (img[row-1,col] == 255 and img[row-1,col+1] == 255 and
                            img[row,col-1] == 255 and img[row,col+1] == 0 and img[row,col+2] == 255 and
                            img[row+1,col-1] == 255 and img[row+1,col] == 0 and 
                            img[row+1,col+1] == 0 and img[row+1,col+2] == 255 and
                            img[row+2,col] == 255 and img[row+2,col+1] == 255):
                                img[row,col] = 255
                                img[row,col+1] = 255
                                img[row+1,col] = 255
                                img[row+1,col+1] = 255

    else:
        for row in range(b,t):
            for col in range(l,r):
                if img[row,col] == 0:
                    if(row == b or col == l or row == t-1 or col == r-1):
                        img[row,col] = 255
                    else:
                        #if 上下左右沒點 自身變白
                            if (img[row-1,col-1] == 255 and img[row-1,col] == 255 and img[row-1,col+1] == 255 and
                            img[row,col-1] == 255 and img[row,col+1] == 255 and
                            img[row+1,col-1] == 255 and img[row+1,col] == 255 and img[row+1,col+1] == 255):
                                img[row,col] = 255
    
# =============================================================================
#                 #若不是心電波->去垂直線
#                 if (col-l) % 59 == 47 and (col-l) <= 280:# left 1/5 col of grid points
#                     #出現直格線位置,判斷是否為波
#                     if(img[row,col-1] == 0 and img[row,col+1] == 0):
#                         #看左右判斷線
#                         img[row,col] = 0
#                     elif ((img[row-1,col-1] == 0 and img[row+1,col+1] == 0) or
#                          (img[row+1,col-1] == 0 and img[row-1,col+1] == 0)):
#                         #看斜線判斷線
#                         img[row,col] = 0
#                     else:
#                         img[row,col] = 255
#                 elif (col-l) % 59 == 48 and (col-l) > 280:# right 4/5 col of grid points
#                     #出現直格線位置,判斷是否為波
#                     if(img[row,col-1] == 0 and img[row,col+1] == 0):
#                         #看左右判斷線
#                         img[row,col] = 0
#                     elif ((img[row-1,col-1] == 0 and img[row+1,col+1] == 0) or
#                          (img[row+1,col-1] == 0 and img[row-1,col+1] == 0)):
#                         #看斜線判斷線
#                         img[row,col] = 0
#                     else:
#                         img[row,col] = 255
# =============================================================================

def SaveLead(img, lead, loc, SavePath, file):
    (l, r, b, t) = loc
    img_lead = img[b:t, l:r]
    if os.path.isfile(SavePath + '/'+ str(lead) + file[-4:]):
        print("img exist,skip\n")
    else:
        print("save img\n")
        cv2.imwrite(SavePath + '/'+ str(lead) + file[-4:], img_lead)

if __name__ == '__main__':

    files = os.listdir(path) #得到資料夾下的所有檔名稱 
    print('files = ', files, '\n') #測試data資料夾下所有檔案名稱是否有誤
    sub_dir = [] 
    
    try:
        os.makedirs(Save_Path)
        print('Make save dir - Save_Path')
        # 檔案已存在的例外處理
    except FileExistsError:
        print('Save_Path dir have already exist')

            
    for file in files: #遍歷資料夾 
        f = os.path.join(path, file) #產生檔案的絕對路徑
        
        print('--------------------------------------')
        
        if (f[-1] != 'g'):
            continue
        print('graph :', file[0:-4])
        time_start = time.time()
        
        img = cv2.imread(f) #讀圖
        img_type =  int(file.split('_')[0])
        range_shift = fr.find_range(img,img_type)
        Loc = fr.combine_shift(range_shift)
        img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #灰階  
        
        # 顯示圖片
        #cv2.imshow('My Image', cv2.resize(img_g, (1300, 700), interpolation=cv2.INTER_AREA))
        # 按下任意鍵則關閉所有視窗
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        print(Loc)

        ret, img_g = cv2.threshold(img_g,120,255,cv2.THRESH_BINARY)
        delete_grid(img_g, Loc, img_type)
        
        # 顯示圖片
        #cv2.imshow('My Image', cv2.resize(img_g, (1300, 700), interpolation=cv2.INTER_AREA))
        # 按下任意鍵則關閉所有視窗
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        Save_Path_Img = Save_Path + '/' + file[0:-4]

        try:
            os.makedirs(Save_Path_Img)
            print(Save_Path_Img)
            # 檔案已存在的例外處理
        except FileExistsError:
            print(Save_Path_Img + '  have alreafy exist')
        
        # for lead in range(1,14):
        for lead in range(1,13):
            lead_shift = fr.find_lead(img_g, range_shift,img_type, lead)
            Loc = fr.combine_shift(range_shift, lead_shift)
            SaveLead(img_g, lead, Loc, Save_Path_Img, file)
        
        time_end = time.time()
        time_c= time_end - time_start
        print('time cost', time_c, 's')

        print('----------------')