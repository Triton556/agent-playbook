"""Ten original Gen2 constructions. No downloaded cells or source geometry used.

Recipe coordinates are integer XYZ, z-up. Each chosen cavity/load sample is in
recipe coordinates, before Grid.normalized(). Shared palette IDs stay0..27.
"""
import math, random
import library_recipes  # registers the existing28-entry palette once
from voxel_recipes import Grid, PALETTE

def meta(g,method,evidence,cavities,core,detached=None):
    evidence=['medieval-fuzzyman-'+e if e.isdigit() else ('baseline-grid-'+e[8:]+'-0' if e.startswith('baseline') else e) for e in evidence]
    g.gen2_meta={'method':method,'evidence':evidence,'cavitySamples':cavities,'cavitysamplepoints':cavities,'loadcore':core,'intentionalDetached':detached or [],'sampleCoordinateSpace':'recipe coordinates before Grid.normalized()','provenance':'original analytic construction; no downloaded cells or geometry','qualityStatus':'Gen2 construction response; subjective improvement requires review'}
    return g

def disk(g,cx,cy,z,r,thick,c,inner=-1):
    for x in range(math.floor(cx-r),math.ceil(cx+r)+1):
        for y in range(math.floor(cy-r),math.ceil(cy+r)+1):
            rr=(x-cx)**2+(y-cy)**2
            if inner*inner<rr<=r*r or (inner<0 and rr<=r*r):g.box(x,y,z,x+1,y+1,z+thick,c)

def shell(g,x,y,z,w,d,h,t=3,c=18):
    g.box(x,y,z,x+w,y+d,z+h,c);g.box(x+t,y+t,z+t,x+w-t,y+d-t,z+h,0)

def grain(g,axis,phase=0,allowed=(1,2)):
    # Long low-frequency strips follow wood members, rather than cellwise noise.
    for p,c in list(g.cells.items()):
        if c not in allowed:continue
        a=p[axis];b=p[(axis+1)%3];d=p[(axis+2)%3]
        if (b+phase)%17 in (0,1) and (a+phase)%41<25:g.cells[p]=16 if c==2 else 2

def patch(g,axis,plane,a0,a1,b0,b1,c,erase=False):
    others=[i for i in range(3) if i!=axis]
    for a in range(a0,a1):
        for b in range(b0,b1):
            # A connected stepped patch with broad center and bounded uneven rim.
            if (a-a0)<1+(b-b0)//4 or a>a1-2-(b-b0)//5:continue
            p=[0,0,0];p[axis]=plane;p[others[0]]=a;p[others[1]]=b
            if tuple(p) in g.cells:g.put(*p,0 if erase else c)

def frame_front(g,x0,x1,y,z0,z1,c=1):
    g.box(x0-1,y,z0-1,x1+1,y+2,z0+1,c);g.box(x0-1,y,z1-1,x1+1,y+2,z1+1,c)
    g.box(x0-1,y,z0,x0+1,y+2,z1,c);g.box(x1-1,y,z0,x1+1,y+2,z1,c)

def pitched_roof(g,x0,x1,y0,y1,h,c=10,phase=0):
    mid=(y0+y1-1)/2
    for y in range(y0,y1):
        z=h+round((min(mid-y0,y1-1-mid)-abs(y-mid))*.78)
        # Paired tile courses have deliberate overlaps over a continuous shell.
        col=c if ((y-y0)//4+phase)%3 else (11 if c==10 else 2)
        g.box(x0,y,z,x1,y+1,z+3,col)
        if (y-y0)%4==0:g.box(x0,y,z+2,x1,y+1,z+4,col)
    ridge=h+round((min(mid-y0,y1-1-mid))*.78)+3
    g.box(x0,int(mid),ridge,x1,int(mid)+2,ridge+2,c)
    return ridge

def gable_fill(g,x0,x1,y0,y1,z0,h,c=18):
    mid=(y0+y1-1)/2
    for y in range(y0,y1):
        top=h+round((min(mid-y0,y1-1-mid)-abs(y-mid))*.78)
        if top>z0:
            g.box(x0,y,z0,x0+3,y+1,top,c);g.box(x1-3,y,z0,x1,y+1,top,c)

def cottage(seed):
    r=random.Random(seed);g=Grid();h=42+(seed%2)
    g.box(4,7,0,88,73,3,14);shell(g,9,14,3,72,52,h,3,18)
    # Timber frame defines a stable structure beneath the plaster skins.
    for x in (9,43,78):g.box(x,13,3,x+3,17,h+3,1)
    for y in (14,63):g.box(9,y,3,12,y+3,h+3,1);g.box(78,y,3,81,y+3,h+3,1)
    for z in (7,30,h+1):g.box(9,13,z,81,16,z+2,2)
    g.box(44,12,3,55,18,31,0)
    for x0,x1 in ((21,34),(63,75)):
        g.box(x0,12,18,x1,18,31,0);frame_front(g,x0,x1,12,18,31)
        g.box((x0+x1)//2,12,18,(x0+x1)//2+1,14,31,1)
    g.box(8,30,18,13,42,31,0)
    # One outward shutter leaves the left opening partly clear.
    g.box(15,7,18,19,10,31,2)
    for z in (20,28):g.box(18,9,z,22,14,z+2,15)
    g.box(39,3,1,60,14,3,14);g.box(42,7,3,57,15,5,14)
    gable_fill(g,9,81,14,66,h+3,h+5,18)
    ridge=pitched_roof(g,5,86,10,70,h+2,10,seed%3)
    # Deep flue grounded by an actual fireplace mass, not a floating roof block.
    g.box(66,48,3,76,58,ridge+12,14);g.box(69,51,13,73,55,ridge+14,0)
    g.box(65,47,5,73,51,16,0)
    g.box(65,47,4,76,59,6,15)
    g.box(65,47,ridge+10,77,59,ridge+13,15);g.box(69,51,ridge+10,73,55,ridge+14,0)
    # Local threshold/plaster ageing: one skin layer cut, core remains two cells.
    patch(g,1,14,14,27,8,17,9);patch(g,1,14,17,25,9,14,0,True)
    patch(g,1,65,55,67,7,17,19)
    for x in range(6+(seed%3),13):g.put(x,10,h+4,0)
    grain(g,2,seed%5)
    return meta(g,'half-timber shell, clear entrance/windows, thin tiled gable, grounded hollow fireplace; localized plaster skin loss',['003','119','132','baseline025'],[(49,15,18),(47,37,21),(71,53,ridge+8)],[(10,15,18),(79,64,18),(68,49,20)])

def chalet(seed):
    g=Grid();g.box(0,5,0,102,85,4,14);shell(g,13,25,4,75,52,51,3,2)
    # Floors, balcony and diagonal brackets are substantial geometry changes.
    g.box(16,28,31,85,74,34,1)
    g.box(10,8,31,92,26,34,1)
    for x in (12,84):
        g.box(x,9,4,x+4,14,34,1);g.tube((x+1,24,17),(x+1,9,32),1.5,1)
    for x in range(12,92,8):g.box(x,8,34,x+2,11,44,2)
    g.box(10,8,42,92,11,45,1)
    for z in (12,23,39,51):g.box(13,24,z,88,27,z+2,1)
    for z in range(9,55,6):g.box(16,76,z,85,77,z+1,1)
    for x in (13,37,64,85):g.box(x,24,4,x+3,28,55,1)
    g.box(43,23,4,54,30,29,0);g.box(43,23,34,54,30,55,0)
    for x0,x1 in ((21,32),(66,79)):
        g.box(x0,23,37,x1,30,50,0);frame_front(g,x0,x1,23,37,50,1)
    g.box(19,16-seed%3,51,34,25,53,1)
    # A complete climbable stepped side run meets the balcony floor at x14.
    for x in range(0,16):g.box(x,12,4,x+1,22,5+2*x,14)
    g.box(12,12,31,19,24,34,14)
    gable_fill(g,13,88,25,77,55,60,2)
    ridge=pitched_roof(g,7,95,19,83,55,1,seed%3)
    # Snow is one connected exposed roof patch with an intentionally melt-bare strip.
    for (x,y,z),c in list(g.cells.items()):
        if c in (1,2) and z>ridge-11 and (x,y,z+1) not in g.cells and 14<x<69 and 31<y<67:g.put(x,y,z,6)
    patch(g,1,25,17,31,7,16,1);grain(g,0,seed%7)
    return meta(g,'two-storey timber shell with internal floor, open upper/lower entry, supported balcony and genuine stair run',['177','279','283','baseline025'],[(49,26,18),(49,26,43),(50,46,44)],[(14,26,18),(13,10,22),(86,26,43)])

def watchtower(seed):
    g=Grid();cx=37;cy=37;g.box(2,2,0,73,73,4,14)
    for z in range(4,80):
        radius=26 if z<13 else (24 if z<48 else 23)
        for x in range(cx-radius,cx+radius+1):
            for y in range(cy-radius,cy+radius+1):
                rr=(x-cx)**2+(y-cy)**2
                if 17**2<rr<=radius**2:
                    angle=math.atan2(y-cy,x-cx);course=z//7;sector=int((angle+math.pi)*9/math.pi)+course%2
                    g.put(x,y,z,15 if z%7==0 or sector%5==0 else 14)
    g.box(30,9,4,45,23,29,0)
    for z in (35,53):
        g.box(58,34,z,65,41,z+8,0);g.box(34,58,z,41,65,z+8,0)
    g.box(9,35,42,24,40,51,0)
    # Buttresses and a supported lookout balcony, rather than added facade noise.
    for x,y in ((10,25),(58,44),(25,58)):
        g.box(x,y,4,x+6,y+9,35,14);g.box(x+1,y+1,35,x+5,y+8,43,14)
    g.box(24,2,57,51,16,60,1)
    for x in (26,47):g.tube((x,16,44),(x,4,58),1.8,1)
    g.box(24,2,68,51,4,71,1)
    for x in range(24,52,6):g.box(x,2,60,x+2,4,70,1)
    g.box(31,11,59,44,23,73,0)
    # Central column supports all24 wedge treads; adjacent3-cell-high rises touch.
    disk(g,cx,cy,4,3.5,73,14)
    for n in range(24):
        for x in range(cx-17,cx+18):
            for y in range(cy-17,cy+18):
                rr=(x-cx)**2+(y-cy)**2;angle=(math.atan2(y-cy,x-cx)+2*math.pi)%(2*math.pi)
                if 2**2<=rr<=17**2 and n*math.pi/12<=angle<(n+1)*math.pi/12:g.box(x,y,4+3*n,x+1,y+1,7+3*n,14)
    disk(g,cx,cy,76,23,3,14);g.box(28,24,75,38,32,80,0)
    disk(g,cx,cy,79,23,4,14,18)
    for a in range(0,360,45):
        t=math.radians(a);x=round(cx+21*math.cos(t));y=round(cy+21*math.sin(t));g.box(x-3,y-3,82,x+4,y+4,89,14)
    # Only outer top skin is chipped, leaving a several-cell annular support core.
    for z in range(86,89):
        for y in range(35+seed%2,39):g.put(61,y,z,0)
    return meta(g,'hollow tapering stone tower; central-post radial staircase, functional door, parapet and braced balcony',['183','184','190','baseline031'],[(37,14,17),(46,37,40),(32,28,78)],[(13,37,24),(37,37,40),(59,37,62)])

def gatehouse(seed):
    g=Grid();g.box(2,3,0,142,66,4,14)
    for x in (7,99):
        shell(g,x,17,4,36,39,65,4,14)
        for z in range(11,68,8):
            g.box(x,16,z,x+36,18,z+1,15);g.box(x-1,17,z,x+1,56,z+1,15)
        for xx in (x,x+31):g.box(xx,15,4,xx+5,21,69,9)
        doorx=x+12;g.box(doorx,15,4,doorx+11,23,29,0)
        g.box(x-2,15,67,x+38,58,70,14);g.box(x+3,22,69,x+33,51,72,0)
        for xx in range(x-2,x+38,8):
            for yy in (15,53):g.box(xx,yy,70,xx+5,yy+5,77,14)
    # True vaulted middle passage; upper bridge is a separate hollow chamber.
    g.box(43,17,4,99,56,65,14)
    for z in range(11,65,8):g.box(43,55,z,99,57,z+1,15)
    for x in range(47,96):
        xx=x-71;top=20+math.sqrt(max(0,23**2-xx**2)) if abs(xx)<=23 else 0
        if top:
            for z in range(4,int(top)+1):g.box(x,15,z,x+1,58,z+1,0)
    g.box(48,22,47,94,51,62,0)
    g.box(56,16,49,65,23,59,0);g.box(78,16,49,87,23,59,0)
    # Raised grille starts above the arch clearance, rooted into its top housing.
    g.box(46,12,62,97,19,66,15)
    for x in range(49,97,7):g.box(x,12,45,x+2,15,65,15)
    for z in (48,55,61):g.box(49,12,z,95,15,z+2,15)
    for x in range(45,100,9):
        g.box(x,17,65,x+5,22,72,14);g.box(x,52,65,x+5,57,72,14)
    # One oriel/service room makes the gate's two sides meaningfully different.
    shell(g,106,8,37,23,13,17,2,2);g.box(110,7,41,125,11,52,0)
    g.box(105,7,53,130,22,56,10)
    g.box(109,5,41,111+seed%3,10,51,2)
    for x in (108,125):g.tube((x,18,27),(x,9,38),1.5,1)
    patch(g,1,17,82,95,6,19,15);patch(g,1,17,84,91,8,14,0,True)
    return meta(g,'two hollow towers joined by real arch passage and hollow upper bridge; raised lattice, one braced service oriel',['121','132','184','273'],[(71,31,22),(71,35,53),(23,37,30),(117,14,46)],[(8,21,35),(136-4,40,30),(46,40,45)])

def pagoda(seed):
    g=Grid();g.box(2,2,0,86,86,4,14);g.box(8,8,4,80,80,8,14)
    # Persistent posts form a load path through three differently sized chambers.
    for x in (30,55):
        for y in (30,55):g.box(x,y,8,x+3,y+3,96,22)
    for level,(lo,hi,base,h) in enumerate(((17,71,8,25),(25,63,44,22),(31,57,75,18))):
        shell(g,lo,lo,base,hi-lo,hi-lo,h,3,18)
        for x in (lo,hi-3):
            for y in (lo,hi-3):g.box(x,y,base,x+3,y+3,base+h+4,22)
        g.box(38,lo-1,base+3,50,lo+4,base+h-2,0)
        if level==0:
            for x in (23,57):g.box(x,lo-1,base+11,x+8,lo+4,base+h-4,0)
        outer=(hi-lo)/2+8;cx=(lo+hi-1)/2
        for x in range(lo-8,hi+8):
            for y in range(lo-8,hi+8):
                e=max(abs(x-cx),abs(y-cx))/outer
                z=base+h+round(10*(1-e)+(5+seed%3)*max(0,(e-.78)/.22)**2)
                col=3 if (max(abs(x-44),abs(y-44))//4+seed%3)%3 else 4
                g.box(x,y,z,x+1,y+1,z+3,col)
        # Continuous beams tie posts to the broad roof shell.
        g.box(lo,lo,base+h,hi,lo+3,base+h+4,1);g.box(lo,hi-3,base+h,hi,hi,base+h+4,1)
    for x in range(10,81,10):
        g.box(x,8,8,x+2,11,18,22);g.box(x,77,8,x+2,80,18,22)
    g.box(9,8,17,80,11,19,22);g.box(9,77,17,80,80,19,22)
    # Leave a conspicuous aligned entrance through the veranda railing.
    g.box(37,7,8,51,12,20,0)
    g.box(38,0,0,50,9,2,14);g.box(38,3,2,50,9,5,14)
    g.box(42,42,101,46,46,113,13)
    g.box(51,13,11,60,16,31,2)
    for z in (14,27):g.box(51,15,z,54,18,z+2,15)
    patch(g,1,17,20,28,12,22,9);patch(g,1,17,22,26,13,18,0,True)
    # Restore continuous structural columns after subtracting all room interiors.
    for x in (30,55):
        for y in (30,55):g.box(x,y,8,x+3,y+3,96,22)
    return meta(g,'three real chambers around persistent timber columns, continuous curved hip-roof shells, clear veranda/door axis',['132','177','baseline031'],[(44,19,20),(44,44,20),(44,44,56),(44,44,85)],[(31,31,26),(56,56,60),(18,18,22)])

def well(seed):
    g=Grid();cx=44;cy=43
    disk(g,cx,cy,0,34,5,14,21)
    for z in range(5,34):
        for x in range(14,75):
            for y in range(13,74):
                rr=(x-cx)**2+(y-cy)**2
                if 23**2<rr<=30**2:
                    a=math.atan2(y-cy,x-cx);sector=int((a+math.pi)*8/math.pi)+(z//6)%2
                    g.put(x,y,z,15 if z%6==0 or sector%6==0 else 14)
    disk(g,cx,cy,5,23,1,7)
    for x in (11,72):g.box(x,38,3,x+5,48,82,1)
    g.box(11,37,78,77,49,84,1)
    g.box(15,40,61,73,46,67,2)
    # Timber kingposts/triangular rafters give the roof a real connected support.
    for x in (13,74):
        g.box(x,41,82,x+3,45,102,1)
        g.tube((x+1,17,86),(x+1,43,102),1.5,1);g.tube((x+1,43,102),(x+1,69,86),1.5,1)
    pitched_roof(g,5,83,13,74,83,10,seed%3)
    # Hollow hanging bucket and an attached handle/rope, clear air around them.
    disk(g,cx,cy,13,6,2,15)
    disk(g,cx,cy,15,6,11,15,4)
    g.box(38,42,25,51,44,27,15);g.box(38,42,22,40,44,27,15);g.box(49,42,22,51,44,27,15)
    g.box(44,43,26,45,44,62,16)
    # Crank on the right side: a deliberately asymmetric readable mechanism.
    g.box(76,40,62,84,44,66,15);g.box(81,40,57,84,44,66,15);g.box(82,40,57,88,44,60,2)
    for z in range(31,34):
        for x in range(21+seed%2,27):g.put(x,25,z,0)
    grain(g,0,seed%5)
    return meta(g,'open annular well, real water/bucket separation, timber posts/trusses, supported windlass and rope; outer rim chips only',['040','253','255','286'],[(54,43,20),(44,43,19),(46,43,47)],[(15,42,30),(73,42,70),(18,43,15)])

def guitar(seed):
    g=Grid();cx=33;mask=set()
    for x in range(6,61):
        for y in range(5,73):
            if ((x-cx)/25)**2+((y-27)/22)**2<=1 or ((x-cx)/18)**2+((y-54)/18)**2<=1:mask.add((x,y))
    inner={(x,y) for x,y in mask if all((x+dx,y+dy) in mask for dx,dy in ((2,0),(-2,0),(0,2),(0,-2)))}
    for x,y in mask:
        g.box(x,y,1,x+1,y+1,15,11)
        if (x,y) in inner:g.box(x,y,4,x+1,y+1,12,0)
        g.put(x,y,14,16)
    # Real acoustic cavity; top sound opening, not a painted black disk.
    for x in range(23,44):
        for y in range(35,56):
            rr=(x-cx)**2+(y-45)**2
            if rr<=9**2:
                g.box(x,y,11,x+1,y+1,16,0)
                if (x,y) in inner:g.put(x,y,3,1)  # darker interior lining, still below the cavity
            elif rr<=10**2 and (x,y) in mask:g.put(x,y,14,1)
    for y in (20,57):g.box(18,y,10,49,y+2,12,1)
    g.box(29,64,9,38,105,13,1);g.box(28,65,13,39,103,15,1)
    for y in range(67,101,5):g.box(28,y,15,39,y+1,16,14)
    g.box(27,102,10,40,118,14,2)
    for y in (106,112,116):
        g.box(24,y,11,29,y+2,14,15);g.box(38,y,11,43,y+2,14,15)
    g.box(24-seed%3,106,11,29,108,14,15)
    g.box(24,22,14,43,27,17,1)
    for x in (28,30,32,34,36,38):g.box(x,24,15,x+1,115,16,18)
    # Continuous rim/binding and one coherent shoulder abrasion.
    for x,y in mask:
        if any((x+dx,y+dy) not in mask for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):g.put(x,y,14,18)
    patch(g,2,14,13+seed%3,24,27,37,23)
    return meta(g,'hollow waisted acoustic body, top sound hole, internal braces, actual thin neck/frets/strings and tuning pegs',['baseline044','239'],[(33,30,7),(33,43,8),(35,43,13)],[(8,27,6),(33,68,11),(33,24,14)])

def chest(seed):
    g=Grid();shell(g,8,8,4,64,42,29,4,2)
    for x in (8,65):
        for y in (8,43):g.box(x,y,0,x+7,y+7,6,1)
    for z in (8,18,28):g.box(8,7,z,72,9,z+2,1)
    for x in (9,24,53,69):g.box(x,7,4,x+2,10,33,15)
    g.box(8,8,30,72,50,33,1);g.box(12,12,30,68,46,34,0)
    # Open lid is a connected inclined barrel-cambered board shell, not a second box.
    for z in range(32,69):
        for x in range(8,72):
            camber=round(3*(1-(abs(x-39.5)/31.5)**2));y=47+round((z-32)*(.32+.03*(seed%3)))+camber
            g.box(x,y,z,x+1,y+3,z+1,2 if ((x-8)//8+seed%3)%3 else 16)
            if x in (8,9,69,70,71):g.box(x,y-1,z,x+1,y+4,z+1,15)
    for x in (15,61):g.box(x,45,28,x+5,53,35,15)
    # Thick front loop with a real grip gap, attached at both sides.
    g.box(29,3,15,49,9,24,15);g.box(33,2,18,45,6,22,0)
    patch(g,1,8,16+seed%3,27,10,20,16);grain(g,0,seed%7)
    return meta(g,'four-foot hollow plank chest, open connected cambered lid, independent rim/frame and real front handle gap',['296','285','009'],[(39,27,18),(39,4,19)],[(9,9,9),(69,48,12),(17,48,31)])

def bookshelf(seed):
    g=Grid();g.box(4,4,0,82,33,4,1);g.box(7,28,4,79,31,91,1)
    for x in (7,75):g.box(x,6,4,x+4,31,92,2)
    for z in (8,30,52,74,92):g.box(7,6,z,79,31,z+3,2)
    # Book groups leave a deliberate empty bay, with bounded height/lean differences.
    colors=(10,7,3,20,22,16)
    for level,zbase in enumerate((11,33,55,77)):
        for j,x0 in enumerate((12,19,27,54,61,69)):
            width=5+(j%2);height=14+(j+level+seed)%5;lean=(-2 if j==2 else (2 if j==3 else 0))
            col=colors[(j+level+seed)%len(colors)]
            for k in range(height):
                dx=round(lean*k/max(1,height-1));x=x0+dx
                g.box(x,9,zbase+k,x+width,25,zbase+k+1,18)
                g.box(x,8,zbase+k,x+width,10,zbase+k+1,col)
                g.box(x,9,zbase+k,x+1,25,zbase+k+1,col);g.box(x+width-1,9,zbase+k,x+width,25,zbase+k+1,col)
            g.box(x0,8,zbase,x0+width,25,zbase+1,col)
    # Lower shelf's offset paper pile adds one recognizable use-state.
    for n in range(4):g.box(37+n%2,12,11+n*2,49+n%2,25,13+n*2,18)
    g.box(36,11,10,51,26,11,10)
    patch(g,2,54,8,25,7,18,16);grain(g,0,seed%5)
    return meta(g,'continuous backed shelf/post skeleton, genuinely open bays, thick covers/pages/spines and deliberate leaned book groups',['257','259','baseline038'],[(44,18,44),(44,18,65),(44,18,85)],[(8,15,41),(76,15,41),(12,29,41)])

def vending(seed):
    g=Grid();g.box(7,9,0,76,48,4,15);shell(g,11,13,4,61,31,87,3,22)
    # Recessed stock display and clear delivery mouth in the thick front shell.
    g.box(16,10,20,54,18,81,0);g.box(22,10,6,49,33,17,0)
    for x in (15,53):g.box(x,11,19,x+2,16,83,15)
    for z in (18,81):g.box(15,11,z,55,16,z+2,15)
    g.box(56,10,21,69,14,82,14)
    for z in (28,38,48,58):g.box(59,8,z,66,11,z+4,13)
    g.box(59,8,71,66,11,78,8);g.box(59,8,70,66,9,71,18)
    for row,zbase in enumerate((23,42,61)):
        g.box(16,16,zbase-2,54,35,zbase,15)
        for j,x in enumerate((22,34,46)):
            if row==1 and j==seed%3:continue  # one sold stock slot, not random holes
            col=(7,3,13)[(j+row)%3]
            disk(g,x,23,zbase,3,10,col);disk(g,x,23,zbase+10,1.6,4,col)
            disk(g,x,23,zbase+14,2,1,15)
            g.box(x-2,19,zbase+4,x+3,21,zbase+7,18)
    # Display header, metal threshold and backside service hatch are real depth.
    g.box(15,10,83,69,15,89,18)
    g.box(10,12,90,73,45,93,15)
    for x in range(21,64,7):g.box(x,9,85,x+4,11,87,7)
    g.box(22,10,5,49,15,7,15);g.box(22,10,17,49,16,19,15)
    g.box(16,44,13,67,46,75,15);g.box(19,45,16,64,47,72,27)
    for x in (17,64):
        for z in (16,69):g.box(x,46,z,x+2,48,z+2,15)
    patch(g,1,13,63,71,5,19,11);patch(g,1,13,65,69,7,13,0,True)
    return meta(g,'hollow cabinet with open recessed three-row stock display, one sold slot, separate controls and clear delivery/service cavities',['baseline080','145','119'],[(35,19,10),(39,37,43),(35,13,30)],[(12,14,48),(70,42,48),(60,12,36)])

ROWS=[
 ('architecture','cottage','Дом с фахверком','Полый каркас, открытые проёмы и локальный износ штукатурки',cottage),
 ('architecture','chalet','Шале с балконом','Два этажа, опоры балкона и настоящая лестница',chalet),
 ('architecture','watchtower','Сторожевая башня','Полая башня с центральной опорой винтовой лестницы',watchtower),
 ('architecture','gatehouse','Надвратная крепость','Свободный сводчатый проход и поднятая решётка',gatehouse),
 ('architecture','pagoda','Пагода','Три полые камеры и несущий каркас под изогнутыми кровлями',pagoda),
 ('props','well','Колодец','Открытая шахта, подвешенное ведро и настоящий каркас крыши',well),
 ('props','guitar','Акустическая гитара','Полый корпус, звуковое отверстие, струны и лады',guitar),
 ('props','chest','Открытый сундук','Полость, соединённая откинутая крышка и сквозная ручка',chest),
 ('props','bookshelf','Книжный стеллаж','Слои книг, наклонённые группы и свободные полки',bookshelf),
 ('props','vending','Торговый автомат','Полый корпус, глубина витрины, проданный слот и выдача',vending),
]
