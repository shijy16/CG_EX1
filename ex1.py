import numpy as np
import cv2
import math

global ROW 
global COLUMN
global img
global SSAA_img
global cnt
global mode

class Rgb:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b

    def lighten(self,p):
        return Rgb((float)(self.r)*p,(float)(self.g)*p,(float)(self.b)*p)

def drawPoint(x,y,color):
    global mode
    try:
        #图像上显示的坐标与数组下标xy颠倒
        if mode == 1:
            img[int(y)][int(x)] = (color.b,color.g,color.r)
        else:
            SSAA_img[int(x)][int(y)] = (color.b,color.g,color.r)
    except:
        return


def bresenhamLine(x1,y1,x2,y2,color):
    if(x1 > x2):
        x1,x2 = x2,x1
        y1,y2 = y2,y1
    dx = (float) (x2 - x1)
    dy = (float) (y2 - y1)
    # print("\t",x1,y1,"  ",x2,y2,"  ",dx,dy,abs(dy)/abs(dx))
    dy_sign = 1 if dy >= 0 else -1
    dy = abs(dy)
    if abs(dy) > 0.5*abs(dx):
        e = -dx
        for i in range(0,(int)(abs(dy))):
            drawPoint(x1,y1,color)
            y1 += dy_sign
            e = e + 2*dx
            if e >= 0:
                x1 += 1
                e = e - 2*dy
    else:
        e = -dy
        for i in range(0,(int)(abs(dx))):
            drawPoint(x1,y1,color)
            x1 += 1
            e = e + 2*dy
            if e >= 0:
                y1 += dy_sign
                e = e - 2*dx

#Wu Xiaolin http://www.wikiwand.com/zh-mo/吴小林直线算法
def ipart(x):
    return int(x)

def fpart(x):
    return float(x - ipart(x))

def rfpart(x):
    return float(1) - fpart(x)

def wuLine(x1,y1,x2,y2,color):
    dx = x2 - x1
    dy = y2 - y1
    flag = False
    if(abs(dx) < abs(dy)):
        x1,y1 = y1,x1
        x2,y2 = y2,x2
        dx,dy = dy,dx
        flag = True
    if x2 < x1:
        x1,x2 = x2,x1
        y1,y2 = y2,y1
    print(dy,dx)
    k = dy/dx
    print("\t",x1,y1,"  ",x2,y2,"  ",dx,dy,abs(dy)/abs(dx))

    xgap = 0.5
    xpxl1 = x1
    ypxl1 = 0
    xpxl2 = x2
    ypxl2 = 0
    intery = y1 + k

    #loop
    if(flag):
        for x in range(xpxl1,xpxl2):
            drawPoint(ipart(intery),x,color.lighten(rfpart(intery)))
            drawPoint(ipart(intery) + 1,x,color.lighten(fpart(intery)))
            intery = intery + k
    else:    
        for x in range(xpxl1,xpxl2):
            drawPoint(x,ipart(intery),color.lighten(rfpart(intery)))
            drawPoint(x,ipart(intery) + 1,color.lighten(fpart(intery)))
            intery = intery + k


def circlePoint(x0,y0,x,y,color):
    # print("\t",x0,y0,x,y)
    drawPoint(x0+x,y0+y,color)
    drawPoint(x0+x,y0-y,color)
    drawPoint(x0-x,y0+y,color)
    drawPoint(x0-x,y0-y,color)
    drawPoint(x0+y,y0+x,color)
    drawPoint(x0+y,y0-x,color)
    drawPoint(x0-y,y0+x,color)
    drawPoint(x0-y,y0-x,color)


def midPointCircle(x0,y0,r,color):
    x = 0
    y = x + r
    d = 1.25 - float(r)
    circlePoint(x0,y0,x,y,color)
    while x <= y:
        if(d < 0):
            d = d + 2*x + 3
        else:
            d = d + 2*(x-y) + 5
            y-=1
        x+= 1
        circlePoint(x0,y0,x,y,color)

def SSAAMidPointCircle(x,y,r,color):
    s = 2
    midPointCircle(x*s,y*s,s*r,color)
    for i in range(1,(int)(s/2)+1):
        midPointCircle(x*s,y*s,r*s-i,color)

def SSAABresenhamLine(x1,y1,x2,y2,color):
    s = 2
    bresenhamLine(x1*s,y1*s,x2*s,y2*s,color)
    for i in range(1,(int)(s/2)+1):
        bresenhamLine(x1*s,y1*s+i,x2*s,y2*s+i,color)

def drawWhich(x1,y1,x2,y2):
    global cnt
    cnt += 1
    if(cnt % 3 == 0):
        print("bresenhamLine")
        bresenhamLine(x1,y1,x2,y2,Rgb(0,0,0))
    elif(cnt % 3 == 1):
        print("Wu Xiaolin")
        wuLine(x1,y1,x2,y2,Rgb(255,0,0))
    elif(cnt % 3 == 2):
        print("midPointCircle")
        midPointCircle((x1+x2)/2,(y1+y2)/2,math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))/2,Rgb(0,255,0))
     
def drawLine(event,x,y,flags,param):
    global sx,sy
    if(event == cv2.EVENT_LBUTTONDOWN):
        sx = x
        sy = y
    elif(event == cv2.EVENT_LBUTTONUP):
        drawWhich(sx,sy,x,y)
        cv2.imshow('draw',img)

if __name__ == "__main__":
    mode = 1
    cnt = -1
    ROW = 512
    COLUMN = 512
    img = np.ones((ROW,COLUMN,3),np.uint8)
    SSAA_img = np.ones((ROW*2,COLUMN*2,3),np.uint8)
    img[:][:] = (255,255,255)
    SSAA_img[:][:] = (255,255,255)
    cv2.namedWindow('draw')
    cv2.setMouseCallback('draw',drawLine)
    while(True):
        cv2.imshow('draw',img)
        if(cv2.waitKey(0)):
            break
    cv2.imwrite("img.jpg",img)
    img[:][:] = (255,255,255)
    midPointCircle(250,250,200,Rgb(0,0,255))
    bresenhamLine(1,1,500,500,Rgb(0,0,0))
    #anti-alias
    mode = 2
    SSAAMidPointCircle(250,250,200,Rgb(0,0,255))
    SSAABresenhamLine(1,1,500,500,Rgb(0,0,0))

    SSAA_img = cv2.resize(SSAA_img,(512,512))
    #filter2D
    kernel = [[1.0/16.0, 2.0/16.0, 1.0/16.0], \
        [2.0/16.0, 4.0/16.0, 2.0/16.0], \
        [1.0/16.0, 2.0/16.0, 1.0/16.0]]
    kernel = np.mat(kernel)
    cv2.filter2D(SSAA_img,-1,kernel)
    cv2.imshow("after anti-alias",SSAA_img)
    cv2.imshow("before anti-alias",img)
    cv2.waitKey(0)
    cv2.imwrite("antialias.jpg",SSAA_img)
    cv2.imwrite("before_antialias.jpg",SSAA_img)

