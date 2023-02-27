import string
from _csv import reader
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib
import pandas as pd
import xlwt  # 负责写excel
import xlrd

data = pd.read_csv("test.csv", header=None, sep=' ', dtype='str')

hex_tem = data.values.tolist()[0]
print(hex_tem)
dec_tem = []
i = 1
while i <= 9920:
    dec_tem.append(int(hex_tem[i], 16))
    i += 1
print(dec_tem)
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
np.savetxt("new.csv", tem_array, delimiter=',')
plt.imshow(a, interpolation='None', cmap=plt.cm.hot, origin='upper')

# 温标  shrink=0.8
plt.colorbar()
plt.xlabel("80")
plt.ylabel("62")
plt.title("Infrared image")
plt.xticks(())
plt.yticks(())
plt.show()
# 保存图片
# matplotlib.image.imsave('test.png', a, cmap=plt.cm.hot)
filename = xlwt.Workbook()  # 创建工作簿
sheet1 = filename.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
[h, l] = a.shape  # h为行数，l为列数
for i in range(h):
    for j in range(l):
        sheet1.write(i, j, a[i, j])
filename.save('name_of_your_excel_file.xls')
