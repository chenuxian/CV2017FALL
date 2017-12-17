from PIL import Image
import numpy as np
import math
import scipy.signal

img_input = Image.open('lena.bmp')
img_p = img_input.load()
img_p2 = np.zeros((512, 512))
for i in range(512):
    for j in range(512):
        img_p2[i, j] = img_p[i, j]

p = np.zeros((522, 522))
for x in range(512):
    for y in range(512):
        p[x+5, y+5] = img_p[x, y]

output = Image.new(img_input.mode, img_input.size)
p_output = output.load()


# laplace1, kernel = [0 1 0 1 -4 1 0 1 0], threshold = 20
for x in range(5, img_input.width+5):
    for y in range(5, img_input.height+5):
        tmp = -4 * p[x, y] + p[x-1, y] + p[x, y-1] + p[x+1, y] + p[x, y+1]
        if tmp > 20:
            p_output[x-5, y-5] = 0
        else:
            p_output[x-5, y-5] = 255
output.save("laplace1.bmp")

# laplace2, kernel = 1/3 * [1 1 1 1 -8 1 1 1 1], threshold = 20
for x in range(5, img_input.width+5):
    for y in range(5, img_input.height+5):
        tmp = (-8 * p[x, y] + p[x-1, y] + p[x, y-1] + p[x+1, y] + p[x, y+1] + p[x-1, y-1] + p[x+1, y-1] + p[x+1, y+1] + p[x-1, y+1]) / 3
        if tmp > 20:
            p_output[x-5, y-5] = 0
        else:
            p_output[x-5, y-5] = 255
output.save("laplace2.bmp")

# min-var, kernel = 1/3 * [2 -1 2 -1 -4 -1 2 -1 2], threshold = 20
for x in range(5, img_input.width+5):
    for y in range(5, img_input.height+5):
        tmp = (-4 * p[x, y] + -1*(p[x-1, y] + p[x, y-1] + p[x+1, y] + p[x, y+1]) + 2*(p[x-1, y-1] + p[x+1, y-1] + p[x+1, y+1] + p[x-1, y+1])) / 3
        if tmp > 20:
            p_output[x-5, y-5] = 0
        else:
            p_output[x-5, y-5] = 255
output.save("minvar.bmp")

def LoG(x, y, std):
    return (((x ** 2 + y ** 2 - 2 * (std ** 2)) / (std ** 4)) * (math.e ** ((-1 * (x ** 2 + y ** 2)) / (2 * (std ** 2)))))
def gaussian(x, y, std):
    return (math.e ** ((-1 * (x ** 2 + y  ** 2)) / (2 * (std ** 2)))) / ((2 * math.pi * (std ** 2)))
def DoG(x, y, std1, std2):
    return gaussian(x, y, std1) - gaussian(x, y, std2)


kernel = np.zeros((11, 11))
for i in range(11):
    out_tmp = ""
    for j in range(11):
        kernel[i, j] = LoG(i-5, j-5, 1)
        k = str(kernel[i, j])
        if len(k) < 8:
            k += "0000000000"
        out_tmp += k[0:8]
        out_tmp += " "
    print(out_tmp)
tmp = scipy.signal.correlate2d(img_p2, kernel, mode='same', boundary='fill', fillvalue=0)
for x in range(img_input.width):
    for y in range(img_input.height):
        if tmp[x, y] > 30:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("LoG.bmp")

print("---------------")
print("---------------")

kernel = np.zeros((11, 11))
for i in range(11):
    out_tmp = ""
    for j in range(11):
        kernel[i, j] = -1*DoG(i-5, j-5, 1, 3)
        out_tmp += str(kernel[i, j])[0:8]
        out_tmp += " "
    print(out_tmp)
tmp = scipy.signal.correlate2d(img_p2, kernel, mode='same', boundary='fill', fillvalue=0)
for x in range(img_input.width):
    for y in range(img_input.height):
        if tmp[x, y] > 0.1:
            p_output[x, y] = 0
        else:
            p_output[x, y] = 255
output.save("DoG.bmp")