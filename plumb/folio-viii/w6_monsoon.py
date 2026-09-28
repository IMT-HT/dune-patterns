from harness import *
import random
random.seed(11)
b=sandlib.Builder(true_geometry=True)
R=0.93; Y0=0.46
xl=-math.sqrt(R*R-Y0**2)+0.03; xr=-xl
# cloud-base billows: arcs of uneven size along y=Y0, drawn left to right, then back doubled higher
bill=[]; x=xl
while x<xr-0.05:
    w=min(0.10+0.12*random.random(), xr-x); bill.append((x,w)); x+=w
b.move(-0.60,0.68)                        # from the rim, into the storm
b.line(xl,Y0)
for x,w in bill: b.arc(x+w/2,Y0,w/2,180,0)
b.line(xr,Y0)
for x,w in reversed(bill): b.arc(x+w/2,Y0+0.02,w/2+0.01,0,180)   # doubled billows: a heavy base
b.line(xl,Y0)
# rain: each streak goes out from the base and back up itself (the return is a retrace and does not
# show); the ball walks along the base line between streaks -- also a retrace. Slanted on the wind.
ang=math.radians(-110); dx,dy=math.cos(ang),math.sin(ang)
x=xl+0.06; bolt_done=False
while x<xr-0.06:
    L=0.22+0.55*random.random()**1.3
    if 0.30<x<0.52 and bolt_done: x+=0.09; continue
    if abs(x-0.0)<0.22: L=min(L,0.20)     # the rain thins above the mound
    ex,ey=x+dx*L, Y0+dy*L
    if math.hypot(ex,ey)>0.86: s=(0.86)/math.hypot(ex,ey); ex,ey=ex*s,ey*s
    b.line(x,Y0); b.line(ex,ey)
    if L>0.55: b.circle(ex,ey-0.022,0.022,start=90); b.line(ex,ey)   # a splash where it lands
    b.line(x,Y0)
    if (not bolt_done) and x>0.30:
        bolt=[(0.40,Y0),(0.25,0.25),(0.47,0.16),(0.23,-0.12),(0.45,-0.19),(0.21,-0.52)]
        for p in bolt: b.line(*p)
        for p in reversed(bolt): b.line(p[0]+0.022,p[1])
        for p in bolt: b.line(p[0]+0.011,p[1]-0.004)
        b.line(0.40,Y0)
        b.line(x,Y0); bolt_done=True
    x+=0.08+0.035*random.random()
b.line(xr,Y0); b.line(0.70,0.62)           # out along the base; the ball waits at the rim
finish(b,'monsoon',["the redeeming weather: a heavy billowed cloud-base rolls over, rain slants in on the wind in uneven",
  "streaks, splashing where the long ones land; one bolt goes to ground. Every streak is drawn out and back up itself,",
  "so no connector shows. The lower field -- the desert -- is left untouched grain, waiting."],'2026-09-28')
sim('monsoon')
