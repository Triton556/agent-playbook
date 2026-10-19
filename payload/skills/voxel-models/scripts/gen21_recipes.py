"""Targeted original Gen2.1 repairs; the delivered Gen1/Gen2 remain immutable.

World sizes are authored stylized kit targets, not measured species dimensions.
Part ownership is captured before union, so shared-cell conflicts cannot vanish
merely because one part overwrote another's palette. No imported asset geometry.
"""
import collections, copy, importlib.util, math, pathlib, random, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
for branch in ('nature','anatomy','built'):
    candidate=ROOT/'research'/'gen2'/branch
    if candidate.exists():sys.path.insert(0,str(candidate))
import library_recipes, gen2_nature as N, gen2_anatomy as A, gen2_built, gen2_root as R
from voxel_recipes import Grid, PALETTE

# A separate built-module namespace allows new roof/wood grammar without mutating
# the Gen2 module, even when both versions are generated in the same process.
_spec=importlib.util.spec_from_file_location('gen21_built_core',gen2_built.__file__)
B=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(B)
DIRS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
HEIGHTS={'fir':8,'oak':9,'willow':7,'palm':7,'mushroom':.5,
 'cottage':5,'chalet':6,'watchtower':10,'gatehouse':10,'pagoda':14,
 'snow-mountain':48,'mesa':32,'river-gorge':20,'island':10,'rock-arch':18,
 'ranger':1.9,'knight':1.95,'north':1.9,'mage':2,'farmer':1.9,
 'fox':.65,'wolf':1,'bear':1.6,'deer':2.15,'dragon':3.4,
 'blue-compact':1.72,'pickup':1.8,'bus':3.2,'tractor':2.9,'boat':4.8,
 'well':2.9,'guitar':1.05,'chest':.9,'bookshelf':1.9,'vending':1.85}
PRESERVED={'fir','mushroom','palm','willow','snow-mountain','north','mage','guitar'}

def surface_points(cells):
    return {p for p in cells if any(tuple(p[i]+d[i] for i in range(3)) not in cells for d in DIRS)}

def restore_bridges(original,retained):
    """Keep source connections when deleting opaque interior cells.
    Minimum-cost0/1 paths use existing cells for free and only original removed
    cells for bridges. They cannot alter the source exterior or invent a strut.
    """
    cells=dict(retained);restored=0
    while True:
        unseen=set(cells);groups=[]
        while unseen:
            queue=[unseen.pop()];group=set(queue)
            while queue:
                p=queue.pop()
                for d in DIRS:
                    q=tuple(p[i]+d[i] for i in range(3))
                    if q in unseen:unseen.remove(q);group.add(q);queue.append(q)
            groups.append(group)
        if len(groups)<=1:return cells,restored
        groups.sort(key=len,reverse=True);main=groups[0];target=groups[-1]
        distance={p:0 for p in target};previous={};queue=collections.deque(sorted(target));found=None
        while queue:
            p=queue.popleft()
            if p in main:found=p;break
            for d in DIRS:
                q=tuple(p[i]+d[i] for i in range(3))
                if q not in original:continue
                cost=0 if q in cells else 1;dd=distance[p]+cost
                if q not in distance or dd<distance[q]:
                    distance[q]=dd;previous[q]=p
                    (queue.appendleft if cost==0 else queue.append)(q)
        if found is None:raise ValueError('Disconnected source needs declared island policy before hollow storage')
        p=found
        while p not in target:
            if p not in cells:cells[p]=original[p];restored+=1
            p=previous[p]

def leaf_shell(g,thickness=3,colors=(3,4,5)):
    """Preserve outer leaf cells and all wood; removable core is not a load core.

    Keep the original filled occupancy as opaque mesh source: exporting new inner
    shell faces would increase mesh complexity without a visible benefit.
    """
    before=dict(g.cells); selected={p for p,c in before.items() if c in colors}
    depth={};queue=collections.deque()
    for p in selected:
        if any(tuple(p[i]+d[i] for i in range(3)) not in before for d in DIRS):depth[p]=1;queue.append(p)
    while queue:
        p=queue.popleft()
        for d in DIRS:
            q=tuple(p[i]+d[i] for i in range(3))
            if q in selected and q not in depth:depth[q]=depth[p]+1;queue.append(q)
    remove={p for p in selected if depth.get(p,999)>thickness}
    for p in remove:g.cells.pop(p)
    g.cells,bridged=restore_bridges(before,g.cells)
    g.opaque_mesh_source=before
    g.gen2_meta['storageOptimization']={'scope':'opaque foliage master only','shellThickness':thickness,'removedHiddenCells':len(remove)-bridged,'restoredConnectivityCells':bridged,'outerSurfaceUnchanged':surface_points(before)<=set(g.cells),'meshPolicy':'use retained original opaque filled occupancy, omit artificial inaccessible inner faces','caveat':'not a volume/collision mesh; no FPS measurement'}
    return g

def grain(g,axis,phase=0,allowed=(1,2)):
    # One coherent abrasion/grain region, never the old skin-yellow stripe.
    for p,c in list(g.cells.items()):
        if c not in allowed:continue
        a=p[axis];b=p[(axis+1)%3];d=p[(axis+2)%3]
        if (b+phase)%19 in (0,1) and (a+phase)%37<22:g.cells[p]=2 if c==1 else 11
B.grain=grain

def pitched_roof(g,x0,x1,y0,y1,h,c=10,phase=0):
    mid=(y0+y1-1)/2;course_width=5
    for y in range(y0,y1):
        base=h+round((min(mid-y0,y1-1-mid)-abs(y-mid))*.78)
        course=(y-y0)//course_width
        for x in range(x0,x1):
            tile=(x-x0+course%2*5)//10
            choice=(tile*11+course*7+phase*3)%9
            col=(10 if choice<5 else 11 if choice<8 else 1) if c==10 else (1 if choice<5 else 2 if choice<8 else 11)
            # Continuous two-cell underlay, separate overlapping tile edges.
            g.box(x,y,base,x+1,y+1,base+2,c)
            edge=1 if (y-y0)%5==0 else 0
            height=base+3+edge
            if (x+course*5-x0)%10==0:height-=1
            if choice==8 and (x-x0)%10<3 and (y-y0)%5<2:height-=1
            g.box(x,y,base+2,x+1,y+1,height,col)
    ridge=h+round((min(mid-y0,y1-1-mid))*.78)+3
    for x in range(x0,x1):g.box(x,int(mid),ridge,x+1,int(mid)+2,ridge+2,10 if c==10 and x//8%4 else c)
    return ridge
B.pitched_roof=pitched_roof

def wear(g,slug,seed):
    """Cause-based surface patches: rain at bases, use at grips, edge loss.
    Large intentional quiet surfaces survive; no global independent-cell noise.
    """
    surf=surface_points(g.cells)
    for p in sorted(surf):
        x,y,z=p;c=g.cells.get(p)
        field=math.sin(x*.13+y*.06)+.8*math.cos(y*.17-z*.10)+.4*math.sin(z*.26+x*.06)
        if c in (14,15) and slug in ('watchtower','gatehouse','well'):
            # Variable stones and staggered seam positions instead of a grid.
            if slug in('watchtower','well'):
                cx,cy,rr=(37,37,24) if slug=='watchtower' else(44,43,28)
                u=round(math.atan2(y-cy,x-cx)*rr)
            else:u=x if (x,y-1,z) not in g.cells or (x,y+1,z) not in g.cells else y
            level=z+round(1.2*math.sin(u*.11)+.7*math.sin(u*.04))
            course=level//7;width=10+course%4;stagger=(course*7)%11
            tile=(u+stagger)//width;choice=(course*19+tile*5+seed)%17
            seam=level%7==0 or (u+stagger)%width==0
            g.cells[p]=15 if seam else 9 if choice==0 else 15 if choice==7 else 14
            if 3<z<17 and field>.8:g.cells[p]=27 if z>10 else 3
        elif c in (18,9) and slug in ('cottage','pagoda') and z>4:
            if field<-.9:g.cells[p]=9
            elif z<13 and field>.6:g.cells[p]=19
        elif c in (1,2,11) and slug in ('cottage','chalet','pagoda','well','chest','bookshelf','boat'):
            if field>1.45:g.cells[p]=11 if c==2 else 2
            elif field<-1.4:g.cells[p]=1
        elif c==22 and slug=='vending' and z<21 and field>.5:g.cells[p]=10 if field<1.2 else 11
        elif c==22 and slug=='pagoda' and field>1.15:g.cells[p]=10 if z>20 else 11
        elif c in(3,4) and slug=='pagoda' and z>30:
            if field>1.25:g.cells[p]=5
            elif field<-1.3:g.cells[p]=3
    # Geometric loss is bounded to exposed skin/edges; cavities and load paths stay.
    if slug in ('watchtower','gatehouse','well'):
        for p in sorted(surf):
            x,y,z=p
            if z>12 and (x*13+y*7+z*3+seed)%337==0 and sum(tuple(p[i]+d[i] for i in range(3)) not in g.cells for d in DIRS)>=3:g.cells.pop(p,None)
    if slug=='chest':
        for x in range(30,45):
            for z in range(12,17):
                if (x,7,z) in g.cells and (x+z)%5<2:g.put(x,7,z,11)
    if slug=='bookshelf':
        # Remove yellow skin-tone stripe on frame only; leave book pigments/pages.
        for p,c in list(g.cells.items()):
            x,y,z=p
            if c==16 and (x<=11 or x>=75 or z in range(92,95) or y>=28):g.cells[p]=2
        # Top bay is18 cells tall, unlike the lower22-cell bays. Its books must
        # stop below the cap, not overwrite it with a yellow/purple page stripe.
        for p in list(g.cells):
            x,y,z=p
            if 11<=x<75 and 7<=y<28 and z>=91:g.cells.pop(p)
        g.box(7,6,92,79,31,95,2)
        g.gen2_meta['airGapSamples']=[[x,12,91] for x in(14,21,29,58,64,71)]
    return g

def built(slug,seed):
    g=getattr(B,slug)(seed)
    if slug=='cottage':
        # End-window reveal has actual mullion, frame and a displaced shutter.
        for y in (29,41):g.box(7,y,17,10,y+2,32,1)
        for z in (17,30):g.box(7,29,z,10,43,z+2,1)
        g.box(7,35,18,9,37,31,1);g.box(5,44,18,7,54,31,2)
    if slug=='chalet':
        for p,c in list(g.cells.items()):
            if c==6:g.cells[p]=1
        tops={}
        for (x,y,z),c in g.cells.items():
            if c in (1,2,11) and z>=55:tops[x,y]=max(z,tops.get((x,y),0))
        for (x,y),z in tops.items():
            exposure=math.sin((x-6)/19)+.7*math.cos((y-44)/15)+.5*math.sin((x+y)/23)
            if 11+2*math.sin(y*.1)<x<89+2*math.cos(y*.13) and exposure>.05:
                depth=1+max(0,round((exposure+.5)*1.4))
                # Attached snow with scalloped melt boundaries, broad drift zones.
                ideal=55+round((31.5-abs(y-50.5))*.78)+3
                top=max(z+2,ideal+2+min(depth,4))
                for zz in range(z+1,top+1):g.put(x,y,zz,6 if zz>=top-1 else 25)
    wear(g,slug,seed)
    g.gen2_meta['repair']='staggered tile geometry, coherent material variation and location-based wear; functional side selected by camera contract'
    return g

def eyes(g,slug):
    y,z={'fox':(-18,62),'wolf':(-19,65),'bear':(-18,52),'deer':(-17,80),'dragon':(-24,71)}[slug]
    masks={}
    for side in (-1,1):
        region=set()
        # Locate the actual head surface, not an internal guessed eye point.
        for yy in range(y-2,y+3):
            for zz in range(z-1,z+2):
                xs=[x for x,qy,qz in g.cells if qy==yy and qz==zz]
                if not xs:continue
                x=max(xs) if side>0 else min(xs)
                g.put(x,yy,zz,12);region.add((x,yy,zz))
        if region:
            p=max(region,key=lambda p:p[2]);g.put(*p,18);region.remove(p)
        masks['left-eye' if side<0 else 'right-eye']=region
    g.semantic_parts.update(masks)
    g.gen2_meta['eyeZones']={k:[list(p) for p in sorted(v)] for k,v in masks.items()}
    return g

def ranger(seed):
    g,feet,j=A.human_core(seed,'ranger',3,19,[(-22,-2,52),(-28,-9,54)],[(20,-4,57),(17,-17,61)])
    A.tunic_hem(g,3,32,41,12,8);A.collar(g,4);A.hair(g,2)
    # Crooked wide hat and a visible feather preserve the Gen1 character cue.
    for z in range(86,98):
        rr=11-(z-86)*.72;g.ellipsoid((z-86)*.28,0,z,max(rr,2),max(rr*.8,2),1.1,3)
    g.ellipsoid(-1,0,87,16,12,1.8,3);g.ellipsoid(-1,-.5,89,10.7,9,1.2,2)
    A.segment(g,(-8,0,92),(-14,2,105),1,1,18)
    g.box(-8,5,45,9,13,64,1)
    for side in(-1,1):A.segment(g,(side*8,-7,62),(side*6,-7,45),1.2,1.2,2)
    # Left hand holds the bow's central grip; right rests on an attached arrow.
    bow=Grid();A.chain(bow,[(-35,-9,30),(-32,-9,42),(-29,-9,54),(-32,-9,66),(-35,-9,78)],[1.5]*5,2)
    A.segment(bow,(-35,-9,30),(-35,-9,78),.8,.8,18)
    A.segment(bow,(-29,-9,48),(-29,-9,60),2.2,2.2,1)
    g.cells.update(bow.cells)
    A.segment(g,(-28,-9,55),(17,-17,61),.7,.7,2)
    g=A.finish(g,'ranger',feet,j,'stylized crooked wide hat/feather, quiver, left hand on bow grip and right hand on arrow; scouting scope removed')
    g.semantic_parts={'bow':set(bow.cells),'left-hand':{p for p,c in g.cells.items() if c==16 and math.dist(p,(-28,-9,54))<4.5}}
    g.gen2_meta['grips']=[{'part':'bow','hand':'left-hand','point':[-29,-9,54],'action':'carry a bow; arrow rests in right hand'}]
    return g

def knight(seed):
    g=A.knight(seed)
    # Retain body/helmet/pose; align the blade centerline with hilt and hand.
    for p in list(g.cells):
        x,y,z=p
        if 25<=x<=44 and -12<=y<=-6 and z>=69:g.cells.pop(p)
    A.segment(g,(28,-9,69),(28,-9,97),2.3,.65,25)
    g.semantic_parts={'sword-grip':{p for p,c in g.cells.items() if c==1 and math.dist(p,(28,-9,64))<6},'right-hand':{p for p,c in g.cells.items() if c==16 and math.dist(p,(28,-9,65))<5}}
    g.gen2_meta['grips']=[{'part':'sword-grip','hand':'right-hand','point':[28,-9,65],'action':'upright sword held through central hilt axis'}]
    return g

def farmer(seed):
    # Repose the basket arm downward; action is carrying rather than offering.
    g=A.farmer(seed)
    for p in list(g.cells):
        x,y,z=p
        if x>=17 and z<62:g.cells.pop(p)
    A.chain(g,[(14,0,64),(21,0,49),(23,-2,39)],[5.7,4.5,3.1],18)
    g.ellipsoid(23,-2,39,3.6,3.7,4.1,16)
    basket=Grid();basket.box(17,-9,15,35,4,29,2);basket.box(20,-6,18,32,1,31,0)
    for z in(18,22,26):basket.box(17,-10,z,35,-8,z+1,1)
    A.chain(basket,[(17,-2,28),(19,-2,34),(23,-2,39),(31,-2,34),(34,-2,28)],[1.6]*5,1)
    for x,y,c in[(23,-3,22),(28,-4,17),(26,-2,4)]:basket.ellipsoid(x,y,23,3,3,3,c)
    g.cells.update(basket.cells);g.semantic_parts={'basket':set(basket.cells),'right-hand':{p for p,c in g.cells.items() if c==16 and math.dist(p,(23,-2,39))<5}}
    g.gen2_meta['jointLandmarks']['right-arm']={'shoulder':[14,0,64],'elbow':[21,0,49],'wrist':[23,-2,39]}
    g.gen2_meta['grips']=[{'part':'basket','hand':'right-hand','point':[23,-2,39],'action':'carry harvest basket at hip height'}]
    return g

def creature(slug,seed):
    g=getattr(A,slug)(seed);g.semantic_parts={}
    if slug=='wolf':
        # Replace tail mass, preserve hip connection; add directional tufts.
        for p in list(g.cells):
            if p[1]>58:g.cells.pop(p)
        lean=random.Random(seed).choice((-3,3))
        A.chain(g,[(0,54,45),(lean,66,40),(lean*2,79,31)],[7,5,1.5],15)
        for i in range(7):
            y=60+i*3;z=43-i*1.3
            A.segment(g,(lean*(y-54)/15,y,z),(lean*(y-54)/15-3,y+3,z-4),2.5,1,15)
        # Neck ruff's white patch has directional flow, no circular side discs.
        for p,c in list(g.cells.items()):
            x,y,z=p
            if c==9 and y<14 and z>42:g.cells[p]=15 if z>48+(y+5)*.45+math.sin(x*.5)*2 else 9
    if slug=='dragon':
        # Old wing palettes are exclusively membrane20/frame3 above the torso.
        for p,c in list(g.cells.items()):
            if p[2]>=42 and abs(p[0])>17 and c in(3,20):g.cells.pop(p)
        g.ellipsoid(0,20,44,20,29,22,4)
        for side in(-1,1):
            root=(side*15,10,55);elbow=(side*34,15,76)
            tips=[(side*66,18,103),(side*65,43,83),(side*48,63,66),(side*27,52,48)]
            wing=Grid();A.segment(wing,root,elbow,3.4,2.7,3)
            for t in tips:A.segment(wing,elbow,t,2.2,.9,3)
            # Each membrane edge sags toward the elbow between finger tips.
            for a,b in zip(tips,tips[1:]):
                last=a
                for n in range(1,25):
                    t=n/24;sag=math.sin(math.pi*t)*.28
                    p=tuple((1-sag)*((1-t)*a[k]+t*b[k])+sag*elbow[k] for k in range(3))
                    A.triangle(wing,elbow,last,p,20);last=p
            A.triangle(wing,root,elbow,tips[-1],20)
            g.cells.update(wing.cells);g.semantic_parts['left-wing' if side<0 else'right-wing']=set(wing.cells)
        g.gen2_meta['wingContract']='attached root and radiating fingers; concave membrane edges between tips, no wing-root clearance rule'
    eyes(g,slug)
    if slug in ('fox','wolf','bear','dragon'):
        # A detailed opaque render master can omit unseen core cells while
        # retaining exactly its authored outer shape and original mesh boundary.
        leaf_shell(g,3,tuple(range(1,28)))
        g.gen2_meta['storageOptimization']['scope']='opaque static creature render master; not a filled simulation volume'
    return g

def terrain(slug,seed):
    g=getattr(N,slug.replace('-','_'))(seed)
    if slug=='river-gorge':
        # Damp temperate ravine: vegetation follows exposed land near the water.
        tops={}
        for (x,y,z),c in g.cells.items():
            if c not in(7,8,24,18):tops[x,y]=max(z,tops.get((x,y),-1))
        for (x,y),z in tops.items():
            near=min(abs(x-54-7*math.sin(y/12)),abs(x-54))
            if 8<near<22 and (x,y,z+1) not in g.cells and z<52:g.put(x,y,z,4 if near<15 else 19)
        for x,y in((30,15),(76,28),(34,76),(79,69)):
            z=tops.get((x,y),8);N._path(g,[(x,y,z),(x+1,y,z+13)],1.6,.8,1)
            N._lobe(g,(x+1,y,z+12),(4,3.5,5),3,.4,x,.12)
        g.gen2_meta['biome']='temperate riparian gorge; green damp lower banks, rock upper ledges'
    elif slug=='rock-arch':
        # Broad edge notches/joint fractures; preserve the approved spanning core.
        for p in list(g.cells):
            x,y,z=p
            if 15<z<62 and ((x<20 and math.sin(z*.25+y*.18)>1.0) or (x>85 and math.cos(z*.23-y*.2)>.7)):g.cells.pop(p)
            elif z>12 and (y<24+4*math.sin(x*.14+z*.19)+2*math.cos(z*.31) or y>50+4*math.sin(x*.16-z*.18)):g.cells.pop(p)
        for x,y,z,rx,ry,rz in((17,35,49,5,5,6),(88,42,31,5,6,5),(22,22,27,4,4,5)):
            g.ellipsoid(x,y,z,rx,ry,rz,0)
    elif slug=='mesa':
        # Additive fossil on an exposed sediment face; terrain form is preserved.
        bone=[]
        def exposed_bone(x,z):
            ys=[y for xx,y,zz in g.cells if xx==x and zz==z and g.cells[xx,y,zz]!=18]
            if not ys:return
            y=min(ys);g.put(x,y-1,z,18);bone.append((x,y-1,z))
        for dx in range(-8,9):exposed_bone(54+dx,24+round(1.5*math.sin(dx*.23)))
        for dx in(-6,-3,0,3,6):
            for dz in range(-4,5):exposed_bone(54+dx,24+dz)
        g.gen2_meta['easterEgg']='partial fossil spine/ribs protrude one cell from the actual exposed sediment face; approved terrain form retained'
        if bone:g.gen2_meta['detailViews']=[{'name':'fossil','bounds':[[43,65],[min(p[1] for p in bone)-3,max(p[1] for p in bone)+4],[17,31]]}]
    elif slug=='island':
        # Beach ball and SOS stones on actual dry near-shore sand.
        land=[]
        tops={}
        for (x,y,z),c in g.cells.items():tops[x,y]=max(z,tops.get((x,y),0))
        for (x,y),z in tops.items():
            if g.cells.get((x,y,z))==23 and 15<x<40 and y<40:land.append((x,y,z))
        if land:
            x,y,z=min(land,key=lambda p:abs(p[0]-24)+abs(p[1]-27))
            g.ellipsoid(x,y,z+3,2.8,2.8,2.8,18)
            for p,c in list(g.cells.items()):
                if c==18 and math.dist(p,(x,y,z+3))<3 and p[0]>=x:g.cells[p]=22
        # One small grounded shelter narrative; SOS formed from voxel stones.
        letters=[['11111','10000','11111','00001','11111'],['11111','10001','10001','10001','11111'],['11111','10000','11111','00001','11111']]
        glyphs=['0'.join(letter[y] for letter in letters) for y in range(5)]
        strokes=[(xx,yy) for yy,line in enumerate(glyphs) for xx,c in enumerate(line) if c=='1'];found=None
        for y in range(6,88):
            for x in range(6,89):
                if all(g.cells.get((x+a,y+b,tops.get((x+a,y+b),0)))==23 for a,b in strokes):found=(x,y);break
            if found:break
        if found:
            x,y=found
            for a,b in strokes:g.put(x+a,y+b,tops[x+a,y+b]+1,18)
            g.gen2_meta['detailViews']=[{'name':'sos','angleRadians':0,'bounds':[[x-2,x+19],[y-2,y+7],[min(tops[x+a,y+b] for a,b in strokes)-2,max(tops[x+a,y+b] for a,b in strokes)+5]]}]
        g.gen2_meta['easterEgg']='red/cream beach ball'+(' and complete SOS stone letters on dry sand' if found else '; no suitable dry-sand footprint for SOS')+'; approved island form retained'
    return g

def vehicle(slug,seed):
    if slug=='boat':return wear(R.vehicle('boat',seed),slug,seed)
    # Class dimensions and wheel positions are explicit, not a shared buggy SUV.
    cfg={
      'blue-compact':(96,19,42,7,[22,77],7),
      'pickup':(108,20,42,9,[24,83],22),
      'bus':(154,22,63,10,[27,100,127],18),
      'tractor':(100,19,68,0,[20,78],4)}[slug]
    length,half,h,r,axles,color=cfg;g=Grid();parts={}
    body=Grid();windshield=Grid();body.box(-half,9,10,half+1,length-6,24,color)
    body.box(-half+3,12,13,half-2,length-9,22,0)
    if slug=='bus':
        body.box(-half,9,24,half+1,length-6,h,color);body.box(-half+3,13,27,half-2,length-10,h-3,0)
        body.box(-half+3,8,36,half-2,11,h-7,8)
        for x in(-half-1,half):
            for y in range(41,length-20,19):body.box(x,y,38,x+2,y+14,h-8,8)
        # Passenger door on the visible negativeX side, tall split glazing + sill.
        body.box(-half-1,14,17,-half+2,36,h-8,8)
        for y in(14,24,34):body.box(-half-2,y,15,-half, y+2,h-6,15)
        body.box(-half-2,14,16,-half,36,18,14)
        body.box(-half+4,length-8,34,half-3,length-5,h-10,8)
    elif slug=='tractor':
        body.cells.clear();body.box(-11,4,20,12,46,38,4);body.box(-10,3,24,11,6,35,15)
        body.box(-9,31,12,10,91,26,4)
        for x in(-13,11):
            for y in(49,85):body.box(x,y,25,x+2,y+2,h-2,2)
        body.box(-16,46,h-4,17,91,h,4)
        body.box(-7,69,27,8,81,30,12);body.box(-7,78,30,8,83,42,12)
        body.box(-4,26,35,-1,29,62,15)
        for x in(-25,18):body.box(x,59,39,x+7,96,42,4)
    else:
        cabend=length-11 if slug=='blue-compact' else 64
        # Compact has short sloping nose, tall rounded cabin; pickup has a longer
        # squared hood, separate bed, dark grille and distinct headlight grammar.
        start=26 if slug=='blue-compact' else 34
        body.box(-half, start,24,half+1,cabend,h-3,color)
        body.box(-half+3,start+3,25,half-2,cabend-3,h-4,0)
        body.box(-half+2,start+2,h-3,half-1,cabend-1,h-1,color)
        body.box(-half+5,start+4,h-1,half-4,cabend-3,h,color)
        for z in range(25,h-3):
            yy=start+round((z-25)*.4)
            body.box(-half+1,start-1,z,half,yy,z+1,0)
            windshield.box(-half+3,yy,z,half-2,yy+2,z+1,8)
        body.cells.update(windshield.cells)
        for x in(-half-1,half):body.box(x,start+7,28,x+2,cabend-6,h-7,8)
        body.box(-half+3,cabend-2,28,half-2,cabend,h-7,8)
        if slug=='blue-compact':
            # Rounded shoulders and a short curved bonnet, unlike pickup hood.
            for p in list(body.cells):
                x,y,z=p
                if y<start and z>21+round((y-9)*.16):body.cells.pop(p)
                elif z>h-6 and abs(x)>half-2-round((z-(h-6))*.35):body.cells.pop(p)
            for x in(-half,half):
                for y in(45,76):body.box(x,y,18,x+1,y+1,h-6,8)
            body.box(-half-2,61,25,-half,70,27,14)
            body.box(-5,7,18,6,10,21,8)
        else:
            body.box(-half+3,66,24,half-2,length-8,27,2)
            for x in(-half,half-2):body.box(x,66,24,x+3,length-6,34,color)
            body.box(-half,length-9,24,half+1,length-6,34,color)
            body.box(-10,7,18,11,10,24,15)
            for xx in range(-9,11,4):body.box(xx,6,19,xx+2,8,23,14)
    wheels={};socket=set()
    for i,y in enumerate(axles):
        radius=(9 if i==0 else 17) if slug=='tractor' else r
        for side in(-1,1):
            x=side*(half+3);wg=Grid()
            # Narrow smooth road tires; tractor has a purposeful tread silhouette.
            for yy in range(y-radius,y+radius+1):
                for zz in range(0,2*radius+1):
                    dd=math.hypot(yy-y,zz-radius)
                    if dd<=radius:
                        col=12 if dd>radius*.67 else 15 if dd>radius*.27 else 14
                        wg.box(x-2,yy,zz,x+3,yy+1,zz+1,col)
            name=('left' if side<0 else'right')+f'-wheel-{i}';wheels[name]=set(wg.cells)
            # Subtract an expanded swept disk only near the side panel. Moving
            # tire-body gap is real; narrow axle/socket deliberately contacts hub.
            for p in list(body.cells):
                xx,yy,zz=p
                if abs(xx-x)<5 and math.hypot(yy-y,zz-radius)<=radius+2:body.cells.pop(p)
            g.cells.update(wg.cells)
            axle=Grid();axle.box(-half-3,y-1,radius-1,half+4,y+2,radius+2,15)
            body.cells.update(axle.cells);socket.update(axle.cells)
    for side in(-1,1):
        x=side*(half-6);lw=4 if slug=='blue-compact' else 6
        body.box(x-lw//2,6,25 if slug=='bus' else 19,x+lw//2+1,9,30 if slug=='bus' else 23,18)
        body.box(x-2,length-6,19,x+3,length-3,24,22)
    body.box(-half-1,6,10,half+2,10,13,14)
    if slug=='blue-compact':
        for side in(-1,1):
            x=side*(half-5);body.box(x-3,6,20,x+4,9,24,18)
    g.cells.update(body.cells);parts.update(wheels);parts['body']=set(body.cells)
    if windshield.cells:parts['windshield']=set(windshield.cells)
    g.semantic_parts=parts;g.allowed_socket_cells=socket
    g.gen2_meta={'method':'vehicle-class dimensions, independent wheel masks, carved arches, explicit axle sockets, symmetric lamps and functional door','wheelCenters':[[side*(half+3),y,(9 if i==0 else 17) if slug=='tractor' else r] for i,y in enumerate(axles) for side in(-1,1)],'wheelParts':list(wheels),'bodyClass':slug,'functionalFrontAxis':'-y','doorSide':'-x' if slug in('bus','blue-compact') else None,'cavitySamples':[],'reference':'Toyota NNP10 official2004/75years proportions for blue compact; stylized not replica','rigTested':False}
    return g

def scene(slug,seed):
    g=Grid();r=random.Random(seed);w,d=184,154;heights={};layers={'ground':set(),'water':set(),'path':set(),'dock':set()};placements=[]
    for x in range(w):
        for y in range(d):
            margin=5+3*math.sin(y*.067)+2*math.sin(x*.049+y*.021)
            if min(x,w-1-x,y,d-1-y)<margin:continue
            h=5+round(1.1*math.sin(x*.046)+1.3*math.sin(y*.041+x*.019));heights[x,y]=h
            g.box(x,y,0,x+1,y+1,h,2);g.put(x,y,h,6 if slug=='alpine-camp' else 23 if slug=='desert-market' else 4);layers['ground'].add((x,y))
    if slug=='harbour':
        for x,y in list(heights):
            if x>=88+round(5*math.sin(y*.043)):
                g.box(x,y,0,x+1,y+1,18,0);g.box(x,y,0,x+1,y+1,4,7);heights[x,y]=3;layers['water'].add((x,y));layers['ground'].discard((x,y))
    def place(name,x,y,scale,turn=0):
        part=make_model(name,seed);sz,cells=part.normalized();transformed={}
        for (a,b,c),col in cells.items():
            if turn%2:a,b=b,sz[0]-1-a
            transformed[round(a*scale),round(b*scale),round(c*scale)]=col
        # Only true contact columns get adaptive soil; no rectangular prefab pad.
        low={}
        for a,b,c in transformed:low[a,b]=min(c,low.get((a,b),999))
        contacts=[(a,b) for (a,b),z in low.items() if z<=1]
        base=max(heights.get((x+a,y+b),4) for a,b in contacts)+1
        for a,b in contacts:
            local=heights.get((x+a,y+b),4)
            for z in range(local+1,base):g.put(x+a,y+b,z,6 if slug=='alpine-camp' else 23 if slug=='desert-market' else 4)
        for (a,b,c),col in transformed.items():g.put(x+a,y+b,base+c,col)
        offset=part.gen2_meta['normalizationOffset']
        sourceanchors=part.gen2_meta.get('cavitySamples',[])
        anchors=[[x+round((a-offset[0])*scale),y+round((b-offset[1])*scale),base+round((c-offset[2])*scale)] for a,b,c in sourceanchors] if not turn else[]
        placements.append({'name':name,'origin':[x,y,base],'scale':scale,'support':'contact-footprint terrain infill, no bbox podium','normalizationOffset':offset,'functionalAnchors':anchors})
        return base,sz
    def path(points,width=7):
        for a,b in zip(points,points[1:]):
            for t in range(max(1,round(math.dist(a,b)*2))):
                tt=t/max(1,round(math.dist(a,b)*2)-1);xx,yy=[round(a[k]+(b[k]-a[k])*tt) for k in range(2)]
                for x in range(xx-width//2,xx+width//2+1):
                    for y in range(yy-width//2,yy+width//2+1):
                        if (x,y) in layers['ground']:
                            g.put(x,y,heights[x,y],23 if slug!='desert-market' else 18);layers['path'].add((x,y))
    def smoke(x,y,z):
        for i in range(6):g.ellipsoid(x+round(math.sin(i)*2),y+i//2,z+i*3,2+i*.4,2+i*.3,2,25 if i<3 else 18)
    life=[];effects=[]
    if slug=='farmstead':
        base,sz=place('cottage',12,13,.8);place('oak',19,92,.63);place('well',87,105,.32);path([(7,88),(87,91),(175,80)])
        flue=placements[0]['functionalAnchors'][2];emitter=[flue[0],flue[1],base+round(sz[2]*.8)]
        smoke(*emitter);effects.append({'kind':'smoke','sourceAsset':'cottage','socket':flue,'emitter':emitter,'attachment':'source cavity anchor transformed through actual normalizationOffset; emitter above flue outlet'});life.append('chimney smoke')
        for x in range(113,173,12):
            for y in range(16,73):
                z=heights[x,y];g.put(x,y,z,1)
                if y%8 in(2,3):g.tube((x+2,y,z+1),(x+3,y,z+8),1,4);g.put(x+3,y,z+8,26)
        for x,y in((84,20),(86,34),(89,47),(77,51)):
            z=heights[x,y];g.box(x-3,y-4,z,x+4,y+5,z+1,1);g.ellipsoid(x,y,z+3,3,3,3,4);g.put(x,y,z+6,22)
        place('farmer',95,63,.23);life.append('gardener with basket')
    elif slug=='harbour':
        place('cottage',12,14,.68);path([(14,96),(48,89),(80,76)])
        for x in range(78,142):
            for y in range(69,83):g.box(x,y,7,x+1,y+1,10,2 if x//4%3 else 1);layers['dock'].add((x,y))
        for x in(79,99,121,139):
            for y in(70,80):g.box(x,y,0,x+3,y+3,12,1)
        boat=vehicle('boat',seed);sz,cells=boat.normalized();origin=(113,89,4);hull=set()
        for (a,b,c),col in cells.items():
            xx,yy=origin[0]+round(a*.38),origin[1]+round(b*.38);zz=origin[2]+round(c*.38);g.put(xx,yy,zz,col)
            if c<20:hull.add((xx,yy))
        layers['boat-hull']=hull
        g.box(125,80,10,128,83,14,15);g.tube((126,81,13),(124,91,12),.7,18)
        for x,y in((63,66),(66,64),(69,66)):
            z=heights[x,y];g.ellipsoid(x,y,z+4,3,3,4,2)
        place('farmer',66,81,.22);life.append('dock worker, barrels and mooring rope')
    elif slug=='knight-camp':
        path([(6,87),(87,87),(174,95)])
        for x,y in((19,18),(118,110)):
            base=max(heights.get((a,b),4) for a in range(x,x+40) for b in range(y,y+27))+1
            for xx in range(40):
                top=base+3+round(18*(1-abs(xx-19)/21));g.box(x+xx,y,top,x+xx+1,y+27,top+2,9)
            for sidey in(y,y+26):
                for xx in range(40):
                    top=base+round(18*(1-abs(xx-19)/21))
                    if abs(xx-19)>6:g.box(x+xx,sidey,heights.get((x+xx,sidey),4)+1,x+xx+1,sidey+1,top+3,9)
            g.box(x+18,y,base,x+21,y+27,base+20,1)
        place('knight',88,35,.23);place('chest',60,31,.17);place('fir',14,110,.62)
        z=heights[90,116];g.ellipsoid(90,116,z+1,7,7,2,14);g.tube((84,114,z+3),(96,119,z+3),1,1);g.ellipsoid(90,116,z+6,2,2,4,17)
        z=heights[70,51];g.box(70,51,z,72,53,z+52,1)
        for x in range(72,93):
            for zz in range(z+32,z+48-round((x-72)/7)):g.put(x,52,zz,22 if x<87 else 13)
        life+=['camp fire','restored banner','open tent entrance']
    elif slug=='alpine-camp':
        place('chalet',65,26,.75);place('north',91,110,.25)
        for x,y,s in((9,12,.68),(136,19,.8),(18,113,.53),(143,114,.48)):place('fir',x,y,s)
        path([(8,90),(90,91),(150,106)]);life.append('traveller holding an axe')
    else:
        # Dry stone market house with flat sun roof, no unexplained cold-climate
        # pitched cottage chimney. Bread can be baked in desert towns elsewhere.
        z=heights[15,19]+1;g.box(13,18,z,62,61,z+28,9);g.box(17,22,z+2,58,57,z+28,0);g.box(31,16,z,42,24,z+19,0)
        g.box(11,16,z+28,64,63,z+31,23);g.box(12,18,z+30,15,62,z+35,9);g.box(60,18,z+30,63,62,z+35,9)
        place('palm',103,13,.9);place('chest',114,109,.17);path([(7,89),(91,88),(176,102)])
        for x,y in((85,21),(31,109)):
            z=max(heights.get((x+a,y+b),4) for a,b in((0,0),(43,0),(0,27),(43,27)))+1
            for xx,yy in((x,y),(x+43,y),(x,y+27),(x+43,y+27)):g.box(xx,yy,heights.get((xx,yy),4),xx+2,yy+2,z+27,1)
            for xx in range(x-2,x+49):
                top=z+25-round(3*math.sin((xx-x)/48*math.pi));g.box(xx,y-2,top,xx+1,y+31,top+2,18 if xx%13<8 else 22)
            g.box(x+4,y+5,z,x+40,y+17,z+11,2)
            for xx in range(x+7,x+39,7):g.ellipsoid(xx,y+10,z+13,2.8,2.8,2.5,26 if xx%2 else 17)
        place('farmer',94,74,.22);life.append('seller and stocked fruit stalls')
    g.semantic_layers=layers
    g.gen2_meta={'method':'terrain contact footprints, era/biome-specific modules, explicit land/water masks and life anchors','sceneCellPitchMeters':.08,'worldHeightMeters':None,'era':'medieval fantasy','biome':'desert' if slug=='desert-market' else 'alpine' if slug=='alpine-camp' else 'temperate','placements':placements,'lifeAnchors':life,'effects':effects,'layerColumnCounts':{k:len(v) for k,v in layers.items()},'physicalSimulation':False}
    return g

BASE_ROWS=sum((m.ROWS for m in(N,A,gen2_built,R)),[])
def make_model(slug,seed=153):
    group=next(r[0] for r in BASE_ROWS if r[1]==slug)
    if group=='scenes':g=scene(slug,seed)
    elif slug in PRESERVED:g=next(r[4] for r in BASE_ROWS if r[1]==slug)(seed)
    elif group=='architecture' or group=='props':g=built(slug,seed)
    elif group=='characters':g={'ranger':ranger,'knight':knight,'farmer':farmer}[slug](seed)
    elif group=='creatures':g=creature(slug,seed)
    elif group=='terrain':g=terrain(slug,seed)
    elif group=='transport':g=vehicle(slug,seed)
    else:g=N.oak(seed);leaf_shell(g)
    g.gen2_meta=getattr(g,'gen2_meta',{})
    sz,_=g.normalized();dimension_axis=1 if slug=='guitar' else 2;pitch=.08 if group=='scenes' else HEIGHTS[slug]/sz[dimension_axis]
    g.gen2_meta.update({'version':'gen2.1','facingAxis':'+z' if slug=='guitar' else '-y','functionalCameraRadians':math.pi/2 if slug=='well' else math.pi,'primaryDimensionAxis':'y' if slug=='guitar' else 'z','targetPrimaryExtentMeters':HEIGHTS.get(slug),'voxelPitchMeters':pitch,'worldHeightMeters':sz[2]*pitch,'worldDimensionsMeters':[n*pitch for n in sz],'scaleEvidence':'authored stylized kit target; Toyota compact dimensions use NNP10 official archive; guitar1.05 is lengthY, not thicknessZ; other sizes are design assumptions','style':'stylized detailed voxel master, approved silhouettes preserved','unchangedApprovedGeometry':slug in PRESERVED,'normalizationOffset':[min(p[i] for p in g.cells) for i in range(3)],'coordinateSpace':'all semantic anchors/masks use authored grid; exported coordinate = authored - normalizationOffset'})
    g.semantic_parts=getattr(g,'semantic_parts',{})
    return g

ROWS=[(group,slug,('Разведчик в шляпе с луком' if slug=='ranger' else title),'Локальные правки по приёмке; масштаб, функция и контекст проверяются отдельно',lambda seed,slug=slug:make_model(slug,seed)) for group,slug,title,_,_ in BASE_ROWS]
