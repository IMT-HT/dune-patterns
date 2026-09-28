from harness import *
import numpy as np
b = sandlib.Builder(true_geometry=True)
P = np.array([(-0.94,-0.17),(-0.62,-0.31),(-0.28,-0.35),(0.03,-0.25),(0.24,-0.02),(0.35,0.26),(0.39,0.44)])
def catmull(P, n=900):
    pts=[]
    Q=np.vstack([P[0]*2-P[1],P,P[-1]*2-P[-2]])
    for i in range(1,len(Q)-2):
        p0,p1,p2,p3=Q[i-1],Q[i],Q[i+1],Q[i+2]
        for t in np.linspace(0,1,n//(len(P)-1),endpoint=False):
            pts.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    pts.append(P[-1]); return np.array(pts)
C = catmull(P)
# a slight hand: low-frequency wander
s = np.r_[0,np.cumsum(np.hypot(*np.diff(C,axis=0).T))]; L=s[-1]
T = np.gradient(C,axis=0); T/=np.linalg.norm(T,axis=1)[:,None]; N=np.stack([-T[:,1],T[:,0]],1)
C = C + N*(0.012*np.sin(s/L*2*np.pi*2.3)+0.006*np.sin(s/L*2*np.pi*5.1))[:,None]
HALF = 0.05                                   # skis 0.10 apart: two clean troughs
left = C + N*HALF; right = C - N*HALF
def pole_marks(side_pts, sgn, forward=True):
    """walk a ski line; plant poles on its outer side, fading: smaller and sparser toward the end."""
    idx = range(len(side_pts)) if forward else range(len(side_pts)-1,-1,-1)
    next_s = 0.10 if forward else None
    plants = []
    k=0; ss=0.12
    while ss < L*0.93:
        f = ss/L
        plants.append((ss + (0.07 if sgn<0 else 0), 0.018 - 0.008*f))
        ss += 0.17 + 0.16*f + 0.03*math.sin(k*1.7)
        k+=1
    marks = {int(np.searchsorted(s, p)): r for p,r in plants}
    order = list(idx)
    for i in order:
        b.line(*side_pts[i]) if b.pts else b.move(*side_pts[i])
        if i in marks and (i % 2 == (0 if sgn>0 else 1) or True):
            r = marks[i]
            n = N[i]*sgn
            foot = side_pts[i] + n*0.015
            cen = foot + n*r
            b.line(*foot)
            ang = math.degrees(math.atan2(-n[1],-n[0]))
            b.circle(cen[0],cen[1],r,start=ang)
            b.line(*side_pts[i])
# in along the left ski, poles on the left
pole_marks(left, +1, True)
# the end of the track: a small rounded turn
end = C[-1]; tdir = T[-1]
b.arc(end[0], end[1], HALF, math.degrees(math.atan2(N[-1][1],N[-1][0])), math.degrees(math.atan2(N[-1][1],N[-1][0]))-180)
# back along the right ski, poles on the right (sparser: the other hand)
pole_marks(right, -1, False)
# and in again along the right ski without marks (a retrace does not show) to stand at the end
for i in range(len(right)): b.line(*right[i])
b.line(*end)
finish(b, 'into-the-white', ["for the half of the heart that stays in the snow: a single ski track comes in from the edge,",
   "its pole-marks fading and thinning as it goes, and stops. No one else for miles. The grain is the snowfield;",
   "the ball, parked at the end of the track, is the one standing figure, staring into the white."], '2026-09-28')
sim('into-the-white')
