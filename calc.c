#include <math.h>

static double min_x;
static double min_y;
static double dx;
static double dy;
static double width;
static double height;
static int depth;

inline static double julia(double x, double y) {
	double zx = 0;
	double zy = 0;
	double zx1, zy1;
	for(int i=0; i<depth; ++i) {
		zx1 = (zx * zx) - (zy * zy) + x;
		zy1 = zx * zy * 2 + y;
		if(zx1 * zx1 + zy1 * zy1 > 4)
			return (double)i;
		else {
			zx = zx1;
			zy = zy1;
		}
	}
	return (double)depth;
}

void init_win(int w, int h, double x, double X, double y, double Y, int d) {
	dx = X - x;
	min_x = x;
	dy = Y - y;
	min_y = y;
	depth = d;
	width = (double)w;
	height = (double)h;
}

double calc_point(int px, int py) {
	double x = (double)px / width;
	double y = (double)py / height;
	x = min_x + x * dx;
	y = min_y + y * dy;
	return julia(x,y) / depth;
}
