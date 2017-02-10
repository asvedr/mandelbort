import PIL.Image as Image
#import PIL.ImageFilter as ImageFilter
from PIL import ImageFilter
import cffi
import sys

# use np.longdouble for crd

colors = [
            (0,0,0),
			(0,0,255),
			(255,255,0),
#            (0,0,255),
#            (0,255,0),
#            (255,255,0),
            (255,255,255)
        ]
#colors = [(0x05,0x37,0x79), (0x14,0x7D,0x0D), (0xff, 0xff, 0xff), (0xCC,0xFF,0x00)]
#colors = [(0,0,0), (0xff,0xff,0xff)]
#colors = [(0,0,0), (0,0xff,0), (0x33,0xff,0x33), (0x33,0xff,0xff)]

depth = 60
use_long = False

def draw_c(width,height,x,X,y,Y):
    img = Image.new('RGB', (width, height), 'white')
    pic = img.load()
    ffi = cffi.FFI()
    ffi.cdef('struct Color{int r; int g; int b;};')
    ffi.cdef('void init_win(int w, int h, double x, double X, double y, double Y, int d);')
    ffi.cdef('void null_clr();')
    ffi.cdef('void add_clr(int r, int g, int b);')
    ffi.cdef('struct Color point_color(int px, int py);')
    ffi.cdef('struct Color point_color_long(int px, int py);')
    lib = ffi.dlopen('./libcalc.so')
    for (r,g,b) in colors:
        lib.add_clr(r,g,b)
    lib.init_win(width,height,x,X,y,Y,depth)
    f = None
    if use_long:
        f = lib.point_color_long
    else:
        f = lib.point_color
    for x in range(width):
        for y in range(height):
            clr = f(x,y)
            pic[x,y] = (clr.r, clr.g, clr.b)
    img = img.filter(ImageFilter.SMOOTH)
    img.save('pic.png')

if __name__ == "__main__":
	px = int(sys.argv[1])
	mx = float(sys.argv[2])
	my = float(sys.argv[3])
	d  = float(sys.argv[4])
	try:
		depth = int(sys.argv[5])
	except:
		pass
	try:
		assert(sys.argv[6] == "l")
		use_long = True
	except:
		pass
	draw_c(px,px,mx - d, mx + d, my - d, my + d)

#draw_c(500,500,-2,-1,-0.5,0.5)
