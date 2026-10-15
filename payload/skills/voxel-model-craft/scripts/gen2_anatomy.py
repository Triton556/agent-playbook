"""Ten original detailed Gen2 animal/character constructions.

All occupied cells are authored below. No downloaded source grid is loaded.
Static pose evidence only; no rig, gait or physical stability claim.
Call make(seed) with tools/ on sys.path. Palette entries remain0..27.
"""
import math, random
import library_recipes  # initializes the project's existing28-color palette once
from voxel_recipes import Grid, PALETTE

EVIDENCE={
 'quadruped':'research/gen2/anatomy/reusable-constraints.md: beagle/oryx/dragon front-side-ground sections; distinct joint profiles and wider oriented feet',
 'support':'research/gen2/anatomy/anatomy-measurements.json: contact islands are not limb counts; use semantic foot regions',
 'character':'research/gen2/anatomy/reusable-constraints.md: cloak/hat bounds and prop contacts must not replace body landmarks',
}

def segment(g,a,b,r0,r1,c):
    """Union of tapered spherical cross-sections around an authored limb axis."""
    v=[b[i]-a[i] for i in range(3)]; vv=sum(q*q for q in v); r=max(r0,r1)
    bounds=[range(math.floor(min(a[i],b[i])-r),math.ceil(max(a[i],b[i])+r)+1) for i in range(3)]
    for x in bounds[0]:
        for y in bounds[1]:
            for z in bounds[2]:
                p=(x,y,z);t=max(0,min(1,sum((p[i]-a[i])*v[i] for i in range(3))/vv)) if vv else 0
                rr=r0+(r1-r0)*t
                if sum((p[i]-a[i]-t*v[i])**2 for i in range(3))<=rr*rr:g.put(x,y,z,c)

def chain(g,points,radii,c):
    for i in range(len(points)-1):segment(g,points[i],points[i+1],radii[i],radii[i+1],c)

def triangle(g,a,b,c,color):
    n=math.ceil(max(math.dist(a,b),math.dist(a,c),math.dist(b,c))*1.5)
    for i in range(n+1):
        for j in range(n-i+1):
            u=i/n;v=j/n; p=[round(a[k]+u*(b[k]-a[k])+v*(c[k]-a[k])) for k in range(3)]
            g.box(*p,p[0]+2,p[1]+2,p[2]+2,color)

def pad(g,id,cx,cy,rx,ry,h,c,hoof=False):
    """A flat continuous planted sole; upper hoof cleft does not split contact."""
    points=[]
    for x in range(math.floor(cx-rx),math.ceil(cx+rx)+1):
        for y in range(math.floor(cy-ry),math.ceil(cy+ry)+1):
            if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1:
                for z in range(h):g.put(x,y,z,c);points.append((x,y,z))
    # Slightly smaller upper toe/hoof cap, clear ankle-to-sole transition.
    g.ellipsoid(cx,cy+.5,h-1,rx*.86,ry*.78,max(1.4,h*.65),c)
    if hoof:g.box(round(cx),math.floor(cy-ry),1,round(cx)+1,math.floor(cy-ry)+2,h+1,12)
    return {'id':id,'bounds':[[min(p[k] for p in points),max(p[k] for p in points)] for k in range(3)],'soleZ':0,'soleCells':sum(p[2]==0 for p in points),'toeDirection':'-y','role':'planted hoof' if hoof else'planted flat foot'}

def finish(g,family,feet,landmarks,method):
    for p in list(g.cells):
        if p[2]<0:g.cells.pop(p)
    mins=[min(p[k] for p in g.cells) for k in range(3)]
    landmarks={id:{name:list(p) for name,p in values.items()} for id,values in landmarks.items()}
    size,_=g.normalized()
    if max(size)>160:raise ValueError((family,'Gen2 axis exceeds160',size))
    if any(c<1 or c>27 for c in g.cells.values()) or len(PALETTE)!=28:raise ValueError('existing palette IDs only')
    g.gen2_meta={'family':family,'facingAxis':'-y','coordinateSpace':'authored grid cell coordinates before Grid.normalized','plantedFeet':feet,'jointLandmarks':landmarks,'method':method,'sourceEvidence':EVIDENCE,'intentionalDetached':[],'pose':'authored static planted stance; animation and physical stability untested','originalGeometry':True,'normalizationOffset':mins}
    return g

def animal_legs(g,body,kind,coat,distal,rx=4,ry=7,h=4):
    """Fore chain drops below chest; rear chain folds knee forward/hock back."""
    feet=[];joints={};rootz,front,rear,spread=body
    for side in(-1,1):
        points=[(side*spread,front,rootz),(side*(spread+2),front-2,rootz*.64),(side*(spread+2),front-4,5 if kind=='deer' else 8)]
        r=[6 if kind not in('deer','bear') else(5 if kind=='deer' else 9),3.6 if kind!='deer' else 2.5,3 if kind!='deer' else 2]
        if kind=='bear':r=[9,7,5.7]
        id=('left' if side<0 else'right')+'-fore';chain(g,points,r,coat)
        segment(g,points[-2],points[-1],r[-2],r[-1],distal)
        foot=(side*(spread+2),front-6)
        feet.append(pad(g,id,*foot,rx,ry,h,distal,kind=='deer'))
        joints[id]={'shoulder':points[0],'elbow':points[1],'ankle':points[2],'toe':(foot[0],foot[1]-ry+1,1)}
        # Hind knee moves toward chest, then hock returns rearward.
        points=[(side*spread,rear,rootz+1),(side*(spread+3),rear-9,rootz*.61),(side*(spread+3),rear+2,14),(side*(spread+3),rear-2,5 if kind=='deer' else 7)]
        r=[7.2,5.3,3.5,2.8]
        if kind=='deer':r=[5.8,3.7,2.5,2]
        elif kind=='bear':r=[11,8,6.5,5.7]
        id=('left' if side<0 else'right')+'-hind';chain(g,points,r,coat)
        segment(g,points[-2],points[-1],r[-2],r[-1],distal)
        foot=(side*(spread+3),rear-5)
        feet.append(pad(g,id,*foot,rx,ry,h,distal,kind=='deer'))
        joints[id]={'hip':points[0],'knee':points[1],'hock':points[2],'ankle':points[3],'toe':(foot[0],foot[1]-ry+1,1)}
    return feet,joints

def wedge_ear(g,cx,cy,z,h,w,coat,inner=18):
    for dz in range(h):
        rr=max(.6,w*(1-dz/h));g.ellipsoid(cx,cy+dz*.1,z+dz,rr,2.8 if dz<h*.6 else 1.5,1,coat)
        if 2<dz<h-2:g.ellipsoid(cx,cy-2,z+dz,rr*.54,.8,1,inner)

def muzzle(g,y,z,width,length,coat,light):
    # Wedge shrinks toward the nose instead of a ball protrusion.
    for d in range(length):
        w=width*(1-d/length*.65);hh=max(2.2,4.8-d*.16)
        g.ellipsoid(0,y-d,z-d*.06,w,1.5,hh,light if d>length*.25 else coat)
    g.ellipsoid(0,y-length,z-length*.06+1,2.9,1.9,2.2,12)
    for side in(-1,1):
        g.ellipsoid(side*width*.72,y+3,z+5,1.9,1.3,1.7,12)
        g.put(round(side*width*.72),y+2,round(z+6),18)

def fox(seed):
    rng=random.Random(seed);g=Grid();lean=rng.choice((-1,0,1))
    g.ellipsoid(0,25,42,13,28,15,17);g.ellipsoid(0,5,43,13,13,16,17);g.ellipsoid(0,45,41,13.5,12,14,17)
    chain(g,[(0,4,48),(0,-5,55),(0,-12,59)],[9,9,9],17)
    g.ellipsoid(0,-13,59,10,13,10,17)
    for p,c in list(g.cells.items()):
        x,y,z=p
        if y<12 and z<43 and abs(x)<8:g.put(*p,18)
    feet,j=animal_legs(g,(42,6,46,9),'fox',17,12,4,7,4)
    muzzle(g,-20,55,6,12,17,18)
    for side in(-1,1):wedge_ear(g,side*6,-10,65,17,4.5,17,18)
    chain(g,[(0,51,44),(lean*3,64,43),(lean*4,83,51),(lean*5,103,55)],[7,10,9,4.5],17)
    segment(g,(lean*4,91,54),(lean*5,106,55),7,3,18)
    return finish(g,'fox',feet,j,'original thorax/haunch masses, different fore/hind tapered paths, dark flat paws, long raised bushy tail, wedge muzzle/ears')

def wolf(seed):
    rng=random.Random(seed);g=Grid();taillean=rng.choice((-3,3))
    g.ellipsoid(0,28,43,15,30,17,15);g.ellipsoid(0,7,46,15,16,19,15);g.ellipsoid(0,48,44,14,13,16,15)
    chain(g,[(0,9,50),(0,-2,59),(0,-13,63)],[11,11,10],15);g.ellipsoid(0,-14,64,11,12,10,15)
    for p,c in list(g.cells.items()):
        x,y,z=p
        if z>54 and y>0:g.put(*p,12)
        elif z<42 and y<24:g.put(*p,9)
    feet,j=animal_legs(g,(45,7,49,11),'wolf',15,12,4.6,8,4)
    muzzle(g,-21,59,7,13,15,9)
    for side in(-1,1):wedge_ear(g,side*7,-11,70,14,4.2,15,9)
    chain(g,[(0,56,45),(taillean,67,43),(taillean*2,87,39)],[8,8,3],15)
    for side in(-1,1):g.ellipsoid(side*9,0,54,6,11,13,9)
    return finish(g,'wolf',feet,j,'original sloped shoulder/ruff, longer forefoot, distinct folded hindlegs, wedge head and lifted tapering tail')

def bear(seed):
    rng=random.Random(seed);g=Grid();yshift=rng.randrange(2)
    g.ellipsoid(0,32,43,21,36,23,1);g.ellipsoid(0,10,46,20,21,24,1);g.ellipsoid(0,53,40,20,17,21,1)
    g.ellipsoid(0,-8,47,15,17,14,1);g.ellipsoid(0,-23,42,11,10,7,2);g.ellipsoid(0,-31,44,5,3,4,12)
    for side in(-1,1):
        g.ellipsoid(side*10,-5,60,5.7,4.6,6.5,1);g.ellipsoid(side*10,-8,61,3,1.6,3,2)
        g.ellipsoid(side*9,-18,51,2.1,1.2,2,12)
    feet,j=animal_legs(g,(40,9+yshift,55,14),'bear',1,2,6.8,10,5)
    for f in feet:
        b=f['bounds'];cx=(b[0][0]+b[0][1])/2;yy=b[1][0]+2
        for dx in(-3,0,3):g.ellipsoid(cx+dx,yy,3,1,1.8,1.1,12)
    return finish(g,'bear',feet,j,'original broad shoulder hump, low muzzle/round ears, short thick but segmented limbs and broad flat forefoot pads')

def deer(seed):
    rng=random.Random(seed);g=Grid();fork=rng.choice((-1,1))
    g.ellipsoid(0,27,50,12,25,13,2);g.ellipsoid(0,7,51,12,13,15,2);g.ellipsoid(0,45,50,12,12,14,2)
    chain(g,[(0,4,55),(0,-2,67),(0,-8,77)],[7.5,6.5,6],2);g.ellipsoid(0,-12,78,7,11,8,2)
    muzzle(g,-19,74,4.2,8,2,9)
    for side in(-1,1):
        segment(g,(side*5,-9,81),(side*15,-6,86),3,2.1,2);g.ellipsoid(side*12,-8,85,4,1.1,2,18)
        chain(g,[(side*4,-7,84),(side*7,-3,92),(side*12,0,97)],[2.1,1.7,1],1)
        segment(g,(side*7,-3,91),(side*12,-8,97),1.6,1,1)
        segment(g,(side*10,-1,94),(side*(15+fork),4,99),1.2,.8,1)
    for p,c in list(g.cells.items()):
        x,y,z=p
        if z<47 and abs(x)<8:g.put(*p,18)
        if y>40 and z>48 and abs(x)>8:g.put(*p,23)
    feet,j=animal_legs(g,(50,7,46,8),'deer',2,12,3.2,5,3)
    segment(g,(0,52,54),(0,64,58),3.8,1.4,18)
    return finish(g,'deer',feet,j,'original tall narrow body, elbow/knee/hock landmark paths, small continuous planted hooves, raised neck and branching antlers')

def dragon(seed):
    rng=random.Random(seed);g=Grid();tailturn=rng.choice((-1,1))
    g.ellipsoid(0,25,38,17,28,18,4);g.ellipsoid(0,4,42,17,15,21,4);g.ellipsoid(0,46,37,17,13,17,4)
    chain(g,[(0,3,48),(0,-7,61),(0,-15,68)],[10,9,9],4);g.ellipsoid(0,-18,69,11,13,10,4)
    muzzle(g,-27,64,7.2,11,4,9)
    feet,j=animal_legs(g,(37,7,45,12),'dragon',4,3,5.8,8,4)
    for side in(-1,1):
        chain(g,[(side*8,-12,76),(side*11,-6,84),(side*13,-2,88)],[3,2,1],18)
        root=(side*13,12,51);elbow=(side*32,19,66);tip=(side*55,28,80);back=(side*46,52,60);low=(side*22,41,44)
        triangle(g,root,elbow,low,20);triangle(g,elbow,tip,low,20);triangle(g,tip,back,low,20)
        chain(g,[root,elbow,tip,back,low],[3,2.5,1.8,1.8,2],3)
        segment(g,elbow,low,2,1.8,3);segment(g,tip,low,1.7,1.7,3)
        j[('left' if side<0 else'right')+'-wing']={'root':root,'elbow':elbow,'tip':tip}
    chain(g,[(0,50,39),(tailturn*5,67,32),(tailturn*10,88,29),(tailturn*15,106,36)],[10,8,4.5,1.5],4)
    for y,z in[(7,59),(17,55),(28,56),(39,52),(52,45),(64,38),(79,34)]:
        triangle(g,(-2,y,z),(2,y,z),(0,y+4,z+7),3)
    for p,c in list(g.cells.items()):
        x,y,z=p
        if c==4 and abs(x)<10 and y<47 and z<38:g.put(*p,9)
    return finish(g,'dragon',feet,j,'original four bent legchains, grounded claw-pad silhouettes, thorax/neck/tail volumes, raised triangulated membrane wings and dorsal spines')

def human_core(seed,role,shirt,pants,left,right):
    rng=random.Random(seed);g=Grid();stand=rng.choice((-1,0,1));j={};feet=[]
    g.ellipsoid(0,0,39,10,6.6,8,pants);g.ellipsoid(0,0,54,13.5,7.5,16,shirt)
    g.ellipsoid(0,0,69,4.5,4.5,7,16);g.ellipsoid(0,-.5,80,8.4,7.5,10.5,16)
    for side in(-1,1):
        id=('left' if side<0 else'right')+'-leg';p=[(side*7,0,40),(side*(8 if side<0 else 10),-2 if side<0 else 4,23),(side*(8 if side<0 else 11),-2 if side<0 else 2+stand,7)]
        chain(g,p,[5.5,4.6,3.6],pants);feet.append(pad(g,id,p[-1][0],p[-1][1]-3,5.2,8,4,12));j[id]={'hip':p[0],'knee':p[1],'ankle':p[2],'toe':(p[-1][0],p[-1][1]-10,1)}
    for id,side,pose in[('left-arm',-1,left),('right-arm',1,right)]:
        shoulder=(side*14,0,64);elbow,wrist=pose;chain(g,[shoulder,elbow,wrist],[5.7,4.5,3.1],shirt)
        g.ellipsoid(*wrist,3.6,3.7,4.1,16);g.ellipsoid(wrist[0]-side*2.8,wrist[1]-2,wrist[2],1.8,2.3,2.2,16)
        j[id]={'shoulder':shoulder,'elbow':elbow,'wrist':wrist}
    for side in(-1,1):g.ellipsoid(side*3.2,-7.3,82,1.4,1.1,1.1,12)
    g.ellipsoid(0,-8,79.5,2,2.6,2,16);g.box(-2,-8,75,3,-7,76,10)
    # Three-dimensional belt follows waist; buckle is attached to its front.
    for p,c in list(g.cells.items()):
        x,y,z=p
        if 40<=z<=42 and abs(x)<=12:g.put(*p,1)
    g.box(-2,-8,40,3,-6,43,13)
    return g,feet,j

def collar(g,c,z=67,fur=False):
    g.ellipsoid(0,0,z,10,7,3.7,c);g.ellipsoid(0,-3,z+2,5,4,4,16)
    if fur:
        for side in(-1,1):g.ellipsoid(side*10,0,z-2,7,7,5,c)

def hair(g,c=1):
    for x in range(-9,10):
        for y in range(-7,9):
            for z in range(76,91):
                if (x/8.9)**2+((y+.5)/8.1)**2+((z-80)/11.5)**2<=1 and(y>2 or z>86):g.put(x,y,z,c)

def tunic_hem(g,c,z0=32,z1=44,radius=12,depth=8):
    for z in range(z0,z1):
        r=radius-(z-z0)*.12
        for x in range(-math.ceil(r),math.ceil(r)+1):
            for y in range(-depth,depth+1):
                if (x/r)**2+(y/depth)**2<=1:g.put(x,y,z,c)

def ranger(seed):
    g,feet,j=human_core(seed,'ranger',3,19,[(-21,0,52),(-24,-4,42)],[(22,-1,56),(27,-8,65)])
    tunic_hem(g,3,32,41,12,8);collar(g,4);hair(g,2)
    # Hood is a shell around the back/sides, leaving an open face.
    for x in range(-11,12):
        for y in range(-10,12):
            for z in range(71,94):
                d=(x/10.5)**2+((y-1)/10)**2+((z-81)/12)**2
                if .76<d<=1.15 and(y>0 or abs(x)>7 or z>90):g.put(x,y,z,3)
    g.box(-8,5,45,9,13,64,1);g.box(-6,12,49,7,15,60,2)
    # Backpack straps and quiver are attached masses, not painted equipment.
    for side in(-1,1):segment(g,(side*8,-7,62),(side*6,-7,45),1.2,1.2,2)
    chain(g,[(-24,-4,42),(-29,-5,50),(-29,-5,65),(-24,-5,77)],[1.5,1.4,1.4,1.2],2)
    segment(g,(-24,-5,42),(-24,-5,77),.8,.8,18)
    segment(g,(8,9,44),(12,12,73),3.3,3.3,2)
    for x in(10,13):segment(g,(x,12,68),(x,12,82),.9,.9,1);g.ellipsoid(x,12,81,1.6,1.6,2.5,18)
    # Raised right glove holds a short scouting scope, directly touching fingers.
    segment(g,(25,-9,66),(31,-9,66),2.5,2.5,14);g.ellipsoid(31,-9,66,1.8,2.7,2.7,8)
    return finish(g,'ranger',feet,j,'original asymmetric leg/arm landmark body; open hood shell, flared tunic hem, backpack/quiver, lowered bow and raised scope')

def knight(seed):
    g,feet,j=human_core(seed,'knight',15,15,[(-22,-2,53),(-23,-4,44)],[(22,-2,57),(28,-9,65)])
    g.ellipsoid(0,-3,55,13,7,14,14);g.ellipsoid(0,-8,57,9,2,10,25)
    for side in(-1,1):
        g.ellipsoid(side*16,0,64,8 if side<0 else 7,7,7,14)
        p=j[('left' if side<0 else'right')+'-leg']['knee'];g.ellipsoid(p[0],p[1]-3,p[2],5.1,3.5,5.5,14)
        ankle=j[('left' if side<0 else'right')+'-leg']['ankle'];g.ellipsoid(ankle[0],ankle[1],8,5,5,5,14)
    g.ellipsoid(0,0,80,9.5,8.5,12,14);g.box(-7,-9,79,8,-7,83,12);g.box(-1,-10,76,2,-8,89,15)
    g.box(-8,-9,83,9,-7,86,25);g.box(-2,-2,89,3,3,99,22)
    # Shield plane is in front of the left arm; handed load has a real attachment.
    for z in range(29,69):
        rr=11 if z>40 else max(3,(z-29)*.7+3)
        for x in range(math.floor(-27-rr),math.ceil(-27+rr)+1):
            if ((x+27)/rr)**2+((z-49)/20)**2<=1:g.box(x,-9,z,x+1,-5,z+1,15)
    g.box(-29,-10,35,-25,-8,62,13);g.box(-36,-10,48,-17,-8,52,13)
    segment(g,(28,-9,59),(28,-9,69),2,2,1);segment(g,(22,-9,68),(34,-9,68),1.8,1.8,13)
    segment(g,(28,-9,69),(40,-9,96),2.3,.75,25)
    return finish(g,'knight',feet,j,'original steel body/pauldrons/knee caps/helmet geometry, staggered boot stance, lowered shield and raised tapered sword')

def north(seed):
    g,feet,j=human_core(seed,'north',2,1,[(-20,1,49),(-21,-3,37)],[(23,-1,52),(25,-5,44)])
    tunic_hem(g,2,27,43,15,10);collar(g,9,68,True);hair(g,2)
    # Fur cap and ear covers change head occupancy; beard hangs onto chest.
    g.ellipsoid(0,1,87,10,8,6,9)
    for side in(-1,1):g.ellipsoid(side*8,1,78,3,5,6,9)
    chain(g,[(0,-7,77),(0,-7,73),(0,-6,69)],[4.8,4,2],2)
    for z in range(31,63):
        width=15-(z-31)*.14;g.box(-int(width),7,z,int(width)+1,12,z+1,19)
    g.box(-10,12,36,11,14,58,2)
    for side in(-1,1):
        ankle=j[('left' if side<0 else'right')+'-leg']['ankle'];g.ellipsoid(ankle[0],ankle[1],10,5.5,5.5,6,9)
    # Axe remains above the ground; hand contacts its shaft atz44.
    segment(g,(25,-5,23),(25,-5,81),1.8,1.8,1)
    for x in range(19,36):
        for z in range(70,83):
            if ((x-27)/8)**2+((z-76)/7)**2<=1:g.box(x,-7,z,x+1,-3,z+1,14)
    g.box(24,-7,70,27,-3,82,13)
    return finish(g,'north',feet,j,'original layered winter silhouette, fur shoulder collar/hat/boot cuffs, thick tunic plus rear cloak, beard and held axe')

def mage(seed):
    g,feet,j=human_core(seed,'mage',20,20,[(-20,-1,51),(-23,-5,42)],[(24,-4,61),(30,-12,74)])
    for z in range(14,46):
        rx=15-(z-14)*.18;ry=10-(z-14)*.08
        for x in range(-16,17):
            for y in range(-11,12):
                if (x/rx)**2+(y/ry)**2<=1:g.put(x,y,z,20)
    collar(g,21);hair(g,1)
    for z in range(88,102):
        rr=max(.65,11.5*(1-(z-88)/14));cx=(z-88)*.22;g.ellipsoid(cx,0,z,rr,rr*.85,1,20)
    g.ellipsoid(0,0,88,14,12,1.7,20);g.ellipsoid(0,0,90,11,9,1.5,13)
    # Front trim follows the robe silhouette rather than an unconnected glyph.
    for z in range(16,45):
        yy=-round(10-(z-14)*.08);g.box(-1,yy-1,z,2,yy+1,z+1,21)
    for z in(19,26,33):g.box(-5,-10,z,6,-8,z+2,13)
    segment(g,(-23,-5,7),(-23,-5,86),1.8,1.8,1);g.ellipsoid(-23,-5,88,5,5,5,24)
    # Held crystal touches raised palm: no unsupported floating effect.
    g.ellipsoid(30,-12,81,4,4,5,24);segment(g,(30,-12,77),(30,-12,74),2,2,24)
    return finish(g,'mage',feet,j,'original conical flared robe, visible planted boots, asymmetric casting arm, crooked hat silhouette and attached held staff/crystal')

def farmer(seed):
    g,feet,j=human_core(seed,'farmer',18,7,[(-20,1,50),(-21,-3,38)],[(23,-3,56),(28,-9,48)])
    hair(g,2)
    # Overall bib and raised straps are distinct layers on the shirt.
    g.box(-8,-8,43,9,-6,57,7)
    for side in(-1,1):segment(g,(side*7,-7,56),(side*9,-4,66),1.6,1.6,7);g.ellipsoid(side*7,-8,55,1.3,.9,1.3,13)
    g.ellipsoid(0,0,89,14,12,1.6,23);g.ellipsoid(0,0,93,9.5,8,5,23);g.ellipsoid(0,0,91,10,8.5,1.6,1)
    g.box(-14,-2,28,-9,5,37,2)
    # Open produce basket hangs from a connected arch held in the right hand.
    g.box(19,-13,26,37,0,38,2);g.box(22,-10,29,34,-3,40,0)
    for z in(28,32,36):g.box(18,-14,z,38,-12,z+1,1);g.box(18,-1,z,38,1,z+1,1)
    chain(g,[(19,-8,37),(21,-8,44),(28,-8,48),(35,-8,44),(37,-8,37)],[1.7,1.7,1.7,1.7,1.7],1)
    for x,y,c in[(25,-6,22),(31,-7,17),(28,-8,4)]:g.ellipsoid(x,y,32,3.3,3.3,3.5,c)
    return finish(g,'farmer',feet,j,'original shirt and layered bib/straps, straw hat, asymmetric working stance, low pouch and open handled produce basket')

ROWS=[
 ('creatures','fox','Лис с гибким хвостом','Плечо и таз → разные суставные цепи → плоские ориентированные лапы',fox),
 ('creatures','wolf','Волк с высоким загривком','Выделенные плечи и задние скакательные суставы; стопы шире голени',wolf),
 ('creatures','bear','Медведь на широких лапах','Короткие сегментированные конечности и широкие опоры под тяжёлым корпусом',bear),
 ('creatures','deer','Олень с тонкими голенями','Разные передние и задние суставы; четыре малых опорных копыта',deer),
 ('creatures','dragon','Дракон с перепончатыми крыльями','Четыре опоры, локальные корни крыльев и открытые просветы между лапами',dragon),
 ('characters','ranger','Разведчик с луком и оптикой','Новая асимметричная фигура; открытый капюшон и прикреплённое снаряжение',ranger),
 ('characters','knight','Рыцарь с поднятым мечом','Суставные цепи, объёмная броня и разное положение рук со щитом и мечом',knight),
 ('characters','north','Северянин в меховом воротнике','Слои тёплой одежды поверх новой фигуры, широкие сапоги и удерживаемый топор',north),
 ('characters','mage','Маг с поднятой рукой','Плащевидная роба, видимые сапоги и кристалл, соединённый с ладонью',mage),
 ('characters','farmer','Фермер с корзиной урожая','Рубаха, объёмный нагрудник и лямки; открытая корзина на соединённой ручке',farmer),
]
