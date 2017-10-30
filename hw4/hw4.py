from PIL import Image
import numpy as np

################ dilation
def dilation(kernel, input_name):
    img_input = Image.open(input_name)
    pixels_input = img_input.load()

    dilation_output = Image.new(img_input.mode, img_input.size)
    dilation_pixels = dilation_output.load()

    # initial
    for x in range(dilation_output.width):
        for y in range(dilation_output.height):
            dilation_pixels[x, y] = 0

    for x in range(img_input.width):
        for y in range(img_input.height):
            if pixels_input[x, y] == 255:
                flag = True
                # check boundry
                for z in range(len(kernel)):
                    x1 = x + kernel[z][0]
                    y1 = y + kernel[z][1]
                    if x1 < 0 or x1 > 511 or y1 < 0 or y1 > 511:
                        flag = False
                        break
                if flag == True:
                    for z in range(len(kernel)):
                        x1 = x + kernel[z][0]
                        y1 = y + kernel[z][1]
                        dilation_pixels[x1, y1] = 255
    return dilation_output
    #dilation_output.save(output_name)

################ erosion
def erosion(kernel, input_name):
    img_input = Image.open(input_name)
    pixels_input = img_input.load()

    erosion_output = Image.new(img_input.mode, img_input.size)
    erosion_pixels = erosion_output.load()

    # initial
    for x in range(erosion_output.width):
        for y in range(erosion_output.height):
            erosion_pixels[x, y] = 0

    for x in range(img_input.width):
        for y in range(img_input.height):
            flag = True
            # check boundry
            for z in range(len(kernel)):
                x1 = x + kernel[z][0]
                y1 = y + kernel[z][1]
                if x1 < 0 or x1 > 511 or y1 < 0 or y1 > 511:
                    flag = False
                    break
                if pixels_input[x1, y1] != 255:
                    flag = False
                    break
            if flag == True:
                    erosion_pixels[x, y] = 255
    return erosion_output
    #erosion_output.save(output_name)


kernel = []
for i in range(5):
    for j in range(5):
        temp = [i-2, j-2]
        kernel.append(temp)
kernel.remove([-2,-2])
kernel.remove([-2,2])
kernel.remove([2,-2])
kernel.remove([2,2])

output = dilation(kernel, "binary.bmp")
output.save("dilation.bmp")
output = erosion(kernel, "binary.bmp")
output.save("erosion.bmp")
output = dilation(kernel, "erosion.bmp")
output.save("openning.bmp")
output = erosion(kernel, "dilation.bmp")
output.save("closing.bmp")

################ h&m
kernel = [[0,0],[-1,0],[0,1]]
kernel2 = [[0,-1],[1,-1],[1,0]]

img_input = Image.open("binary.bmp")
pixels_input = img_input.load()
complement_output = Image.new(img_input.mode, img_input.size)
complement_pixels = complement_output.load()
for x in range(img_input.width):
    for y in range(img_input.height):
        if pixels_input[x, y] == 0:
            complement_pixels[x, y] = 255
        else:
            complement_pixels[x,y] = 0
complement_output.save("complement.bmp")

output1 = erosion(kernel, "binary.bmp")
output1_pixels = output1.load()
output2 = erosion(kernel2, "complement.bmp")
output2_pixels = output2.load()

hnm_output = Image.new(output1.mode, output1.size)
hnm_pixels = hnm_output.load()

for x in range(output1.width):
    for y in range(output1.height):
        if output1_pixels[x, y] == 255 and output2_pixels[x, y] == 255:
            hnm_pixels[x, y] = 255
hnm_output.save("hnm.bmp")
