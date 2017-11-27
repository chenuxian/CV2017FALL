from PIL import Image
import numpy as np

img_input = Image.open('binary.bmp')
pixels_input = img_input.load()

yokoiNum = np.zeros((512, 512))
mark_arr = np.zeros((512, 512))

thining = Image.new(img_input.mode, img_input.size)
thining_pixels = thining.load()
for y in range(512):
    for x in range(512):
        thining_pixels[x, y] = pixels_input[x, y]

######################################################## yokoiNum 4 connected

def find_number(x, y):
    x0 = 255
    x1 = x2 = x3 = x4 = x5 = x6 = x7 = x8 = 0

    if x + 1 < 512:
        x1 = thining_pixels[x + 1, y]
    if y - 1 > -1:
        x2 = thining_pixels[x, y - 1]
    if x - 1 > -1:
        x3 = thining_pixels[x - 1, y]
    if y + 1 < 512:
        x4 = thining_pixels[x, y + 1]
    if x + 1 < 512 and y + 1 < 512:
        x5 = thining_pixels[x + 1, y + 1]
    if x + 1 < 512 and y - 1 > -1:
        x6 = thining_pixels[x + 1, y - 1]
    if x - 1 > -1 and y - 1 > -1:
        x7 = thining_pixels[x - 1, y - 1]
    if x - 1 > -1 and y + 1 < 512:
        x8 = thining_pixels[x - 1, y + 1]
    
    r_count = 0
    q_count = 0
    
    if x0 == x1:
        if x2 == 0 or x6 == 0:
            q_count += 1
        else:
            r_count += 1
    if x0 == x2:
        if x3 == 0 or x7 == 0:
            q_count += 1
        else:
            r_count += 1
    if x0 == x3:
        if x4 == 0 or x8 == 0:
            q_count += 1
        else:
            r_count += 1
    if x0 == x4:
        if x1 == 0 or x5 == 0:
            q_count += 1
        else:
            r_count += 1

    if r_count == 4:
        return 5
    else:
        return q_count


########################################################### mark interior or border, 4 connected

def mark():
    for y in range(512):
        for x in range(512):
            a = np.zeros(5)
            xx = np.zeros(5)
            a[0] = xx[0] = thining_pixels[x, y]
            
            for i in range(1, 5):
                xx[i] = 100 # impossible pixel value, i.e.: take boundary pixels as border
            
            if x + 1 < 512:
                xx[1] = thining_pixels[x + 1, y]
            if x - 1 > -1:
                xx[3] = thining_pixels[x - 1, y]
            if y + 1 < 512:
                xx[4] = thining_pixels[x, y + 1]
            if y - 1 > -1:
                xx[2] = thining_pixels[x, y - 1]
            
            for j in range(4):
                if a[j] == xx[j + 1]:
                    a[j + 1] = a[j]
                else:
                    a[j + 1] = 1000 # 1000 = "b"
            
            if a[4] == 1000:
                mark_arr[x, y] = 1000
            else:
                mark_arr[x, y] = 2000 # 2000 = "i"

    for y in range(512):
        for x in range(512):
            if mark_arr[x, y] == 1000:
                if x + 1 < 512:
                    if mark_arr[x + 1, y] == 2000:
                        mark_arr[x, y] = 3000 # 3000 = "p"
                        continue
                if x - 1 > -1:
                    if mark_arr[x - 1, y] == 2000:
                        mark_arr[x, y] = 3000
                        continue
                if y + 1 < 512:
                    if mark_arr[x, y + 1] == 2000:
                        mark_arr[x, y] = 3000
                        continue
                if y - 1 > -1:
                    if mark_arr[x, y - 1] == 2000:
                        mark_arr[x, y] = 3000
                        continue

########################################################################

change = 1
while change == 1:
    change = 0
    mark()
    for y in range(512):
        for x in range(512):
            if thining_pixels[x, y] == 255:
                yokoiNum[x, y] = find_number(x, y)

    for y in range(512):
        for x in range(512):
            if thining_pixels[x, y] == 255:
                if yokoiNum[x, y] == 1 and mark_arr[x, y] == 3000:
                    thining_pixels[x, y] = 0
                    change = 1

thining.save("thining.bmp")


