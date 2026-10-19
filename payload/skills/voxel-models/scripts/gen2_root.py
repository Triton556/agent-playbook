"""Original Gen2 vehicle and scene construction. No imported source geometry."""
import math,random,sys,pathlib
import library_recipes
from voxel_recipes import Grid,PALETTE
def load_branches():
 import gen2_nature,gen2_anatomy,gen2_built
 return {r[1]:r[4] for m in (gen2_nature,gen2_anatomy,gen2_built) for r in m.ROWS}
def wheel(g,x,y,r,z=None):
 z=r if z is None else z
 for yy in range(y-r,y+r+1):
  for zz in range(z-r,z+r+1):
   d=math.hypot(yy-y,zz-z)
   if d<=r:
    c=12 if d>r*.66 else 15 if d>r*.24 else 14
    g.box(x-3,yy,zz,x+4,yy+1,zz+1,c)
    if r*.7<d<r-1 and (round(math.atan2(zz-z,yy-y)*8/math.pi)%3==0):g.put(x+(4 if x>0 else -4),yy,zz,15)
def vehicle(kind,seed):
 r=random.Random(seed);g=Grid()
 if kind=='boat':
  # Unequal bow/stern, real open cockpit and a continuous keel/sidewall.
  for y in range(103):
   w=max(3,round(18*(math.sin(math.pi*(y+4)/111))**.7))
   for z in range(20):
    ww=max(2,w-round(max(0,11-z)*.55));g.box(-ww,y,z,ww+1,y+1,z+1,1 if z<5 else 11)
    if z>=8 and 7<y<95:g.box(-ww+3,y,z,ww-2,y+1,z+1,0)
   if y%9<2:g.box(-w,y,18,w+1,y+1,20,2)
  g.box(-13,32,12,14,37,15,2);g.box(-10,69,12,11,74,15,2)
  g.tube((0,48,8),(2,48,88),2,2)
  for z in range(27,81):
   reach=round(32*(81-z)/54)
   g.box(2,48,z,3+reach,50,z+1,18 if z%14>1 else 23)
  g.tube((2,48,77),(0,8,20),.8,18);g.tube((2,48,77),(0,94,20),.8,18)
  g.box(-7,96,10,8,100,13,2)
  g.gen2_meta={'method':'open tapered hull, unequal bow/stern, benches, mast and attached sail; local gunwale wear','cavitySamples':[[0,25,17],[0,65,17]],'intentionalDetached':False}
  return g
 length={'blue-compact':84,'pickup':96,'bus':120,'tractor':68}[kind]
 color={'blue-compact':7,'pickup':22,'bus':18,'tractor':4}[kind]
 g.box(-17,12,10,18,length-4,22,color);g.box(-12,12,9,13,length-3,12,15)
 front,back=(24,length-21)
 for x in (-20,20):
  wheel(g,x,front,11 if kind!='tractor' else 10)
  wheel(g,x,back,11 if kind!='tractor' else 17)
 if kind=='bus':
  for x in (-20,20):wheel(g,x,length-37,11)
  g.box(-19,10,20,20,length,48,color);g.box(-16,13,23,17,length-3,45,0)
  g.box(-16,10,29,17,12,44,8);g.box(-16,length-2,29,17,length,43,8)
  for y in range(18,length-10,17):
   for x in (-20,18):g.box(x,y,30,x+2,y+12,44,8)
  # Functional passenger door on one side, one open vent at the back.
  g.box(18,15,13,20,32,44,8);g.box(20,15,12,22,32,15,15)
  g.box(-8,length-1,20,10,length+1,23,15)
 elif kind=='tractor':
  g.box(-11,4,18,12,33,32,4);g.box(-9,3,23,10,5,30,15)
  for x in (-11,9):
   for y in (38,59):g.box(x,y,25,x+2,y+2,58,2)
  g.box(-14,36,57,15,64,61,4);g.box(-9,50,25,10,61,31,1)
  g.box(-4,25,27,-1,28,57,15);g.box(-5,24,56,0,29,59,12)
  g.box(-7,45,31,8,57,34,12);g.box(-7,54,34,8,58,43,12)
  for x in (-20,16):g.box(x,back-18,30,x+5,back+18,33,4)
  g.box(-12,length,12,13,length+4,15,15)
 else:
  cabend=length-7 if kind=='blue-compact' else 56
  g.box(-17,18,22,18,cabend,39,color);g.box(-14,23,24,15,cabend-3,38,0)
  g.box(-15,17,29,16,20,38,8);g.box(-15,cabend-2,28,16,cabend,37,8)
  for x in (-18,16):g.box(x,25,28,x+2,cabend-7,37,8)
  # Roof shoulders are stepped, not a box with painted windows.
  g.box(-16,20,39,17,cabend-1,41,color);g.box(-13,22,41,14,cabend-2,43,color)
  g.box(-15,30,25,-13,47,35,color);g.box(15,30,25,17,45,35,color)
  if kind=='blue-compact':
   # Porte-inspired blue sliding-door compact; original stylized geometry.
   g.box(17,45,22,19,73,27,7);g.box(19,52,27,20,61,29,14)
   g.box(-20,35,27,-18,42,29,14);g.box(-2,19,38,10,21,39,12)
  else:
   g.box(-16,58,22,17,length-4,25,2);g.box(-16,58,25,-13,length-4,33,color);g.box(14,58,25,17,length-4,33,color);g.box(-16,length-7,25,17,length-4,33,color)
   for y in (62,73,85):g.box(-13,y,25,14,y+2,26,1)
  # Replace the upper front slab by a raked screen and stepped roof shoulder.
  for z in range(30,42):
   lip=17+round((z-30)*.35)
   g.box(-16,16,z,17,lip,z+1,0)
   g.box(-14,lip,z,15,lip+1,z+1,8 if z<39 else color)
  # Recessed door seam and a bounded scratch on the usage side.
  for yy in (29,cabend-6):
   for z in range(24,37):
    if (17,yy,z) in g.cells:g.put(17,yy,z,15)
  for yy in range(cabend-22,cabend-9):
   zz=23+(yy//5)%2
   if (-17,yy,zz) in g.cells:g.put(-17,yy,zz,14)
 g.box(-19,9,12,20,12,16,14);g.box(-19,length-3,12,20,length,16,15)
 for x in (-14,9):g.box(x,8,23,x+6,10,27,18);g.box(x,length-1,22,x+5,length+1,27,22)
 # Quiet body panels; only usage/contact regions receive coherent wear.
 for y in (back-9,back-3,back+4):
  for x in (-18,17):
   for zz in range(13,17):
    if (x,y,zz) in g.cells:g.put(x,y,zz,1 if kind=='tractor' else 15)
 for yy in range(33,47):
  if (18,yy,22) in g.cells:g.put(18,yy,22,14)
 g.gen2_meta={'method':'stepped body shell, declared cab openings, oriented wheels, functional one-sided details and localized use wear','wheelCenters':[[x,y,11 if kind!='tractor' else (10 if y==front else 17)] for x in (-20,20) for y in (front,back)],'cavitySamples':[] if kind=='tractor' else ([[0,40,33]] if kind!='bus' else [[0,45,36]]),'rigTested':False}
 return g
def stamp(g,part,x,y,z,scale=1,turn=0):
 size,cells=part.normalized()
 for (a,b,c),color in cells.items():
  if turn%2:a,b=b,size[0]-1-a
  g.put(x+round(a*scale),y+round(b*scale),z+round(c*scale),color)
def scene(kind,seed):
 r=random.Random(seed);g=Grid();w,d=184,154
 # Continuous vignette edge; undulating surface with deliberate building pads.
 heights={}
 for x in range(w):
  for y in range(d):
   margin=5+3*math.sin(y*.067)+2*math.sin(x*.049+y*.021)
   if min(x,w-1-x,y,d-1-y)<margin:continue
   h=5+round(1.1*math.sin(x*.046)+1.3*math.sin(y*.041+x*.019));heights[x,y]=h
   g.box(x,y,0,x+1,y+1,h,2);g.put(x,y,h,6 if kind=='alpine-camp' else 23 if kind=='desert-market' else 4)
 make=load_branches()
 def pad(x,y,ww,dd):
  z=max(heights.get((a,b),3) for a in range(x,x+ww) for b in range(y,y+dd))+1
  for a in range(x,x+ww):
   for b in range(y,y+dd):g.box(a,b,0,a+1,b+1,z,2)
  return z
 def place(slug,x,y,scale=.55,turn=0):
  part=make[slug](seed);sz,_=part.normalized();ww,dd=round(sz[0]*scale)+1,round(sz[1]*scale)+1
  if turn%2:ww,dd=dd,ww
  z=pad(x,y,ww,dd);stamp(g,part,x,y,z,scale,turn)
 def path(ybase,width=11):
  for x in range(6,w-5):
   cy=ybase+round(5*math.sin(x*.036))
   for y in range(cy-width//2,cy+width//2):
    if (x,y) in heights:g.put(x,y,heights[x,y],23 if kind!='desert-market' else 18)
 if kind=='farmstead':
  place('cottage',12,13,.8);place('oak',19,102,.63);place('well',87,105,.32);path(88)
  for x in range(112,172,12):
   for y in range(16,74):
    z=heights.get((x,y),4);g.box(x,y,z,x+5,y+1,z+1,1)
    if y%8 in (2,3):g.tube((x+2,y,z+1),(x+3,y,z+9),1,4);g.put(x+3,y,z+9,26)
  for x in range(95,173,13):
   z=heights.get((x,108),4)+1;g.box(x,108,z,x+2,110,z+13,1)
  g.box(95,108,13,174,110,15,2)
 elif kind=='harbour':
  # Coast is a designed curve, with continuous water and grounded pier piles.
  for x in range(80,w):
   edge=88+round(8*math.sin(x*.043))
   for y in range(max(5,edge-43),d-5):
    g.box(x,y,3,x+1,y+1,18,0);g.box(x,y,0,x+1,y+1,4,7)
  place('cottage',12,14,.68);place('vending',14,101,.24)
  for x in range(73,154):
   for y in range(69,89):g.box(x,y,8,x+1,y+1,11,2 if (x//4)%2 else 1)
  for x in (74,102,133,151):
   for y in (70,86):g.box(x,y,0,x+3,y+3,13,1)
  stamp(g,vehicle('boat',seed),119,35,4,.43,1);path(120)
 else:
  path(87)
  if kind=='knight-camp':
   for x,y in ((20,20),(113,108)):
    z=pad(x,y,46,32);g.box(x,y,z,x+46,y+32,z+2,1)
    for xx in range(46):
     top=z+3+round(20*(1-abs(xx-22)/24))
     g.box(x+xx,y,top,x+xx+1,y+32,top+2,9)
    for yy in (y,y+31):g.box(x+21,yy,z+2,x+24,yy+1,z+24,1)
   place('knight',87,25,.23);place('chest',133,25,.17);place('fir',13,107,.62)
   z=pad(81,110,17,17);g.ellipsoid(89,118,z+2,9,8,2,14);g.tube((83,113,z+3),(96,121,z+3),1,1);g.ellipsoid(90,117,z+7,3,3,6,17)
  elif kind=='alpine-camp':
   place('chalet',65,26,.75);place('north',88,109,.25)
   for x,y,s in ((9,12,.68),(135,18,.8),(18,113,.53),(143,114,.48)):place('fir',x,y,s)
  else:
   place('cottage',12,17,.65);place('palm',136,13,.9);place('chest',113,108,.17)
   for x,y in ((85,21),(31,109)):
    z=pad(x,y,47,30)
    for xx,yy in ((x,y),(x+44,y),(x,y+27),(x+44,y+27)):g.box(xx,yy,z,xx+2,yy+2,z+28,1)
    for xx in range(x-2,x+49):
     top=z+26-round(3*math.sin((xx-x)/48*math.pi));g.box(xx,y-2,top,xx+1,y+32,top+2,18 if xx%12<8 else 22)
    g.box(x+4,y+5,z,x+40,y+17,z+12,2)
    for xx in range(x+7,x+38,8):g.ellipsoid(xx,y+10,z+13,3,3,2,26)
 # Grounded, asymmetric rock cluster near the trail, with a visible cause/location.
 for x,y,rx in ((49,95,5),(54,99,3),(58,95,2)):
  z=heights.get((x,y),4);g.ellipsoid(x,y,z+2,rx,rx*.75,3,14)
 g.gen2_meta={'method':'continuous shaped base, functional pads, meandering path and role-scaled modules; original detailed assets assembled with human/building/prop hierarchy','sceneCellPitchMeters':.08,'kitResamplingScale':'.17–.9; intentional role-height conversion to scene grid, not a runtime LOD','roleHeightsMeters':{'standingHuman':'1.8–1.9','chest':'.9','coveredWell':'2.9','house':'4.3–5.4','tree':'4–8'},'intentionalDetached':True,'terrainSupport':'solid base and localized pads; harbor water and pier piles explicit','physicalSimulation':False}
 return g
ROWS=[*[('transport',k,t,'Силуэт кузова, функциональные проёмы и следы использования',lambda seed,k=k:vehicle(k,seed)) for k,t in [('blue-compact','Синий компактный автомобиль'),('pickup','Рабочий пикап'),('bus','Городской автобус'),('tractor','Фермерский трактор'),('boat','Парусная лодка')]],*[('scenes',k,t,'Связный маршрут, неровная основа и осмысленные места предметов',lambda seed,k=k:scene(k,seed)) for k,t in [('knight-camp','Рыцарский лагерь'),('farmstead','Ферма с полями'),('harbour','Гавань'),('alpine-camp','Северный лагерь'),('desert-market','Пустынный рынок')]]]
