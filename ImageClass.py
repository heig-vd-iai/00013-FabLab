import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.signal import savgol_filter
from os import path

from math import atan2, pi

from GeometricClass import Point, Line
from FileClass import File

class Image:
    def __init__(self, file = "", data = None):
        self.data = data
        self.file = File(file)

        if data is None and file:
            assert(path.exists(file))
            self.data = cv.imread(file, cv.IMREAD_GRAYSCALE)

    def __repr__(self):
        return 'Image: {width:' + str(self.width) + \
                ', height:' + str(self.height) + '}'

    @property
    def width(self):
        return self.shape[1]

    @property
    def height(self):
        return self.shape[0]

    @property
    def shape(self):
        return self.data.shape

    def binarize(self,thrs = 127):
        _, data = cv.threshold(self.data, thrs, 255, \
                    cv.THRESH_BINARY + cv.THRESH_OTSU)
        return Image(data = data);

    def mainContour(self, thres = 127, linewidth = 3):
        maxSize = 0;
        bin = self.binarize(thres)
        contours, hierarchy = cv.findContours(bin.data, \
                                cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for cont in contours:
            size = cv.contourArea(cont)
            if size > maxSize:
                maxSize = size
                maxCont = cont

        data = np.zeros(shape = self.shape, dtype = np.uint8)
        cv.drawContours(data, [maxCont], 0, 255, linewidth);

        return Image(data = data), maxCont

    def invert(self):
        return Image(data = cv.bitwise_not(self.data))

    def rotate(self,angle):
        self.data = cv.imrotate(self.data,angle)

    def crop(self, p1, p2):
        return Image(data = self.data[p1.y:p2.y, p1.x:p2.x])

    def warp(self, T):
        srcShape = np.float32(self.shape).reshape(-1, 1, 2)
        s = cv.perspectiveTransform(srcShape, T).reshape(2)

        return Image(data = cv.warpPerspective(self.data, T, (s[1], s[0])))

    def dilate(self, s):
        strel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (s, s))
        return Image(data = cv.dilate(self.data, strel, 1))

    def erode(self, s):
        strel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (s, s))
        return Image(data = cv.erode(self.data, strel, 1))

    def open(self,s):
        return self.erode(s).dilate(s)

    def close(self,s):
        return self.dilate(s).erode(s)

    def image2tform(self, s, r = .25):
        assert(isinstance(self.data, np.ndarray))

        h_r = int(self.height * r)
        w_r = int(self.width * r)
        h_1_r = self.height - h_r
        w_1_r = self.width - w_r

        contour, _ = self.mainContour();

        P1 = Point(1, 1);
        P2 = Point(self.width, h_r)
        P3 = Point(1, h_1_r)
        P4 = Point(self.width, self.height)
        P5 = Point(w_1_r, 1)
        P6 = Point(w_r, self.height)

        lN = contour.getEdge(P1, P2)
        lS = contour.getEdge(P3, P4)
        lE = contour.getEdge(P5, P4)
        lW = contour.getEdge(P1, P6)

        pNW = lN.intersection(lW)
        pNE = lN.intersection(lE)
        pSW = lS.intersection(lW)
        pSE = lS.intersection(lE)

        pts1 = np.float32([list(pNW), list(pNE), list(pSW), list(pSE)])
        pts2 = np.float32([[0, 0], [s.x, 0], [0, s.y], [s.x, s.y]])
        pts2 = pts2 + np.float32(list(pNW))

        corner = [pNW + Point(20,20), pNW + s - Point(20,20)]
        return cv.getPerspectiveTransform(pts1, pts2), corner

    def image2list(self, T, corner, scale=[1,1]):
        assert(isinstance(self.data, np.ndarray))

        warped = self.warp(T)
        tool = warped.crop(corner[0].round(),corner[1].round())
        tool = tool.invert()

        _, list = tool.dilate(15).mainContour(thres = 200, linewidth = 1)
        list = list.reshape(-1,2)

        list = list - np.mean(list, axis = 0)
        list[:,1] = np.max(list[:,1]) - list[:,1]

        list = list * scale

        mo2 = stats.moment(list, moment = 2)
        angle = atan2(mo2[1], mo2[0]) * 180 / pi

        list[:,0] = savgol_filter(list[:,0], 9, 2)
        list[:,1] = savgol_filter(list[:,1], 9, 2)

        return list, warped

    def show(self, cmap="gray"):
        plt.imshow(self.data, cmap=cmap, vmin=0, vmax=255)
        plt.show()

    def getEdge(self, p1, p2, thres=400):
        mainLine = Line()
        cropped = self.crop(p1, p2)

        lines = cv.HoughLinesP(cropped.data, 1, np.pi/360, thres, 100, 50)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            l = Line(Point(x1,y1), Point(x2,y2))
            mainLine = l if (l.length > mainLine.length) else mainLine

        mainLine.offsetLine(p1)

        return mainLine
