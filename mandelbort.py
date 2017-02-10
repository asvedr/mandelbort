import numpy as np
import PIL.Image as Image
import cffi
import sys

# use np.longdouble for crd

colors = [
            (0,0,0),
            (0,0,255),
            (255,255,0),
            (255,255,255)
        ]

depth = 60

def draw_c(width,height,x,X,y,Y):
    img = Image.new('RGB', (width, height), 'white')
    pic = img.load()
    ffi = cffi.FFI()
    ffi.cdef('struct Color{int r; int g; int b;};')
    ffi.cdef('void init_win(int w, int h, double x, double X, double y, double Y, int d);')
    ffi.cdef('void null_clr();')
    ffi.cdef('void add_clr(int r, int g, int b);')
    ffi.cdef('struct Color point_color(int px, int py);')
    lib = ffi.dlopen('./libcalc.so')
    for (r,g,b) in colors:
        lib.add_clr(r,g,b)
    lib.init_win(width,height,x,X,y,Y,depth)
    for x in range(width):
        for y in range(height):
            clr = lib.point_color(x,y)
            pic[x,y] = (clr.r, clr.g, clr.b)
    img.save('pic.png')

draw_c(500,500,-2,2,-2,2)
