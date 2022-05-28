import multiprocessing as mp

from PIL import Image, ImageDraw
import random
import os
from utils.settings import *


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
    x2 = random.randint(min(x0, x1) + zone - 1, max(x0, x1) - zone)
    midy = (y0 + y1) // 2
    args = [0, midy - zone * 2] if midy > SIZE - midy else [midy + zone * 2,
                                                            SIZE]
    y2 = random.randint(*args)
    return [(x0, y0), (x1, y1), (x2, y2)]


def gen_shape(shape_type, color, uid):
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

    if random.choice([True, False]):
        noise_img = Image.effect_noise((SIZE, SIZE), 25)
        noise_img.putalpha(100)
        img.paste(noise_img, (0, 0), noise_img)
    percentage = area / TOTAL_AREA * 100
    path = f"images/{uid}-{shape_type}-{color}-{percentage:.2f}.png"
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


def generate_each(n):
    start = n * SEQ_SIZE
    stop = start + SEQ_SIZE
    for i in range(start, stop):
        gen_shape(TRIANGLE, random.choice(["red", "blue", "green"]), i)
    for i in range(start, stop):
        gen_shape(RECTANGLE, random.choice(["red", "blue", "green"]), i)
    for i in range(start, stop):
        gen_shape(ELLIPSE, random.choice(["red", "blue", "green"]), i)


def generate():
    init()
    processes = []
    for k in range(NUM_PROCESSES):
        proc = mp.Process(target=generate_each, args=(k,))
        processes.append(proc)
        proc.start()
    for p in processes:
        p.join()

    file_paths = os.listdir("./images/")
    with open('data.txt', 'a') as f:
        print(len(file_paths))
        for path in file_paths:
            data = path[:-4].split('-')
            f.write(f"images/{path},{SHAPE_CODES[data[1]]},"
                    f" {COLOR_CODES[data[2]]}, "
                    f"{data[3]}\n")
