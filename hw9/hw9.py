from PIL import Image
import numpy as np
import math

img_input = Image.open('lena.bmp')
p_input = img_input.load()
output = Image.new(img_input.mode, img_input.size)
p_output = output.load()

for x in range(img_input.width):
    for y in range(img_input.height):
        p = np.zeros(4)
        p[0] = p_input[x, y]
        if x + 1 < 512:
            p[1] = p_input[x+1, y]
        if y + 1 < 512:
            p[2] = p_input[x, y+1]
            if x + 1 < 512:
                p[3] = p_input[x+1, y+1]
        r1 = p[3] - p[0]
        r2 = p[2] - p[1]
        tmp = (r1 ** 2 + r2 ** 2) ** 0.5
        if tmp > 12:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("robert.bmp")

for x in range(img_input.width):
    for y in range(img_input.height):
        p = np.zeros(9)
        p[4] = p_input[x, y]
        if x + 1 < 512:
            p[5] = p_input[x+1, y]
            if y + 1 < 512:
                p[8] = p_input[x+1, y+1]
            if y - 1 > -1:
                p[2] = p_input[x+1, y-1]
        if y + 1 < 512:
            p[7] = p_input[x, y+1]
            if x - 1 > -1:
                p[6] = p_input[x-1, y+1]
        if x - 1 > -1:
            p[3] = p_input[x-1, y]
            if y - 1 > -1:
                p[0] = p_input[x-1, y-1]
        if y - 1 > -1:
            p[1] = p_input[x, y-1]
        r1 = p[6] + p[7] + p[8] - p[0] - p[1] - p[2]
        r2 = p[2] + p[5] + p[8] - p[0] - p[3] - p[6]
        tmp = (r1 ** 2 + r2 ** 2) ** 0.5
        if tmp > 24:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("prewitt.bmp")

for x in range(img_input.width):
    for y in range(img_input.height):
        p = np.zeros(9)
        p[4] = p_input[x, y]
        if x + 1 < 512:
            p[5] = p_input[x+1, y]
            if y + 1 < 512:
                p[8] = p_input[x+1, y+1]
            if y - 1 > -1:
                p[2] = p_input[x+1, y-1]
        if y + 1 < 512:
            p[7] = p_input[x, y+1]
            if x - 1 > -1:
                p[6] = p_input[x-1, y+1]
        if x - 1 > -1:
            p[3] = p_input[x-1, y]
            if y - 1 > -1:
                p[0] = p_input[x-1, y-1]
        if y - 1 > -1:
            p[1] = p_input[x, y-1]
        r1 = p[6] + 2*p[7] + p[8] - p[0] - 2*p[1] - p[2]
        r2 = p[2] + 2*p[5] + p[8] - p[0] - 2*p[3] - p[6]
        tmp = (r1 ** 2 + r2 ** 2) ** 0.5
        if tmp > 38:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("sobel.bmp")

for x in range(img_input.width):
    for y in range(img_input.height):
        p = np.zeros(9)
        p[4] = p_input[x, y]
        if x + 1 < 512:
            p[5] = p_input[x+1, y]
            if y + 1 < 512:
                p[8] = p_input[x+1, y+1]
            if y - 1 > -1:
                p[2] = p_input[x+1, y-1]
        if y + 1 < 512:
            p[7] = p_input[x, y+1]
            if x - 1 > -1:
                p[6] = p_input[x-1, y+1]
        if x - 1 > -1:
            p[3] = p_input[x-1, y]
            if y - 1 > -1:
                p[0] = p_input[x-1, y-1]
        if y - 1 > -1:
            p[1] = p_input[x, y-1]
        r1 = p[6] + (2**0.5)*p[7] + p[8] - p[0] - (2**0.5)*p[1] - p[2]
        r2 = p[2] + (2**0.5)*p[5] + p[8] - p[0] - (2**0.5)*p[3] - p[6]
        tmp = (r1 ** 2 + r2 ** 2) ** 0.5
        if tmp > 30:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("fnc.bmp")

for x in range(img_input.width):
    for y in range(img_input.height):
        p = np.zeros(9)
        p[4] = p_input[x, y]
        if x + 1 < 512:
            p[5] = p_input[x+1, y]
            if y + 1 < 512:
                p[8] = p_input[x+1, y+1]
            if y - 1 > -1:
                p[2] = p_input[x+1, y-1]
        if y + 1 < 512:
            p[7] = p_input[x, y+1]
            if x - 1 > -1:
                p[6] = p_input[x-1, y+1]
        if x - 1 > -1:
            p[3] = p_input[x-1, y]
            if y - 1 > -1:
                p[0] = p_input[x-1, y-1]
        if y - 1 > -1:
            p[1] = p_input[x, y-1]
        r = []
        r.append(5 * (p[2] + p[5] + p[8]) + -3 * (p[0] + p[1] + p[3] + p[6] + p[7]))
        r.append(5 * (p[2] + p[5] + p[1]) + -3 * (p[0] + p[8] + p[3] + p[6] + p[7]))
        r.append(5 * (p[2] + p[0] + p[1]) + -3 * (p[5] + p[8] + p[3] + p[6] + p[7]))
        r.append(5 * (p[0] + p[1] + p[3]) + -3 * (p[2] + p[5] + p[8] + p[6] + p[7]))
        r.append(5 * (p[0] + p[3] + p[6]) + -3 * (p[2] + p[1] + p[5] + p[8] + p[7]))
        r.append(5 * (p[3] + p[6] + p[7]) + -3 * (p[0] + p[1] + p[2] + p[5] + p[8]))
        r.append(5 * (p[6] + p[7] + p[8]) + -3 * (p[0] + p[1] + p[2] + p[3] + p[5]))
        r.append(5 * (p[7] + p[5] + p[8]) + -3 * (p[0] + p[1] + p[3] + p[6] + p[2]))
        tmp = max(r)
        if tmp > 135:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("kirsch.bmp")

for x in range(img_input.width):
    for y in range(img_input.height):
        p = np.zeros(9)
        p[4] = p_input[x, y]
        if x + 1 < 512:
            p[5] = p_input[x+1, y]
            if y + 1 < 512:
                p[8] = p_input[x+1, y+1]
            if y - 1 > -1:
                p[2] = p_input[x+1, y-1]
        if y + 1 < 512:
            p[7] = p_input[x, y+1]
            if x - 1 > -1:
                p[6] = p_input[x-1, y+1]
        if x - 1 > -1:
            p[3] = p_input[x-1, y]
            if y - 1 > -1:
                p[0] = p_input[x-1, y-1]
        if y - 1 > -1:
            p[1] = p_input[x, y-1]
        r = []
        r.append(p[2]+p[8]+-1*(p[0]+p[6])+2*p[5]+-2*p[3])
        r.append(p[1]+p[5]+-1*(p[3]+p[7])+2*p[2]+-2*p[6])
        r.append(p[0]+p[2]+-1*(p[6]+p[8])+2*p[1]+-2*p[7])
        r.append(p[1]+p[3]+-1*(p[5]+p[7])+2*p[0]+-2*p[8])
        r.append(p[0]+p[6]+-1*(p[2]+p[8])+2*p[3]+-2*p[5])
        r.append(p[3]+p[7]+-1*(p[1]+p[5])+2*p[6]+-2*p[2])
        r.append(p[6]+p[8]+-1*(p[0]+p[2])+2*p[7]+-2*p[1])
        r.append(p[5]+p[7]+-1*(p[1]+p[3])+2*p[8]+-2*p[0])
        tmp = max(r)
        if tmp > 43:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("robinson.bmp")

for x in range(img_input.width):
    for y in range(img_input.height):
        p = np.zeros(25)
        p[12] = p_input[x, y]
        if x + 2 < 512:
            p[13] = p_input[x+1, y]
            p[14] = p_input[x+2, y]
            if y + 2 < 512:
                p[17] = p_input[x, y+1]
                p[18] = p_input[x+1, y+1]
                p[19] = p_input[x+2, y+1]
                p[22] = p_input[x, y+2]
                p[23] = p_input[x+1, y+2]
                p[24] = p_input[x+2, y+2]
            elif y + 1 < 512:
                p[17] = p_input[x, y+1]
                p[18] = p_input[x+1, y+1]
                p[19] = p_input[x+2, y+1]

            if y - 2 > -1:
                p[7] = p_input[x, y-1]
                p[8] = p_input[x+1, y-1]
                p[9] = p_input[x+2, y-1]
                p[2] = p_input[x, y-2]
                p[3] = p_input[x+1, y-2]
                p[4] = p_input[x+2, y-2]
            elif y - 1 > -1:
                p[7] = p_input[x, y-1]
                p[8] = p_input[x+1, y-1]
                p[9] = p_input[x+2, y-1]
        elif x + 1 < 512:
            p[13] = p_input[x+1, y]
            if y + 2 < 512:
                p[17] = p_input[x, y+1]
                p[18] = p_input[x+1, y+1]
                p[22] = p_input[x, y+2]
                p[23] = p_input[x+1, y+2]
            elif y + 1 < 512:
                p[17] = p_input[x, y+1]
                p[18] = p_input[x+1, y+1]

            if y - 2 > -1:
                p[7] = p_input[x, y-1]
                p[8] = p_input[x+1, y-1]
                p[2] = p_input[x, y-2]
                p[3] = p_input[x+1, y-2]
            elif y - 1 > -1:
                p[7] = p_input[x, y-1]
                p[8] = p_input[x+1, y-1]
        else:
            if y + 2 < 512:
                p[17] = p_input[x, y+1]
                p[22] = p_input[x, y+2]
            elif y + 1 < 512:
                p[17] = p_input[x, y+1]

            if y - 2 > -1:
                p[7] = p_input[x, y-1]
                p[2] = p_input[x, y-2]
            elif y - 1 > -1:
                p[7] = p_input[x, y-1]

        
        if x - 2 > -1:
            p[11] = p_input[x-1, y]
            p[10] = p_input[x-2, y]
            if y + 2 < 512:
                p[17] = p_input[x, y+1]
                p[16] = p_input[x-1, y+1]
                p[15] = p_input[x-2, y+1]
                p[22] = p_input[x, y+2]
                p[21] = p_input[x-1, y+2]
                p[20] = p_input[x-2, y+2]
            elif y + 1 < 512:
                p[17] = p_input[x, y+1]
                p[16] = p_input[x-1, y+1]
                p[15] = p_input[x-2, y+1]

            if y - 2 > -1:
                p[7] = p_input[x, y-1]
                p[6] = p_input[x-1, y-1]
                p[5] = p_input[x-2, y-1]
                p[2] = p_input[x, y-2]
                p[1] = p_input[x-1, y-2]
                p[0] = p_input[x-2, y-2]
            elif y - 1 > -1:
                p[7] = p_input[x, y-1]
                p[6] = p_input[x-1, y-1]
                p[5] = p_input[x-2, y-1]
        elif x - 1 > -1:
            p[11] = p_input[x-1, y]
            if y + 2 < 512:
                p[17] = p_input[x, y+1]
                p[16] = p_input[x-1, y+1]
                p[22] = p_input[x, y+2]
                p[21] = p_input[x-1, y+2]
            elif y + 1 < 512:
                p[17] = p_input[x, y+1]
                p[16] = p_input[x-1, y+1]

            if y - 2 > -1:
                p[7] = p_input[x, y-1]
                p[6] = p_input[x-1, y-1]
                p[2] = p_input[x, y-2]
                p[1] = p_input[x-1, y-2]
            elif y - 1 > -1:
                p[7] = p_input[x, y-1]
                p[6] = p_input[x-1, y-1]
        else:
            if y + 2 < 512:
                p[17] = p_input[x, y+1]
                p[22] = p_input[x, y+2]
            elif y + 1 < 512:
                p[17] = p_input[x, y+1]

            if y - 2 > -1:
                p[7] = p_input[x, y-1]
                p[2] = p_input[x, y-2]
            elif y - 1 > -1:
                p[7] = p_input[x, y-1]

        r = []
        r.append(100*(p[0]+p[1]+p[2]+p[3]+p[4]+p[5]+p[6]+p[7]+p[8]+p[9]-p[15]-p[16]-p[17]-p[18]-p[19]-p[20]-p[21]-p[22]-p[23]-p[24]))
        r.append(100*(p[0]+p[1]+p[2]+p[3]+p[4]+p[5]+p[6]+p[7]+p[10]-p[14]-p[17]-p[18]-p[19]-p[20]-p[21]-p[22]-p[23]-p[24]) + 78*(p[8]-p[16]) + 32*(p[15]-p[9]) + 92*(p[11]-p[13]))
        r.append(100*(p[0]+p[1]+p[2]+p[5]+p[6]+p[10]+p[11]+p[15]+p[20]-p[4]-p[9]-p[13]-p[14]-p[18]-p[19]-p[22]-p[23]-p[24]) + 78*(p[16]-p[8]) + 32*(p[3]-p[21]) + 92*(p[7]-p[17]))
        r.append(100*(p[3]+p[4]+p[8]+p[9]+p[13]+p[14]+p[18]+p[19]+p[23]+p[24]-p[0]-p[1]-p[5]-p[6]-p[10]-p[11]-p[15]-p[16]-p[20]-p[21]))
        r.append(100*(p[2]+p[3]+p[4]+p[8]+p[9]+p[13]+p[14]+p[19]+p[24]-p[0]-p[5]-p[10]-p[11]-p[15]-p[16]-p[20]-p[21]-p[22]) + 32*(p[1]-p[23]) + 78*(p[18]-p[6]) + 92*(p[7]-p[17]))
        r.append(100*(p[0]+p[1]+p[2]+p[3]+p[4]+p[7]+p[8]+p[9]+p[14]-p[10]-p[15]-p[16]-p[17]-p[20]-p[21]-p[22]-p[23]-p[24]) + 78*(p[6]-p[18]) + 32*(p[19]-p[5]) + 92*(p[13]-p[11]))
        tmp = max(r)
        if tmp > 12500:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("nevatia.bmp")
