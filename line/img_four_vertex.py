import sys
import cv2
import numpy as np
import imutils
from matplotlib import pyplot
from scipy.stats import gaussian_kde

# 讀取圖檔
img = cv2.imread('S__18677792.jpg')
img_blank = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
img_blank.fill(255)

# 使用縮圖以減少計算量
img_small = imutils.resize(img, width=640)

# 轉換至 HSV 色彩空間
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2HSV)

# 取出飽和度
saturation = hsv[:, :, 1]
saturation_small = hsv_small[:, :, 1]

# 取出明度
value = hsv[:,:,2]
value_small = hsv_small[:,:,2]

# 綜合飽和度與明度
sv_ratio = 0.5
sv_value = cv2.addWeighted(saturation, sv_ratio, value, 1-sv_ratio, 0)
sv_value_small = cv2.addWeighted(saturation_small, sv_ratio, value_small, 1-sv_ratio, 0)

# 使用 Kernel Density Estimator 計算出分佈函數
density = gaussian_kde(sv_value_small.ravel(), bw_method=0.2)

# 找出 PDF 中第一個區域最小值（Local Minimum）作為門檻值
step = 0.5
xs = np.arange(0, 256, step)
ys = density(xs)
cum = 0
threshold_value = 0
for i in range(1, 250):
  cum += ys[i-1] * step
  if (cum > 0.02) and (ys[i] < ys[i+1]) and (ys[i] < ys[i-1]):
    threshold_value = xs[i]
    break

'''
# 除錯用的圖形
pyplot.hist(sv_value_small.ravel(), 256, [0, 256], True, alpha=0.5)
pyplot.plot(xs, ys, linewidth = 2)
pyplot.axvline(x = threshold_value, color='r', linestyle='--', linewidth = 2)
pyplot.xlim([0, max(threshold_value*2, 80)])
pyplot.show()
'''

# 以指定的門檻值篩選區域
_, threshold = cv2.threshold(sv_value, threshold_value, 255.0, cv2.THRESH_BINARY)

# 去除微小的雜訊
kernel_radius = int(img.shape[1]/100)
kernel = np.ones((kernel_radius, kernel_radius), np.uint8)
threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

# 產生等高線
contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 建立除錯用影像
img_debug = img.copy()

# 線條寬度
line_width = int(img.shape[1]/1000)

# 以藍色線條畫出所有的等高線
cv2.drawContours(img_debug, contours, -1, (255, 0, 0), line_width)
img_group = cv2.drawContours(img_blank, contours, -1, (255, 0, 0), line_width)

# 處理藍色邊框
# cv2.rectangle (img_group, Point(0, 0), Point(2729, 3921), Scalar(0, 255, 255), 2, 8, 0);
img_group = cv2.rectangle(img_group, (0, 0), (img.shape[1], img.shape[0]), (255, 255, 255), 20)

# 把邊緣圖像重新處理
edged = cv2.Canny(img_group, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# 把邊緣圖像重新分層
contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print("there are " + str(len(contours)) + " contours")
cnt = contours[1]
print("there are " + str(len(cnt)) + " points in contours[1]")
approx = cv2.approxPolyDP(cnt, 30, True)
print("after approx, there are " + str(len(approx)) + " points")
print(approx)
print(type(approx))


if len(approx) == 4:
  print()
  print('=============~完美~=============')

else:
  print()
  print('=============~你有%s個頂點,你.不.美~=============' % len(approx))
