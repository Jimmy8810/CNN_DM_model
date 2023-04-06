# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 15:14:40 2020

@author: user
"""

import pandas as pd
ExcelPath = './test.xlsx'

def ReadExcel(ExcelPath):
    df = pd.read_excel(ExcelPath)
    #print(df)
    B_num = df[['病歷號碼']].values
    #print(B_num)
    B_list = []
    
    for i in range(len(B_num)):
        B_list.append(int(B_num[i]))
          
    print(B_list)
    
    return(B_list)

def ReadBloodExcel(ExcelPath):
    '''
    ==========================================================
    blood_data一筆資料長這樣:[ 病例編號, 區間開頭, 區間結尾 ]
    病例編號相同，比對年份是否有在區間內
    ==========================================================
    '''
    df = pd.read_excel(ExcelPath)
    num = df[['number']].values
    year = df[['year']].values
    try:
        date = df[['date']].values
    except:
        date = False
    bloodData = []
    bloodYear = []
    bloodDate = []
    count = 0
    currentValue = num[0][0]
    # print(range(len(num)))
    
    for i in range(len(num)):
        if num[i][0] == currentValue:
            count+=1
        elif i == len(num)-1:
            if num[i][0] == currentValue:
                count+=1
                bloodData.append([currentValue,i+1-count,i+1])
            else:
                bloodData.append([currentValue,i-count,i])
                bloodData.append([num[i][0],i,i+1])
        else:
            bloodData.append([currentValue,i-count,i])
            currentValue = num[i][0]
            count = 1

        bloodYear.append(year[i][0])
        if date != False:
            bloodDate.append(int(str(date[i][0])[0:4]+str(date[i][0])[5:7]+str(date[i][0])[8:10]))

    # for i in range(len(blood_data)):
    #     print(blood_data[i])
    # print(year)
    
    return bloodData, bloodYear, bloodDate

def handleMissingData(df, subset, fileName):
    print("Begin to handle missing data for" + str(subset) + "...")
    processed = df.dropna(axis = 'index', how='any',subset=subset,inplace = False)
    processed.to_excel(fileName+'.xlsx',index = False)
    print("Handle complete!")
    return fileName+'.xlsx'
    
if __name__ == '__main__':
    B_list = ReadExcel(ExcelPath)

