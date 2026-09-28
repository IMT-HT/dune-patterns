import math, numpy as np
def rot(x,y,a):
    c,s=math.cos(a),math.sin(a); return (x*c-y*s, x*s+y*c)
def rect_raster(b, cx, cy, w, h, ang, pitch, along='w'):
    """serpentine raster filling a rotated rectangle; returns exit point"""
    a=math.radians(ang)
    n=max(1,int(round(h/pitch)))
    for i in range(n+1):
        yy=-h/2+h*i/n
        xs=(-w/2,w/2) if i%2==0 else (w/2,-w/2)
        for xx in xs:
            px,py=rot(xx,yy,a); b.line(cx+px,cy+py) if b.pts else b.move(cx+px,cy+py)
def woven_disc(b, cx, cy, R, sp=0.02):
    b.line(cx-R,cy)
    rmin=0.006; turns=(R-rmin)/sp; n=int(turns*180)
    for i in range(1,n+1):
        f=i/n; a=math.pi-turns*2*math.pi*f; r=R+(rmin-R)*f; b.line(cx+r*math.cos(a),cy+r*math.sin(a))
    a0=math.pi-turns*2*math.pi-math.pi
    for i in range(1,n+1):
        f=i/n; a=a0-turns*2*math.pi*f; r=rmin+(R-rmin)*f; b.line(cx+r*math.cos(a),cy+r*math.sin(a))
