"""Read-only structural/metric design gate; visual judgments remain attestations."""
import argparse, datetime, hashlib, json, math, pathlib, struct, sys
VIEWS={'front':(0,1,2,1),'back':(0,-1,2,1),'right':(1,1,2,1),'left':(1,-1,2,1),'top':(0,1,1,1),'bottom':(0,1,1,-1)}
GATES=('coherence','style','context','function','readability','usability')
def text(v):return isinstance(v,str) and bool(v.strip())
def number(v):return type(v) in (int,float) and math.isfinite(v)
def vec(v,n=3):return isinstance(v,list) and len(v)==n and all(number(x) for x in v)
def same(a,b):return math.isclose(a,b,rel_tol=1e-6,abs_tol=1e-7)
def path(root,rel):
    if not text(rel) or pathlib.Path(rel).is_absolute():raise ValueError('expected relative project path')
    p=(root/rel).resolve()
    if not p.is_relative_to(root):raise ValueError('path outside project')
    return p
def read(root,rel):
    p=path(root,rel)
    if p.stat().st_size>8_388_608:raise ValueError('JSON input too large')
    value=json.loads(p.read_text(encoding='utf-8-sig'))
    if not isinstance(value,dict):raise ValueError('JSON input must be an object')
    return value
def dimensions(p):
    with p.open('rb') as f:
        head=f.read(24)
        if head[:8]==b'\x89PNG\r\n\x1a\n' and head[12:16]==b'IHDR':return struct.unpack('>II',head[16:24])
        f.seek(0)
        if f.read(2)!=b'\xff\xd8':raise ValueError('view must be PNG or JPEG')
        while True:
            marker=f.read(1)
            if not marker:raise ValueError('JPEG size missing')
            if marker!=b'\xff':continue
            while marker==b'\xff':marker=f.read(1)
            code=ord(marker)
            if code in (0xd8,0xd9,0x01) or 0xd0<=code<=0xd7:continue
            raw=f.read(2)
            if len(raw)!=2:raise ValueError('truncated JPEG')
            length=int.from_bytes(raw,'big')
            if length<2:raise ValueError('invalid JPEG segment')
            if code in (0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf):
                segment=f.read(5)
                if len(segment)!=5:raise ValueError('truncated JPEG size')
                return int.from_bytes(segment[3:5],'big'),int.from_bytes(segment[1:3],'big')
            f.seek(length-2,1)
def snapshot(root,passport_rel):
    p=read(root,passport_rel);rels={passport_rel}
    for b in p.get('basis',[]):rels.add(b['path'])
    for v in p.get('views',{}).values():rels.add(v['path'])
    for v in p.get('supporting_views',[]):rels.add(v['path'])
    kit=p.get('kit',{})
    if kit.get('mode')=='existing':rels.update([kit['path'],kit['comparison_path']])
    files=[]
    for rel in sorted(rels):
        f=path(root,rel)
        if not f.is_file():raise ValueError('missing input '+rel)
        files.append({'path':rel,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    digest=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'input_digest':digest,'files':files}
def validate(root,passport_rel,review_rel):
    p=read(root,passport_rel);s=snapshot(root,passport_rel);errors=[]
    def need(ok,message):
        if not ok:errors.append(message)
    need(p.get('schema_version')==1,'passport schema1 required');a=p.get('asset',{})
    for key in ('id','pose','context','intended_use'):need(text(a.get(key)),'asset '+key+' required')
    need(a.get('forward')=='-Y' and a.get('up')=='+Z','fixed design axes required')
    origin=a.get('origin_m');valid_origin=vec(origin)
    need(valid_origin,'explicit finite3D origin required');need(number(a.get('ground_z_m')),'explicit support/ground plane required')
    dims=a.get('dimensions_m');pitch=a.get('master_pitch_m')
    good_dims=vec(dims) and all(x>0 for x in dims);good_pitch=number(pitch) and pitch>0
    need(good_dims,'positive finite dimensions required');need(good_pitch,'positive finite master pitch required')
    if good_dims and good_pitch:need(all(math.ceil(x/pitch-1e-7)<=256 for x in dims),'single VOX exceeds256; declare modular plan')
    styles=a.get('style_features',[]);need(isinstance(styles,list) and bool(styles) and all(text(x) for x in styles),'style features required')
    basis=p.get('basis',[]);need(isinstance(basis,list) and bool(basis),'inspected local basis required')
    for b in basis:need(text(b.get('observations')),'basis observation required')
    features=p.get('critical_features',[]);need(isinstance(features,list) and bool(features),'critical feature checks required')
    for c in features:
        need(text(c.get('id')) and text(c.get('check')),'critical feature id/check required')
        indices=c.get('basis',[])
        supported=isinstance(indices,list) and bool(indices) and all(type(i)==int and 0<=i<len(basis) for i in indices)
        need(supported or text(c.get('authored_choice')),'critical feature has no inspected basis or declared authored choice')
    lm=p.get('landmarks_m',{});valid_lm=isinstance(lm,dict) and bool(lm) and all(vec(v) for v in lm.values())
    need(valid_lm,'finite3D recognition/contact landmarks required')
    views=p.get('views',{});need(set(views)==set(VIEWS),'six named orthographic views required')
    need(len({v.get('path') for v in views.values() if isinstance(v,dict)})==6,'six separate named view files required')
    ppm=[]
    for name,axes in VIEWS.items():
        v=views.get(name)
        if not isinstance(v,dict):continue
        need(v.get('projection')=='orthographic',name+' projection mismatch');need(v.get('pose')==a.get('pose'),name+' pose mismatch')
        span=v.get('span_m');valid_span=vec(span,2)
        need(valid_span,name+' projected span required')
        if good_dims and valid_span:need(same(span[0],dims[axes[0]]) and same(span[1],dims[axes[2]]),name+' dimensions disagree')
        scale=v.get('pixels_per_meter');need(number(scale) and scale>0,name+' positive metric camera scale required')
        if number(scale):ppm.append(scale)
        if valid_lm:
            points=v.get('landmarks_2d_m',{});need(set(points)==set(lm),name+' landmark set mismatch')
            for key,xyz in lm.items():
                q=points.get(key)
                if valid_origin:need(vec(q,2) and same(q[0],(xyz[axes[0]]-origin[axes[0]])*axes[1]) and same(q[1],(xyz[axes[2]]-origin[axes[2]])*axes[3]),name+' landmark '+key+' disagrees')
        w,h=dimensions(path(root,v['path']));need(w>=480 and h>=480,name+' image below480px review size')
        if valid_span and number(scale):need(span[0]*scale<=w and span[1]*scale<=h,name+' metric extent does not fit canvas')
    if ppm:need(all(same(x,ppm[0]) for x in ppm),'views use unequal pixels per metre')
    for v in p.get('supporting_views',[]):
        need(text(v.get('purpose')),'supporting view purpose required')
        w,h=dimensions(path(root,v['path']));need(w>=480 and h>=480,'supporting view below review size')
    kit=p.get('kit',{});need(kit.get('mode') in('standalone','existing'),'kit mode required')
    if kit.get('mode')=='existing':
        k=read(root,kit['path']);ranges=k.get('asset_dimension_ranges_m',[])
        need(len(ranges)==3 and all(vec(r,2) and 0<r[0]<=r[1] for r in ranges),'kit dimension constraints required')
        if good_dims and len(ranges)==3 and all(vec(r,2) for r in ranges):need(all(r[0]<=d<=r[1] for r,d in zip(ranges,dims)),'asset outside kit world-size range')
        kp=k.get('integration_pitch_m');need(number(kp) and kp>0,'kit positive integration pitch required')
        ip=kit.get('integration_pitch_m');need(number(ip) and number(kp) and same(ip,kp),'kit integration pitch mismatch')
        need(k.get('master_policy') in ('independent','shared'),'kit master policy required')
        if k.get('master_policy')=='shared' and good_pitch and number(kp):need(same(pitch,kp),'shared master pitch mismatch')
        need(isinstance(k.get('style_features'),list) and bool(k['style_features']),'kit style constraints required')
        w,h=dimensions(path(root,kit['comparison_path']));need(w>=480 and h>=480,'kit comparison below review size')
    r=read(root,review_rel) if review_rel else{};need(r.get('schema_version')==1,'design review schema1 required')
    need(r.get('input_digest')==s['input_digest'],'design review absent or stale')
    need(r.get('inspected') is True,'actual design inspection record required')
    reviewer=r.get('reviewer',{});need(reviewer.get('kind') in('agent','human') and text(reviewer.get('name')),'named reviewer required')
    try:
        date=datetime.datetime.fromisoformat(r.get('observed_at','').replace('Z','+00:00'));need(date.utcoffset() is not None,'review timestamp timezone required')
    except(ValueError,TypeError):need(False,'review timestamp required')
    for key in GATES:
        g=r.get('gates',{}).get(key,{});need(g.get('verdict')=='pass' and text(g.get('observation')),key+' review not passed')
    need(snapshot(root,passport_rel)==s,'inputs changed during validation')
    return {'schema_version':1,'ready_to_voxelize':not errors,'blockers':errors,**s,'limits':['Validates authored metric metadata and current review records, not actual landmark pixels, image meaning or beauty.','A six-view design does not uniquely determine hidden3D volume.','Reviewer inspection/identity is an attestation; later voxel-to-design checks and human acceptance remain separate.']}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('command',choices=('snapshot','validate'));ap.add_argument('--root',type=pathlib.Path,required=True);ap.add_argument('--passport',required=True);ap.add_argument('--review');ap.add_argument('--output');args=ap.parse_args();root=args.root.resolve()
    try:
        result=snapshot(root,args.passport) if args.command=='snapshot' else validate(root,args.passport,args.review)
        if args.output:
            out=path(root,args.output)
            inputs={x['path'] for x in result['files']}|{args.review}
            if out in {path(root,p) for p in inputs if p}:raise ValueError('report would overwrite an input')
            out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
        print(json.dumps(result,ensure_ascii=False))
        return 0 if args.command=='snapshot' or result['ready_to_voxelize'] else 2
    except(ValueError,KeyError,TypeError,AttributeError,IndexError,OSError,struct.error) as e:
        print(json.dumps({'ready_to_voxelize':False,'malformed':str(e)},ensure_ascii=False));return 1
if __name__=='__main__':sys.exit(main())
