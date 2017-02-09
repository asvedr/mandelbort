import numpy as np
import PIL.Image as Image
import cffi
import sys

# use np.longdouble for crd

black = (0,0,0)
white = (255,255,255)

depth = 60

def color_num(x):
    return (int(x * 255), int(x * 255), int(x * 255))#int((1 - x) * 255))

def draw_c(width,height,x,X,y,Y):
    img = Image.new('RGB', (width, height), 'white')
    pic = img.load()
    ffi = cffi.FFI()
    ffi.cdef('void init_win(int w, int h, double x, double X, double y, double Y, int d);')
    ffi.cdef('double calc_point(int px, int py);')
    lib = ffi.dlopen('./libcalc.so')
    lib.init_win(width,height,x,X,y,Y,depth)
    for x in range(width):
        for y in range(height):
            pic[x,y] = color_num(lib.calc_point(x,y))
    img.save('pic.png')

draw_c(1024,768,-2,2,-2,2)
