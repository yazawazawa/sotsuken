#動画を利用した緑色の割合プログラム

#-*- coding:utf-8 -*-
import cv2
import csv
import os
import numpy as np
import datetime
import time
import smtplib
import sys
import tkinter 
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from email.mime.text import MIMEText
from email.header import Header

charset = 'utf-8'

#tkinters_Graphics_Setting
root = tkinter.Tk()
root.title(u"Setting")
root.geometry("400x300")

def a_reader():
    global addrdeta
    f = open('C:\\Users\\deros\\Documents\\sotsuken\\deta\\addr.txt')
    addrdeta = f.read()
    addbox.insert(tkinter.END,addrdeta)
    f.close()

def p_reader():
    global passdeta
    f = open('C:\\Users\\deros\\Documents\\sotsuken\\deta\\pass.txt')
    passdeta = f.read()
    passbox.insert(tkinter.END,passdeta)
    f.close()

#入力された文字列を変数に代入
def check(event):
    global val
    global fromaddr
    global frompass
    global textdeta

    text = ''
    if val.get() == True:
        text += 'Bright is checked'
    else:
        text += 'Bright is not checked'
    
    fromaddr = addbox.get()
    frompass = passbox.get()

    f = open('C:\\Users\\deros\\Documents\\sotsuken\\deta\\addr.txt',mode="w")
    f.write(fromaddr)
    f.close()

    f = open('C:\\Users\\deros\\Documents\\sotsuken\\deta\\pass.txt',mode="w")
    f.writelines(frompass)
    f.close()

    res = messagebox.showinfo('info',text)
    print("showinfo", res)

def DeleteEntryValue(event):
    #エントリーの中身を削除
    addbox.delete(0, tkinter.END)
    passbox.delete(0, tkinter.END) 

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

#----------------------GUI----------------------------

#チェックボックスの初期化
val = tkinter.BooleanVar()
val.set(False)

#label
static1 = tkinter.Label(text=u'Address')
static1.place(x=50, y=50)

static2 = tkinter.Label(text=u'AppsPassWord')
static2.place(x=50, y=80)

#entry
addbox = tkinter.Entry(width=30)
a_reader()
addbox.place(x=150, y=50)

passbox = tkinter.Entry(width=30)
p_reader()
passbox.place(x=150, y=80)

value = addbox.get()

#button
run = tkinter.Button(root, text=u'Run', width=10)
run.bind("<Button-1>",check)
run.place(x=300, y=230)

reset = tkinter.Button(text=u'Reset', width=10)
reset.bind("<Button-1>",DeleteEntryValue) 
reset.place(x=200, y=230)

#checkbox
checkbox = tkinter.Checkbutton(text=u"Bright", variable=val)
checkbox.place(x=150, y=110)



#--------------------Opencv-------------------------------

#fromaddr = addressget
#toaddr  = "derosa0103+1@gmail.com"

server = smtplib.SMTP('smtp.gmail.com',587)

server.ehlo()
server.starttls()
server.login(fromaddr,frompass)

server.set_debuglevel(1)

now = datetime.datetime.now()
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
        #img = "C:\\Users\\deros\\Documents\\sotsuken\\photo.png"
        img = "C:\\Users\\deros\\Documents\\sotsuken\\img\\" + now.strftime('%Y%m%d_%H') +".png"
        cv2.imwrite(img,frame)

# キャプチャの後始末と，ウィンドウをすべて消す
cap.release()
cv2.destroyAllWindows()
#画像の読み込み
img = cv2.imread("C:\\Users\\deros\\Documents\\sotsuken\\img\\" + now.strftime('%Y%m%d_%H') +".png")
height, width, ch = 640,480,3

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
plant = round(white_area / pixcel_size * 100, 1) 
other = round(black_area / pixcel_size * 100, 1) 

#結果を出力
cv2.imwrite("C:\\Users\\deros\\Documents\\sotsuken\\img\\" + now.strftime('%Y%m%d_%H') + "mask.png", green_mask)
cv2.imwrite("C:\\Users\\deros\\Documents\\sotsuken\\img\\" + now.strftime('%Y%m%d_%H') + "masked.png", green_masked_img)
print(" 植物の割合 = " + str(plant) + " % ")
print(" 　土の割合 = " + str(other) + " % ")
if float(plant) > 15:#6.25
    phrase = '収穫ができそうですよ。'
elif float(plant) > 12:
    phrase = '明日には収穫ができそうですよ。'
elif float(plant) > 8:
    phrase = '二日後には収穫ができそうですよ。'
elif float(plant) > 0:
    phrase = '収穫にはもうすこし時間がかかりそうです。'

if float(plant) >= 20:
    plant = 20

plant *= 5
#csv出力

with open('C:\\Users\\deros\\Documents\\sotsuken\\csv\\new.csv','a',newline='') as f:
    writer = csv.writer(f)
    writer.writerow([ now.strftime('%Y%m%d_%H'),  str(plant) ," % "])
    #writer.writerow([ now.strftime('%Y%m%d_%H'),'　土の割合 = ' + str(other) + " % "])

users = [
    {'name': fromaddr,'address':fromaddr}
]
for user in users:
    content = f'''

        こんにちは
        {user["name"]}さん。
        現在の状況は
        {int(plant)}%です。

        {str(phrase)}
        
    '''
    message = MIMEText(content,'plain', charset)
    message['Subject'] = Header('題名'.encode(charset), charset)
    server.sendmail(fromaddr, user['address'], message.as_string())
server.quit()

root.mainloop()