# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:04:57 2019

@author: 陳俊諺
"""
import cv2


#4、5、6、14是掃描檔 先不做
def find_range(img_src, img_type):
    """
    find EKG graph location(shift)
    input:the image need to find range
    output:EKG graph top_left point & bottom_right point
    """
    img_match = img_src.copy()
    try:
        if img_type == 1:
            img_t = cv2.imread("./Sample_Image/1.jpg") #用第一型的心電圖當範例圖片
        elif img_type == 2:
            img_t = cv2.imread("./Sample_Image/2.jpg") #用第二型的心電圖當範例圖片
        elif img_type == 3:
            img_t = cv2.imread("./Sample_Image/3.jpg") #用第三型的心電圖當範例圖片
        elif img_type == 7:
            img_t = cv2.imread("./Sample_Image/7.jpg") #用第七型的心電圖當範例圖片
        elif img_type == 8:
            img_t = cv2.imread("./Sample_Image/8.jpg") #用第八型的心電圖當範例圖片                
        elif img_type == 9:
            img_t = cv2.imread("./Sample_Image/9.png") #用第九型的心電圖當範例圖片
        elif img_type == 10:
            img_t = cv2.imread("./Sample_Image/10.png") #用第十型的心電圖當範例圖片
        elif img_type == 12:
            img_t = cv2.imread("./Sample_Image/12.png") #用第十二型的心電圖當範例圖片
        elif img_type == 13:
            img_t = cv2.imread("./Sample_Image/13.png") #用第十三型的心電圖當範例圖片
        else:
            raise ValueError('Undefined img_type Error!')
    except ValueError:
        raise
    
    #灰階
    img_match = cv2.cvtColor(img_match, cv2.COLOR_BGR2GRAY)
    img_t = cv2.cvtColor(img_t, cv2.COLOR_BGR2GRAY)
    #訂好範例圖片的長寬
    w = img_t.shape[1]
    h = img_t.shape[0]
    
    method = eval('cv2.TM_SQDIFF_NORMED')
    # Apply template Matching
    res = cv2.matchTemplate(img_match,img_t,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) #找最大最小值&所在位置 -> 和範例圖片相符的左上角位置
    
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h) #靠長寬來訂出右下角位置
    
    loc = (top_left, bottom_right)
#    print(loc)
    
    return loc

def scanLead(img, top, bottom, left, right, threshold):
    max = 0
    Position = []
    tempTop = 0
    for col in range(top,bottom):
        count = 0
        for row in range (left,right):
            if img[col][row] == 0 :
                if col == top:
                    print(row)
                count = count + 1
        if count == 0:
            if max == 0:
                continue
            else:
                if max < threshold:
                    max = 0
                    continue
                else:
                    Position.append(tempTop)
                    Position.append(col)
                    max = 0
        else:
            if count == right-left:
                max = 0
                continue
            elif col == bottom-1:
                Position.append(tempTop)
                Position.append(col)
                max = 0
            elif max == 0:
                tempTop = col
                max = count
            elif count > max :
                max = count
        
    
    print("Position",Position)
    return Position

def CheckValue(img, img_type):
    resizeCoef = []
    if img_type == 1:
        checkH = [58, 294, 530, 766, 1002, 1238]
        checkW = [47, 1582]
        for lead in range(1,13):
            if lead < 7:
                if(sum(sum(img[checkH[lead-1]:checkH[lead-1]+3, checkW[0]:checkW[0]+26] == 0))) >= 20:
                    resizeCoef.append(2)
                elif(sum(sum(img[checkH[lead-1]+29:checkH[lead-1]+32, checkW[0]:checkW[0]+26] == 0))) >= 20:
                    resizeCoef.append(1)
                elif(sum(sum(img[checkH[lead-1]+45:checkH[lead-1]+48, checkW[0]:checkW[0]+26] == 0))) >= 20:
                    resizeCoef.append(0.5)
                else:
                    resizeCoef.append(1)
            else:
                if(sum(sum(img[checkH[lead-7]:checkH[lead-7]+3, checkW[1]:checkW[1]+26] == 0))) >= 20:
                    resizeCoef.append(2)
                elif(sum(sum(img[checkH[lead-7]+29:checkH[lead-7]+32, checkW[1]:checkW[1]+26] == 0))) >= 20:
                    resizeCoef.append(1)
                elif(sum(sum(img[checkH[lead-7]+45:checkH[lead-7]+48, checkW[1]:checkW[1]+26] == 0))) >= 20:
                    resizeCoef.append(0.5)
                else:
                    resizeCoef.append(1)
        return resizeCoef
    elif img_type == 2:
        checkH = [81, 479, 877]
        checkW = [23, 70]
        for lead in range(1,13):
            if lead < 4:
                if(sum(sum(img[checkH[lead-1]:checkH[lead-1]+3, checkW[0]:checkW[0]+27] == 0))) >= 20:
                    resizeCoef.append(2)
                elif(sum(sum(img[checkH[lead-1]+59:checkH[lead-1]+62, checkW[0]:checkW[0]+27] == 0))) >= 20:
                    resizeCoef.append(1)
                else:
                    resizeCoef.append(1)
            elif lead < 7:
                if(sum(sum(img[checkH[lead-4]:checkH[lead-4]+3, checkW[0]:checkW[0]+27] == 0))) >= 20:
                    resizeCoef.append(2)
                elif(sum(sum(img[checkH[lead-4]+59:checkH[lead-4]+62, checkW[0]:checkW[0]+27] == 0))) >= 20:
                    resizeCoef.append(1)
                else:
                    resizeCoef.append(1)
            elif lead < 10:
                if(sum(sum(img[checkH[lead-7]:checkH[lead-7]+3, checkW[1]:checkW[1]+27] == 0))) >= 20:
                    resizeCoef.append(2)
                elif(sum(sum(img[checkH[lead-7]+59:checkH[lead-7]+62, checkW[1]:checkW[1]+27] == 0))) >= 20:
                    resizeCoef.append(1)
                else:
                    resizeCoef.append(1)
            else:
                if(sum(sum(img[checkH[lead-10]:checkH[lead-10]+3, checkW[1]:checkW[1]+27] == 0))) >= 20:
                    resizeCoef.append(2)
                elif(sum(sum(img[checkH[lead-10]+59:checkH[lead-10]+62, checkW[1]:checkW[1]+27] == 0))) >= 20:
                    resizeCoef.append(1)
                else:
                    resizeCoef.append(1)
        return resizeCoef
    # 其他type未做


def find_lead(img, loc, img_type):
    """
    find lead location(shift)
    input:the EKG graph need to find lead
    output:lead top_left point & bottom_right point
    """
    top_left, bottom_right = loc
    w = bottom_right[0] - top_left[0]
    h = bottom_right[1] - top_left[1]
    
    checkOverlapping = 0
    leadShiftArr = [0]
    
    try:
        #type 1
        if img_type == 1:
            #可能的lead範圍
            shift_w = [0, (w/2), w]
            shift_h = [0, h/7, 2*h/7, 3*h/7, (4*h/7)-1, (5*h/7)-1, (6*h/7)-1, h-1]
            #將範圍整數化
            for i in range(len(shift_w)):
                shift_w[i] = int(shift_w[i])
            for i in range(len(shift_h)):
                shift_h[i] = int(shift_h[i])
                
            for lead_idx in range(0,13):
                #定義lead範圍
                if lead_idx < 6:
                    if(sum(sum(img[shift_h[lead_idx]:shift_h[lead_idx]+1, shift_w[0]:shift_w[1]] == 0))) >= 3:
                        checkOverlapping = 1
                    lead_tl = (shift_w[0], shift_h[lead_idx]+1)
                    lead_br = (shift_w[1], shift_h[lead_idx+1]+1)
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx == 12: #第II型--有額外範圍
                    if(sum(sum(img[shift_h[6]:shift_h[6]+1, shift_w[0]:shift_w[2]] == 0))) >= 3:
                        checkOverlapping = 1
                    lead_tl = (shift_w[0], shift_h[6]+2)
                    lead_br = (shift_w[2], shift_h[-1]+1)
                    leadShiftArr.append(((lead_tl,lead_br)))
                else:
                    if(sum(sum(img[shift_h[lead_idx-6]:shift_h[lead_idx-6]+1, shift_w[1]:shift_w[2]] == 0))) >= 3:
                        checkOverlapping = 1
                    lead_tl = (shift_w[1], shift_h[lead_idx-6]+1)
                    lead_br = (shift_w[2], shift_h[lead_idx-5]+1)
                    leadShiftArr.append(((lead_tl,lead_br)))
            
# =============================================================================
#             #決定 return 值
#             if lead_idx == 1:
#                 #lead 2
#                 lead_range = ((lead_tl,lead_br), (lead_tl2,lead_br2))
#             else:
# =============================================================================
            return leadShiftArr, checkOverlapping

        #type 2(scan)
        elif img_type == 2:
            threshold = 60
            w = w-159
            #shift_w[第一排左邊, 第二排左邊, 第三排左邊, 第四排左邊, 邊線左邊]
            shift_w = [156, 156+(w/4), 156+(2*w/4), 156+(3*w/4), 156+w]
            #將範圍整數化
            for i in range(len(shift_w)):
                shift_w[i] = int(shift_w[i])
            shift_h1 = scanLead(img, 3, 1594, shift_w[0], shift_w[1], threshold)
            shift_h2 = scanLead(img, 3, 1594, shift_w[1], shift_w[2], threshold)
            shift_h3 = scanLead(img, 3, 1594, shift_w[2], shift_w[3], threshold)
            shift_h4 = scanLead(img, 3, 1594, shift_w[3], shift_w[4], threshold)

            for lead_idx in range(0,13):
            #定義lead範圍
                if lead_idx < 3:
                    lead_tl = (shift_w[0], shift_h1[lead_idx*2])
                    lead_br = (shift_w[1], shift_h1[lead_idx*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 6:
                    lead_tl = (shift_w[1], shift_h2[(lead_idx-3)*2])
                    lead_br = (shift_w[2], shift_h2[(lead_idx-3)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 9:
                    lead_tl = (shift_w[2], shift_h3[(lead_idx-6)*2])
                    lead_br = (shift_w[3], shift_h3[(lead_idx-6)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 12:
                    lead_tl = (shift_w[3], shift_h4[(lead_idx-9)*2])
                    lead_br = (shift_w[4], shift_h4[(lead_idx-9)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                else: #lead 13
                    lead_tl = (shift_w[0], min(shift_h1[6],shift_h2[6],shift_h3[6],shift_h4[8]))
                    lead_br = (shift_w[4], max(shift_h1[7],shift_h2[7],shift_h3[7],shift_h4[9]))
                    leadShiftArr.append(((lead_tl,lead_br)))

            return leadShiftArr, checkOverlapping

        #type 3(scan) 暫時不做
        elif img_type == 3:
            threshold = 30
            #shift_w[第一排左邊, 第二排左邊, 第三排左邊, 第四排左邊, 邊線左邊]
            shift_w = [0, 245, 466, 687, w]
            shift_h1 = scanLead(img, 0, h, shift_w[0], shift_w[1], threshold)
            shift_h2 = scanLead(img, 0, h, shift_w[1], shift_w[2], threshold)
            shift_h3 = scanLead(img, 0, h, shift_w[2], shift_w[3], threshold)
            shift_h4 = scanLead(img, 0, h, shift_w[3], shift_w[4], threshold)

            for lead_idx in range(0,13):
            #定義lead範圍
                if lead_idx < 3:
                    lead_tl = (shift_w[0], shift_h1[lead_idx*2])
                    lead_br = (shift_w[1], shift_h1[lead_idx*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 6:
                    lead_tl = (shift_w[1], shift_h2[(lead_idx-3)*2])
                    lead_br = (shift_w[2], shift_h2[(lead_idx-3)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 9:
                    lead_tl = (shift_w[2], shift_h3[(lead_idx-6)*2])
                    lead_br = (shift_w[3], shift_h3[(lead_idx-6)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 12:
                    lead_tl = (shift_w[3], shift_h4[(lead_idx-9)*2])
                    lead_br = (shift_w[4], shift_h4[(lead_idx-9)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                else: #lead 13
                    lead_tl = (shift_w[0], min(shift_h1[6],shift_h2[6],shift_h3[6],shift_h4[6]))
                    lead_br = (shift_w[4], max(shift_h1[7],shift_h2[7],shift_h3[7],shift_h4[7]))
                    leadShiftArr.append(((lead_tl,lead_br)))

            return leadShiftArr, checkOverlapping

        #type 7(scan) 暫時不做
        elif img_type == 7:
            threshold = 30
            w = w - 21
            #shift_w[第一排左邊, 第二排左邊, 第三排左邊, 第四排左邊, 邊線左邊]
            shift_w = [21, 20+(w/4), 20+(w*2/4), 20+(w*3/4), 20+w]
            #將範圍整數化
            for i in range(len(shift_w)):
                shift_w[i] = int(shift_w[i])
            shift_h1 = scanLead(img, 60, 604, shift_w[0], shift_w[1], threshold)
            shift_h2 = scanLead(img, 60, 604, shift_w[1], shift_w[2], threshold)
            shift_h3 = scanLead(img, 60, 604, shift_w[2], shift_w[3], threshold)
            shift_h4 = scanLead(img, 60, 604, shift_w[3], shift_w[4], threshold)

            for lead_idx in range(0,13):
            #定義lead範圍
                if lead_idx < 3:
                    lead_tl = (shift_w[0], shift_h1[lead_idx*2])
                    lead_br = (shift_w[1], shift_h1[lead_idx*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 6:
                    lead_tl = (shift_w[1], shift_h2[(lead_idx-3)*2])
                    lead_br = (shift_w[2], shift_h2[(lead_idx-3)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 9:
                    lead_tl = (shift_w[2], shift_h3[(lead_idx-6)*2])
                    lead_br = (shift_w[3], shift_h3[(lead_idx-6)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 12:
                    lead_tl = (shift_w[3], shift_h4[(lead_idx-9)*2])
                    lead_br = (shift_w[4], shift_h4[(lead_idx-9)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                else: #lead 13
                    lead_tl = (shift_w[0], min(shift_h1[6],shift_h2[6],shift_h3[6],shift_h4[6]))
                    lead_br = (shift_w[4], max(shift_h1[7],shift_h2[7],shift_h3[7],shift_h4[7]))
                    leadShiftArr.append(((lead_tl,lead_br)))

            return leadShiftArr, checkOverlapping

        #type 8 暫時不做
        elif img_type == 8:
            #shift_w[第一排左邊, 第一排右邊, 第二排左邊, 邊線左邊] 
            shift_w = [21, 516, 521, 1016]
            #shift_h左邊數來第幾排
            #[第一排上面, 第二排上面, 第三排上面, 第四排上面, 第五排上面, 第六排上面, 第六排下面, 第七排上面, 邊線上面] 
            shift_h = [40, 100, 166, 240, 310, 380, 440, 505, 604]

            for lead_idx in range(0,13):
                #定義lead範圍
                if lead_idx < 6:
                    lead_tl = (shift_w[0], shift_h[lead_idx])
                    lead_br = (shift_w[1], shift_h[lead_idx+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx == 12: #lead 13
                    lead_tl = (shift_w[0], shift_h[-2])
                    lead_br = (shift_w[-1], shift_h[-1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                else:
                    lead_tl = (shift_w[2], shift_h[lead_idx-6])
                    lead_br = (shift_w[3], shift_h[lead_idx-5])
                    leadShiftArr.append(((lead_tl,lead_br)))

            return leadShiftArr, checkOverlapping

        #type 9(scan) 暫時不做
        elif img_type == 9:
            threshold = 40
            #shift_w[第一排左邊, 第二排左邊, 第三排左邊, 第四排左邊, 第四排右邊]
            shift_w = [116, 436, 749, 1061, 1374]
            shift_h1 = scanLead(img, 49, 624, shift_w[0], shift_w[1], threshold)
            shift_h2 = scanLead(img, 49, 624, shift_w[1], shift_w[2], threshold)
            shift_h3 = scanLead(img, 49, 624, shift_w[2], shift_w[3], threshold)
            shift_h4 = scanLead(img, 49, 624, shift_w[3], shift_w[4], threshold)
            
            for lead_idx in range(0,13):
            #定義lead範圍
                if lead_idx < 3:
                    lead_tl = (shift_w[0], shift_h1[lead_idx*2])
                    lead_br = (shift_w[1], shift_h1[lead_idx*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 6:
                    lead_tl = (shift_w[1], shift_h2[(lead_idx-3)*2])
                    lead_br = (shift_w[2], shift_h2[(lead_idx-3)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 9:
                    lead_tl = (shift_w[2], shift_h3[(lead_idx-6)*2])
                    lead_br = (shift_w[3], shift_h3[(lead_idx-6)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx < 12:
                    lead_tl = (shift_w[3], shift_h4[(lead_idx-9)*2])
                    lead_br = (shift_w[4], shift_h4[(lead_idx-9)*2+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                else: #lead 13
                    lead_tl = (shift_w[0], min(shift_h1[6],shift_h2[6],shift_h3[6],shift_h4[6]))
                    lead_br = (shift_w[4], max(shift_h1[7],shift_h2[7],shift_h3[7],shift_h4[7]))
                    leadShiftArr.append(((lead_tl,lead_br)))

            return leadShiftArr, checkOverlapping

        #type 10 暫時不做
        elif img_type == 10:
            #shift_w[邊線右邊, 第一排左邊, 第一排右邊, 第二排左邊, 邊線左邊] 
            shift_w = [1, 21, 590, 595, 1164]
            #shift_h左邊數來第幾排
            #[第一排上面, 第二排上面, 第三排上面, 第四排上面, 第五排上面, 第六排上面, 第六排下面, 第七排上面, 邊線上面] 
            shift_h = [40, 120, 200, 280, 360, 440, 520, 565, 644]

            for lead_idx in range(0,13):
                #定義lead範圍
                if lead_idx < 6:
                    lead_tl = (shift_w[1], shift_h[lead_idx])
                    lead_br = (shift_w[2], shift_h[lead_idx+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx == 12: #lead 13
                    lead_tl = (shift_w[0], shift_h[-2])
                    lead_br = (shift_w[-1], shift_h[-1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                else:
                    lead_tl = (shift_w[3], shift_h[lead_idx-6])
                    lead_br = (shift_w[4], shift_h[lead_idx-5])
                    leadShiftArr.append(((lead_tl,lead_br)))

            return leadShiftArr, checkOverlapping

        #type 12 暫時不做
        elif img_type == 12:
            w = w - 2
            h = h - 2
        #可能的lead範圍
            shift_w = [0, w/2, w]
            shift_h = [0, h/7, 2*h/7, 3*h/7, 4*h/7, 5*h/7, 6*h/7, h]
            #將範圍整數化
            for i in range(len(shift_w)):
                shift_w[i] = int(shift_w[i])
            for i in range(len(shift_h)):
                shift_h[i] = int(shift_h[i])

            for lead_idx in range(0,13):
                #定義lead範圍
                if lead_idx < 6:
                    lead_tl = (shift_w[0], shift_h[lead_idx])
                    lead_br = (shift_w[1], shift_h[lead_idx+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx == 12: #lead 13
                    lead_tl = (shift_w[0], shift_h[6])
                    lead_br = (shift_w[2], shift_h[-1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                else:
                    lead_tl = (shift_w[1], shift_h[lead_idx-6])
                    lead_br = (shift_w[2], shift_h[lead_idx-5])
                    leadShiftArr.append(((lead_tl,lead_br)))

            return leadShiftArr, checkOverlapping

        #type 13 暫時不做
        elif img_type == 13:
            w = w - 5
            h = h - 7
        #可能的lead範圍
            shift_w = [5, 5+(w/2), 5+w]
            shift_h = [7, 7+(h/7), 7+(2*h/7), 7+(3*h/7)-1, 7+(4*h/7), 7+(5*h/7)-1, 7+(6*h/7)-1, 7+h]
            #將範圍整數化
            for i in range(len(shift_w)):
                shift_w[i] = int(shift_w[i])
            for i in range(len(shift_h)):
                shift_h[i] = int(shift_h[i])

            for lead_idx in range(0,13):
                #定義lead範圍
                if lead_idx < 6:
                    lead_tl = (shift_w[0], shift_h[lead_idx])
                    lead_br = (shift_w[1], shift_h[lead_idx+1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                elif lead_idx == 12: #lead 13
                    lead_tl = (shift_w[0], shift_h[6])
                    lead_br = (shift_w[2], shift_h[-1])
                    leadShiftArr.append(((lead_tl,lead_br)))
                else:
                    lead_tl = (shift_w[1], shift_h[lead_idx-6])
                    lead_br = (shift_w[2], shift_h[lead_idx-5])
                    leadShiftArr.append(((lead_tl,lead_br)))

            return leadShiftArr, checkOverlapping
        else:
            raise ValueError('Undefined img_type Error!')
    except ValueError:
        raise


    """
==================學長版本===========================
def combine_shift(range_shift, lead_shift = ((0,0),(0,0)), img_type=1, lead=1):

    #combine range_shift & lead_shift
    #input:shift of EKG graph & shift of lead 
    #output:location of lead
    if img_type == 1:
        top_left, bottom_right = range_shift
        #print('range_shift:',range_shift)
# =============================================================================
#         if lead == 2:        
#             ((lead_tl, lead_br),(lead_tl2, lead_br2)) = lead_shift
#             print('1:', lead_tl, lead_br, '2:', lead_tl2, lead_br2)
#             l = top_left[0] + lead_tl[0]
#             r = top_left[0] + lead_br[0]
#             b = top_left[1] + lead_tl[1]
#             t = top_left[1] + lead_br[1]
#             #第二張圖的range
#             l2 = top_left[0] + lead_tl2[0]
#             r2 = top_left[0] + lead_br2[0]
#             b2 = top_left[1] + lead_tl2[1]
#             t2 = top_left[1] + lead_br2[1]
#             
#             lead_loc = ((l, r, b, t), (l2, r2, b2, t2))
#             
#         else:
# =============================================================================
        if lead_shift == ((0,0),(0,0)):
#            return(165, 3236, 650, 2304)
            return(0, 3071, 0, 1654)
        else:
            #print(lead_shift)
            #print('++++')
            lead_tl, lead_br = lead_shift
            #print('lead_range:', lead_tl, lead_br)
            l = top_left[0] + lead_tl[0]
            r = top_left[0] + lead_br[0]
            b = top_left[1] + lead_tl[1]
            t = top_left[1] + lead_br[1]
            
            lead_loc = (l, r, b, t)
            #print('123++++++++==',lead_loc)
        return lead_loc
    else:
        #img_type 2~9還沒作
        print('Unfinished...')
    """
def combine_shift(range_shift, lead_shift = ((0,0),(0,0))):
    """
    combine range_shift & lead_shift
    input:shift of EKG graph & shift of lead 
    output:location of lead
    """
    top_left, bottom_right = range_shift
    if lead_shift == ((0,0),(0,0)):
        return(0, bottom_right[0], 0, bottom_right[1])
    else:
        #print(lead_shift)
        #print('++++')
        lead_tl, lead_br = lead_shift
        #print('lead_range:', lead_tl, lead_br)
        l = top_left[0] + lead_tl[0]
        r = top_left[0] + lead_br[0]
        b = top_left[1] + lead_tl[1]
        t = top_left[1] + lead_br[1]
            
        lead_loc = (l, r, b, t)
        #print('123++++++++==',lead_loc)
    return lead_loc

if __name__ == '__main__':
    img_type = int(input("img_type = "))
    try:
        if img_type == 1:
            img = cv2.imread("./EKG/00823815/1/00823815_20181121_EKG_1_1_2.jpg") #用第一型的心電圖當範例來源圖片
        elif img_type == 2:
            img = cv2.imread("./EKG/00729722/2/00729722_20180123_EKG_1_0_2.jpg") #用第二型的心電圖當範例來源圖片
        elif img_type == 3:
            img = cv2.imread("./ECG_378/3/07756927_20180504_OT_1_1_1.jpg") #用第三型的心電圖當範例來源圖片
        elif img_type == 7:
            img = cv2.imread("./ECG_378/7/07643415_20101221_USCSRV01_1_0_1.jpg") #用第七型的心電圖當範例來源圖片
        elif img_type == 8:
            img = cv2.imread("./ECG_378/8/07949977_20101111_USCSRV01_1_0_2.jpg") #用第八型的心電圖當範例來源圖片
        else:
            raise ValueError('Undefined img_type Error!')
    except ValueError:
        raise
        
    
    img2 = img.copy()
    img3 = img.copy()
    #src
    img = cv2.resize(img, None, fx=0.3,fy=0.2,interpolation=cv2.INTER_CUBIC)
    cv2.imshow("src", img)
    
    loc = find_range(img2, img_type)
    top_left, bottom_right = loc

    if img_type == 1:
        
        lead = int(input("lead = "))
        if lead == 2:        
            ((lead_tl, lead_br),(lead_tl2, lead_br2)) = find_lead(loc, img_type, lead)
            print('1:', lead_tl, lead_br, '2:', lead_tl2, lead_br2)
            l = top_left[0] + lead_tl[0]
            r = top_left[0] + lead_br[0]
            b = top_left[1] + lead_tl[1]
            t = top_left[1] + lead_br[1]
            #第二張圖的range
            l2 = top_left[0] + lead_tl2[0]
            r2 = top_left[0] + lead_br2[0]
            b2 = top_left[1] + lead_tl2[1]
            t2 = top_left[1] + lead_br2[1]
            img3 = img3[b2:t2,l2:r2]
#            print('???????',l2,r2,b2,t2)
            img3 = cv2.resize(img3, None, fx=0.4,fy=0.4,interpolation=cv2.INTER_CUBIC)
            cv2.imshow("match lead2", img3)    
        else:
            lead_tl, lead_br = find_lead(loc, img_type, lead)
    #        print('lead_range:', lead_tl, lead_br)
            l = top_left[0] + lead_tl[0]
            r = top_left[0] + lead_br[0]
            b = top_left[1] + lead_tl[1]
            t = top_left[1] + lead_br[1]
        img2 = img2[b:t,l:r]

    else:
        #other img_type unfinished
        img2 = img2[b:t,l:r]
    img2 = cv2.resize(img2, None, fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
        
    #match
    cv2.imshow("lead", img2)
    cv2.waitKey (0)
    cv2.destroyAllWindows()
    
