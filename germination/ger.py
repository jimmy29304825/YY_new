import cv2  # 影像處理ML
import numpy as np  # 數學計算用
import time  # 時間紀錄
import datetime  # 日期時間紀錄


class germination():
    def __init__(self, ID, sowDate, filename, thershold, percent):
        self.ID = ID  # 手動輸入品種編號
        self.sowDate = datetime.datetime.strptime(sowDate, '%Y/%m/%d').date()  # 手動輸入播種日期
        self.dateTime = datetime.datetime.now().date()  # 紀錄拍攝時間
        self.days = (self.dateTime - self.sowDate).days  # 紀錄培育時長
        self.thershold = thershold  # 從SQL抓取二元化參數
        self.percent = percent  # 從SQL抓取判斷閾值
        self.result_list = []  #預設結果儲存物件
        self.filename = filename
        
        
    def convert_photo(self, slice_img):  # 圖片換(灰階、高斯模糊、二元化)，計算發芽比例
        kernel_size = (3, 3)  # 高斯模糊矩陣大小
        sigma = 3  # 高斯模糊標準差參數(0=自動)
        grayImage = cv2.cvtColor(slice_img, cv2.COLOR_BGR2GRAY)  # gray(0-255) 圖像轉換灰階
#         grayImage = cv2.GaussianBlur(grayImage, kernel_size, sigma)  # GaussianBlur  圖校進行模糊化(高斯)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage,  self.thershold, 255, cv2.THRESH_BINARY)  # black and white(0, 255)  圖像透過thershold閾值進行二元化 
        caculateImg = blackAndWhiteImage[10:90, 10:90]  # 邊緣10%不計算發芽率
        slice_percent =  round(sum(sum(caculateImg == 0))/64, 2)  # 計算黑色比例(作物占比)
        if slice_percent >= self.percent:  # 判斷是否發芽
            is_germination = 1
        else: 
            is_germination = 0
        result = [slice_percent, is_germination]  
        return result  # 結果回傳(作物比例、是否發芽)
    
    
    def caculate(self):  # 計算整片作物的發芽率
        germination_sum = 0
        for i in self.result_list:
            germination_sum += i[3]
        germination_rate = round((germination_sum / (14*22))*100, 2)
        return germination_rate
       
    
    def get_photo(self):  # 拍攝照片並轉換、計算、裁切
        print('拍攝照片...')
#         fileName = "3G1_rect1.jpg"  # 暫時抓本地端照片
#         fileDirs = './'  # 資料夾位置
        img = cv2.imread(self.filename)  #載入照片（之後換成控制CAM拍攝照片)
        self.result_list = []  # 重製結果暫存清單
        print('裁切照片')
        top = 0  # 最上面(+h)
        left = 0  # 最左邊(+w)
        plus = 100  # 長寬設定 100 * 100
        for i in range(14):  # 等比例裁切每一株的照片
            for j in range(22):
                slice_img = img[top:top+plus, left:left+plus]
                ans = self.convert_photo(slice_img)  # 使用convert_photo運算
                result = [i, j, ans[0], ans[1],slice_img]  # 儲存單個結果
                self.result_list.append(result)  # 彙整整片結果至暫存清單
                left = left + plus
            top = top +plus
            left = 0  # 算完一列重製(like a打字機)
        result = self.caculate()  # 使用caculate計算整片發芽率
        return result
    
    
    def saving_to_sql(self):  # 儲存結果到SQL
        print('saving to sql...')  # 回存暫存清單至SQL中
        time.sleep(2)
        self.result_list = []  # 儲存完重製暫存清單
        return 'done'
       
       
    def __str__(self):
        return "作物編號: %s\n播種日期: %s\n判斷日期: %s\n育苗天數: %s\n閾值參數: %s\n判斷條件: %s\n結果暫存清單: 共%s筆數據(詳細請看self.result_list)" % (self.ID, self.sowDate, self.dateTime, self.days, self.thershold, self.percent, len(self.result_list))