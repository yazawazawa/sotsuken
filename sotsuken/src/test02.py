#動画を利用した緑色の割合プログラム

#-*- coding:utf-8 -*-
import cv2
import numpy as np

def detect_green_color(img):
    #HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #緑色の領域
    #HSVの範囲を指定
    hsv_min = np.array([30,64,0])        #hsvの下限
    hsv_max = np.array([90,255,255])    #hsvの上限
    mask = cv2.inRange(hsv, hsv_min, hsv_max) 

    #マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask = mask)
    
    return mask, masked_img

# VideoCapture オブジェクトを取得します
cap = cv2.VideoCapture(0)

while(True):
    # フレームをキャプチャする
    ret, frame = cap.read()

    # 画面に表示する
    cv2.imshow('frame',frame)

    # キーボード入力待ち
    key = cv2.waitKey(1) & 0xFF

    # qが押された場合は終了する
    if key == ord('q'):
        break
    # sが押された場合は保存する
    if key == ord('s'):
        img = "C:\\Users\\deros\\Documents\\sotsuken\\photo.png"
        cv2.imwrite(img,frame)

# キャプチャの後始末と，ウィンドウをすべて消す
cap.release()
cv2.destroyAllWindows()
#画像の読み込み
img = cv2.imread("C:\\Users\\deros\\Documents\\sotsuken\\photo.png")
height, width, ch = img.shape

#色検出
green_mask, green_masked_img = detect_green_color(img)

#全体の画素数
pixcel_size = width * height
#print(type(pixcel_size))

#白色の画素数
white_area = cv2.countNonZero(green_mask)
#print(type(white_area))

#黒色の画素数
black_area = pixcel_size - white_area

#割合計算
plane = round(white_area / pixcel_size * 100, 1) 
other = round(black_area / pixcel_size * 100, 1) 

#結果を出力
cv2.imwrite("C:\\Users\\deros\\Documents\\sotsuken\\green_mask2.png", green_mask)
cv2.imwrite("C:\\Users\\deros\\Documents\\sotsuken\\green_masked_img2.png", green_masked_img)
print(" 植物の割合 = " + str(plane) + " % ")
print(" 　土の割合 = " + str(other) + " % ")

