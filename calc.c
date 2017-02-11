#include <stdlib.h>

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
//static ColorR color[MAX_LEN];
//static int color_len = 0;

typedef struct {
	double min_x;
	double min_y;
	double dx;
	double dy;
	double width;
	double height;
	long double min_x_l;
	long double min_y_l;
	long double dx_l;
	long double dy_l;
	long double width_l;
	long double height_l;
	int depth;
	ColorR color[MAX_LEN];
	int color_len;
} State;

inline static double julia(double x, double y, int depth) {
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

inline static double julia_long(long double x, long double y, int depth) {
	long double zx = 0;
	long double zy = 0;
	long double zx1, zy1;
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

inline static ColorI get_color(State* state, double x) {
	ColorR buf[MAX_LEN];
	ColorR* color = state -> color;
	for(int i=0; i<state -> color_len - 1; ++i) {
#define COMP(c) buf[i].c = color[i].c + (color[i+1].c - color[i].c) * x
		COMP(r);
		COMP(g);
		COMP(b);
#undef COMP
	}
	int len = state -> color_len - 1;
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
}

/*void null_clr() {
	color_len = 0;
}*/

void add_clr(State* state, int r, int g, int b) {
	ColorR* color = state -> color;
	int color_len = state -> color_len;
	color[color_len].r = (double)r;
	color[color_len].g = (double)g;
	color[color_len].b = (double)b;
	state -> color_len = (color_len + 1) % MAX_LEN;
}

State* new_state(int w, int h, double x, double X, double y, double Y, int d) {
	State* state = malloc(sizeof(State));
	state -> dx = X - x;
	state -> min_x = x;
	state -> dy = Y - y;
	state -> min_y = y;
	state -> width = (double)w;
	state -> height = (double)h;
	
	state -> dx_l = X - x;
	state -> min_x_l = x;
	state -> dy_l = Y - y;
	state -> min_y_l = y;
	state -> width_l = w;
	state -> height_l = h;
	
	state -> depth = d;
	state -> color_len = 0;
	return state;
}

void delete_state(State* s) {
	free(s);
}

ColorI point_color(State* state, int px, int py) {
	double x = (double)px / state -> width;
	double y = (double)py / state -> height;
	x = state -> min_x + x * state -> dx;
	y = state -> min_y + y * state -> dy;
	int d = state -> depth;
	return get_color(state, julia(x,y,d) / d);
}

ColorI point_color_long(State* state, int px, int py) {
	long double x = (long double)px / state -> width_l;
	long double y = (long double)py / state -> height_l;
	x = state -> min_x_l + x * state -> dx_l;
	y = state -> min_y_l + y * state -> dy_l;
	int d = state -> depth;
	return get_color(state, julia_long(x,y,d) / d);
}
