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

typedef struct {
	double r;
	double g;
	double b;
} ColorR;

typedef struct {
	int r;
	int g;
	int b;
} ColorI;

#define MAX_LEN 5
static ColorR color[MAX_LEN];
static int color_len = 0;

inline static ColorI get_color(double x) {
	static ColorR buf[MAX_LEN];
	for(int i=0; i<MAX_LEN - 1; ++i) {
#define COMP(c) buf[i].c = color[i].c + (color[i+1].c - color[i].c) * x
		COMP(r);
		COMP(g);
		COMP(b);
#undef COMP
	}
	int len = MAX_LEN - 1;
	while(len > 1) {
#define COMP(c) buf[i].c = buf[i].c + (buf[i+1].c - buf[i].c) * x
		for(int i=0; i<len-1; ++i) {
			COMP(r);
			COMP(g);
			COMP(b);
		}
		len--;
#undef COMP
	}
	ColorI res;
	res.r = (int)buf[0].r;
	res.g = (int)buf[0].g;
	res.b = (int)buf[0].b;
	return res;
//	int r = ((int)buf[0].r) * 0xff * 0xff;
//	int g = ((int)buf[0].g) * 0xff;
//	int b = (int)buf[0].b;
//	return r | g | b;
}

void null_clr() {
	color_len = 0;
}

void add_clr(int r, int g, int b) {
	color[color_len].r = (double)r;
	color[color_len].g = (double)g;
	color[color_len].b = (double)b;
	color_len = (color_len + 1) % MAX_LEN;
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

ColorI point_color(int px, int py) {
	double x = (double)px / width;
	double y = (double)py / height;
	x = min_x + x * dx;
	y = min_y + y * dy;
	return get_color(julia(x,y) / depth);
}
