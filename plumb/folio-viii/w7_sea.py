from harness import *
from lib2 import woven_disc
import random
random.seed(3)
b=sandlib.Builder(true_geometry=True)
R=0.93; HZ=-0.10                                   # the horizon
# the sea: swells below the horizon, uneven, spacing widening toward the viewer (perspective)
ys=[HZ-0.0]; g=0.078
while ys[-1]-g>-0.86: ys.append(ys[-1]-g); g*=1.13
def swell(y,k,forward):
    xm=math.sqrt(max(R*R-y*y,0))-0.01
    n=260; out=[]
    amp=0.010+0.005*k; f1=5+random.random()*3; ph=random.random()*6
    for i in range(n+1):
        x=-xm+2*xm*i/n
        out.append((x, y+amp*math.sin(f1*x*math.pi+ph)+0.5*amp*math.sin(2.3*f1*x+ph*1.7)))
    return out if forward else out[::-1]
first=True
for k,y in enumerate(ys):
    sw=swell(y,k,k%2==0)
    if first: b.move(*sw[0]); first=False
    else:
        # step down to the next swell along the rim, not across the water
        x0,y0=b.pos(); a0=math.degrees(math.atan2(y0,x0)); a1=math.degrees(math.atan2(sw[0][1],sw[0][0]))
        r0=math.hypot(x0,y0)
        d=(a1-a0+540)%360-180
        b.arc(0,0,r0,a0,a0+d)
    for p in sw: b.line(*p)
# up the right edge to the horizon; the horizon line itself (a single thread, the sea's edge)
xh=math.sqrt(R*R-HZ*HZ)-0.02
x0,y0=b.pos(); r0=math.hypot(x0,y0); a0=math.degrees(math.atan2(y0,x0)); a1=math.degrees(math.atan2(HZ,xh))
d=(a1-a0+540)%360-180
b.arc(0,0,r0,a0,a0+d)                               # up the rim, not across the water
b.line(xh,HZ)
b.line(-xh,HZ)
# the Silver River rising out of the sea: a braid of two strands arching from the horizon (left)
# over the sky and back into the sea (right) -- 'the Star-Han, brilliant, as if it came from within it'
def arch(t, off):
    a=math.pi*(1-t)
    return (0.74*math.cos(a), HZ+0.02+0.74*math.sin(a)*0.98+off)
xL,yL=arch(0,0)
b.line(-xh+0.05,HZ); b.line(xL,yL)
n=500
for i in range(n+1):
    t=i/n; x,y=arch(t,0); b.line(x,y+0.028*math.sin(t*math.pi*14))
for i in range(n,-1,-1):
    t=i/n; x,y=arch(t,0); b.line(x,y-0.028*math.sin(t*math.pi*14))
# the sun rising out of the sea, left (a woven dish, bright); the moon right (a ring round an island)
b.line(-0.51,HZ); b.line(-0.51,HZ+0.11)
woven_disc(b,-0.40,HZ+0.11,0.11)
b.line(-0.29,HZ); b.line(0.30,HZ)
b.circle(0.40,HZ+0.12,0.08,start=270)
# the ball goes down into the sea and rests in the swell
b.line(0.40,HZ+0.04)          # the ball rests at the moon's foot, on the sea
finish(b,'viewing-the-blue-sea',["after Cao Cao's 'Viewing the Blue Sea' (Jieshi, 207): the sea in uneven swells widening toward the",
  "shore, and rising out of it the sun (a woven dish), the moon (a ring round its island) and the Silver River",
  "arching overhead as a braid -- 'as if they came out of it.' A response to the first hand's star-han-river."],'2026-09-28')
sim('viewing-the-blue-sea')
