from PIL import Image
import numpy as np

img_input = Image.open('lena.bmp')
pixels_input = img_input.load()

################ binary
img_output1 = Image.new(img_input.mode, img_input.size)
pixels_output1 = img_output1.load()

for x in range(img_input.width):
    for y in range(img_input.height):
        if pixels_input[x, y] >= 128:
            pixels_output1[x, y] = 255
        else:
            pixels_output1[x, y] = 0
img_output1.save('binary.bmp')

################ histogram
img_output2 = Image.new(img_input.mode, (256, 256))
pixels_output2 = img_output2.load()

count = np.zeros(256)
for x in range(img_input.width):
    for y in range(img_input.height):
        count[pixels_input[x, y]] += 1

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
img_output2.save('histogram.bmp')
        
################ connected component
img_binary = Image.open('binary.bmp')
pixels_binary = img_binary.load()
img_output3 = Image.new(img_binary.mode, img_binary.size)
pixels_output3 = img_output3.load()

pixels_label = np.zeros((512, 512))

# label initial
t = 1
for x in range(img_binary.width):
    for y in range(img_binary.height):
        if pixels_binary[x, y] == 0:
            pixels_output3[x, y] = 200
        elif pixels_binary[x, y] == 255:
            pixels_output3[x, y] = 255
            pixels_label[x, y] = t
            t += 1

# label process
label_done = False
while not label_done:
    label_done = True
    # left & up -> right & down
    for x in range(img_binary.width):
        for y in range(img_binary.height):
            if pixels_label[x, y] != 0:
                x2 = x + 1
                y2 = y + 1
                if x2 < img_binary.width and pixels_label[x2, y] > pixels_label[x, y]:
                    label_done = False
                    pixels_label[x2, y] = pixels_label[x, y]

                if y2 < img_binary.height and pixels_label[x, y2] > pixels_label[x, y]:
                    label_done = False
                    pixels_label[x, y2] = pixels_label[x, y]

    # right & down -> left & up
    for x in reversed(range(img_binary.width)):
        for y in reversed(range(img_binary.height)):
            if pixels_label[x, y] != 0:
                x2 = x - 1
                y2 = y - 1
                if x2 > -1 and pixels_label[x2, y] > pixels_label[x, y]:
                    label_done = False
                    pixels_label[x2, y] = pixels_label[x, y]

                if y2 > -1 and pixels_label[x, y2] > pixels_label[x, y]:
                    label_done = False
                    pixels_label[x, y2] = pixels_label[x, y]

# find >= 500 component
count = np.zeros(512*512)
for x in range(img_binary.height):
    for y in range(img_binary.width):
        if pixels_label[x, y] != 0:
            count[int(pixels_label[x, y])] += 1

comp500 = []
for z in range(512*512):
    if count[z] >= 500:
        comp500.append(z)

# initial boundary, up/down/left/right
bound = np.zeros((512*512, 4))
for m in range(len(comp500)):
    bound[comp500[m]][0] = 512
    bound[comp500[m]][1] = -1
    bound[comp500[m]][2] = 512
    bound[comp500[m]][3] = -1

# find boundary
for x in range(img_binary.width):
    for y in range(img_binary.height):
        if pixels_label[x, y] in comp500:
            m = int(pixels_label[x, y])
            if x < bound[m][2]:
                bound[m][2] = x
            if x > bound[m][3]:
                bound[m][3] = x
            if y < bound[m][0]:
                bound[m][0] = y
            if y > bound[m][1]:
                bound[m][1] = y

# draw boundary
for n in range(len(comp500)):
    b_up = int(bound[comp500[n]][0])
    b_down = int(bound[comp500[n]][1])
    b_left = int(bound[comp500[n]][2])
    b_right = int(bound[comp500[n]][3])
    for t in range(b_left, b_right + 1):
        pixels_output3[t, b_up] = 0
        pixels_output3[t, b_down] = 0
    for t in range(b_up, b_down + 1):
        pixels_output3[b_left, t] = 0
        pixels_output3[b_right, t] = 0

img_output3.save('boundary.bmp')

                     
