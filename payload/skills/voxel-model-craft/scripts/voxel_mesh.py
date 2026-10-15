"""Original palette-preserving visible-face and greedy-rectangle mesher.

No source code from studied assets is used. Input cell coordinates are z-up.
Merging keys include axis, sign, plane and palette index. AO/UV/translucency need
additional keys in a production renderer; this baseline handles opaque colors.
"""
import argparse,collections,json,pathlib,random
from voxel_recipes import RECIPES,PALETTE,Grid

def surface(cells):
    masks=collections.defaultdict(set)
    for coord,color in cells.items():
        for axis in range(3):
            u=(axis+1)%3;v=(axis+2)%3
            for sign in (-1,1):
                neighbor=list(coord);neighbor[axis]+=sign
                if tuple(neighbor) in cells: continue
                plane=coord[axis]+(1 if sign>0 else 0)
                masks[(axis,sign,plane,color)].add((coord[u],coord[v]))
    return masks

def rectangles(cells):
    output=[]
    for (axis,sign,plane,color),points in sorted(surface(cells).items()):
        remaining=set(points)
        while remaining:
            u,v=min(remaining,key=lambda p:(p[1],p[0]));width=1
            while (u+width,v) in remaining:width+=1
            height=1
            while all((u+i,v+height) in remaining for i in range(width)):height+=1
            for du in range(width):
                for dv in range(height):remaining.remove((u+du,v+dv))
            output.append({'axis':axis,'sign':sign,'plane':plane,'color':color,'u':u,'v':v,'width':width,'height':height})
    return output

def corners(r):
    axis=r['axis'];u=(axis+1)%3;v=(axis+2)%3
    origin=[0,0,0];origin[axis]=r['plane'];origin[u]=r['u'];origin[v]=r['v']
    a=origin[:];b=origin[:];c=origin[:];d=origin[:]
    b[u]+=r['width'];c[u]+=r['width'];c[v]+=r['height'];d[v]+=r['height']
    return [a,b,c,d] if r['sign']>0 else [a,d,c,b]

def export_obj(cells,path,palette=PALETTE):
    rects=rectangles(cells);lines=['# Original voxel specimen; x-right, y-up, z=-depth',f'mtllib {path.with_suffix(".mtl").name}','s off'];index=1
    for r in rects:
        for x,y,z in corners(r):lines.append(f'v {x} {z} {-y}')
        lines.append(f'usemtl color{r["color"]}');lines.append('f '+' '.join(str(index+i) for i in range(4)));index+=4
    path.write_text('\n'.join(lines)+'\n',encoding='utf8')
    materials=[]
    for c in sorted(set(cells.values())):
        rgb=palette[c][:3];materials.extend([f'newmtl color{c}','Kd '+' '.join(f'{v/255:.6f}' for v in rgb),'d 1','illum 1',''])
    path.with_suffix('.mtl').write_text('\n'.join(materials),encoding='utf8')
    return len(rects)

def verify():
    g=Grid();g.box(0,0,0,2,3,4,7);r=rectangles(g.cells);assert len(r)==6
    # Exact face coverage, directions and colors, including an internal cavity.
    cases=[g.cells]
    mixed=Grid();mixed.box(0,0,0,5,5,5,3);mixed.box(1,1,1,4,4,4,0);mixed.box(0,0,4,3,5,5,7);cases.append(mixed.cells)
    cases.extend(f(random.Random(13)).cells for f in RECIPES.values())
    for cells in cases:
        expected=surface(cells);actual=collections.defaultdict(set)
        for r in rectangles(cells):
            key=(r['axis'],r['sign'],r['plane'],r['color'])
            for du in range(r['width']):
                for dv in range(r['height']):
                    p=(r['u']+du,r['v']+dv);assert p not in actual[key],'overlapping face'
                    actual[key].add(p)
            a,b,c=corners(r)[:3];u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
            n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
            assert n[r['axis']]*r['sign']>0,'winding'
        assert dict(actual)==dict(expected),'surface or color mismatch'
    return len(cases)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,required=True);ap.add_argument('--seed',type=int,default=13);ap.add_argument('--family',choices=list(RECIPES)+['all'],default='all');args=ap.parse_args()
    count=verify();out=args.output;out.mkdir(parents=True,exist_ok=True);rows=[]
    for family in RECIPES if args.family=='all' else [args.family]:
        make=RECIPES[family];g=make(random.Random(args.seed));size,cells=g.normalized();unit=sum(len(v) for v in surface(cells).values());quads=export_obj(cells,out/f'{family}-seed{args.seed}.obj')
        rows.append({'family':family,'seed':args.seed,'occupied':len(cells),'naiveCubeFaces':6*len(cells),'visibleUnitFaces':unit,'greedyQuads':quads,'triangles':quads*2,'reductionVsVisibleUnitFaces':round(unit/quads,2),'source':'counts measured from original generated grids; no GPU/FPS claim'})
    content=json.dumps({'checks':count,'seed':args.seed,'exactFaceColorCoverage':'pass','winding':'pass','models':rows},indent=2)
    (out/f'mesh-comparison-seed{args.seed}.json').write_text(content,encoding='utf8')
    if args.seed==13:(out/'mesh-comparison.json').write_text(content,encoding='utf8')
    print('mesher coverage cases',count,'all pass');print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
