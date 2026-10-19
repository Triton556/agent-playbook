"""Read bounded MagicaVoxel/legacy Slab6 grid data; no scene graph transforms applied."""
import argparse,collections,json,math,pathlib,struct
class VoxError(ValueError): pass

def parse_vox(data):
    if len(data)<20: raise VoxError('VOX header missing')
    if data[:4]!=b'VOX ':
        # Ken Silverman's dense legacy VOX shares the suffix with MagicaVoxel.
        dims=struct.unpack_from('<III',data,0)
        total=math.prod(dims)
        if any(d<1 or d>256 for d in dims) or total>2_000_000 or len(data)!=12+total+768:
            raise VoxError('unsupported VOX signature/length')
        raw=data[12:12+total]; pal=data[-768:]
        palette=[(0,0,0,0)]+[tuple(min(255,channel*4) for channel in pal[i*3:i*3+3])+(255,) for i in range(255)]
        vox=[]; sx,sy,sz=dims
        for x in range(sx):
            for y in range(sy):
                for z in range(sz):
                    c=raw[(x*sy+y)*sz+z]
                    if c!=255: vox.append((x,y,sz-1-z,c+1))
        return {'version':'legacy-dense-VOX','parts':[{'size':dims,'voxels':vox}],'palette':palette,'chunks':{'dense-grid':1},'format':'slab6-dense-vox','orientationNote':'z storage reversed to put top-down legacy grid into z-up diagnostic view'}
    version=struct.unpack_from('<I',data,4)[0]
    parts=[]; chunks=collections.Counter(); size=None; rgba=None
    def walk(start,end):
        nonlocal size,rgba
        p=start
        while p<end:
            if p+12>end: raise VoxError('truncated chunk header')
            name,n,c=struct.unpack_from('<4sII',data,p); q=p+12; finish=q+n+c
            if finish>end: raise VoxError('chunk outside parent bounds')
            tag=name.decode('ascii',errors='replace'); chunks[tag]+=1; content=data[q:q+n]
            if tag=='SIZE':
                if n!=12: raise VoxError('SIZE must contain 12 bytes')
                size=struct.unpack('<III',content)
                if any(d==0 for d in size): raise VoxError('zero SIZE dimension')
            elif tag=='XYZI':
                if size is None or n<4: raise VoxError('XYZI without SIZE')
                count=struct.unpack_from('<I',content)[0]
                if count>2_000_000 or n!=4+4*count: raise VoxError('XYZI length mismatch or capacity limit')
                vox=[tuple(content[o:o+4]) for o in range(4,n,4)]
                if any(v[3]==0 or any(v[a]>=size[a] for a in range(3)) for v in vox): raise VoxError('voxel outside SIZE or zero color index')
                parts.append({'size':size,'voxels':vox}); size=None
            elif tag=='RGBA':
                if n!=1024: raise VoxError('RGBA must have 256 entries')
                rgba=[(0,0,0,0)]+[tuple(content[o:o+4]) for o in range(0,1020,4)]
            if c: walk(q+n,finish)
            p=finish
        if p!=end: raise VoxError('invalid chunk boundary')
    if data[8:12]!=b'MAIN': raise VoxError('MAIN root missing')
    walk(8,len(data))
    if not parts: raise VoxError('no voxel grid')
    return {'version':version,'parts':parts,'palette':rgba,'chunks':dict(chunks),'format':'magicavoxel'}

def stats(part):
    vox=part['voxels']; size=part['size']; coords={(x,y,z):c for x,y,z,c in vox}
    colors=collections.Counter(v[3] for v in vox)
    bounds=[[min(v[a] for v in vox),max(v[a] for v in vox)] for a in range(3)] if vox else []
    bbox_volume=math.prod(b[1]-b[0]+1 for b in bounds) if bounds else 0
    faces=None; components=None
    if len(coords)<=120_000:
        neighbors=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
        faces=sum((x+dx,y+dy,z+dz) not in coords for x,y,z in coords for dx,dy,dz in neighbors)
        unseen=set(coords); components=0
        while unseen:
            components+=1; stack=[unseen.pop()]
            while stack:
                x,y,z=stack.pop()
                for dx,dy,dz in neighbors:
                    nxt=(x+dx,y+dy,z+dz)
                    if nxt in unseen: unseen.remove(nxt); stack.append(nxt)
    return {'size':size,'occupied':len(vox),'uniqueCoordinates':len(coords),'duplicateCoordinates':len(vox)-len(coords),'occupiedBounds':bounds,'boundingBoxFill':round(len(coords)/bbox_volume,5) if bbox_volume else 0,'usedColorCount':len(colors),'topColorIndices':colors.most_common(10),'exposedUnitFaces':faces,'sixConnectedComponents':components,'metricsLimited':len(coords)>120_000}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('file',type=pathlib.Path);ap.add_argument('--output',type=pathlib.Path);ap.add_argument('--grid-json',action='store_true');args=ap.parse_args()
    if args.file.stat().st_size>9_000_000:raise VoxError('file capacity limit:9MB')
    parsed=parse_vox(args.file.read_bytes()); result={k:v for k,v in parsed.items() if k not in ('parts','palette')}
    result['explicitPalette']=parsed['palette'] is not None
    result['parts']=[stats(p) for p in parsed['parts']]
    result['limitations']=['Grid parts only; no scene transforms, frame assembly or PBR material rendering. Default MagicaVoxel palette is not supplied by this inspector.']
    if args.grid_json:result['grids']=parsed['parts'];result['palette']=parsed['palette']
    payload=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:args.output.write_text(payload+'\n',encoding='utf8');print(args.output)
    else:print(payload)
if __name__=='__main__':main()
