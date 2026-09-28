import math, os, sys, subprocess
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sandlib, honest_proof, sandsim
COMPASS = math.pi / 2          # house compass: add +pi/2 so 'up' reads upright from the chair
SIG = "Plumb (Claude Opus 5.5)"

def finish(b, name, intent_lines, date, folio="Folio VIII (A Week of True Lines)"):
    """b: sandlib Builder authored in the chair frame. Writes out/<name>.thr with compass applied,
    plus chair-frame honest preview and sim render."""
    os.makedirs('out', exist_ok=True)
    tmp = f'out/.{name}-chair.thr'
    pts = b.write(tmp, name, SIG, intent_lines[0])
    final = f'out/{name}.thr'
    with open(final, 'w') as fh:
        fh.write(f"# {name}.thr  --  {SIG}, {date}\n")
        for l in intent_lines: fh.write(f"# {l}\n")
        fh.write(f"# one continuous line; rho<=0.97; {folio}; house compass applied (+pi/2)\n")
        fh.write(f"# geometry: {'true (compensated for the 19 mm rho-0 offset)' if b.true else 'machine'}\n")
        for t, r in pts: fh.write(f"{t + COMPASS:.6f} {r:.5f}\n")
    # previews in the chair frame
    hp = honest_proof.read_thr(tmp)
    a = honest_proof.draw(hp, honest=False); h = honest_proof.draw(hp, honest=True)
    out = Image.new('RGB', (a.size[0]*2+10, a.size[1]), (20,20,20)); out.paste(a,(0,0)); out.paste(h,(a.size[0]+10,0))
    out.save(f'out/{name}-preview.png')
    return final, tmp

def sim(name):
    final = f'out/{name}.thr'
    pts = sandsim.read_thr(final)
    f = sandsim.simulate(pts)
    img = sandsim.contact(pts, f)
    # rotate each panel back to the chair frame (file = chair + 90deg -> rotate image by -90? check)
    W = img.size[0]; s = (W - 20)//3
    panels = [img.crop((i*(s+10),0,i*(s+10)+s,s)).rotate(90) for i in range(3)]
    out = Image.new('RGB', img.size, (30,26,22))
    for i,p in enumerate(panels): out.paste(p,(i*(s+10),0))
    out.save(f'out/{name}-sim.png')
    r = subprocess.run([sys.executable,'thr_check.py',final],capture_output=True,text=True)
    print(r.stdout.strip())
    return out
