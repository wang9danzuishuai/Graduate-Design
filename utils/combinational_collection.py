import re

import cv2
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import xlwt  # 负责写excel
import serial
import binascii,time

def cut_text(text,length):
    text_arr = re.findall('.{'+str(length)+'}', text)
    text_arr.append(text[(len(text_arr)*length):])
    return text_arr

ser = serial.Serial("COM3", 921600, 8, "N", timeout=50,stopbits=1)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 打开摄像头
photo_name = 0

while 1:
    # get a frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示
    # show a frame
    cv2.imshow("capture", frame)  # 生成摄像头窗口
    file_name = 'data_save/'+str(photo_name) + '.png'
    if cv2.waitKey(1) & 0xFF == ord('a'):  # 如果按下q 就截图保存并退出
        cv2.imwrite(file_name, frame)  # 保存路径
        a = 'ee e1 01 55 ff fc fd ff'
        d = bytes.fromhex(a)
        result = ser.write(d)
        time.sleep(1)
        count = ser.inWaiting()
        if count > 0:
            data = ser.read(count)
            if data != b'':
                data = str(binascii.b2a_hex(data))[2:-1]

        hex_tem = cut_text(data, 2)

        dec_tem = []
        i = 1
        while i <= 9920:
            dec_tem.append(int(hex_tem[i], 16))
            i += 1
        k = 0
        tem = []
        while k < len(dec_tem):
            tem.append((dec_tem[k] * 256 + dec_tem[k + 1] - 2731) / 10)
            k += 2

        j = 0
        tem_array = []
        while j < 62:
            tem_array.append(tem[80 * j:80 * (j + 1)])
            j += 1

        a = np.array(tem_array)
        matplotlib.image.imsave('data_save/'+str(photo_name)+'ir.png', a, cmap=plt.cm.hot)
        filename = xlwt.Workbook()  # 创建工作簿
        sheet1 = filename.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
        [h, l] = a.shape  # h为行数，l为列数
        for i in range(h):
            for j in range(l):
                sheet1.write(i, j, a[i, j])
        filename.save('data_save/'+str(photo_name)+'temp.xls')
        photo_name += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
ser = serial.Serial()