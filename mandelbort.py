import PIL.Image as Image
from PIL import ImageFilter
import cffi
import sys
import os

color_sets = [
        [
            (0,0,0),
            (255,0,0),
            (255,255,0),
            (255,255,255)
        ],
        [
            (0,0,0),
            (0,0,255),
            (255,255,0),
            (255,255,255)
        ],
        [(0x14,0x7D,0x0D), (0xff, 0xff, 0), (255,255,255), (0,0,0)],
        [(255,255,255),(0,255,255),(0,0,0)],
        [(0,0,0), (0,0xff,0), (0x33,0xff,0x33), (0x33,0xff,0xff)],
        [(0,0,0), (0xff,0xff,0xff)]
    ]

class Render:
    def __init__(self):
        ffi = cffi.FFI()
        #ffi.cdef('struct Color{int r; int g; int b;};')
        ffi.cdef('void* new_state(int w, int h, double x, double X, double y, double Y, int d, double x0, double y0);')
        ffi.cdef('void delete_state(void* s);')
        ffi.cdef('void add_clr(void*, int r, int g, int b);')
        ffi.cdef('int pt_color_j(void* s, int px, int py);')
        ffi.cdef('int pt_color_m(void* s, int px, int py);')
        path = os.path.dirname(os.path.abspath(__file__))
        lib = os.path.join(path, 'libcalc.so')
        print(lib)
        self.lib = ffi.dlopen(lib)

    def draw(self,f,width,height,mx,my,cx,cy,depth,clr_scheme,x0,y0):
        use_long = True
        colors = color_sets[clr_scheme]
        img = Image.new('RGB', (width, height), 'white')
        pic = img.load()
        x = mx - cx / 2.0
        X = mx + cx / 2.0
        y = my - cy / 2.0
        Y = my + cy / 2.0
        lib = self.lib
        state = lib.new_state(width,height,x,X,y,Y,depth,x0,y0)
        for (r,g,b) in colors:
            lib.add_clr(state, r, g, b)
        for x in range(width):
            for y in range(height):
                #clr = f(state,x,y)
                #pic[x,y] = (clr.r, clr.g, clr.b)
                pic[x,y] = f(state,x,y)
        lib.delete_state(state)
        img = img.filter(ImageFilter.SMOOTH)
        return img;
    def draw_j(self,*args):
        f = self.lib.pt_color_j
        return self.draw(f, *args)
    def draw_m(self,*args):
        f = self.lib.pt_color_m
        return self.draw(f, *args)

render = Render()

if __name__ == "__main__":
    #px = int(sys.argv[1])
    #py = int(sys.argv[2])
    #mx = float(sys.argv[3])
    #my = float(sys.argv[4])
    #d  = float(sys.argv[5])
    #s  = int(sys.argv[6])
    px = 500
    py = 500
    (mx,my) = eval(sys.argv[1])
    d = float(sys.argv[2])
    s = int(sys.argv[3])
    (x0,y0) = eval(sys.argv[4])
    if px < py:
        dx = d
        dy = (py / float(px)) * d
    else:
        dy = d
        dx = (px / float(py)) * d
#    dx = float(sys.argv[4])
#    dy = float(sys.argv[5])
    print(px,py,mx,my,dx,dy,s)
    pic = render.draw_m(px,py,mx,my,dx,dy,s,0,x0,y0)
    pic.save('pic.jpg', 'jpeg')

#draw_c(500,500,-2,-1,-0.5,0.5)
