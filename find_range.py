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
        #else:
            #raise ValueError('Undefined img_type Error!')
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


def find_lead(loc, img_type, lead_idx):
    """
    find lead location(shift)
    input:the EKG graph need to find lead
    output:lead top_left point & bottom_right point
    """
    top_left, bottom_right = loc
    w = bottom_right[0] - top_left[0]
    h = bottom_right[1] - top_left[1]
    
    lead_list = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'Full lead II']
    lead_idx -= 1
    lead = lead_list[lead_idx]
    print('lead =',lead, 'index =', lead_idx+1)
    
    try:
        if img_type == 1:
            #可能的lead範圍
            shift_w = [0, (w/2), w]
            shift_h = [0, h/7, 2*h/7, 3*h/7, (4*h/7)-1, (5*h/7)-1, (6*h/7)-1, h-1]
            #將範圍整數化
            for i in range(len(shift_w)):
                shift_w[i] = int(shift_w[i])
            for i in range(len(shift_h)):
                shift_h[i] = int(shift_h[i])
            #定義lead範圍
            if lead_idx < 6:
                lead_tl = (shift_w[0], shift_h[lead_idx]+1)
                lead_br = (shift_w[1], shift_h[lead_idx+1]+1)
                
            elif lead_idx == 12: #第II型--有額外範圍
                lead_tl = (shift_w[0],shift_h[6]+2)
                lead_br = (shift_w[2], shift_h[-1]+1)
            else:
                lead_tl = (shift_w[1], shift_h[lead_idx-6]+1)
                lead_br = (shift_w[2], shift_h[lead_idx-5]+1)
            
# =============================================================================
#             #決定 return 值
#             if lead_idx == 1:
#                 #lead 2
#                 lead_range = ((lead_tl,lead_br), (lead_tl2,lead_br2))
#             else:
# =============================================================================
            lead_range = (lead_tl,lead_br)
#            print(lead_range)
            return lead_range
            
        elif img_type == 2:
            #shift_w[第一排左邊, 第二排左邊, 第三排左邊, 第四排左邊, 邊線左邊] 
            shift_w = [156, 895, 1633, 2372, 3105]
            #shift_h左邊數來第幾排[第一排上面, 第二排上面, 第三排上面, 第四排上面, 邊線上面] 
            shift_h1 = [3, 454, 808, 1270, 1594]
            shift_h2 = [3, 480, 831]
            shift_h3 = [3, 395, 820]
            shift_h4 = [3, 458, 865]
            
        elif img_type == 8:
            #shift_w[第一排左邊, 第二排左邊, 邊線左邊] 
            shift_w = [21, 521, 1016]
            #shift_h左邊數來第幾排
            #[第一排上面, 第二排上面, 第三排上面, 第四排上面, 第五排上面, 第六排上面, 第六排下面, 第七排上面, 邊線上面] 
            shift_h1 = [43, 111, 179, 247, 315, 383, 460, 505, 604]
            shift_h2 = [43, 111, 179, 241, 315, 383, 460, 505, 604]
        else:
            raise ValueError('Undefined img_type Error!')
    except ValueError:
        raise

def combine_shift(range_shift, lead_shift = ((0,0),(0,0)), img_type=1, lead=1):
    """
    combine range_shift & lead_shift
    input:shift of EKG graph & shift of lead 
    output:location of lead
    """
    if img_type == 1:
        top_left, bottom_right = range_shift
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
            lead_tl, lead_br = lead_shift
    #        print('lead_range:', lead_tl, lead_br)
            l = top_left[0] + lead_tl[0]
            r = top_left[0] + lead_br[0]
            b = top_left[1] + lead_tl[1]
            t = top_left[1] + lead_br[1]
            
            lead_loc = (l, r, b, t)
        return lead_loc
    else:
        #img_type 2~9還沒作
        print('Unfinished...')

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
    
## test