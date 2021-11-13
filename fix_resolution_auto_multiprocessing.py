from PIL import Image
import os
import sys
import glob
from multiprocessing import Process



def fix_resolution(img, imgpx, filename):
    pixel_width = 0

    square_list = []
    for y in range(img.height):
        for x in range(img.width):
            cy=y
            cx=x
            ly1=0
            lx1=0
            ly2=0
            lx2=0

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
                    continue

            while cy - 1 >= 0 and img.getpixel((cx, cy)) == img.getpixel((cx, cy - 1)):
                cy -= 1
                ly2 += 1
            else:
                if ly2 == ly1:
                    pass
                else:
                    continue

            while cx - 1 >= 0 and img.getpixel((cx, cy)) == img.getpixel((cx - 1, cy)):
                cx -= 1
                lx2 += 1
            else:
                if lx2 == ly1:
                    pass
                else:
                    continue
            sys.stdout.write(".")
            square_list.append(ly1+1)

    print(square_list)
    pixel_width = most_frequent(square_list)

    if pixel_width-1 == 0:
        print("The image is already at the right resolution")
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

    fixed_img.save(filename)



def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num



if __name__ == '__main__':
    while True:
        input = input("""Convert an specific file (1) or every image in this directory (2) ?
        >> """)
        if input == "1":
            path = input("""Path of the image/folder
    >> """)
            try:
                img = Image.open(path)
                imgpx = img.load()
            except Exception as e:
                input(e)
            else:
                fix_resolution(img, imgpx, path)

        elif input == "2":
            for filename in glob.glob('[*.png,*.jpg]'):
                img = Image.open(path)
                imgpx = img.load()
                p = Process(target=fix_resolution, args=(img,imgpx,filename))
            p.join()
            input("Everything done !")
            exit(0)

        else:
            os.system('cls')
