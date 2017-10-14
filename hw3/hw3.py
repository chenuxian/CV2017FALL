from PIL import Image
import numpy as np

img_input = Image.open('lena.bmp')
pixels_input = img_input.load()

################ binary
img_output1 = Image.new(img_input.mode, img_input.size)
pixels_output1 = img_output1.load()

# calculate cdf and do equalize
cdf = np.zeros(256)
for x in range(img_input.width):
    for y in range(img_input.height):
        cdf[pixels_input[x,y]] += 1
for k in range(1, len(cdf)):
    cdf[k] += cdf[k-1]

for x in range(img_input.width):
    for y in range(img_input.height):
        temp = cdf[pixels_input[x,y]]
        temp *= 255
        temp //= (512*512)
        pixels_output1[x, y] = int(temp)

img_output1.save('equalization.bmp')


################ histogram_equal
img_output2 = Image.new(img_input.mode, (256, 256))
pixels_output2 = img_output2.load()

count = np.zeros(256)
for x in range(img_output1.width):
    for y in range(img_output1.height):
        count[pixels_output1[x, y]] += 1

# find max
max = 0
for m in range(len(count)):
    if count[m] > max:
        max = count[m]

for z in range(len(count)):
    if count[z] != 0:
        count[z] = count[z] * (256 / max)

h = 0
for x in range(img_output2.width):
    for y in range(img_output2.height):
        if count[h] > 0:
            pixels_output2[x, 255 - y] = 255
            count[h] -= 1
        else:
            pixels_output2[x, 255 - y] = 0
    h += 1
img_output2.save('histogram_equal.bmp')
