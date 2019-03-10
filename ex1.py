import numpy as np
import cv2

global ROW 
global COLUMN
global img

class Rgb:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b

def drawPoint(x,y,color):
    try:
        #图像上显示的坐标与数组下标xy颠倒
        img[y][x] = (color.b,color.g,color.r)
    except:
        return


def bresenhamLine(x1,y1,x2,y2,color):
    print(x1,y1,"  ",x2,y2)
    if(x1 > x2):
        x1,x2 = x2,x1
        y1,y2 = y2,y1
    dx = (float) (x2 - x1)
    dy = (float) (y2 - y1)
    dy_sign = 1 if dy >= 0 else -1
    e = -dx
    if abs(dy)/abs(dx) > 0.5:
        for i in range(0,(int)(abs(dy))):
            drawPoint(x1,y1,color)
            y1 += dy_sign
            e = e + 2*dx
            if e >= 0:
                x1 += 1
                e = e - 2*dy
    else:
        for i in range(0,(int)(abs(dx))):
            drawPoint(x1,y1,color)
            x1 += 1
            e = e + 2*dy
            if e >= 0:
                y1 += dy_sign
                e = e - 2*dx

def draw_bresenham(event,x,y,flags,param):
    global sx,sy
    if(event == cv2.EVENT_LBUTTONDOWN):
        sx = x
        sy = y
    elif(event == cv2.EVENT_LBUTTONUP):
        bresenhamLine(sx,sy,x,y,Rgb(0,0,0))
        cv2.imshow('bresenham',img)

if __name__ == "__main__":
    ROW = 512
    COLUMN = 512
    img = np.ones((ROW,COLUMN,3),np.uint8)
    img[:][:] = (255,255,255)
    cv2.namedWindow('bresenham')
    cv2.setMouseCallback('bresenham',draw_bresenham)
    while(True):
        cv2.imshow('bresenham',img)
        if(cv2.waitKey(0)):
            break

