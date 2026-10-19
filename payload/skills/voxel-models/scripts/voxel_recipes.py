"""Original procedural voxel specimens. No downloaded geometry is used.

Coordinates: x right, y depth, z up; integer cells. Seed controls bounded shape
variation. Helpers can be reused for an original asset; these recipes are examples.
"""
import argparse,hashlib,json,math,pathlib,random,struct

PALETTE=[(0,0,0,0),(74,48,34,255),(104,73,48,255),(39,77,57,255),(58,105,69,255),
 (88,131,83,255),(220,231,220,255),(54,108,156,255),(32,68,91,255),(188,189,166,255),
 (119,56,41,255),(173,91,56,255),(33,39,41,255),(225,178,82,255),(129,144,148,255),
 (76,87,94,255),(198,155,112,255),(205,115,52,255),(239,226,196,255),(96,104,83,255)]

class Grid:
    def __init__(self): self.cells={}
    def put(self,x,y,z,c):
        if c: self.cells[(int(x),int(y),int(z))]=c
        else: self.cells.pop((int(x),int(y),int(z)),None)
    def box(self,x0,y0,z0,x1,y1,z1,c):
        for x in range(int(x0),int(x1)):
            for y in range(int(y0),int(y1)):
                for z in range(int(z0),int(z1)): self.put(x,y,z,c)
    def ellipsoid(self,cx,cy,cz,rx,ry,rz,c):
        for x in range(math.floor(cx-rx),math.ceil(cx+rx)+1):
            for y in range(math.floor(cy-ry),math.ceil(cy+ry)+1):
                for z in range(math.floor(cz-rz),math.ceil(cz+rz)+1):
                    if ((x-cx)/rx)**2+((y-cy)/ry)**2+((z-cz)/rz)**2<=1: self.put(x,y,z,c)
    def tube(self,a,b,r,c):
        steps=math.ceil(max(abs(b[i]-a[i]) for i in range(3))*2)+1
        for t in range(steps+1):
            pos=[a[i]+(b[i]-a[i])*t/steps for i in range(3)]
            self.ellipsoid(*pos,r,r,r,c)
    def normalized(self):
        mins=[min(k[a] for k in self.cells) for a in range(3)]
        cells={(x-mins[0],y-mins[1],z-mins[2]):c for (x,y,z),c in self.cells.items()}
        size=[max(k[a] for k in cells)+1 for a in range(3)]
        if max(size)>256: raise ValueError('single VOX model exceeds 256 cells per axis')
        return size,cells

def conifer(rng):
    g=Grid(); h=rng.randrange(30,40); radius=rng.randrange(9,13)
    g.box(-1,-1,0,2,2,h-3,1)
    for level,(base,length,scale) in enumerate([(7,15,1),(15,14,.8),(23,h-23,.56)]):
        for z in range(base,base+length):
            rr=max(.9,radius*scale*(1-(z-base)/length))
            for x in range(-radius,radius+1):
                for y in range(-radius,radius+1):
                    d=math.hypot(x,y)
                    if d<=rr and (d<rr-.8 or (x*13+y*7+z)%7!=0):
                        g.put(x,y,z,3+level%3)
    # Authored snow on upward exposed canopy; color-only variation is separate.
    for (x,y,z),c in list(g.cells.items()):
        if c in (3,4,5) and (x,y,z+1) not in g.cells and z>12 and (x//6+y//5+z//4)%3!=0: g.put(x,y,z,6)
    return g

def broadleaf(rng):
    g=Grid(); h=rng.randrange(16,22); span=rng.randrange(9,13)
    g.box(-1,-1,0,2,2,h+6,1)
    for i,(a,b) in enumerate([(-1,-1),(1,-1),(-1,1),(1,1)]):
        x=a*span*.55; y=b*span*.55; z=h+rng.randrange(-2,4)
        g.tube((0,0,h-3),(x,y,z),1,2)
        g.ellipsoid(x,y,z,span*.67,span*.67,span*.57,3+i%3)
    return g

def cottage(rng):
    g=Grid(); w=rng.randrange(22,29); depth=20; h=rng.randrange(16,20)
    g.box(0,0,0,w,depth,h,9); g.box(2,2,2,w-2,depth-2,h,0)
    # Open door; windows remain glazing cells and can be swapped with holes.
    g.box(w//2-2,0,1,w//2+2,2,10,0)
    for x in (3,w-7):
        g.box(x,-1,7,x+4,1,12,1);g.box(x+1,-1,8,x+3,1,11,8)
    for y in (4,12): g.box(-1,y,7,1,y+4,11,8)
    for z in range(h,h+depth//2+2):
        inset=z-h; g.box(-2,inset-2,z,w+2,depth-inset+2,z+1,10 if inset%3 else 11)
    g.box(w-7,depth-7,h+2,w-4,depth-4,h+13,14)
    g.box(w-6,depth-6,h+10,w-5,depth-5,h+13,0)
    return g

def van(rng):
    g=Grid(); length=rng.randrange(28,34); w=14; cabin=rng.randrange(13,17)
    g.box(1,2,3,w-1,length-2,10,7)
    g.box(2,8,10,w-2,length-4,cabin,7)
    g.box(3,8,10,w-3,9,cabin-1,8)
    for x in (1,w-2):
        g.box(x,11,10,x+1,length-7,cabin-2,8)
        for y in (7,length-8):
            for yy in range(y-3,y+4):
                for z in range(0,7):
                    if (yy-y)**2+(z-3)**2<=10: g.box(x-1,yy,z,x+2,yy+1,z+1,12)
            g.box(x-1,y-1,2,x+2,y+2,5,14)
    g.box(1,0,5,w-1,2,7,15)
    for x in (2,w-4): g.box(x,0,7,x+2,2,9,18);g.box(x,length-2,6,x+2,length,9,10)
    return g

def ranger(rng):
    g=Grid(); leg=rng.randrange(8,11); torso=9; neck=leg+torso; head=7
    g.box(-3,-2,leg,4,3,neck,3)
    for x in (-3,1): g.box(x,-1,1,x+3,3,leg+1,15);g.box(x,-3,0,x+3,3,2,12)
    for x in (-5,4): g.box(x,-1,leg+1,x+2,3,neck-1,3);g.box(x,-1,leg,x+2,2,leg+3,16)
    g.box(-3,-3,neck,4,4,neck+head,16)
    g.box(-4,-4,neck+head-1,5,5,neck+head+1,2)
    g.box(-2,-2,neck+head,3,3,neck+head+3,2)
    for x in (-1,2): g.put(x,-3,neck+4,12)
    g.box(-3,3,leg+3,4,5,neck-1,1) # backpack is silhouette variation
    g.box(-3,-3,leg+3,4,-2,leg+5,13) # belt is surface/semantic accent
    return g

def fox(rng):
    g=Grid(); body=rng.randrange(13,18)
    g.ellipsoid(0,body/2,7,4.5,body/2,4,17)
    for x in (-3,3):
        for y in (3,body-3): g.box(x-1,y-1,0,x+1,y+2,7,17);g.box(x-1,y-1,0,x+1,y+2,2,12)
    g.ellipsoid(0,-1,11,4,5,4,17)
    g.ellipsoid(0,-5,10,3,3,2,18);g.box(-1,-8,9,2,-6,11,12)
    for x in (-3,2):
        g.box(x,-1,13,x+2,2,17,17);g.put(x,-1,16,12)
        g.put(x,-4,12,12)
    g.tube((0,body-1,8),(0,body+7,12),2.5,17)
    g.ellipsoid(0,body+8,12,3,4,3,18)
    return g

def crate(rng):
    g=Grid(); w=rng.randrange(16,23); d=16; h=14
    g.box(0,0,0,w,d,h,2);g.box(2,2,2,w-2,d-2,h+1,0)
    for z in (0,5,10):
        g.box(0,0,z,w,1,z+1,1);g.box(0,d-1,z,w,d,z+1,1)
    for x in (0,w-2):g.box(x,-1,0,x+2,d+1,h,1)
    g.box(w//2-1,-1,5,w//2+2,1,8,13)
    return g

def arch(rng):
    g=Grid(); r=rng.randrange(9,13); thick=4; base=12
    for x in range(-r-thick,r+thick+1):
        for z in range(base+r+thick+1):
            is_pillar=abs(x)>=r and z<base
            is_ring=z>=base and r<=math.hypot(x,z-base)<r+thick
            if is_pillar or is_ring:
                for y in range(5):g.put(x,y,z,14 if (x+z//3)%4 else 15)
    return g

RECIPES={f.__name__:f for f in (conifer,broadleaf,cottage,van,ranger,fox,crate,arch)}

def chunk(name,payload): return name+struct.pack('<II',len(payload),0)+payload
def vox_bytes(g):
    size,cells=g.normalized(); data=bytes(v for coord,c in sorted(cells.items()) for v in (*coord,c))
    palette=(PALETTE+[(0,0,0,255)]*(256-len(PALETTE)))
    # RGBA entries 0..254 map to indices1..255. Index0 remains air.
    rgba=b''.join(bytes(c) for c in palette[1:])+bytes(palette[0])
    children=chunk(b'SIZE',struct.pack('<III',*size))+chunk(b'XYZI',struct.pack('<I',len(cells))+data)+chunk(b'RGBA',rgba)
    return b'VOX '+struct.pack('<I',150)+b'MAIN'+struct.pack('<II',0,len(children))+children

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--family',choices=list(RECIPES)+['all'],default='all');ap.add_argument('--seed',type=int,default=13);ap.add_argument('--output',type=pathlib.Path,required=True)
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True); entries=[]
    for family in RECIPES if args.family=='all' else [args.family]:
        g=RECIPES[family](random.Random(args.seed));blob=vox_bytes(g)
        p=args.output/f'{family}-seed{args.seed}.vox';p.write_bytes(blob)
        size,cells=g.normalized(); entries.append({'family':family,'seed':args.seed,'path':p.name,'size':size,'occupied':len(cells),'usedColorCount':len(set(cells.values())),'sha256':hashlib.sha256(blob).hexdigest(),'provenance':'original procedural specimen; no downloaded grid or source geometry'})
    (args.output/f'manifest-seed{args.seed}.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf8'); print(json.dumps(entries,ensure_ascii=False))
if __name__=='__main__':main()
