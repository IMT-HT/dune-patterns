from harness import *
b=sandlib.Builder(true_geometry=True)
# a hawser laid down as a Flemish coil: the rope is a cable (prolate cycloid) running along an
# Archimedean spiral from the heart of the coil outward; then the free end runs off across the deck.
R0,R1=0.22,0.80; GAP=0.115                  # turn spacing: coil diameter 0.06 + a clean gap
turns=(R1-R0)/GAP
AMP=0.028; PITCH=0.050                       # loop radius and advance per loop along the rope
# arc length of the spiral, sampled
N=20000
ths=[2*math.pi*turns*i/N for i in range(N+1)]
pts=[((R0+GAP*t/(2*math.pi))*math.cos(t+math.pi), (R0+GAP*t/(2*math.pi))*math.sin(t+math.pi)) for t in ths]
s=[0.0]
for p,q in zip(pts,pts[1:]): s.append(s[-1]+math.dist(p,q))
L=s[-1]
def at(u):
    import bisect
    i=min(bisect.bisect_left(s,u),N)
    return pts[i], (pts[min(i+1,N)][0]-pts[max(i-1,0)][0], pts[min(i+1,N)][1]-pts[max(i-1,0)][1])
# the rope: phase-locked loops along the path
nloops=int(L/PITCH)
M=nloops*48
first=True
for j in range(M+1):
    phi=2*math.pi*j/48
    u=PITCH*j/48 - AMP*math.sin(phi)*0      # advance
    u=min(max(u,0),L)
    (x,y),(tx,ty)=at(u)
    tl=math.hypot(tx,ty) or 1; tx/=tl; ty/=tl; nx,ny=-ty,tx
    # prolate cycloid in the local frame: along = -AMP*sin, across = AMP*(1-cos)-AMP
    dx=-AMP*math.sin(phi); dy=-AMP*math.cos(phi)
    X=x+tx*dx+nx*dy; Y=y+ty*dx+ny*dy
    if first: b.move(X,Y); first=False
    else: b.line(X,Y)
# the free end: the same rope runs off straight across the deck toward the rim, whipped at the tip
ex,ey=b.pos(); end=(0.12,-0.86)
Ls=math.hypot(end[0]-ex,end[1]-ey); tx,ty=(end[0]-ex)/Ls,(end[1]-ey)/Ls; nx,ny=-ty,tx
m=int(Ls/PITCH)*48
for j in range(1,m+1):
    phi=2*math.pi*j/48; u=PITCH*j/48
    dx=-AMP*math.sin(phi); dy=-AMP*math.cos(phi)+AMP
    b.line(ex+tx*(u+dx)+nx*dy, ey+ty*(u+dx)+ny*dy)
wx,wy=b.pos()
for k in range(4):
    b.line(wx+nx*0.035,wy+ny*0.035); b.line(wx-nx*0.035,wy-ny*0.035)
b.line(wx,wy)
finish(b,'flemish-coil',["a hawser flaked down in a Flemish coil on a scrubbed deck: the rope is drawn as a cable -- a looped line",
  "whose every crossing lies over the one before, so it reads as laid strands twisting one way -- spiralling",
  "out from the heart of the coil; the bitter end runs off across the planking, whipped at the tip. For the Navy."],'2026-09-28')
sim('flemish-coil')
