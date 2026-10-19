"""Forty original detailed probes, five structurally different recipes per category.

Native integer grids, z up. No imported asset geometry. Seeded small variations
stay within semantic parts. Each recipe chooses its object-space design pitch;
auto-fit preview images do not establish common physical scale.
"""
import argparse, hashlib, json, math, pathlib, random
from voxel_recipes import Grid, PALETTE, vox_bytes
from master_recipes import cottage, van, ranger
from voxel_mesh import export_obj

# Extend the shared role palette once; OBJ and VOX use the same entries.
if len(PALETTE)==20:
    PALETTE.extend([(112,82,133,255),(188,140,177,255),(162,46,46,255),
                    (224,168,105,255),(101,164,177,255),(178,196,205,255),
                    (235,193,85,255),(95,120,117,255)])

def stamp(dst,src,dx=0,dy=0,dz=0,turn=0):
    for (x,y,z),c in src.cells.items():
        for _ in range(turn%4): x,y=-y,x
        dst.put(x+dx,y+dy,z+dz,c)
    return dst

def disk(g,cx,cy,z,r,thick,color):
    for x in range(math.floor(cx-r),math.ceil(cx+r)+1):
        for y in range(math.floor(cy-r),math.ceil(cy+r)+1):
            if (x-cx)**2+(y-cy)**2<=r*r:g.box(x,y,z,x+1,y+1,z+thick,color)

def cylinder(g,cx,cy,z0,z1,r,color):disk(g,cx,cy,z0,r,z1-z0,color)

def shell_house(w=48,d=38,h=28,roof=10):
    g=Grid();g.box(0,0,0,w,d,h,9);g.box(3,3,3,w-3,d-3,h,0)
    g.box(w//2-4,-1,2,w//2+5,4,21,0)
    for x in range(6,w-9,16):
        g.box(x,-1,11,x+9,1,23,1);g.box(x+1,-1,12,x+8,1,22,8)
        g.box(x+4,-2,12,x+5,0,22,18);g.box(x+1,-2,16,x+8,0,17,18)
    for y in range(7,d-8,15):g.box(-1,y,12,1,y+8,22,8)
    for y in range(-3,d+3):
        z=h+round((d/2-abs(y-(d-1)/2))*.8)
        g.box(-3,y,z,w+3,y+1,z+2,roof)
        if 0<=y<d:
            for x in (0,1,w-2,w-1):g.box(x,y,h,x+1,y+1,z,9)
    ridge=h+round((d/2-.5)*.8)+1
    g.box(-3,d//2-1,ridge,w+3,d//2+1,ridge+2,roof)
    return g

def fir(seed):
    r=random.Random(seed);g=Grid();h=72+r.randrange(3);g.box(-2,-2,0,3,3,h-5,1)
    for level,(base,length,radius) in enumerate([(10,28,23),(26,27,19),(43,24,14),(59,16,8)]):
        for z in range(base,base+length):
            rr=max(1,radius*(1-(z-base)/length))
            for x in range(-radius,radius+1):
                for y in range(-radius,radius+1):
                    if math.hypot(x,y)<=rr:g.put(x,y,z,3+level%3)
    for (x,y,z),c in list(g.cells.items()):
        if c in (3,4,5) and (x,y,z+1) not in g.cells and z>22 and (x//8+y//8)%3!=0:g.put(x,y,z,6)
    for a in range(0,360,60):
        t=math.radians(a);g.tube((0,0,3),(8*math.cos(t),8*math.sin(t),0),1.4,1)
    return g

def oak(seed):
    r=random.Random(seed);g=Grid();g.tube((0,0,0),(2,0,48),3.2,1)
    for i,a in enumerate(range(0,360,60)):
        t=math.radians(a);x,y=18*math.cos(t),18*math.sin(t);z=44+r.randrange(-3,4)
        g.tube((1,0,28),(x,y,z),2.1,2);g.ellipsoid(x,y,z,16,14,14,3+i%3)
    g.ellipsoid(0,0,57,17,16,14,4)
    for a in range(0,360,90):
        t=math.radians(a);g.tube((0,0,4),(10*math.cos(t),10*math.sin(t),0),2,1)
    return g

def willow(seed):
    g=Grid();g.tube((0,0,0),(3,1,44),2.7,1)
    for i,a in enumerate(range(0,360,45)):
        t=math.radians(a);x,y=17*math.cos(t),17*math.sin(t)
        g.tube((2,0,34),(x,y,47),1.6,2);g.ellipsoid(x,y,48,12,11,8,4+i%2)
        for j in (-5,0,5):
            xx=x+j*math.cos(t+math.pi/2);yy=y+j*math.sin(t+math.pi/2)
            g.tube((xx,yy,47),(xx*1.1,yy*1.1,18+(i+j)%5),1.2,3+i%3)
    return g

def palm(seed):
    g=Grid();g.tube((0,0,0),(5,0,57),2.4,1)
    for z in range(4,55,5):g.ellipsoid(z/12,0,z,2.8,2.8,1.2,2)
    for i,a in enumerate(range(0,360,45)):
        t=math.radians(a)
        for n in range(27):
            x=5+n*math.cos(t);y=n*math.sin(t);z=60+8*math.sin(n/26*math.pi)-n*.36
            g.ellipsoid(x,y,z,2.8,2.8,1.3,3+i%2)
    for x,y in ((2,-3),(8,-2),(4,4)):g.ellipsoid(x,y,55,3,3,3,2)
    return g

def mushroom(seed):
    g=Grid();g.tube((0,0,0),(1,0,31),4,18)
    # Domed cap with underside and a distinct rim, not a solid red sphere.
    for x in range(-23,24):
        for y in range(-23,24):
            d=math.hypot(x,y)
            if d<=22:
                z=31+round(13*math.sqrt(max(0,1-(d/22)**2)))
                g.box(x,y,29,x+1,y+1,32,23);g.box(x,y,z-3,x+1,y+1,z+1,22)
                if any((x-a)**2+(y-b)**2<13 for a,b in ((-9,-6),(8,8),(7,-10),(-10,12))):g.put(x,y,z,18)
    g.tube((1,0,5),(19,10,19),1.5,18);g.ellipsoid(19,10,23,9,8,4,22)
    return g

def chalet(seed):
    g=shell_house(58,42,32,1)
    for x in (0,18,38,56):g.box(x,-2,0,x+2,44,32,2)
    for z in (9,20,30):g.box(0,-2,z,58,1,z+2,2)
    g.box(0,-13,20,58,0,22,1)
    for x in range(0,59,5):g.box(x,-13,22,x+2,-11,29,2)
    g.box(0,-13,28,59,-11,30,2)
    for y in range(-3,45):
        z=32+round((21-abs(y-20.5))*.8)
        g.box(-4,y,z+2,62,y+1,z+3,6)
    return g

def watchtower(seed):
    g=Grid();g.box(0,0,0,32,32,57,14);g.box(4,4,3,28,28,57,0)
    g.box(12,-1,1,21,5,22,0)
    for z in (27,42):
        for x in (7,21):g.box(x,-1,z,x+4,5,z+9,0)
        g.box(-1,13,z,5,18,z+9,0)
    for z in range(6,56,8):g.box(-1,-1,z,33,33,z+1,15)
    g.box(-3,-3,55,35,35,59,14);g.box(1,1,56,31,31,60,0)
    for x in range(-3,35,7):
        for y in (-3,31):g.box(x,y,59,x+4,y+4,65,14)
    for y in range(4,31,7):
        for x in (-3,31):g.box(x,y,59,x+4,y+4,65,14)
    return g

def gatehouse(seed):
    g=Grid()
    stamp(g,watchtower(seed),-38,0);stamp(g,watchtower(seed+1),38,0)
    g.box(-7,6,23,39,25,42,14)
    # Semi-circular passage, separate ramp and open portcullis lattice.
    for x in range(-6,38):
        for z in range(23,43):
            if (x-15)**2+(z-23)**2<20**2:g.box(x,5,z,x+1,26,z+1,0)
    for x in range(-5,38,6):g.box(x,4,34,x+1,6,43,15)
    for z in (35,40):g.box(-5,4,z,39,6,z+1,15)
    g.box(-8,-8,0,40,3,2,14)
    return g

def pagoda(seed):
    g=Grid();g.box(-27,-24,0,28,25,4,14)
    for level,(w,d,h) in enumerate(((40,34,22),(32,28,18),(24,22,16))):
        base=4+level*25;g.box(-w//2,-d//2,base,w//2+1,d//2+1,base+h,9)
        for x in (-w//2,w//2-2):
            for y in (-d//2,d//2-2):g.box(x,y,base,x+3,y+3,base+h+6,22)
        for x in range(-w//2+5,w//2-3,8):g.box(x,-d//2-1,base+7,x+3,-d//2+1,base+16,8)
        for x in range(-w//2-7,w//2+8):
            for y in range(-d//2-7,d//2+8):
                e=max(abs(x)/(w/2+7),abs(y)/(d/2+7));z=base+h+round(7*(1-e)+4*max(0,(e-.8)/.2))
                g.box(x,y,z,x+1,y+1,z+2,3)
    g.box(-1,-1,73,2,2,91,13)
    return g

def person(role):
    g=ranger()
    if role=='ranger':return g
    g.box(4,1,57,24,21,65,0);g.box(9,18,31,20,24,47,0)
    if role=='knight':
        for p,c in list(g.cells.items()):
            if c in (1,2,3):g.cells[p]=14
        g.box(6,3,52,22,20,62,14);g.box(8,2,53,20,4,55,12)
        g.box(7,6,62,21,18,65,14);g.box(13,6,64,16,17,71,22)
        g.ellipsoid(0,8,36,2,10,13,7);g.box(-2,1,31,1,15,43,13)
        g.box(25,5,24,28,8,55,14);g.box(22,3,28,31,10,30,13)
    elif role=='north':
        for p,c in list(g.cells.items()):
            if c==3:g.cells[p]=1
        g.box(6,5,39,22,19,47,6);g.box(6,7,57,22,19,63,1)
        g.box(6,7,62,22,19,65,6);g.tube((25,9,29),(29,9,62),1.5,2)
        g.box(27,7,54,35,11,64,14)
        g.box(23,8,24,30,11,28,16)
    elif role=='mage':
        g.box(6,6,5,23,18,36,20);g.box(10,5,9,19,6,35,21)
        for z in range(58,76):
            rr=max(1,12-(z-58)*.65);disk(g,14,11,z,rr,1,20)
        g.box(1,0,57,27,23,59,20);g.tube((27,9,0),(27,9,70),1.3,1)
        g.ellipsoid(27,9,70,4,4,5,24)
    elif role=='farmer':
        g.box(6,5,29,22,7,43,7);g.box(10,4,29,18,7,40,7)
        g.box(3,0,57,26,22,59,26);g.box(8,5,58,21,18,65,26)
        g.tube((27,9,10),(27,9,70),1,2)
        for x in (23,27,31):g.box(x,8,64,x+1,10,74,14)
        g.box(23,8,63,32,10,65,14)
        g.box(23,8,24,29,11,28,16)
    return g

def animal(kind):
    g=Grid();spec={'fox':(8,34,12,17),'wolf':(10,41,15,15),'bear':(16,44,18,1),'deer':(9,37,22,2),'dragon':(13,48,16,3)}
    width,length,leg,color=spec[kind]
    g.ellipsoid(0,length/2,leg+8,width,length/2,10 if kind!='bear' else 14,color)
    for x in (-width+3,width-3):
        for y in (7,length-7):
            g.box(x-2,y-2,0,x+3,y+3,leg+9,color);g.box(x-2,y-2,0,x+3,y+3,3,12)
    headz=leg+14 if kind!='deer' else leg+27
    g.tube((0,4,leg+10),(0,-2,headz),5 if kind!='bear' else 8,color)
    g.ellipsoid(0,-4,headz,width*.85,9,7,color)
    g.ellipsoid(0,-11,headz-2,width*.62,7,4,18 if kind=='fox' else color)
    g.box(-2,-18,headz-4,3,-16,headz,12)
    for x in (-width//2,width//2):
        g.ellipsoid(x,-1,headz+7,2.5,2.5,4 if kind!='bear' else 2.5,color)
        g.box(x-1,-10,headz+2,x+1,-8,headz+4,12)
    if kind=='fox':
        g.tube((0,length-3,leg+9),(7,length+14,leg+16),4.5,17)
        g.ellipsoid(8,length+16,leg+17,5,6,4,18)
        g.ellipsoid(0,5,leg+4,5,10,6,18)
    elif kind=='wolf':g.tube((0,length-3,leg+7),(3,length+17,leg+3),3.5,15)
    elif kind=='bear':g.ellipsoid(0,length+2,leg+10,3,3,3,1)
    elif kind=='deer':
        for sign in (-1,1):
            g.tube((sign*4,-1,headz+5),(sign*9,3,headz+21),1.2,18)
            for n in (8,14):g.tube((sign*(4+n*.25),n*.2,headz+n),(sign*(13+n*.15),-5,headz+n+5),1,18)
        g.ellipsoid(0,length+2,leg+9,3,4,3,18)
    else:
        g.tube((0,length-3,leg+10),(0,length+34,leg+2),4,3)
        for y in range(8,length+25,7):
            top=max((z for (x,yy,z) in g.cells if abs(x)<=1 and yy==y),default=leg+3)
            g.box(-1,y,top,2,y+2,top+7,18)
        for sign in (-1,1):
            a=(sign*9,17,leg+16);b=(sign*37,9,leg+32);c=(sign*29,39,leg+23)
            g.tube(a,b,1.5,1);g.tube(a,c,1.5,1);g.tube(b,c,1.2,1)
            for u in range(21):
                for v in range(21-u):
                    t=u/20;s=v/20;p=[a[k]+t*(b[k]-a[k])+s*(c[k]-a[k]) for k in range(3)]
                    g.ellipsoid(*p,1,1,1,4)
            g.tube((sign*5,-1,headz+5),(sign*9,3,headz+17),1.6,18)
    return g

def car(kind):
    if kind=='blue-compact':return van()
    g=Grid();w=30
    if kind=='boat':
        for z in range(15):
            half=8+z//2;extent=42+z
            for y in range(-extent//2,extent//2+1):
                taper=max(2,half-int(abs(y)*.4))
                g.box(-taper,y,z,taper+1,y+1,z+1,1)
        g.box(-8,-16,6,9,17,16,0);g.box(-8,-16,5,9,17,7,2)
        g.box(-1,-1,7,2,2,61,1)
        for z in range(24,58):
            length=max(2,25-(z-24)//2);g.box(1,0,z,2,length,z+1,18)
        g.box(-17,-17,13,18,-15,15,2);g.box(-17,14,13,18,16,15,2)
        return g
    length={'pickup':66,'bus':87,'tractor':46}[kind]
    bodycolor={'pickup':22,'bus':26,'tractor':3}[kind]
    g.box(3,4,9,w-3,length-4,21,bodycolor);g.box(4,6,6,w-4,length-5,10,15)
    if kind=='pickup':
        g.box(5,17,20,25,38,37,22);g.box(6,20,22,24,36,35,0)
        g.box(5,17,25,25,19,34,8);g.box(4,21,24,6,35,34,8);g.box(24,21,24,26,35,34,8)
        g.box(5,41,13,25,length-7,23,0)
        for x in (3,25):g.box(x,40,20,x+2,length-5,23,15)
        g.box(3,length-7,20,27,length-5,23,15)
    elif kind=='bus':
        g.box(3,10,20,27,length-5,40,26);g.box(6,13,22,24,length-8,37,0)
        for y in range(16,length-13,14):
            g.box(2,y,25,4,y+10,36,8);g.box(26,y,25,28,y+10,36,8)
        g.box(5,9,25,25,12,37,8);g.box(3,12,21,27,length-6,24,18)
        g.box(20,11,10,27,20,36,8);g.box(23,11,10,24,20,36,15)
    else:
        g.box(8,4,18,22,22,29,3);g.box(6,27,20,24,42,40,3)
        g.box(8,28,24,22,40,38,0);g.box(6,27,28,24,29,38,8)
        g.box(5,26,39,25,43,41,3);g.box(19,10,27,21,12,42,15)
    for y,r in ((13,7),(length-13,11 if kind=='tractor' else 7)):
        for yy in range(y-r-1,y+r+2):
            for z in range(2*r+1):
                if (yy-y)**2+(z-r)**2<=(r+1)**2:
                    g.box(0,yy,z,7,yy+1,z+1,0);g.box(23,yy,z,30,yy+1,z+1,0)
        for x in (1,25):
            for yy in range(y-r,y+r+1):
                for z in range(2*r+1):
                    if (yy-y)**2+(z-r)**2<=r*r:g.box(x,yy,z,x+4,yy+1,z+1,12)
            g.ellipsoid(x+1.5,y,r,2,3 if r==7 else 5,3 if r==7 else 5,14)
        g.box(5,y-1,r-1,25,y+2,r+2,15)
    for x in (5,22):g.box(x,2,14,x+3,5,18,18)
    g.box(5,1,11,25,3,14,15)
    return g

def well(seed):
    g=Grid();cylinder(g,0,0,0,22,17,14);cylinder(g,0,0,2,24,12,0);disk(g,0,0,21,19,3,15)
    cylinder(g,0,0,20,25,12,0)
    g.box(-25,-4,0,25,5,3,14)
    for x in (-23,20):g.box(x,-2,0,x+3,3,64,1)
    g.tube((-24,0,37),(24,0,37),2.3,2)
    g.box(-5,-4,9,6,5,14,1);g.box(-3,-2,11,4,3,15,0);g.tube((0,0,35),(0,0,10),.8,2)
    for y in range(-19,20):
        z=53+round((19-abs(y))*.5);g.box(-29,y,z,30,y+1,z+2,10)
    return g

def guitar(seed):
    g=Grid();g.ellipsoid(0,0,18,15,4,18,2);g.ellipsoid(0,0,35,11,4,12,2)
    g.ellipsoid(0,-3,31,5,2,5,12);g.box(-3,-2,42,4,3,77,1)
    g.box(-5,-2,76,6,3,88,2);g.box(-8,-6,13,9,-4,16,1)
    for x in (-2,0,2):g.box(x,-5,15,x+1,-4,81,18)
    for z in range(48,76,5):g.box(-3,-4,z,4,-3,z+1,14)
    for z in (78,82,86):g.box(-7,-1,z,8,2,z+1,14)
    return g

def chest(seed):
    g=Grid();g.box(-26,-17,0,27,18,27,2);g.box(-23,-14,3,24,15,28,0)
    # Barrel-profile lid, visible slats, hinges and an explicit latch.
    for y in range(-18,19):
        z=27+round(11*math.sqrt(max(0,1-(y/19)**2)));g.box(-27,y,z,28,y+1,z+2,1 if y%5==0 else 2)
    for x in (-19,17):g.box(x,-18,1,x+3,19,28,14)
    g.box(-3,-19,18,4,-17,31,13);g.box(-1,-20,21,2,-18,23,12)
    for x in (-21,18):g.box(x,17,25,x+3,20,30,14)
    return g

def bookshelf(seed):
    g=Grid();g.box(0,0,0,54,16,61,1);g.box(3,-1,4,51,13,58,0)
    for z in (3,20,38,58):g.box(0,-2,z,54,17,z+3,2)
    r=random.Random(seed)
    for z in (6,23,41):
        x=4
        while x<48:
            w=r.randrange(3,6);h=r.randrange(10,16);c=r.choice((3,7,10,20,22))
            g.box(x,1,z,min(50,x+w),11,z+h,c);g.box(x,-1,z+2,min(50,x+w),1,z+3,13);x+=w+1
    return g

def vending(seed):
    g=Grid();g.box(0,0,0,40,25,66,7);g.box(3,-1,16,28,3,54,12)
    g.box(4,-2,16,6,1,54,14);g.box(26,-2,16,28,1,54,14)
    for z in (18,29,40):
        for x in (8,15,22):g.box(x,-1,z,x+4,2,z+7,(10,26,3)[(x//7)%3])
    g.box(32,-2,38,37,0,49,18);g.box(32,-3,34,37,1,36,12)
    for z in (23,27,31):g.box(33,-3,z,36,1,z+2,13)
    g.box(5,-2,4,28,2,12,12);g.box(5,-3,11,28,1,13,14)
    g.box(3,-2,57,37,0,63,18);g.box(10,-3,59,30,-1,61,7)
    return g

def terrain(kind):
    g=Grid();w=80;d=68
    for x in range(w):
        for y in range(d):
            if kind=='snow-mountain':h=3+round(48*max(0,1-math.hypot((x-42)/1.0,(y-36)/.78)/41));top=6 if h>29 else 14
            elif kind=='mesa':
                rr=((x-41)/29)**2+((y-32)/23)**2;h=5+(27 if rr<1 else 12 if rr<1.5 else 0);top=23
            elif kind=='river-gorge':
                center=35+8*math.sin(y/14);dist=abs(x-center);h=3 if dist<8 else 8+round(min(1,(dist-8)/18)*28);top=7 if dist<8 else 3
            elif kind=='island':
                rr=math.hypot((x-39), (y-33)*1.13);h=2+round(10*max(0,1-rr/32));top=7 if rr>32 else 23 if rr>25 else 4
            else:
                h=4;top=19
            for z in range(h):g.put(x,y,z,top if z==h-1 else (11 if kind=='mesa' and z%8<2 else 14 if z>9 else 2))
    if kind=='rock-arch':
        # Original tall arch on a rock bed; true negative space below the crown.
        for x in range(8,72):
            for z in range(4,59):
                r=math.hypot(x-40,z-25)
                if (abs(x-40)>22 and z<25) or (z>=25 and 23<r<32):g.box(x,25,z,x+1,39,z+1,14 if (z//9)%2 else 15)
    if kind=='river-gorge':
        g.box(31,7,3,44,10,28,24);g.box(32,6,26,43,9,29,18)
        for y in (13,35,56):
            x=21 if y!=35 else 56
            support=max(z for (xx,yy,z) in g.cells if xx==x and yy==y)
            g.ellipsoid(x,y,support+2,5,5,4,14)
    return g

def tent(w=30,d=28,h=25):
    g=Grid();g.box(0,0,0,w,d,1,1)
    for y in range(-2,d+2):
        z=2+round(h*(1-abs(y-(d-1)/2)/(d/2+2)))
        g.box(-1,y,z,w+1,y+1,z+3,18)
        if y in (0,d-1):g.box(0,y,1,w,y+1,z,18)
    for x in (0,w-1):g.box(x,d//2,1,x+1,d//2+1,h+3,1)
    g.box(-1,9,1,2,19,17,0);return g

def small_tree(h=35,r=10):
    g=Grid();g.box(-1,-1,0,2,2,h,1)
    for z in range(7,h):
        rr=max(1,r*(1-(z-7)/(h-7)))
        disk(g,0,0,z,rr,1,3 if z<h*.6 else 4)
    return g

def scene(kind,seed):
    g=Grid();w=120;d=104;g.box(0,0,0,w,d,3,2);g.box(0,0,3,w,d,4,4)
    if kind=='knight-camp':
        for x,y in ((8,9),(70,70)):stamp(g,tent(),x,y,4)
        g.box(0,45,3,120,59,4,23)
        for x,y in ((10,86),(103,15),(48,88)):stamp(g,small_tree(),x,y,4)
        disk(g,62,32,4,7,2,14);g.tube((57,30,6),(67,34,6),1,1)
        g.box(61,30,6,64,34,13,17);g.box(62,31,12,64,33,17,26)
        g.box(41,18,4,43,20,44,1);g.box(42,19,31,60,20,43,7);g.box(43,18,34,52,19,37,13)
    elif kind=='farmstead':
        stamp(g,shell_house(44,32,28),7,8,4)
        for x in range(65,111,10):
            g.box(x,9,4,x+5,60,5,2)
            for y in range(12,60,7):g.box(x+1,y,5,x+3,y+2,12,4);g.put(x+1,y,12,26)
        for x in range(5,115,9):g.box(x,78,4,x+2,80,13,1)
        for z in (7,11):g.box(5,78,z,115,80,z+1,2)
        g.box(0,64,3,120,74,4,23);stamp(g,small_tree(38,12),28,92,4)
    elif kind=='harbour':
        g.box(62,0,3,120,104,4,7);g.box(42,41,4,101,61,7,2)
        for x in range(44,99,7):g.box(x,41,7,x+1,61,8,1)
        for x,y in ((48,41),(89,58)):g.box(x,y,4,x+3,y+3,13,1)
        boat=car('boat');stamp(g,boat,94,77,4)
        stamp(g,shell_house(32,29,24),5,10,4);g.box(7,62,4,33,83,18,2)
        for x in (7,29):g.box(x,60,4,x+3,86,20,1)
    elif kind=='alpine-camp':
        g.box(0,0,3,120,104,4,6)
        stamp(g,tent(35,32,28),43,37,4)
        for x,y,h in ((16,20,46),(101,25,56),(97,87,40),(15,91,42)):stamp(g,small_tree(h,13),x,y,4)
        for x,y in ((19,58),(82,63),(48,87)):g.ellipsoid(x,y,7,8,6,5,14)
        g.box(55,0,3,70,36,4,23);g.box(57,69,3,72,104,4,23)
    else:
        g.box(0,0,3,120,104,4,23);stamp(g,shell_house(38,30,24,11),7,8,4)
        for x,y,c in ((64,8,22),(69,68,20),(9,72,7)):
            g.box(x,y,4,x+30,y+20,16,2)
            for xx in (x,x+27):
                for yy in (y,y+17):g.box(xx,yy,4,xx+2,yy+2,32,1)
            for yy in range(y-2,y+23):g.box(x-2,yy,31,x+33,yy+1,33,c if (yy//4)%2 else 18)
            for xx in range(x+3,x+26,7):g.ellipsoid(xx,y+4,18,3,3,3,26)
        g.box(0,47,3,120,59,4,18)
    return g

ROWS=[
 ('nature','fir','Заснеженная ель','Ярусная крона и связные пятна снега',fir),
 ('nature','oak','Ветвистый дуб','Каркас ветвей и перекрывающиеся массы кроны',oak),
 ('nature','willow','Плакучая ива','Радиальный каркас и ниспадающие пряди',willow),
 ('nature','palm','Пальма','Изогнутый ствол, кольца и дуги листьев',palm),
 ('nature','mushroom','Мухомор','Купол, пластинчатый низ и смысловая маска пятен',mushroom),
 ('architecture','cottage','Дом с рамами','Отдельные проёмы, крыша и дымоход',lambda s:cottage()),
 ('architecture','chalet','Альпийское шале','Каркас фасада, балкон и снег на крыше',chalet),
 ('architecture','watchtower','Сторожевая башня','Полая оболочка, бойницы и зубцы',watchtower),
 ('architecture','gatehouse','Надвратная крепость','Две башни и настоящий арочный проход',gatehouse),
 ('architecture','pagoda','Трёхъярусная пагода','Убывающие этажи и поднятые края крыш',pagoda),
 *[('characters',k,n,'Одна базовая фигура, новая одежда и объёмные признаки',lambda s,k=k:person(k)) for k,n in [('ranger','Следопыт'),('knight','Рыцарь со щитом'),('north','Житель Севера'),('mage','Маг с посохом'),('farmer','Фермер с вилами')]],
 *[('creatures',k,n,'Анатомические массы, контакт лап и характерные придатки',lambda s,k=k:animal(k)) for k,n in [('fox','Лиса'),('wolf','Волк'),('bear','Медведь'),('deer','Олень'),('dragon','Крылатый дракон')]],
 *[('transport',k,n,'Новая компоновка функциональных частей и отрицательные объёмы',lambda s,k=k:car(k)) for k,n in [('blue-compact','Синий компактный фургон'),('pickup','Пикап'),('bus','Городской автобус'),('tractor','Трактор'),('boat','Парусная лодка')]],
 ('props','well','Колодец','Полость, ворот и ведро на верёвке',well),
 ('props','guitar','Гитара','Два объёма корпуса, гриф и струны',guitar),
 ('props','chest','Сундук','Полый корпус и бочкообразная крышка',chest),
 ('props','bookshelf','Книжный шкаф','Повтор полок и ограниченный набор книг',bookshelf),
 ('props','vending','Торговый автомат','Витрина, кнопки и ниша выдачи',vending),
 *[('terrain',k,n,'Высотный профиль и явно заданная область поверхности',lambda s,k=k:terrain(k)) for k,n in [('snow-mountain','Снежная гора'),('mesa','Слоистое плато'),('river-gorge','Ущелье с водопадом'),('island','Песчаный остров'),('rock-arch','Скальная арка')]],
 *[('scenes',k,n,'Опора, маршрут, главный акцент и поддерживающие модули',lambda s,k=k:scene(k,s)) for k,n in [('knight-camp','Рыцарский лагерь'),('farmstead','Ферма с полями'),('harbour','Маленькая гавань'),('alpine-camp','Северный лагерь'),('desert-market','Пустынный рынок')]]
]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--category',choices=sorted({r[0] for r in ROWS})+['all'],default='all');ap.add_argument('--model',choices=[r[1] for r in ROWS]);ap.add_argument('--seed',type=int,default=53);ap.add_argument('--output',type=pathlib.Path,required=True);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True);out=[]
    for category,slug,title,principle,make in ROWS:
        if args.category!='all' and category!=args.category:continue
        if args.model and args.model!=slug:continue
        g=make(args.seed);size,cells=g.normalized();blob=vox_bytes(g);(args.output/(slug+'.vox')).write_bytes(blob);quads=export_obj(cells,args.output/(slug+'.obj'))
        out.append({'group':category,'slug':slug,'title':title,'principle':principle,'size':size,'occupied':len(cells),'greedyQuads':quads,'sha256':hashlib.sha256(blob).hexdigest(),'original':True})
    (args.output/'library-manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'models':len(out),'category':args.category},ensure_ascii=False))
if __name__=='__main__':main()
