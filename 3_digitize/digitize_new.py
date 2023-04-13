# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:30:17 2019

@author: 陳俊諺
"""
import cv2
import os
import find_range as fr

import numpy as np 
import csv
#import matplotlib.pyplot as plt

path = r"D:\ECG_DM_Research\BriefDate\AI_0218_dm_briefdate" #資料夾目錄 
Save_Path = "./Save_csv_dmnoviolate_new_0531_1024"
img_type = 1

def delete_grid(img, Loc):
    """
    delete points of EKG graph's grid
    input:EKG graph,lead Location
    ouput:the EKG graph which has no grid point
    """
    (l, r, b, t) = Loc
    print('(l,r,b,t) = ',Loc,'w = ',Loc[1]-Loc[0],'h = ',Loc[3]-Loc[2])
# =============================================================================        
    #lead去格線
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

def CheckValue(img):
    """
    Check Voltage scale
    input:lead img
    ouput:Voltage scale
    """
    #2mv 
    if(sum(sum(img[56:59, 48:71] == 0))) >= 15:
        return 2.0
    #4mv 
    elif(sum(sum(img[86:89, 48:71] == 0))) >= 15:
        return 4.0
    #8mv 
    elif(sum(sum(img[101:104, 48:71] == 0))) >= 15:
        return 8.0
    
def take_peak(img, lead):
    """
    take the hightest point to represent the wave point at each time
    input:lead img, lead number
    output:the lead img which the wave has 1 point has value at each time
    """
    #full lead 2
    if lead == 13:
        for col in range(118,3013):
            for row in range(236):
                if img[row,col] == 0:
                    img[row+1:235,col] = 255
                    continue
    else:
        for col in range(118,1531):
            for row in range(236):
                if img[row,col] == 0:
                    img[row+1:235,col] = 255
                    continue


def digitize(img, lead, volt):
    """
    Change lead img to voltage value
    input:lead img, lead number, voltage scale
    output:1 dim list which has voltage values
    """
#    lead_list = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'FULL II']
    output = [lead,volt]
    
    unitV = (volt/235)
    global value_short
    global value_long 
    
    if lead == 13:
        output.append(2895)
        for col in range(118,3013):
            for row in range(236):
                if img[row,col] == 0:
                    value_long = unitV*(235-row)
                    output.append(value_long)
                    break
                if row == 235:
                    output.append(value_long)
        return(output)
#        print('\nfull lead 2 len =', len(output), '\n full output =', output)
    else:
        output.append(1413)
        for col in range(118,1531):
            for row in range(236):
                if img[row,col] == 0:
                    value_short = unitV*(235-row)
                    output.append(value_short)
                    break
                if row == 235:
                    output.append(value_short)
            
        for i in range(2895-1413):
            output.append(value_short)
        return(output)
#        print('\nlen =', len(output), '\noutput =', output)


def digitize_revise(img, lead, volt):
    """
    Change lead img to voltage value
    input:lead img, lead number, voltage scale
    output:1 dim list which has voltage values
    """
#    lead_list = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'FULL II']
    output = [volt]   
    unitV = (volt/170)
    global value_short
    
    for col in range(1024):
        for row in range(171):
            if img[row,col] == 0:
                value_short = unitV*(170-row)
                output.append(value_short)
                break
            if row == 170:
                output.append(value_short)
        
    return(output)
#        print('\nlen =', len(output), '\noutput =', output)

def saveCSV(EKGname, lead_1to13):
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
        writer.writerows(lead_1to13)
        
def loadCSV(EKGname):
    """
    Load each lead values to csv file
    input:EKG number, lead
    output:lead lists
    """
    out_matrix = []
    FILEname = os.path.join(".\EKG value files", EKGname+".csv")
    with open(FILEname, newline='') as csvfile:
        
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)

        # 以迴圈輸出每一列
        for row in rows:
            del row[0] #lead number
            del row[0] #?mv scale
            del row[0] #length of lead wave
            out_matrix.append(row)
            
#        print(out_matrix)
        return out_matrix               

def graphical(leadValue, leadNumber, volt):
    """
    Draw wave according to lead img by values
    input:list of lead value(matrix), lead number
    output:lead img
    """
    if leadNumber == 13:
        img = np.zeros((236,2895,1), np.uint8)
        # 使用白色填充图片区域,默认为黑色
        img.fill(255)
        
        for col in range(2895):
            for row in range(236):
                if  row == int(235-(235/volt)*float(leadValue[1][col])):
                    img[row,col] = 0

        
    else:
        img = np.zeros((236,1413,1), np.uint8) 
        # 使用白色填充图片区域,默认为黑色
        img.fill(255)
        for col in range(1413):
            for row in range(236):
                if  row == int(235-(235/volt)*float(leadValue[0][col])):
                    img[row,col] = 0

    
def repair(img, lead):
    """
    Draw wave according to lead img which has hole
    input:lead img which has hole, lead number
    output:lead img
    """
    for row in range(236):
        if img[row,0] == 0:
            row_tmp = row
            
    #full lead 2
    if lead == 13:
        for col in range(2895):
            for row in range(236):
                if img[row,col] == 0 and row_tmp > row:
                    img[row:row_tmp,col-1] = 0
                    row_tmp = row
                    continue
                elif img[row,col] == 0 and row_tmp <= row:
                    img[row_tmp:row,col-1] = 0
                    row_tmp = row
                    continue
                
    else:     
        for col in range(1413):
            for row in range(236):
                if img[row,col] == 0 and row_tmp > row:
                    img[row:row_tmp,col-1] = 0
                    row_tmp = row
                    continue
                elif img[row,col] == 0 and row_tmp <= row:
                    img[row_tmp:row,col-1] = 0
                    row_tmp = row
                    continue


            
'''
if __name__ == '__main__':
# =============================================================================
    #copy from main file
# =============================================================================
# #    img = cv2.imread("./EKG/00823815/1/00823815_20170912_EKG_1_1_6.jpg") #用第一型的心電圖當範例來源圖片
# #    img = cv2.imread("./Sample_Image/2.jpg")
# #    img = cv2.imread("./EKG/00721757/1/00721757_20100608_EKG_1_1_7.jpg") #有8mv的(V1~V6)
# =============================================================================
#    img = cv2.imread("./Save_Img/3/1/20170815_OT_1_1_3.jpg")
    files = os.listdir(path) #得到資料夾下的所有檔名稱 
    #print('files = ', files, '\n') #測試data資料夾下所有檔案名稱是否有誤
    sub_dir = [] 
    img_type = 1

    try:
        os.makedirs(Save_Path)
        print('make save dir')
        # 檔案已存在的例外處理
    except FileExistsError:
        print('save dir exist')
        
    for file in files: #遍歷資料夾 
        f = os.path.join(path, file) #產生檔案的絕對路徑
        if os.path.isdir(f): #判斷是否是資料夾,是資料夾才存資料夾名
            sub_dir.append(file) #將資料夾的明子存到list中 
        
        #print('dir = ', sub_dir, '\n') #測試ID檔案名稱是否有誤

    #開始處理每個病人資料
    for ID in sub_dir:
        t_path = os.path.join(path, ID) #產生檔案的絕對路徑
#        print(t_path)
        files = os.listdir(t_path) #得到資料夾下的所有檔名稱
        print('--------------------------------------')
        print('\nthis ID has type', files, 'ECG graph')
        for file in files:
            f = os.path.join(t_path, file) #產生檔案的絕對路徑
            if os.path.isdir(f) and file == str(img_type):
                print('enter ID = ', ID, ' type', img_type, 'ECG graph dir\n')
            
                #進入第n個病人的第一型ECG資料夾
                ID_files = os.listdir(f)
                #num = len(ID_files)
#                n = 1
                for graph in ID_files:
                    graph_path = os.path.join(f, graph) #產生檔案的絕對路徑
                    if (graph_path[-1] != 'g'):
                        continue
                    print('graph :', graph)
                    #Make Dir for save EKG Img
                    DirName = Save_Path + "/" + ID + "/" + str(img_type)
                    try:
                        os.makedirs(DirName)
                        print(graph)
                        # 檔案已存在的例外處理
                    except FileExistsError:
#                       n += 1
                        print(DirName,'dir exist, skip dir creating')
                    #Set path for savefile
                    SavePath = DirName + '/' + graph[0:-4]
                    # 要檢查的檔案路徑

                    # 檢查檔案是否存在
                    if os.path.isfile(SavePath+'.csv'):
                        print("csv exist, skip\n")
                        continue
                    else:
# =============================================================================
# #                         stream = open(graph_path, "rb")
# #                         bytes = bytearray(stream.read())
# #                         numpyarray = np.asarray(bytes, dtype=np.uint8)
# #                         img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
# =============================================================================
                        img = cv2.imread(graph_path) #讀圖
# =============================================================================
#                         cv2.imshow("EKG", img)
#                         cv2.waitKey (0)
#                         cv2.destroyAllWindows()
# =============================================================================
                        range_shift = fr.find_range(img, img_type)
#                        lead_shift = fr.find_lead(range_shift, img_type, lead)
                        Loc = fr.combine_shift(range_shift)
                        img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #灰階  
                        output = []
    
                        ret, img_g = cv2.threshold(img_g,80,255,cv2.THRESH_BINARY)
                        (l, r, b, t) = Loc
                        delete_grid(img_g, Loc)
# =============================================================================
#                        img_lead = img_g[b:t, l:r] #第二lead範圍
#                        img_lead = cv2.resize(img_lead, None, fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
#                        cv2.imshow("lead", img_lead)
#                        cv2.waitKey (0)
#                        cv2.destroyAllWindows()
# =============================================================================
#    
                        for lead in range(1,14):
                            lead_shift = fr.find_lead(range_shift, img_type, lead)
                            Loc = fr.combine_shift(range_shift, lead_shift, img_type, lead)
#                           if lead == 13:
#                               ((l, r, b, t), (l2, r2, b2, t2)) = Loc
#                               pass
#                           else:
                            (l, r, b, t) = Loc
                            img_lead = img_g[b:t, l:r]
                            voltage = CheckValue(img_lead)
                            take_peak(img_lead, lead)
                            output1 = digitize(img_lead, lead, voltage)
                            output.append(output1)

        
                        #存檔
                        saveCSV(SavePath, output)
                        print(graph,'-> .csv , save csv')
                        print('----------------')
# =============================================================================                
'''                   


if __name__ == '__main__':
# =============================================================================
    #copy from main file
# =============================================================================
# #    img = cv2.imread("./EKG/00823815/1/00823815_20170912_EKG_1_1_6.jpg") #用第一型的心電圖當範例來源圖片
# #    img = cv2.imread("./Sample_Image/2.jpg")
# #    img = cv2.imread("./EKG/00721757/1/00721757_20100608_EKG_1_1_7.jpg") #有8mv的(V1~V6)
# =============================================================================
#    img = cv2.imread("./Save_Img/3/1/20170815_OT_1_1_3.jpg")
    pics = os.listdir(path) #得到資料夾下的所有檔名稱 
    #print('files = ', files, '\n') #測試data資料夾下所有檔案名稱是否有誤
    sub_dir = [] 
    img_type = 1

    try:
        os.makedirs(Save_Path)
        print('make save dir')
        # 檔案已存在的例外處理
    except FileExistsError:
        print('save dir exist')

    #開始處理每個病人資料
    for pic in pics:
        if pic[0] == '1':
            pic_path = os.path.join(path, pic) #產生檔案的絕對路徑
    #       
            SavePath = Save_Path + '/' + pic[0:-4]
            # 要檢查的檔案路徑
    
            # 檢查檔案是否存在
            if os.path.isfile(SavePath+'.csv'):
                print("csv exist, skip\n")
                continue
            else:
    # =============================================================================
    # #                         stream = open(graph_path, "rb")
    # #                         bytes = bytearray(stream.read())
    # #                         numpyarray = np.asarray(bytes, dtype=np.uint8)
    # #                         img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
    # =============================================================================
                img = cv2.imread(pic_path) #讀圖
            # =============================================================================
            #                         cv2.imshow("EKG", img)
            #                         cv2.waitKey (0)
            #                         cv2.destroyAllWindows()
            # =============================================================================
                range_shift = fr.find_range(img, img_type)
            #                        lead_shift = fr.find_lead(range_shift, img_type, lead)
                Loc = fr.combine_shift(range_shift)
                img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #灰階  
                output_total = []
            
                ret, img_g = cv2.threshold(img_g,80,255,cv2.THRESH_BINARY)
                (l, r, b, t) = Loc
                delete_grid(img_g, Loc)
            # =============================================================================
            #                        img_lead = img_g[b:t, l:r] #第二lead範圍
            #                        img_lead = cv2.resize(img_lead, None, fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
            #                        cv2.imshow("lead", img_lead)
            #                        cv2.waitKey (0)
            #                        cv2.destroyAllWindows()
            # =============================================================================
            #    
                for lead in range(1,13):
                    lead_shift = fr.find_lead(range_shift, img_type, lead)
                    Loc = fr.combine_shift(range_shift, lead_shift, img_type, lead)
            #                           if lead == 13:
            #                               ((l, r, b, t), (l2, r2, b2, t2)) = Loc
            #                               pass
            #                           else:
                    (l, r, b, t) = Loc
                    img_lead = img_g[b:t, l:r]
                    voltage = CheckValue(img_lead)
                    take_peak(img_lead, lead)
                    shape = img_lead.shape
                    img_lead = img_lead[ 0:shape[0], int(shape[1]/13):int(shape[1]/13*13) ]
                    img_lead = cv2.resize(img_lead,(1024,171),interpolation=cv2.INTER_AREA)
                    ret, img_lead = cv2.threshold(img_lead,200,255,cv2.THRESH_BINARY)
                    output1 = digitize_revise(img_lead, lead, voltage)
                    output_total.append(output1)
            
                # print(output.shape)
                #存檔
                saveCSV(SavePath, output_total)
                print(pic,'-> .csv , save csv')
                print('----------------')
# =============================================================================                
