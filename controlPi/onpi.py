import sys  # 讀取參數用
from picamera import PiCamera  # 控制相機模組
from time import sleep
from io import BytesIO  # 寫入記憶體用
from PIL import Image  # 影像處理
import numpy as np  # 數學計算

ids = str(sys.argv[1])  # 接收遠端傳來的參數
stream = BytesIO()  # 建立記憶體暫存物件
camera = PiCamera()  # 建立相機物件
# camera.rotation = 270  # 相機旋轉 90為單位
camera.resolution = (3280, 2464)  # 相機畫素設定
camera.framerate = 15  # 偵數，需搭配畫素設定
camera.start_preview()  # 啟動相機鏡頭
sleep(2)  # 給相機暖機兩秒
camera.capture(stream, format='jpeg')  # 拍照存於記憶體中
camera.stop_preview()  # 關閉相機

stream.seek(0)
image = Image.open(stream)  # 記憶體中的圖像用PIL讀取
image.save('/home/pi/Desktop/par.jpg')  # 存入本地端，之後改為存入資料庫
imageDB = np.array(image)  # 讀取影像的RGB資料
print(ids, 'finished!')  # 回傳結果給PC





