from harness import *
from lib2 import *
b=sandlib.Builder(true_geometry=True)
b.move(-0.50,0.80)                                   # the entering line, from the rim
cx,cy,w,h,ang=-0.33,0.30,0.50,0.27,-16
a=math.radians(ang)
def P(xx,yy): px,py=rot(xx,yy,a); return (cx+px,cy+py)
b.line(*P(-w/2,-h/2))
rect_raster(b,cx,cy,w,h,ang,0.03)                    # the heavy plane, corrugated
b.line(*P(w/2,h/2))                                  # along its top edge (a retrace, unseen)
X,Y=0.45,0.40
b.line(X-0.02,Y+0.17)                                # a thin rising line to the cross
for p in [(X-0.02,Y-0.17),(X,Y-0.17),(X,Y+0.17),(X+0.02,Y+0.17),(X+0.02,Y-0.17)]: b.line(*p)
b.line(X+0.02,Y); b.line(X-0.22,Y)
for p in [(X-0.22,Y-0.02),(X+0.22,Y-0.02),(X+0.22,Y),(X-0.22,Y),(X-0.22,Y+0.02),(X+0.22,Y+0.02)]: b.line(*p)
b.line(0.86,-0.05)                                   # down the right to the long bar
b.line(-0.35,-0.80); b.line(-0.345,-0.775); b.line(0.855,-0.025)   # the bar, doubled bold
b.line(0.15,-0.15)
b.circle(0.25,-0.15,0.10,start=180)                  # the ring round a flat island
b.line(-0.55,-0.30)
woven_disc(b,-0.48,-0.30,0.07)                       # the small dish; the ball rests here
finish(b,'white-on-white-ground',["a Suprematist composition made of the sand's own textures instead of colours: a heavy tilted plane",
  "corrugated at 0.03, a fused cross, a woven dish, a ring round a flat island, one long bold bar and a few thin",
  "lines -- floating on the white grain. Nothing represented; only weight, tilt and texture. After the wall's #58."],'2026-09-28')
sim('white-on-white-ground')
