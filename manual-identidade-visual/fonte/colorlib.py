from PIL import Image, ImageCms
_src=ImageCms.createProfile("sRGB")
_dst=ImageCms.getOpenProfile("/usr/share/color/icc/colord/FOGRA39L_coated.icc")
_t=ImageCms.buildTransform(_src,_dst,"RGB","CMYK",renderingIntent=1)
_b=ImageCms.buildTransform(_dst,_src,"CMYK","RGB",renderingIntent=1)
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def cmyk(h):
    r,g,b=hx(h)
    if r==g==b:  # cinzas: so preto
        return (0,0,0,round(100-r/2.55))
    v=ImageCms.applyTransform(Image.new("RGB",(1,1),(r,g,b)),_t).getpixel((0,0))
    return tuple(round(x/2.55) for x in v)
def printed(h):
    c=ImageCms.applyTransform(Image.new("RGB",(1,1),hx(h)),_t); return '#%02X%02X%02X'%ImageCms.applyTransform(c,_b).getpixel((0,0))
def lum(h):
    def ch(v):
        v/=255; return v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b=map(ch,hx(h)); return 0.2126*r+0.7152*g+0.0722*b
def cr(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True); return (x+0.05)/(y+0.05)
def mix(a,b,t):
    A,B=hx(a),hx(b); return '#%02X%02X%02X'%tuple(round(A[i]+(B[i]-A[i])*t) for i in range(3))
