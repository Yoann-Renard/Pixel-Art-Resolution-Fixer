from PIL import Image
import os, sys

path = input("""Path of the image/folder
>> """)
try:
    img = Image.open(path)
    imgpx = img.load()
except Exception as e:
    input(e)
    exit(1)
imgpx = img.load()
pixel_width = int(input("""Number of true pixel per pixel to remove ?
>> """))

os.system('cls')

new_width, new_height = img.size
if img.width % pixel_width > 0:
    new_width -= img.width % pixel_width
if img.height % pixel_width > 0:
    new_height -= img.height % pixel_width
img = img.crop((0, 0, new_width, new_height))

fixed_img = Image.new(
                    mode='RGBA',
                    size=(new_width // pixel_width, new_height // pixel_width)
                      )
fixed_img_px = fixed_img.load()

xi = 0
for x in range(fixed_img.width):
    yi = 0
    for y in range(fixed_img.height):
        fixed_img_px[x, y] = imgpx[xi,yi]
        yi += pixel_width
    xi += pixel_width

fixed_img.save("output.png")
sys.exit(0)