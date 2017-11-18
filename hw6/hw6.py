from PIL import Image
import numpy as np

def find_number(x, y):
    x0 = 255
    x1 = x2 = x3 = x4 = x5 = x6 = x7 = x8 = 0

    if x + 1 < 64:
        x1 = pixels_downsampling[x + 1, y]
    if y - 1 > -1:
        x2 = pixels_downsampling[x, y - 1]
    if x - 1 > -1:
        x3 = pixels_downsampling[x - 1, y]
    if y + 1 < 64:
        x4 = pixels_downsampling[x, y + 1]
    if x + 1 < 64 and y + 1 < 64:
        x5 = pixels_downsampling[x + 1, y + 1]
    if x + 1 < 64 and y - 1 > -1:
        x6 = pixels_downsampling[x + 1, y - 1]
    if x - 1 > -1 and y - 1 > -1:
        x7 = pixels_downsampling[x - 1, y - 1]
    if x - 1 > -1 and y + 1 < 64:
        x8 = pixels_downsampling[x - 1, y + 1]
    
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

################################

img_input = Image.open('binary.bmp')
pixels_input = img_input.load()

################ downsampling
downsampling = Image.new(img_input.mode, (64, 64))
pixels_downsampling = downsampling.load()

i = j = -1
for x in range(0, img_input.width, 8):
    i += 1
    j = -1
    for y in range(0, img_input.height, 8):
        j += 1
        pixels_downsampling[i, j] = pixels_input[x, y]

for y in range(0, 64):
    tmp = ""
    for x in range(0, 64):
        if pixels_downsampling[x, y] == 255:
            x = find_number(x, y)
            if x != 0:
                tmp += str(x)
            else:
                tmp += " "
        else:
            tmp += " "
    print(tmp)
