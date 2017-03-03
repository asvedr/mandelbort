from django.http import HttpResponse
from django.template import Template, Context, loader
import datetime
import sys
import os
import json

from . import mandelbort
from . import settings

def fract_man_page(request):
    #now = datetime.datetime.now()
    tmpl = loader.get_template('render_man.html')
    return HttpResponse(tmpl.render(Context({})))

def fract_jul_page(request):
    #now = datetime.datetime.now()
    tmpl = loader.get_template('render_jul.html')
    return HttpResponse(tmpl.render(Context({})))

def index(request):
    tmpl = loader.get_template('index.html')
    return HttpResponse(tmpl.render(Context({})))

mediaurl = 'http://%s:8080/media/' % settings.ALLOWED_HOSTS[0] #'http://95.215.47.224:8000/media/'
mediadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
                                        

def render(request):
    #print('RENDER REQUEST!!!')
    #params w&h&x&y&scl&clr&x0&y0&f[&a]
    END = 'png'#'jpg'
    IMG = 'png'#'jpeg'
    try:
        scrW = int(request.GET.get('w', '')) # image size
        scrH = int(request.GET.get('h', '')) # image size
        midX = float(request.GET.get('x','')) # math pos
        midY = float(request.GET.get('y','')) # math pos
        scl  = float(request.GET.get('scl','')) # scale
        clr  = int(request.GET.get('clr','0')) # color preset
        samp = int(request.GET.get('samp',60)) # samples count
        act  = request.GET.get('a','') # hi res or regular
        x0   = float(request.GET.get('x0','0'))
        y0   = float(request.GET.get('y0','0'))
        fun  = request.GET.get('f','man')
    except:
        return HttpResponse(status=400)
    if scrW > scrH:
        sclY = scl
        sclX = scl * scrW / float(scrH)
    else:
        sclX = scl
        sclY = scl * scrH / float(scrW)
    if fun == "man": # use mandelbort
        fun = mandelbort.render.draw_m
    elif fun == "jul":
        fun = mandelbort.render.draw_j
    else:
        return HttpResponse('use man or jul', status=405) # incorrect method
    if act == "hi":
        pic = fun(scrW,scrH,midX,midY,sclX,sclY,samp,clr,x0,y0)
        ip = get_client_ip(request)
        pic.save(os.path.join(mediadir, ip + 'Hi.' + END), IMG)
        ans = json.dumps({'target': mediaurl + ip + 'Hi.' + END})
        return HttpResponse(ans, content_type='text')
    else:
        pic_h = fun(scrW,scrH,midX,midY,sclX,sclY,samp,clr,x0,y0)
        pic_l = fun(int(scrW / 3),int(scrH / 3),midX,midY,sclX * 3,sclY * 3,samp,clr,x0,y0)
        ip = get_client_ip(request)
        pic_h.save(os.path.join(mediadir, ip + 'H.' + END), IMG)
        pic_l.save(os.path.join(mediadir, ip + 'L.' + END), IMG)
        ans = json.dumps({'target': mediaurl + ip + 'H.' + END, 'bg': mediaurl + ip + 'L.' + END})
        resp = HttpResponse(ans, content_type='text')#content_type='application/json')
        return resp

