"""Generate versioned original Gen2 assets with standard-library helpers."""
import argparse,hashlib,json,pathlib
import library_recipes,gen2_anatomy,gen2_nature,gen2_built,gen2_root
from voxel_recipes import vox_bytes
from voxel_mesh import export_obj
ROWS=sum((m.ROWS for m in (gen2_anatomy,gen2_nature,gen2_built,gen2_root)),[])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--category',choices=sorted({r[0] for r in ROWS})+['all'],default='all');ap.add_argument('--model',choices=[r[1] for r in ROWS]);ap.add_argument('--seed',type=int,default=153);ap.add_argument('--output',type=pathlib.Path,required=True);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True);rows=[]
 for group,slug,title,principle,make in ROWS:
  if args.category!='all' and group!=args.category:continue
  if args.model and slug!=args.model:continue
  g=make(args.seed);size,cells=g.normalized();blob=vox_bytes(g);(args.output/(slug+'.vox')).write_bytes(blob);quads=export_obj(cells,args.output/(slug+'.obj'))
  rows.append({'version':'gen2','group':group,'slug':slug,'title':title,'principle':principle,'seed':args.seed,'size':size,'occupied':len(cells),'greedyQuads':quads,'sha256':hashlib.sha256(blob).hexdigest(),'normalizationOffset':[min(p[a] for p in g.cells) for a in range(3)],'construction':getattr(g,'gen2_meta',{}),'coordinateUnit':'object-space design grid; physical-meter pitch not specified','original':True,'humanAcceptance':'not established by generation'})
 (args.output/'gen2-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'models':len(rows),'version':'gen2','output':str(args.output)}))
if __name__=='__main__':main()
