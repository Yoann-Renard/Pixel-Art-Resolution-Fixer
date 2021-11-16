from PIL import Image
import os
import sys
import glob
from multiprocessing import Process


def find_square(img) -> list():
    square_list = []
    for y in range(round(img.height * 1/4), round(img.height * 3/4)):
        for x in range(round(img.width * 1/4), round(img.width * 3/4)):
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
            square_list.append(ly1+1)
            if len(square_list) == 10:
                return square_list
    return square_list

def fix_resolution(img, filename):
    imgpx = img.load()
    process_pid = os.getpid()
    pixel_width = 0

    print(f"Process {process_pid} is running !")

    square_list = find_square(img)

    pixel_width = most_frequent(square_list)

    if pixel_width-1 == 0:
        print(f"{filename} is already at the right resolution")
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

    new_file_name = "resized_" + filename
    fixed_img.save(new_file_name)

    print(f"Process {process_pid} is done !")
    print(f"{new_file_name} created !")

    exit(0)


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
        inp = input("""Convert an specific file (1) or every image in this directory (2) ?
        >> """)
        if inp == "1":
            path = input("""Path of the image/folder
    >> """)
            try:
                img = Image.open(path)
                imgpx = img.load()
            except Exception as e:
                input(e)
            else:
                fix_resolution(img, path)

        elif inp == "2":
            processes = []
            for filename in glob.glob('*.png'):
                img = Image.open(filename)
                p = Process(target=fix_resolution, args=(img, filename))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
            else:
                input("Everything done !")
                exit(0)
        else:
            os.system('cls')
