from PIL import Image
import numpy as np
import math

img_input = Image.open('lena.bmp')
pixels_input = img_input.load()

# noise
img_gau10 = Image.new(img_input.mode, img_input.size)
pixels_gau10 = img_gau10.load()
img_gau30 = Image.new(img_input.mode, img_input.size)
pixels_gau30 = img_gau30.load()
img_snp01 = Image.new(img_input.mode, img_input.size)
pixels_snp01 = img_snp01.load()
img_snp005 = Image.new(img_input.mode, img_input.size)
pixels_snp005 = img_snp005.load()

for x in range(img_input.width):
    for y in range(img_input.height):
        pixels_gau10[x, y] = pixels_input[x, y] + int(10*np.random.normal(0.0, 1.0, None))
        pixels_gau30[x, y] = pixels_input[x, y] + int(30*np.random.normal(0.0, 1.0, None))
        if np.random.uniform(0.0, 1.0, None) < 0.05:
            pixels_snp005[x, y] = 0
        elif np.random.uniform(0.0, 1.0, None) > 1 - 0.05:
            pixels_snp005[x, y] = 255
        else:
            pixels_snp005[x, y] = pixels_input[x, y]
        if np.random.uniform(0.0, 1.0, None) < 0.1:
            pixels_snp01[x, y] = 0
        elif np.random.uniform(0.0, 1.0, None) > 1 - 0.1:
            pixels_snp01[x, y] = 255
        else:
            pixels_snp01[x, y] = pixels_input[x, y]

# save noise img
img_gau10.save('gau10.bmp')
img_gau30.save('gau30.bmp')
img_snp01.save('snp01.bmp')
img_snp005.save('snp005.bmp')

################ dilation
def dilation(kernel, img_input, pixels_input):
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
def erosion(kernel, img_input, pixels_input):
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

################# opening
def opening(kernel, img_input, pixels_input):
    img_input2 = erosion(kernel, img_input, pixels_input)
    pixels_input2 = img_input2.load()
    return dilation(kernel, img_input2, pixels_input2)

################# closing
def closing(kernel, img_input, pixels_input):
    img_input2 = dilation(kernel, img_input, pixels_input)
    pixels_input2 = img_input2.load()
    return erosion(kernel, img_input2, pixels_input2)

################# filter
def imgfilter(option, size, img_input, pixels_input):
    filter_output = Image.new(img_input.mode, img_input.size)
    filter_pixels = filter_output.load()

    if size == 3:
        half = 1
    else:
        half = 2

    for x in range(img_input.width):
        for y in range(img_input.height):
            tmp = []
            for q in range(-1*half, half+1):
                for p in range(-1*half, half+1):
                    tmp_x = x + q
                    tmp_y = y + p
                    if tmp_x > -1 and tmp_x < 512 and tmp_y > -1 and tmp_y < 512:
                        tmp.append(int(pixels_input[tmp_x, tmp_y]))
                    else:
                        tmp.append(0)
            if option == "box":
                num = np.mean(np.asarray(tmp))
            else:
                num = np.median(np.asarray(tmp))
            
            filter_pixels[x, y] = int(num)
    return filter_output

def computeSNR(pixels_input, pixels_instance):
    tmp = 0
    for x in range(512):
        for y in range(512):
            tmp += pixels_input[x, y]
    miu = tmp / (512 * 512)
    
    tmp = 0
    for x in range(512):
        for y in range(512):
            tmp += ((pixels_input[x, y] - miu)**2)
    VS = tmp / (512 * 512)

    tmp = 0
    for x in range(512):
        for y in range(512):
            tmp += (pixels_instance[x, y] - pixels_input[x, y])
    miu = tmp / (512 * 512)

    tmp = 0
    for x in range(512):
        for y in range(512):
            tmp += ((pixels_instance[x, y] - pixels_input[x, y] - miu)**2)
    VN = tmp / (512 * 512)
    return 20 * math.log10(math.sqrt(VS)/math.sqrt(VN))

############## kernel
kernel = []
for i in range(5):
    for j in range(5):
        temp = [i-2, j-2]
        kernel.append(temp)
kernel.remove([-2,-2])
kernel.remove([-2,2])
kernel.remove([2,-2])
kernel.remove([2,2])


noise_img = [img_gau10, img_gau30, img_snp01, img_snp005]
noise_pixels = [pixels_gau10, pixels_gau30, pixels_snp01, pixels_snp005]
output_name = ["gau10", "gau30", "snp01", "snp005"]
for i in range(len(noise_img)):
    SNR = computeSNR(pixels_input, noise_pixels[i])
    print(output_name[i] + 'SNR:' + str(SNR))

    o = opening(kernel, noise_img[i], noise_pixels[i])
    tmp_p = o.load()
    o2 = closing(kernel, o, tmp_p)
    o2.save(output_name[i] + '_oc.bmp')
    tmp_p = o2.load()
    SNR = computeSNR(pixels_input, tmp_p)
    print(output_name[i] + '_oc SNR:' + str(SNR))

    o = closing(kernel, noise_img[i], noise_pixels[i])
    tmp_p = o.load()
    o2 = opening(kernel, o, tmp_p)
    o2.save(output_name[i] + '_co.bmp')
    tmp_p = o2.load()
    SNR = computeSNR(pixels_input, tmp_p)
    print(output_name[i] + '_co SNR:' + str(SNR))

    o = imgfilter("box", 3, noise_img[i], noise_pixels[i])
    o.save(output_name[i] + '_box3.bmp')
    tmp_p = o.load()
    SNR = computeSNR(pixels_input, tmp_p)
    print(output_name[i] + '_box3 SNR:' + str(SNR))

    o = imgfilter("box", 5, noise_img[i], noise_pixels[i])
    o.save(output_name[i] + '_box5.bmp')
    tmp_p = o.load()
    SNR = computeSNR(pixels_input, tmp_p)
    print(output_name[i] + '_box5 SNR:' + str(SNR))

    o = imgfilter("median", 3, noise_img[i], noise_pixels[i])
    o.save(output_name[i] + '_median3.bmp')
    tmp_p = o.load()
    SNR = computeSNR(pixels_input, tmp_p)
    print(output_name[i] + '_median3 SNR:' + str(SNR))

    o = imgfilter("median", 5, noise_img[i], noise_pixels[i])
    o.save(output_name[i] + '_median5.bmp')
    tmp_p = o.load()
    SNR = computeSNR(pixels_input, tmp_p)
    print(output_name[i] + '_median5 SNR:' + str(SNR))
