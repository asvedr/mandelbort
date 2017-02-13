from django.http import HttpResponse
from django.template import Template, Context, loader
import datetime
import sys
import os
import json

from . import mandelbort
from . import settings

def index(request):
    now = datetime.datetime.now()
    tmpl = loader.get_template('render.html')
    return HttpResponse(tmpl.render(Context({})))

mediaurl = 'http://%s/media/' % settings.ALLOWED_HOSTS[0] #'http://95.215.47.224:8000/media/'
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
    #params w&h&x&y&scl&clr
    try:
        scrW = int(request.GET.get('w', ''))
        scrH = int(request.GET.get('h', ''))
        midX = float(request.GET.get('x',''))
        midY = float(request.GET.get('y',''))
        scl  = float(request.GET.get('scl',''))
        clr  = int(request.GET.get('clr','0'))
        samp = int(request.GET.get('samp',60))
        act  = request.GET.get('a','')
    except:
        return HttpResponse(status=400)
    if scrW > scrH:
        sclY = scl
        sclX = scl * scrW / float(scrH)
    else:
        sclX = scl
        sclY = scl * scrH / float(scrW)
    if act == "hi":
        pic = mandelbort.render.draw(scrW,scrH,midX,midY,sclX,sclY,samp,clr)
        ip = get_client_ip(request)
        pic.save(os.path.join(mediadir, ip + 'Hi.png'), 'png')
        ans = json.dumps({'target': mediaurl + ip + 'Hi.png'})
        return HttpResponse(ans, content_type='text')
    else:
        pic_h = mandelbort.render.draw(scrW,scrH,midX,midY,sclX,sclY,samp,clr)
        pic_l = mandelbort.render.draw(int(scrW / 3),int(scrH / 3),midX,midY,sclX * 3,sclY * 3,samp,clr)
        ip = get_client_ip(request)
        pic_h.save(os.path.join(mediadir, ip + 'H.png'), 'png')
        pic_l.save(os.path.join(mediadir, ip + 'L.png'), 'png')
        ans = json.dumps({'target': mediaurl + ip + 'H.png', 'bg': mediaurl + ip + 'L.png'})
        resp = HttpResponse(ans, content_type='text')#content_type='application/json')
        return resp

