import numpy as np
import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt
import math
from geometry import Line, Point
from itertools import combinations
from os import listdir
from os.path import isfile, join
import glob
from PIL import Image
from pathlib import Path

lightbox_size = [429, 349] # mm
dpi = 150

green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
thickness = 10


def order_points(points, angle=0):
    centroid = Point(
        sum([p.x for p in points]) / len(points),
        sum([p.y for p in points]) / len(points)
    )

    return [l.p for l in sorted([Line(p, centroid) for p in points], key=lambda l: ((l.theta - angle) % (2 * math.pi) , l.length))]

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
    rect = np.float32([list(p) for p in order_points(pts)])
    print(rect)
    x, y = np.int32(np.array(lightbox_size) * dpi / 25.4)
    dst = np.array([[0, 0], [x, 0], [x, y], [0, y]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(image, M, (x, y))
    # return the warped image
    return warped

def crop(im, gutter, dpi=dpi):
    x, y = im.shape[:2]
    g = int(gutter / 25.4 * dpi)
    return im[g:x - g, g:y - g]

def trim(im, gutter, dpi=dpi, color=(255, 255, 255)):
    y, x = im.shape[:2]
    g = int(gutter / 25.4 * dpi)
    cv.rectangle(im, (0, 0), (x, g), color, -1)
    cv.rectangle(im, (0, 0), (g, y), color, -1)
    cv.rectangle(im, (x - g, 0), (x, y), color, -1)
    cv.rectangle(im, (0, y - g), (x, y), color, -1)

    return im[g:x - g, g:y - g]

def dilate(im, s):
    strel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (s, s))
    return cv.dilate(im, strel, 1)

def erode(im, s):
    strel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (s, s))
    return cv.erode(im, strel, 1)

def iopen(im, s):
    return dilate(erode(im, s), s)

def close(im, s):
    return erode(dilate(im, s), s)

def to_svg(filename, contour, width=lightbox_size[0], height=lightbox_size[1]):
    f = open(filename, 'w+')
    data = ' '.join([f"{x/dpi*25.4} {y/dpi*25.4}" for ((x, y),) in contour])
    f.write('<svg '
        f'width="{width} mm" '
        f'height="{height} mm" '
        f'viewBox="0 0 {width} {height}" '
        'xmlns="http://www.w3.org/2000/svg">'
        f'<path d="M{data}"/>'
        '</svg>'
    )
    f.close()

def process(filename):
    global lines

    filename = Path(filename)
    assert(filename.exists())

    im = cv.imread(str(filename))
    imgray = cv.imread(str(filename), cv.IMREAD_GRAYSCALE)

    _, im3 = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    contours, hierarchy = cv.findContours(im3, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)

    u = np.zeros(imgray.shape, np.uint8)
    cv.drawContours(u, contours, 0, 255, 1)

    lines = cv.HoughLines(u, 1, np.pi / 180, 150, None, 0, 0)

    border = []
    for ((rho, theta),) in lines[:4]:
        x, y = math.cos(theta), math.sin(theta)
        x0, y0 = x * rho, y * rho
        p = Point(x0 + 10000*(-y), y0 + 10000*x)
        q = Point(x0 - 10000*(-y), y0 - 10000*x)
        border.append(Line(p, q))

    for line in border:
        cv.line(im, tuple(line.p.round()), tuple(line.q.round()), red, thickness)

    intersections = [u.intersection(v) for u, v in combinations(border, 2)]
    intersections = [u for u in intersections if u is not None]
    intersections = [Point(int(x), int(y)) for x, y in intersections if y < im.shape[0] and x < im.shape[1]]

    for p in intersections:
        cv.circle(im, tuple(p), 50, green, thickness)

    lines = sorted([Line(u, v) for u, v in combinations(intersections, 2)], key=lambda x: x.length)[:-2]

    for line in lines:
        cv.line(im, tuple(line.p), tuple(line.q), red, thickness)

    plt.imshow(im, extent=[0,lightbox_size[0],0,lightbox_size[1]])
    plt.show()

    im2 = four_point_transform(imgray, intersections)
    im = four_point_transform(im, intersections)

    trim(im2, 10, color=255)

    _, im3 = cv.threshold(im2, 127, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    contours, hierarchy = cv.findContours(im3, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)

    u = np.ones(im3.shape, np.uint8)*255

    cv.drawContours(u, contours, 1, 0, -1)

    #u = iopen(u, int(5 * dpi / 25.4)) # In mm

    contours, hierarchy = cv.findContours(u, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)

    if len(contours) > 1:
        to_svg(Path('output').joinpath(filename.stem + '.svg'), contours[1])

    cv.drawContours(im, contours, 1, red, 10)

    plt.imshow(im)
    plt.show()

process('tests/hex.jpg')

# for i, filename in enumerate(glob.glob("../Images/*.JPG")):
#     filename = Path(filename)
#     process(filename)


# m = four_point_transform(im, intersections)
# cv.drawContours(m, contours, 1, red, thickness)

# m = crop_minAreaRect(m, cv.minAreaRect(contours[1]))

# rect = cv.minAreaRect(contours[1])
# box = cv.boxPoints(rect)
# box = np.int0(box)
# cv.drawContours(m,[box],0,green,thickness)

# rect = cv.minAreaRect(contours[1])
# box = cv.boxPoints(rect)
# box = np.int0(box)
# cv.drawContours(m,[box],0,green,thickness)

# cc = cv.cvtColor(u, cv.COLOR_BGR2RGB)
# rect = cv.minAreaRect(contours[1])
# box = cv.boxPoints(rect)
# box = np.int0(box)
# cv.drawContours(cc,[box],0,green,thickness)

# cim = cv.cvtColor(u, cv.COLOR_BGR2RGB)
# cc = contours[1]
# rows,cols = u.shape[:2]
# [vx,vy,x,y] = cv.fitLine(cc, cv.DIST_L2,0,0.01,0.01)
# lefty = int((-x*vy/vx) + y)
# righty = int(((cols-x)*vy/vx)+y)
# cv.line(cim,(cols-1,righty),(0,lefty),(0,255,123),2)


# plt.imshow(cim, extent=[0,lightbox_size[0],0,lightbox_size[1]])
# plt.show()


# im = Image.fromarray(cim)
# im.save('foobar.jpg', dpi=(dpi, dpi))

# """
# [ ] Auto alignment
# [ ] Crop image
# [ ] Save svg contour ?
# """
