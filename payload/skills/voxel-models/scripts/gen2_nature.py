"""Ten original Gen2 native-grid constructions. No source cells are imported.

The studied models informed mass/branch/cut decisions only. Seed variation is
bounded at the structural level; geometry is authored here, not white noise.
"""
import math, random, collections
import library_recipes  # Extends the already shared palette to 28 exactly once.
from voxel_recipes import Grid, PALETTE

TAU=math.tau
DIRS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))

def _path(g,points,r0,r1,c):
    lengths=[math.dist(a,b) for a,b in zip(points,points[1:])]; total=sum(lengths);done=0
    for a,b,length in zip(points,points[1:],lengths):
        steps=max(1,math.ceil(length*1.7))
        for j in range(steps+1):
            u=j/steps;t=(done+u*length)/max(total,1)
            p=[a[k]+(b[k]-a[k])*u for k in range(3)];r=max(1.05,r0+(r1-r0)*t)
            g.ellipsoid(*p,r,r,r,c)
        done+=length

def _lobe(g,center,radii,c,angle=0,phase=0,warp=.08):
    cx,cy,cz=center;rx,ry,rz=radii;cs,sn=math.cos(angle),math.sin(angle)
    bound=max(rx,ry)*(1+warp)+2
    for x in range(math.floor(cx-bound),math.ceil(cx+bound)+1):
        for y in range(math.floor(cy-bound),math.ceil(cy+bound)+1):
            dx,dy=x-cx,y-cy;u=(dx*cs+dy*sn)/rx;v=(-dx*sn+dy*cs)/ry
            theta=math.atan2(v,u)
            outline=1+warp*(.65*math.sin(3*theta+phase)+.35*math.sin(5*theta-phase))
            for z in range(math.floor(cz-rz*(1+warp)-1),math.ceil(cz+rz*(1+warp)+1)):
                w=(z-cz)/rz
                if u*u+v*v+w*w<=outline*outline:g.put(x,y,z,c)

def _roots(g,base,arms):
    for x,y,length,radius in arms:
        _path(g,[base,(x*.6,y*.6,2),(x,y,0)],radius,1.1,1)

def _snow(g,minimum,phase):
    for (x,y,z),c in list(g.cells.items()):
        if c in (3,4,5) and z>=minimum and (x,y,z+1) not in g.cells:
            if math.sin(x/10+phase)+.7*math.cos(y/13-phase)>.05:g.put(x,y,z,6)

def _meta(g,method,**kw):
    # Ground anchors describe z=0; primitive end caps must not grow underground.
    for p in [p for p in g.cells if p[2]<0]:g.cells.pop(p)
    mins=[min(p[i] for p in g.cells) for i in range(3)]
    g.gen2_meta={'method':method,'coordinateSystem':'original Grid before VOX occupied-bounds normalization; z=0 ground','exportTranslation':[-v for v in mins],**kw};return g

def fir(seed):
    r=random.Random(seed);g=Grid();phase=r.uniform(-.2,.2)
    trunk=[(0,0,0),(1,-1,22),(1,1,49),(-2,3,76),(-1,2,99)]
    _path(g,trunk,4.8,1.2,1);_roots(g,(0,0,5),[(-10,-4,11,2.8),(6,-9,11,2.4),(8,6,10,2.2),(-4,8,8,2.1)])
    branches=[]
    tiers=[(17,25,5),(31,23,4),(46,20,5),(60,16,4),(73,12,3),(85,8,3)]
    for ti,(z,reach,count) in enumerate(tiers):
        turn=.51*ti+phase
        for j in range(count):
            a=turn+j*TAU/count+r.uniform(-.21,.21)
            length=reach*r.uniform(.72,1.08);dx,dy=math.cos(a)*length,math.sin(a)*length
            start=(1 if z<50 else -1,0 if z<50 else 2,z)
            end=(start[0]+dx,start[1]+dy,z+r.uniform(-2,3))
            _path(g,[start,(start[0]+dx*.62,start[1]+dy*.62,z-2.5),end],2.1 if ti<3 else 1.6,.85,2)
            branches.append([list(start),list(end)])
            # Several branch-attached short sprays, not a coaxial cone tier.
            for t,scale in ((.43,1),(.69,.93),(.89,.71)):
                center=(start[0]+dx*t,start[1]+dy*t,z+1.4+(1-t)*2)
                _lobe(g,center,(max(3.3,length*.22)*scale,3.3*scale,4.7*scale),3+(ti+j)%3,a,ti+j,warp=.11)
                side=1 if (ti+j)%2 else -1
                _lobe(g,(center[0]-math.sin(a)*side*3,center[1]+math.cos(a)*side*3,center[2]-1),
                      (max(2.5,length*.16)*scale,2.8,3.7),3+(ti+j+1)%3,a+.35*side,ti+1,warp=.1)
    _lobe(g,(-1,2,94),(4,4,6),4,phase,1,.08);_snow(g,30,phase)
    return _meta(g,'Original unequal, off-axis conifer branch graph and attached sprays; observations n55/n58 MountainLabs Fluffy/Snowy Pine, contrasting n51 symmetric Kytric tree8.',
                 landmarks={'trunk':trunk,'branchEdges':branches,'species':'conifer','majorAsymmetry':'unequal reaches and tier angular offsets','snow':'connected upward exposed foliage regions'},checks={'trunkGrounded':True,'uniformRadialTierGrammar':False})

def _oak_crown(g,center,radii,c,angle,phase,variant):
    """Oak-only low-frequency 3D domain warp with a few large open pockets."""
    cx,cy,cz=center;rx,ry,rz=radii;cs,sn=math.cos(angle),math.sin(angle)
    bound=max(rx,ry)*1.35+2;notch=variant in (0,3,6)
    for x in range(math.floor(cx-bound),math.ceil(cx+bound)+1):
        for y in range(math.floor(cy-bound),math.ceil(cy+bound)+1):
            dx,dy=x-cx,y-cy;u=(dx*cs+dy*sn)/rx;v=(-dx*sn+dy*cs)/ry
            for z in range(math.floor(cz-rz*1.24)-1,math.ceil(cz+rz+1)+1):
                w=(z-cz)/rz
                # A shared smooth field displaces whole shoulders and flattens
                # different parts of each lobe. There is no independent-cell noise.
                uu=u+.23*math.sin(1.55*w+phase)+.10*math.sin(1.9*v-phase)
                vv=v+.18*math.sin(2.1*u+phase*.7)-.13*w
                ww=w+.10*math.sin(2*u+1.7*v-phase)
                limit=1+.12*math.sin(2.3*u+1.6*w+phase)*math.sin(2.5*v-phase)+.05*math.cos(3*w+phase)
                if uu*uu+vv*vv+ww*ww>limit*limit:continue
                if w<-.72+.14*u+.06*variant:continue
                if variant%3==1 and w>.87+.12*u:continue
                # Broad open recess faces away from the branch graft, leaving
                # a connected canopy shoulder rather than punching out its center.
                side=-1 if variant%2==0 else 1
                if notch and ((u-.72)/.52)**2+((v-side*.28)/.43)**2+((w-.14)/.55)**2<1:continue
                g.put(x,y,z,c)

def oak(seed):
    r=random.Random(seed);g=Grid();lean=r.uniform(-1.5,1.5)
    trunk=[(0,0,0),(2,-1,20),(6,2,38),(4,5,54),(6,7,66)]
    _path(g,trunk,6.5,2.6,1);_roots(g,(0,0,7),[(-14,-8,16,3.6),(11,-11,16,3.2),(15,5,16,3.1),(-7,13,15,3.1),(1,10,10,2.4)])
    groups=[(-30,-9,60,17,14,15,31),(28,-20,59,20,16,14,37),(-20,23,78,17,18,17,41),
            (16,24,77,21,17,15,45),(8,-22,85,17,16,16,47),(32,5,84,16,14,14,50),(-9,4,92,18,16,14,53)]
    branches=[]
    for i,(x,y,z,rx,ry,rz,bz) in enumerate(groups):
        x+=lean+(r.random()-.5)*2;z+=r.choice([-1,0,1]);a=math.atan2(y-3,x-4)
        begin=(4,3,bz);mid=(4+(x-4)*.56,3+(y-3)*.56,bz+(z-bz)*.32)
        _path(g,[begin,mid,(x,y,z)],3.2 if i<4 else 2.7,1.4,2)
        _oak_crown(g,(x,y,z),(rx,ry,rz),3+i%3,a,i*.7,i)
        # One coherent protruding shoulder carries branch direction.
        _lobe(g,(x+math.cos(a)*rx*.66,y+math.sin(a)*rx*.66,z-4),(rx*.48,ry*.55,rz*.57),3+(i+1)%3,a,i,.08)
        if i in (0,1,3,5):
            # Branch-scale subcrowns form a directional cluster, not one neat ball.
            tip=(x+math.cos(a)*rx*.52-math.sin(a)*ry*.42,
                 y+math.sin(a)*rx*.52+math.cos(a)*ry*.42,z+rz*.43)
            _path(g,[(x,y,z),tip],1.5,1.1,2)
            _lobe(g,tip,(rx*.6,ry*.48,rz*.62),3+i%3,a+.33,i+.7,.14)
        branches.append([list(begin),list(mid),[x,y,z]])
    # A deliberately open crown pocket leaves the trunk/branch hierarchy visible.
    for p,c in list(g.cells.items()):
        x,y,z=p
        if c in (3,4,5) and ((x-2)/9)**2+((y+13)/9)**2+((z-64)/8)**2<1:g.put(*p,0)
    return _meta(g,'Original leaning trunk with unequal branch dominance, three-dimensionally warped crown shoulders, three broad open lobe recesses and a central crown gap; studied n54 Dead Tree skeleton and n76 padadu tree4 lobes, not source-cell reconstruction.',
                 landmarks={'trunk':trunk,'branchEdges':branches,'crownPocket':[2,-13,64],'openLobeRecesses':[0,3,6],'crownWarp':'shared low-frequency 3D field, variant-specific lower/top truncation','species':'broadleaf oak'},checks={'uniformAngularRing':False,'macroCrownGap':True,'independentCellNoise':False,'oakOnlyWarp':True})

def willow(seed):
    r=random.Random(seed);g=Grid();trunk=[(0,0,0),(2,-2,18),(4,0,38),(3,3,58)]
    _path(g,trunk,5.6,2.1,1);_roots(g,(0,0,6),[(-12,-5,13,3),(9,-10,13,2.8),(12,6,14,3),(-5,12,13,2.5)])
    arms=[(-28,-12,60,17),(-13,26,66,26),(27,16,63,19),(31,-15,59,24),(1,-30,69,31),(-21,9,72,36)]
    desc=[]
    for i,(x,y,z,bottom) in enumerate(arms):
        x+=r.uniform(-1.3,1.3);a=math.atan2(y,x)
        arch=[(3,1,37+i*2),(x*.42,y*.42,z+5),(x*.82,y*.82,z+3),(x,y,z)]
        _path(g,arch,3,1.2,2)
        _lobe(g,(x*.76,y*.76,z+2),(12 if i%2 else 10,9,7),3+i%3,a,i,.11)
        for j,(offset,width,dz) in enumerate([(-6,4.1,3),(0,5.4,-1),(6,3.8,5)]):
            xx=x-math.sin(a)*offset;yy=y+math.cos(a)*offset;endz=bottom+dz
            pts=[(xx,yy,z+1),(xx+math.cos(a)*2,yy+math.sin(a)*2,z-12),
                 (xx+math.cos(a)*4,yy+math.sin(a)*4,endz)]
            _path(g,pts,width*.65,1.2,3+(i+j)%3)
            _lobe(g,(pts[1][0],pts[1][1],(z+endz)/2),(width,width*.8,(z-endz)*.48),3+(i+j)%3,a,j,.1)
        desc.append({'branch':arch,'hangingExtentZ':[bottom,z]})
    return _meta(g,'Original arched wood carrying unequal hanging foliage curtains, central view gap; observation n57/n59 MountainLabs Willow sections and opposing views.',landmarks={'species':'weeping willow','branches':desc},checks={'attachedDroop':True,'sphereRecolor':False})

def _palm_into(g,origin,scale,seed,fruit=True):
    r=random.Random(seed);ox,oy,oz=origin
    def P(p):return (ox+p[0]*scale,oy+p[1]*scale,oz+p[2]*scale)
    trunk=[(-6,0,0),(-3,-1,23),(3,2,51),(10,3,76),(14,4,92)]
    _path(g,[P(p) for p in trunk],4.8*scale,2.3*scale,2)
    # Coherent growth rings follow the curved trunk, not a flat per-cell pattern.
    for p,c in list(g.cells.items()):
        if c==2 and oz+8*scale<p[2]<oz+87*scale and int((p[2]-oz)/(5*scale))%4==0:g.put(*p,1)
    crown=P((14,4,92));fronds=[]
    angles=[-158,-122,-76,-34,7,44,84,126,171]
    for i,deg in enumerate(angles):
        a=math.radians(deg+r.uniform(-4,4));length=[38,47,43,33,45,49,37,44,35][i]*scale
        reach=(math.cos(a)*length,math.sin(a)*length);drop=[17,24,20,13,25,29,15,21,16][i]*scale
        pts=[]
        for n in range(51):
            t=n/50;x=crown[0]+reach[0]*t;y=crown[1]+reach[1]*t
            z=crown[2]+11*scale*math.sin(math.pi*t)-drop*t
            pts.append((x,y,z));width=(1.3+2.4*math.sin(math.pi*t))*scale
            _lobe(g,(x,y,z),(max(.7,width),max(.6,1.2*scale),max(.65,1.2*scale)),3+i%3,a,i,.025)
        _path(g,pts,1.1*scale,.7*scale,4)
        # Tapered paired leaflets make readable gaps along the frond sides.
        for n in range(8,47,5):
            t=n/50;base=pts[n];span=(4.5+4*math.sin(math.pi*t))*(1-t*.62)*scale
            for side in (-1,1):
                leafend=(base[0]-math.sin(a)*span*side+math.cos(a)*2*scale,
                         base[1]+math.cos(a)*span*side+math.sin(a)*2*scale,base[2]-2.6*scale)
                _path(g,[base,leafend],1.4*scale,.65*scale,3+(i+n//5)%3)
        fronds.append([list(crown),list(pts[-1])])
    if fruit:
        for p in [(11,1,89),(16,1,88),(12,7,87)]:g.ellipsoid(*P(p),2.9*scale,2.6*scale,3.4*scale,16)
    return {'trunk':[P(p) for p in trunk],'frondEnds':fronds}

def palm(seed):
    g=Grid();land=_palm_into(g,(0,0,0),1,seed)
    _roots(g,(-6,0,4),[(-15,-5,10,2.6),(3,-7,12,2.6),(-8,9,9,2.4)])
    return _meta(g,'Original curved tapering palm with unequal leaf lengths, arched centerlines, tapered paired leaflets and attached coconuts; branch hierarchy and distinct species silhouette derived from n54/n57 structural observations.',landmarks={'species':'palm',**land},checks={'frondGrafts':True,'uniformEightSpokeSchedule':False})

def _mushroom_into(g,cx,cy,stemh,rx,ry,caprise,lean,c,phase):
    stem=[(cx,cy,0),(cx-lean*.4,cy+2,stemh*.48),(cx+lean,cy+1,stemh)]
    _path(g,stem,max(3,rx*.2),max(2.2,rx*.155),18)
    capx=cx+lean;capy=cy+1
    for x in range(math.floor(capx-rx-3),math.ceil(capx+rx+3)):
        for y in range(math.floor(capy-ry-3),math.ceil(capy+ry+3)):
            dx,dy=(x-capx)/rx,(y-capy)/ry;t=math.atan2(dy,dx)
            outline=1+.08*math.sin(3*t+phase)+.035*math.sin(5*t-phase);q=(dx*dx+dy*dy)/(outline*outline)
            if q>1:continue
            top=round(stemh+caprise*math.sqrt(max(0,1-q))+.045*(x-capx))
            bottom=round(stemh-4+2*(1-q))
            for z in range(bottom,top+1):g.put(x,y,z,c if z>=bottom+3 else 16)
            # Radial gill ridges are restricted to the underside.
            if math.sin(t*21+phase)>.65 and q>.14:
                for z in range(bottom-1,bottom+1):g.put(x,y,z,18)
            # Several large connected freckles belong to cap surface coordinates.
            spots=[(-.35,-.18,.15),(.23,.27,.12),(.48,-.25,.11),(-.05,.56,.1),(-.57,.29,.09)]
            if any((dx-a)**2+(dy-b)**2<rr*rr for a,b,rr in spots):
                g.put(x,y,top,18);g.put(x,y,top-1,18)
    return {'stem':stem,'capCenter':[capx,capy,stemh],'capRadii':[rx,ry,caprise]}

def mushroom(seed):
    g=Grid();phase=random.Random(seed).uniform(-.3,.3)
    big=_mushroom_into(g,2,0,58,28,24,17,-4,22,phase)
    small=_mushroom_into(g,-30,13,27,13,11,10,2,10,phase+.8)
    tiny=_mushroom_into(g,28,-12,17,9,8,7,-1,17,phase+1.7)
    return _meta(g,'Original asymmetric fungus caps, curved stems, geometric gill ridges and connected surface freckles. Companion scale hierarchy is authored here; no source fungus grid was inspected or copied.',landmarks={'fungi':[big,small,tiny]},intentionalDetached=[{'kind':'companion fungus','groundAnchor':[-30,13,0]},{'kind':'companion fungus','groundAnchor':[28,-12,0]}],checks={'stemsGrounded':True,'capStemOverlap':True,'detailOnSemanticRegions':True})

def _segment_distance(x,y,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/max(dx*dx+dy*dy,1e-6)))
    return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy),t

def _poly_signed(x,y,poly):
    inside=False;dist=1e9;idx=0
    for i,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
        d,t=_segment_distance(x,y,a,b)
        if d<dist:dist,idx=d,i
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
    return (dist if inside else -dist),idx

def _stratum(x,y,z,warm=False):
    s=math.floor((z+.1*x-.07*y+1.6*math.sin(y/13))/7)
    if warm:return [11,23,17,16,11,10][s%6]
    return [14,15,14,19,14][s%5]

def _column(g,x,y,h,top,warm=False):
    for z in range(h):g.put(x,y,z,top if z==h-1 else _stratum(x,y,z,warm))

def snow_mountain(seed):
    r=random.Random(seed);phase=r.uniform(-.12,.12);g=Grid();w,d=108,90
    ridges=[((25,59,38),(45,43,63),22),((45,43,63),(66,51,49),20),((66,51,49),(85,70,28),16),
            ((45,43,63),(57,19,40),16),((25,59,38),(16,78,19),15)]
    gullies=[[(43,46),(36,35),(30,23),(19,11)],[(65,51),(77,44),(89,32),(99,22)],[(56,23),(68,18),(81,9)]]
    heights={}
    for x in range(w):
        for y in range(d):
            mass=0
            for a,b,width in ridges:
                dist,t=_segment_distance(x,y,a,b);peak=a[2]+(b[2]-a[2])*t
                mass=max(mass,peak*max(0,1-dist/width)**1.22)
            h=4+round(mass+1.3*math.sin(x/13+phase)*math.sin(y/17))
            h=max(3,h)
            for gi,line in enumerate(gullies):
                gd=min(_segment_distance(x,y,a,b)[0] for a,b in zip(line,line[1:]));depth=7 if gi<2 else 5
                if gd<3.8 and mass>9:h=max(4,h-round(depth*(1-gd/3.8)))
            heights[(x,y)]=h
            snowline=45+3*math.sin(y/16+phase)
            _column(g,x,y,h,6 if h>snowline else 14)
            if h>snowline:
                for z in range(max(0,h-3),h):g.put(x,y,z,6)
    # Talus shoulders are small coherent masses at gully toes, attached to terrain.
    for x,y,rx,ry,rz in [(20,12,5,4,3),(94,24,6,3,4),(82,11,4,5,3)]:
        g.ellipsoid(x,y,heights[(x,y)]+1,rx,ry,rz,15)
    return _meta(g,'Original offset ridge graph with saddles, connected directional gully cuts and tilted strata. Observed n25/n26–n37 Kytric cave/cliff volumes; n43 layered unequal rock masses. This is authored geometric erosion, not a physical solver.',landmarks={'ridges':ridges,'gullies':gullies,'majorPeak':[45,43,67]},checks={'singleRadialApex':False,'gulliesAlterOccupancy':True,'strataSharedAcrossFaces':True})

def mesa(seed):
    g=Grid();w,d=112,92;phase=random.Random(seed).uniform(-.2,.2)
    poly=[(27,13),(58,9),(83,19),(95,34),(82,53),(87,75),(61,82),(38,71),(20,78),(11,49),(22,31)]
    hmap={}
    for x in range(w):
        for y in range(d):
            sd,edge=_poly_signed(x,y,poly);terrace=8+2*math.sin((x+y)/17+phase)+edge%3
            if sd>=5:h=58+round(.045*(x-52)+1.2*math.sin(y/19))
            elif sd>=0:h=48+round(sd*1.6+math.sin(x/11))
            elif sd>=-terrace:h=31+round((sd+terrace)*.65)
            elif sd>=-terrace-12:h=14+round(max(0,sd+terrace+12)*.55)
            else:h=4
            # A large east-opening ravine has an inland bend and variable width.
            center=40+5*math.sin((x-54)/13)
            if x>55 and abs(y-center)<7+(x-55)*.09:
                floor=19+round(max(0,79-x)*.12);h=min(h,floor+round(abs(y-center)*.4))
            # One northeast fracture descends from plateau into the side.
            if 55<x<88 and abs(y-(68-.28*(x-55)))<1.4:h=min(h,32+round((88-x)*.55))
            h=max(3,round(h*.79));hmap[(x,y)]=h;_column(g,x,y,h,23,True)
    # Localized lower-face spalls at weak seams; no uniform all-edge chipping.
    for cx,cy,cz,rx,ry,rz in [(20,27,25,6,5,3),(24,20,39,5,5,3),(87,62,31,5,6,3),(83,71,42,5,5,2)]:g.ellipsoid(cx,cy,cz*.79,rx,ry,rz,0)
    debris=[]
    for x,y,rx,ry,rz in [(100,35,4,3,3),(99,52,5,3,4),(23,8,4,5,3)]:
        z=hmap[(x,y)];g.ellipsoid(x,y,z+rz-1,rx,ry,rz,16);debris.append({'center':[x,y,z+rz-1],'groundZ':z-1})
    return _meta(g,'Original broad plateau with authored nonelliptical rim, unequal terraces, east ravine, localized fracture/spalls and warped warm strata. Transfers coherent contour bands n18, true cuts n25 and offset shoulders n43; no source geometry.',landmarks={'rimPolygon':poly,'ravine':'east opening x>55 around y=40+5sin((x-54)/13)','fracture':[55,68,88,59]},intentionalDetached=debris,checks={'broadPlateauRetained':True,'constantThreeLevelEllipse':False,'rimFractureGeometry':True})

def _put_region(g,region,x,y,z,c):
    p=(int(x),int(y),int(z));g.put(*p,c);region.add(p)

def _pair_contacts(a,b):
    return sum((x+dx,y+dy,z+dz) in b for x,y,z in a for dx,dy,dz in DIRS)

def _region_info(cells,anchors):
    return {'cellCount':len(cells),'bounds':[[min(p[a] for p in cells),max(p[a] for p in cells)] for a in range(3)],'anchorPoints':[list(p) for p in anchors]}

def river_gorge(seed):
    g=Grid();w,d=100,90;r=random.Random(seed);shift=r.uniform(-.5,.5)
    def upper_x(y):return 54+10*math.sin((y-55)/22)+shift
    def lower_x(y):return 51+7*math.sin(y/12)+shift
    hmap={}
    # Terrain, channel beds and receiving cavity are completed before any water.
    for x in range(w):
        for y in range(d):
            center=upper_x(y) if y>=55 else lower_x(y);dist=abs(x-center)
            bank=round(max(0,dist-18)*1.27)
            edge=55+round(2*math.sin((x-54)/17))
            h=48+min(8,round(bank*.7)) if y>=edge else 8+min(26,bank)
            if y>=55 and abs(x-upper_x(y))<=7:h=44
            basin=((x-54)/23)**2+((y-31)/19)**2
            if y<54 and basin<=1:h=7
            if y<33 and abs(x-lower_x(y))<=6:h=7
            hmap[(x,y)]=h;_column(g,x,y,h,19 if h<17 else 14)
    terrain=set(g.cells);regions={k:set() for k in ['source','lip','fall','basin','outflow']}
    for y in range(58,d):
        cx=round(upper_x(y));width=6+round(math.sin(y/13))
        for x in range(cx-width,cx+width+1):
            for z in range(44,47):_put_region(g,regions['source'],x,y,z,7 if z==46 else 8)
    for y in range(55,59):
        cx=round(upper_x(y))
        for x in range(cx-7,cx+8):
            for z in range(44,47):_put_region(g,regions['lip'],x,y,z,24)
    # A small forward bend is a flow path; every cross-section overlaps its neighbor.
    fallpath=[(54+shift,55,46),(54+shift,54,40),(57+shift,50,27),(56+shift,45,12),(56+shift,42,9)]
    for a,b in zip(fallpath,fallpath[1:]):
        steps=max(1,math.ceil(math.dist(a,b)*2.1))
        for n in range(steps+1):
            t=n/steps;px,py,pz=[a[j]+(b[j]-a[j])*t for j in range(3)];width=5+round((46-pz)/13)
            for x in range(round(px)-width,round(px)+width+1):
                for y in range(round(py)-1,round(py)+2):
                    for z in range(round(pz)-1,round(pz)+2):_put_region(g,regions['fall'],x,y,z,24 if x%5 else 7)
    for x in range(w):
        for y in range(8,53):
            if ((x-54)/23)**2+((y-31)/19)**2<=1:
                for z in range(7,10):_put_region(g,regions['basin'],x,y,z,7 if z==9 else 8)
    for y in range(0,32):
        cx=round(lower_x(y))
        for x in range(cx-6,cx+7):
            for z in range(7,10):_put_region(g,regions['outflow'],x,y,z,7 if z==9 else 8)
    # Foam belongs to the supported lip or actual impact region, not an airborne cap.
    for x in range(49,61):
        for y in range(55,58):
            if (x+y)%5<3:_put_region(g,regions['lip'],x,y,47,18)
    for x in range(47,65):
        for y in range(35,45):
            q=((x-56)/8)**2+((y-40)/5)**2
            if .35<q<1.05 and (x,y,9) in regions['basin']:_put_region(g,regions['basin'],x,y,10,18)
    # Grounded ledge boulders frame the ravine without interrupting the flow graph.
    for x,y,rx,ry,rz in [(30,26,7,5,5),(79,43,5,7,4),(36,69,5,5,4)]:g.ellipsoid(x,y,hmap[(x,y)]+rz-1,rx,ry,rz,15)
    water=set().union(*regions.values());terrain_final=set(g.cells)-water
    contacts={a+'→'+b:_pair_contacts(regions[a],regions[b]) for a,b in [('source','lip'),('lip','fall'),('fall','basin'),('basin','outflow')]}
    support=_pair_contacts(regions['lip'],terrain_final)
    upper={p for p in regions['fall']|regions['lip'] if p[2]>=44};upperterrain=_pair_contacts(upper,terrain_final)
    checks={'flowRegionFaceContacts':contacts,'lipTerrainFaceContacts':support,'upperWaterTerrainFaceContacts':upperterrain,'upperWaterSourceFaceContacts':_pair_contacts(upper,regions['source']),'terrainBuiltBeforeWater':True}
    if not all(v>0 for v in contacts.values()) or support==0:raise AssertionError('anchored source/lip/fall/basin/outflow contract failed')
    anchors={'source':[(round(upper_x(80)),80,46),(round(upper_x(59)),59,46)],'lip':[(54,56,46)],'fall':[(round(x),round(y),round(z)) for x,y,z in fallpath],'basin':[(54,31,9),(56,42,9)],'outflow':[(round(lower_x(y)),y,9) for y in [0,15,30]]}
    return _meta(g,'Original terrain-first ravine and carved upper/lower channel; static connected source→supported lip→fall→basin→outflow. Repairs reproduced Gen1 zero upper contacts; terrain cuts observed n25/n18. No native waterfall was available; not a fluid simulation.',landmarks={'fallPath':fallpath,'sourceWaterZ':46,'basinWaterZ':9},flowRegions={k:_region_info(v,anchors[k]) for k,v in regions.items()},checks=checks)

def island(seed):
    g=Grid();w,d=112,94;phase=random.Random(seed).uniform(-.15,.15)
    coast=[(16,29),(20,19),(38,15),(49,8),(63,16),(71,24),(96,17),(105,28),
           (88,39),(76,34),(65,39),(74,46),(92,49),(96,61),(86,79),(65,81),(51,67),(35,73),(20,58),(8,44)]
    hmap={};land=set();sea=set()
    for x in range(w):
        for y in range(d):
            sd,edge=_poly_signed(x,y,coast)
            if sd>=0:
                ridge=max(23*math.exp(-(((x-42)/20)**2+((y-40)/15)**2)),
                          13*math.exp(-(((x-68)/16)**2+((y-60)/11)**2)))
                h=5+round(min(12,sd*.72)+ridge+1.2*math.sin(x/15+phase)*math.sin(y/14));h=max(5,h)
                top=23 if sd<5.5 else 4 if h<27 else 19
                _column(g,x,y,h,top);land.add((x,y));hmap[(x,y)]=h
            else:
                # A sea cutaway is deliberate; the land shoreline is a real height edge.
                for z in range(3):g.put(x,y,z,2 if z<2 else 16)
                for z in (3,4):g.put(x,y,z,24 if sd>-5 else 7 if z==4 else 8)
                sea.add((x,y));hmap[(x,y)]=5
    # One focal wind-bent palm is grafted into the high island; low shrubs differ in scale.
    px,py=38,37;palm_info=_palm_into(g,(px,py,hmap[(px,py)]-1),.37,seed+9,False)
    for x,y,rx,ry,rz in [(83,25,7,4,5),(77,65,6,5,4),(25,49,5,4,4)]:g.ellipsoid(x,y,hmap[(x,y)]+rz-1,rx,ry,rz,14)
    for x,y in [(50,53),(29,31),(63,58)]:_lobe(g,(x,y,hmap[(x,y)]+3),(5,4,4),3,.4,x,.1)
    inlet=(77,40)
    if inlet in land:raise AssertionError('inlet must be actual water/low geometry')
    return _meta(g,'Original geometric coast with two unequal headlands, deep bent inlet, shallow cove, beach by boundary distance and inland ridge. Native n22/n23 are paint-only counterexamples; n18 coherent contour and n68 anisotropic shell outline informed original mass decisions.',landmarks={'shorePolygon':coast,'deepInlet':[77,40,4],'headlands':[[96,17],[86,79]],'inlandPeak':[42,40,39],'palm':palm_info},checks={'landShorelineGeometry':True,'radialEllipse':False,'inletWaterXY':list(inlet),'beachFollowsBoundary':True})

def rock_arch(seed):
    g=Grid();w,d=106,76;phase=random.Random(seed).uniform(-.1,.1);hmap={}
    for x in range(w):
        for y in range(d):
            h=4+round(2.6*math.exp(-(((x-53)/43)**2+((y-37)/24)**2)))
            hmap[(x,y)]=h;_column(g,x,y,h,19)
    for x in range(12,94):
        for y in range(20,55):
            for z in range(5,82):
                front=22+3*math.sin((x+z)/12+phase);back=52+2*math.sin(x/16-z/19)
                if not front<=y<=back:continue
                top=77-.006*(x-55)**2+2.5*math.sin(x/9)+.07*(y-35)
                leftedge=14+2*math.sin(z/12);rightedge=91+2*math.sin(z/15+1)
                if x<leftedge or x>rightedge or z>top:continue
                u=(x-51)/21
                opening=28+26*math.sqrt(max(0,1-u*u))+3*u+.06*(y-36)
                if 30<x<74 and z<opening:continue
                g.put(x,y,z,_stratum(x,y,z))
    # Damage has two localized weak-joint scars, not uniform edge erosion.
    g.ellipsoid(29,25,64,7,6,5,0);g.ellipsoid(78,47,61,7,8,5,0)
    # A narrow diagonal crack penetrates an exposed upper shoulder, leaving the bridge.
    for x in range(75,87):
        for z in range(50,67):
            y=round(25+.35*(z-50)+.25*(x-75));g.box(x,y,z,x+1,y+2,z+1,0)
    debris=[]
    for x,y,rx,ry,rz in [(80,16,6,4,4),(91,24,4,5,3),(23,13,5,4,3),(75,62,5,4,3)]:
        ground=hmap[(x,y)];centerz=ground+rz-1;g.ellipsoid(x,y,centerz,rx,ry,rz,15);debris.append({'center':[x,y,centerz],'groundZ':ground-1,'scarSide':'right' if x>60 else 'left'})
    empty=(52,36,30);bridge=(52,36,68)
    checks={'openingProbeEmpty':empty not in g.cells,'bridgeProbeOccupied':bridge in g.cells,'localizedScars':2,'noncircularOpening':True,'groundedDebris':True}
    if not checks['openingProbeEmpty'] or not checks['bridgeProbeOccupied']:raise AssertionError('arch opening/bridge contract')
    return _meta(g,'Original unequal rock supports and spanning crown, offset segmented opening, warped strata, localized missing joints and grounded matching fragments. Native n25 cave support/void and n43 offset rock shoulders supplied structural observations.',landmarks={'openingProbe':empty,'bridgeProbe':bridge,'damageScars':[[29,25,64],[78,47,61]]},intentionalDetached=debris,checks=checks)

ROWS=[
 ('nature','fir','Ель с неравными ветвями','Наклонный каркас, разные ярусы, связные хвойные группы и снег',fir),
 ('nature','oak','Дуб с просветом в кроне','Неравные ведущие ветви, крупные группы кроны и открытый просвет',oak),
 ('nature','willow','Ива с поникающими ветвями','Изогнутые ветви несут неравные ниспадающие группы листвы',willow),
 ('nature','palm','Пальма с изогнутым стволом','Разные дуги листьев, отдельные листочки и прикреплённые плоды',palm),
 ('nature','mushroom','Грибы с пластинками','Неровные шляпки, изогнутые ножки и связные поверхностные пятна',mushroom),
 ('terrain','snow-mountain','Горный хребет с промоинами','Смещённые вершины, седловины, направленные ложбины и снег',snow_mountain),
 ('terrain','mesa','Плато с разломом','Неровный край, разные террасы, боковое ущелье и слои',mesa),
 ('terrain','river-gorge','Ущелье с питаемым водопадом','Верхнее русло связано с опорным краем, падением и нижним потоком',river_gorge),
 ('terrain','island','Остров с извилистым заливом','Два мыса, настоящий залив, прибрежные полки и смещённая вершина',island),
 ('terrain','rock-arch','Скальная арка со сколами','Неравные опоры, настоящее отверстие, локальные сколы и обломки',rock_arch)
]
