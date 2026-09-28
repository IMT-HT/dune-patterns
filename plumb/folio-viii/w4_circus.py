from harness import *
b=sandlib.Builder(true_geometry=True)
A0,B0,DA,DB=0.92,0.68,0.064,0.078          # outermost lap; lap-to-lap spacing (clean, >=0.075)
def ell(k): return A0-DA*(6-k), B0-DB*(6-k)  # k=0 innermost .. 6 outermost
b.move(-0.95,0.0)                            # enter on the starting line from the carceres
b.line(-0.50,0.0)
# the spina: metae (three cones) at each end, the obelisk ringed at the centre
def meta(x,s):
    for d in (0.035,0,-0.035): b.line(x+s*0.05,d); b.line(x,0)
meta(-0.46,-1)
b.line(-0.16,0.0); b.arc(0,0,0.16,180,0); b.line(0.46,0.0)
meta(0.46,+1)
b.line(0.16,0.0); b.arc(0,0,0.16,0,-180); b.line(-0.46,0.0)
# the laps, from the inside line outward; each lap begins on the starting line (left) and runs round
for k in range(7):
    a,bb=ell(k)
    b.line(-a,0.0)
    turns = 1.0 if k<6 else 0.5              # the seventh lap is still running
    n=int(900*turns)
    for i in range(1,n+1):
        t=math.pi-2*math.pi*turns*i/n        # clockwise, as the chariots ran
        b.line(a*math.cos(t), bb*math.sin(t))
finish(b,'circus-maximus',["the Circus Maximus in one line: the spina with its metae, the obelisk Augustus brought from",
  "Heliopolis in 10 BC standing at the centre (the table's mound, which no lap can reach), and the laps run",
  "clockwise from the carceres, six complete; the seventh is still being run. The ball is the leading chariot."],'2026-09-28')
sim('circus-maximus')
