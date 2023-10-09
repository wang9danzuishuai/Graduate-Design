import re

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

ser = serial.Serial("COM4", 921600, 8, "N", timeout=50,stopbits=1)
a='ee e1 01 55 ff fc fd ff'
d=bytes.fromhex(a)
result=ser.write(d)
time.sleep(1)
count=ser.inWaiting()

if count>0:
    data=ser.read(count)
    if data!=b'':
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
#np.savetxt("new.csv", tem_array, delimiter=',')

# plt.imshow(a, interpolation='None', cmap=plt.cm.hot, origin='upper')
# plt.colorbar()
# plt.xlabel("80")
# plt.ylabel("62")
# plt.title("Infrared image")
# plt.xticks(())
# plt.yticks(())
# plt.show()

# 保存图片
matplotlib.image.imsave('test.png', a, cmap=plt.cm.hot)
filename = xlwt.Workbook()  # 创建工作簿
sheet1 = filename.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
[h, l] = a.shape  # h为行数，l为列数
# for i in range(h):
#     for j in range(l):
#         sheet1.write(i, j, a[i, j])
# filename.save('name_of_your_excel_file.xls')
# 关闭串口
ser.close()
ser = serial.Serial()
