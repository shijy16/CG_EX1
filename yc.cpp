#include<opencv2\opencv.hpp>
using namespace cv;

const int col = 500, row = 500;
const int scale = 2;

struct color{
	int R;
	int G;
	int B;
	bool operator ==(const color& c){
		if(this->R==c.R && this->G==c.G && this->B==c.B) return true;
		return false;
	}
};

void drawpoint(int x, int y, Mat img, color mycolor){
	if(x >=0 && y >= 0 && x <= col*scale && y <= row*scale){
		img.at<Vec3b>(y,x)[0] = mycolor.B; //B  
		img.at<Vec3b>(y,x)[1] = mycolor.G; //G 
		img.at<Vec3b>(y,x)[2] = mycolor.R; //R
	}
}

void Bresenhamline(int x0, int y0, int x1, int y1, Mat img, color mycolor){
	if((x0<x1&&y0>y1&&(x1-x0<y0-y1))||(x0>x1&&y0<y1&&(x0-x1>y1-y0))||(x0>x1&&y0>y1)){
		swap(x0, x1);
		swap(y0, y1);
	}
	int x, y, dx, dy, e;
	dx = x1-x0, dy = y1-y0, e = -dx;
	x = x0, y = y0;
	if(abs(dx)>=abs(dy)){
		int flag;
		if(dy>0) flag = 1;
		else flag = -1;
		e*=flag;
		for(int i = 0; i <= dx; i++){
			drawpoint(x, y, img, mycolor);
			x++; e = e+2*dy;
			if(e*flag>=0){
				y+=flag;
				e = e-2*dx*flag;
			}
		}
	}
	else{
		int flag;
		if(dx>0) flag = 1;
		else flag = -1;
		e*=flag;
		for(int i = 0; i <= dy; i++){
			drawpoint(x, y, img, mycolor);
			y++; e = e+2*dx;
			if(e*flag>=0){
				x+=flag;
				e = e-2*dy*flag;
			}
		}
	}
}

void CirclePoints(int x0, int y0, int x, int y, Mat img, color mycolor){
	drawpoint(x0+x, y0+y, img, mycolor); drawpoint(x0+y, y0+x, img, mycolor);
	drawpoint(x0-x, y0+y, img, mycolor); drawpoint(x0+y, y0-x, img, mycolor);
	drawpoint(x0+x, y0-y, img, mycolor); drawpoint(x0-y, y0+x, img, mycolor);
	drawpoint(x0-x, y0-y, img, mycolor); drawpoint(x0-y, y0-x, img, mycolor);
}

void MidPointCircle(int x0, int y0, int r, Mat img, color mycolor){
	int x, y;
	x = 0;
	float d;
	y = x+r;
	d = 1.25-r;
	CirclePoints(x0, y0, x, y, img, mycolor);
	while(x<=y){
		if(d<0) d += 2*x+3;
		else{
			d+=2*(x-y)+5;
			y--;
		}
		x++;
		CirclePoints(x0, y0, x, y, img, mycolor);
	}
}

void mydrawCircle(int x, int y, int r, Mat img, color mycolor){
	MidPointCircle(x*scale, y*scale, r*scale, img, mycolor);
	for(int i = 1; i <= scale/2; i++){
		MidPointCircle(x*scale, y*scale, r*scale-i, img, mycolor);
	}
}

void mydrawline(int x1, int y1, int x2, int y2, Mat img, color mycolor){
	Bresenhamline(x1*scale, y1*scale, x2*scale, y2*scale, img, mycolor);
	for(int i = 1; i <= scale/2; i++){
		Bresenhamline(x1*scale, y1*scale+i, x2*scale, y2*scale+i, img, mycolor);
	}
} 

int main(int argc, char** argv){
	Mat img = Mat::zeros(row*scale,col*scale,CV_8UC3);
	Mat _img = Mat::zeros(row, col, CV_8UC3);
	color mycolor, color1, color2;
	mycolor.R=255;
	mycolor.G=255;
	mycolor.B=255;
	mydrawline(260, 470, 10, 10, img, mycolor);
	mydrawCircle(200, 150, 100, img, mycolor);
	mydrawCircle(250, 150, 100, img, mycolor);
	Mat kernel = (Mat_<double>(3,3) << 1.0/16.0, 2.0/16.0, 1.0/16.0,
								   2.0/16.0, 4.0/16.0, 2.0/16.0,
								   1.0/16.0, 2.0/16.0, 1.0/16.0);
	Mat dst;
	resize(img, _img, _img.size());
	filter2D(_img, dst, _img.depth(),kernel); 
	imwrite("dst.png", dst);
	namedWindow("dst", CV_WINDOW_AUTOSIZE );
	imshow("dst", dst);
	waitKey(0); 
	destroyWindow("dst");
	return 0;
}