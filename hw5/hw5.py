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
            if pixels_input[x, y] != 0:
                for z in range(len(kernel)):
                    x1 = x + kernel[z][0]
                    y1 = y + kernel[z][1]
                    if x1 < 0 or x1 > 511 or y1 < 0 or y1 > 511:
                        continue
                    else:
                        if pixels_input[x, y] > dilation_pixels[x1, y1]:
                            dilation_pixels[x1, y1] = pixels_input[x, y]
    return dilation_output

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
            min_pixel = 255
            # check boundry
            for z in range(len(kernel)):
                x1 = x + kernel[z][0]
                y1 = y + kernel[z][1]
                if x1 < 0 or x1 > 511 or y1 < 0 or y1 > 511:
                    flag = False
                    break
                if pixels_input[x1, y1] == 0:
                    flag = False
                    break
                if pixels_input[x1, y1] < min_pixel:
                    min_pixel = pixels_input[x1, y1]
            if flag == True:
                    erosion_pixels[x, y] = min_pixel
    return erosion_output

kernel = []
for i in range(5):
    for j in range(5):
        temp = [i-2, j-2]
        kernel.append(temp)
kernel.remove([-2,-2])
kernel.remove([-2,2])
kernel.remove([2,-2])
kernel.remove([2,2])

output = dilation(kernel, "lena.bmp")
output.save("dilation.bmp")
output = erosion(kernel, "lena.bmp")
output.save("erosion.bmp")
output = dilation(kernel, "erosion.bmp")
output.save("opening.bmp")
output = erosion(kernel, "dilation.bmp")
output.save("closing.bmp")
