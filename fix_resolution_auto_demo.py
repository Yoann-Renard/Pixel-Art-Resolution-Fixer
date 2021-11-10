from PIL import Image
import os
import sys
import turtle

path = input("""Path of the image/folder
>> """)
img = Image.open(path)
imgpx = img.load()

pixel_width = 0
"""TURTLE"""
tr = turtle.Turtle()



def reset_tr(x,y):
    tr.clear()
    tr.pu()
    tr.goto(-img.width / 2, img.height / 2)
    tr.fd(x)
    tr.rt(90)
    tr.fd(y)
    tr.pd()
    tr.setheading(270)


tr.ht()
tr.color('red')
tr.speed(0)
screen = turtle.Screen()
screen.setup(width=img.width+10, height=img.height+10)
screen.bgpic(path)

reset_tr(90, 50)
tr.fd(50)
#tr.fd(1)
#tr.rt(90)
#tr.lt(90)





'''AUTO'''

square_list = []
for y in range(img.height):
    for x in range(img.width):
        reset_tr(x, y)
        cy = y
        cx = x
        ly1 = 0
        lx1 = 0
        ly2 = 0
        lx2 = 0

        while cy + 1 < img.height and img.getpixel((cx, cy)) == img.getpixel((cx, cy + 1)):
            cy += 1
            ly1 += 1

        while cx + 1 < img.width and img.getpixel((cx, cy)) == img.getpixel((cx + 1, cy)):
            cx += 1
            lx1 += 1
        else:
            if lx1 == ly1:
                pass
            else:
                tr.fd(ly1)
                tr.lt(90)
                tr.fd(lx1)
                continue

        while cy - 1 >= 0 and img.getpixel((cx, cy)) == img.getpixel((cx, cy - 1)):
            cy -= 1
            ly2 += 1
        else:
            if ly2 == ly1:
                pass
            else:
                tr.fd(ly1)
                tr.lt(90)
                tr.fd(lx1)
                tr.lt(90)
                tr.fd(ly2)
                tr.lt(90)
                continue

        while cx - 1 >= 0 and img.getpixel((cx, cy)) == img.getpixel((cx - 1, cy)):
            cx -= 1
            lx2 += 1
        else:
            tr.fd(lx2)
            if lx2 == ly1:
                pass
            else:
                tr.fd(ly1)
                tr.lt(90)
                tr.fd(lx1)
                tr.lt(90)
                tr.fd(ly2)
                tr.lt(90)
                tr.fd(lx2)
                continue
        tr.fd(ly1)
        tr.lt(90)
        tr.fd(lx1)
        tr.lt(90)
        tr.fd(ly2)
        tr.lt(90)
        tr.fd(lx2)
        square_list.append(ly1+1)


def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num


print(square_list)
pixel_width = most_frequent(square_list)

if pixel_width-1 == 0:
    print("The image have already the right resolution")
    exit(0)


''''''

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
        fixed_img_px[x, y] = imgpx[xi, yi]
        yi += pixel_width
    xi += pixel_width

fixed_img.save("output.png")
screen.mainloop()
sys.exit(0)
