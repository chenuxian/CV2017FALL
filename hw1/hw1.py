from PIL import Image

img_input = Image.open('lena.bmp')
img_output = Image.new(img_input.mode, img_input.size )
pixels_input = img_input.load()
pixels_output = img_output.load()

# upside-down 
for x in range(img_output.height):    
    for y in range(img_output.width):
         pixels_output[x, y] = pixels_input[x, img_output.width - y - 1]
img_output.save('upside-down.bmp')

# rightside-left 
for x in range(img_output.height):    
    for y in range(img_output.width):
        pixels_output[x, y] = pixels_input[img_output.height - x - 1, y]
img_output.save('rightside-left.bmp')

# diagonally mirrored 
for x in range(img_output.height):    
    for y in range(img_output.width):
        pixels_output[x, y] = pixels_input[y, x]
img_output.save('diagonally-mirrored.png')

