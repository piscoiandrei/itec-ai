import time
import math
from PIL import Image, ImageDraw
import random
import os
from utils.settings import *


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.5f} s'.format(f.__name__,
                                                   (time2 - time1)))
        return ret
    return wrap


def rand2():
    # generating the coordinates for the bounding box
    x0 = random.randint(0, SIZE - zone)
    # x1 must be > x0, same for y
    x1 = random.randint(x0 + zone, SIZE)
    y0 = random.randint(0, SIZE - zone)
    y1 = random.randint(y0 + zone, SIZE)
    return [(x0, y0), (x1, y1)]


def rand3():
    # generating coordinates for a triangle
    x0 = random.randint(zone * 2, SIZE - zone * 2)
    args = [0, x0 - zone * 2] if x0 > SIZE - x0 else [x0 + zone * 2, SIZE]
    x1 = random.randint(*args)
    y0 = random.randint(zone * 2, SIZE - zone * 2)
    args = [0, y0 - zone * 2] if y0 > SIZE - y0 else [y0 + zone * 2, SIZE]
    y1 = random.randint(*args)
    x2 = random.randint(min(x0, x1) + zone, max(x0, x1) - zone)
    midy = (y0 + y1) // 2
    args = [0, midy - zone * 2] if midy > SIZE - midy else [midy + zone * 2,
                                                            SIZE]
    y2 = random.randint(*args)
    return [(x0, y0), (x1, y1), (x2, y2)]


def generate_shape(shape_type, color, uid):
    img = Image.new(mode="RGB", size=(SIZE, SIZE), color="black")
    img_draw = ImageDraw.Draw(img)
    if shape_type == ELLIPSE:
        img_draw.ellipse(rand2(), fill=COLORS[color])
        area = 0
        for pixel in img.getdata():
            if pixel != (0, 0, 0):
                area += 1
    elif shape_type == TRIANGLE:
        img_draw.polygon(rand3(), fill=COLORS[color])
        area = 0
        for pixel in img.getdata():
            if pixel != (0, 0, 0):
                area += 1
    else:
        p1, p2 = rand2()
        area = (p2[0] - p1[0]) * (p2[1] - p1[1])
        img_draw.rectangle([p1, p2], fill=COLORS[color])

    path = f"images/{uid}-{shape_type}-{color}.png"
    with open('data.txt', 'a') as f:
        f.write(f"{path},{SHAPE_CODES[shape_type]},{COLOR_CODES[color]},"
                f"{area / TOTAL_AREA}\n")
    img.save(path)


def init():
    try:
        os.remove('data.txt')
    except OSError:
        pass
    try:
        os.makedirs('images')
    except OSError:
        pass


@timing
def generate(n):
    for i in range(n):
        generate_shape(TRIANGLE, random.choice(["red", "blue", "green"]), i)
    for i in range(n):
        generate_shape(RECTANGLE, random.choice(["red", "blue", "green"]), i)
    for i in range(n):
        generate_shape(ELLIPSE, random.choice(["red", "blue", "green"]), i)


if __name__ == '__main__':
    init()
    generate(10)
