from PIL import Image
import os, sys

img = Image.open(r"img/char_sample/royal.png")
imgpx = img.load()
pixel_width = int(input("""Nombre de pixel réel pour un pixel ?
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

fixed_img.save("test.png")
sys.exit(0)